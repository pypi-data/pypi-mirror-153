from enum import IntEnum, unique
from ctypes import c_uint8, c_int16, c_uint16, c_int32, c_uint32, c_uint64
from ctypes import byref, create_string_buffer, sizeof, Structure
from ctypes import c_bool, c_char, c_char_p, c_float, c_double
from pathlib import Path
from typing import Optional, Dict, Union, List, cast
from . import _MPuLib, _MPuLib_variadic, _check_limits
from .MPStatus import CTS3ErrorCode
from .MPException import CTS3Exception
from struct import iter_unpack
from math import sqrt
from warnings import warn


class _ChannelConfig(Structure):
    """Channel configuration"""
    _pack_ = 1
    _fields_ = [('config', c_uint32),
                ('range', c_uint32),
                ('impedance', c_uint32),
                ('term', c_uint32),
                ('slope', c_double),
                ('offset', c_double),
                ('rms_noise', c_double),
                ('demod_noise', c_double)]


class _DaqHeader(Structure):
    """Acquisition file header"""
    _pack_ = 1
    _fields_ = [('id', c_uint32),
                ('version', c_uint16),
                ('header_size', c_uint16),
                ('measurements_count', c_uint32),
                ('timestamp', c_uint32),
                ('device_id', c_char * 32),
                ('device_version', c_char * 32),
                ('bits_per_sample', c_uint8),
                ('channels', c_uint8),
                ('source', c_uint8),
                ('channel_size', c_uint8),
                ('sampling', c_uint32),
                ('trig_date', c_uint64),
                ('ch1', _ChannelConfig),
                ('ch2', _ChannelConfig),
                ('rfu1', c_uint8 * 96),
                ('normalization', c_float),
                ('demod_delay', c_int32),
                ('probe_id_ch1', c_char * 16),
                ('probe_id_ch2', c_char * 16),
                ('delay', c_int32),
                ('rfu2', c_uint8 * 52)]


class _DaqFooter(Structure):
    """Acquisition file footer"""
    _pack_ = 1
    _fields_ = [('id', c_uint32),
                ('version', c_uint16),
                ('footer_size', c_uint16),
                ('metadata_size', c_uint16)]


class DaqPoint():
    """DAQ point definition

    Attributes
    ----------
    x : float
        Date
    y : float
        Value (in V, ° or dimensionless)
    """

    def __init__(self, x: float, y: float):
        """Inits DaqPoint

        Parameters
        ----------
        x : float
            Date
        y : float
            Value (in V, ° or dimensionless)
        """
        self.x = x
        self.y = y


def load_signals(file_path: Union[str, Path]) -> List[List[DaqPoint]]:
    """Loads DAQ signals from an acquisition file (single mode)

    Parameters
    ----------
    file_path : str or Path
        Acquisition file

    Returns
    -------
    list(list(DaqPoint))
        List of signals loaded from acquisition file
    """
    with open(file_path, 'rb') as f:
        header = _DaqHeader.from_buffer_copy(f.read(sizeof(_DaqHeader)))
        if header.version < 2:
            raise Exception(f'Unsupported DAQ file version ({header.version})')
        data_width = int(header.bits_per_sample / 8)
        data_length = cast(int, header.measurements_count)
        start_date = 0.0
        if header.version > 2:
            start_date = cast(int, header.delay) / 1e9
        sampling = cast(int, header.sampling)
        channels = cast(int, header.channels)
        file_content = f.read(channels * data_length * data_width)
        footer = _DaqFooter.from_buffer_copy(f.read(sizeof(_DaqFooter)))
        if footer.metadata_size:
            f.read(footer.metadata_size)

    signal: List[DaqPoint] = []
    date = start_date
    if data_width == sizeof(c_int16):
        SOURCE_TXRX = 1
        SOURCE_PHASE = 6
        SOURCE_VDC = 5
        if channels == 1:
            if header.source == SOURCE_PHASE:
                # Phase
                for y in iter_unpack('<h', file_content):
                    value = float('nan') if y[0] > 8192 else \
                            180.0 * cast(int, y[0]) / 8192.0
                    signal.append(DaqPoint(date, value))
                    date += 1.0 / sampling
            elif header.source == SOURCE_VDC:
                # Vdc
                offset = cast(float, header.ch1.offset)
                slope = cast(float, header.ch1.slope)
                quadratic = cast(float, header.ch1.rms_noise)
                cubic = cast(float, header.ch1.demod_noise)
                for y in iter_unpack('<h', file_content):
                    value = (offset + slope * cast(int, y[0]) +
                             quadratic * cast(int, y[0]) ** 2 +
                             cubic * cast(int, y[0]) ** 3) / 1e3
                    signal.append(DaqPoint(date, value))
                    date += 1.0 / sampling
            else:
                # Modulated signal
                if header.ch1.config & 1:
                    offset = cast(float, header.ch1.offset)
                    slope = cast(float, header.ch1.slope)
                else:
                    offset = cast(float, header.ch2.offset)
                    slope = cast(float, header.ch2.slope)
                if header.source != SOURCE_TXRX:
                    slope /= 1e3
                for y in iter_unpack('<h', file_content):
                    value = slope * (cast(int, y[0]) + offset)
                    signal.append(DaqPoint(date, value))
                    date += 1.0 / sampling
            return [signal]

        else:
            # CH1 and CH2 data interleaved
            offset_1 = cast(float, header.ch1.offset)
            slope_1 = cast(float, header.ch1.slope) / 1e3
            offset_2 = cast(float, header.ch2.offset)
            slope_2 = cast(float, header.ch2.slope) / 1e3

            signal_1: List[DaqPoint] = []
            signal_2: List[DaqPoint] = []
            date = start_date
            toggle = True
            for y in iter_unpack('<h', file_content):
                if toggle:
                    value = slope_1 * (cast(int, y[0]) + offset_1)
                    signal_1.append(DaqPoint(date, value))
                else:
                    value = slope_2 * (cast(int, y[0]) + offset_2)
                    signal_2.append(DaqPoint(date, value))
                    date += 1.0 / sampling
                toggle = not toggle
            return [signal_1, signal_2]

    elif data_width == sizeof(c_uint32):
        # Demodulated signal
        if header.ch1.config & 1:
            slope = cast(float, header.ch1.slope)
            noise = cast(float, header.ch1.demod_noise)
        else:
            slope = cast(float, header.ch2.slope)
            noise = cast(float, header.ch2.demod_noise)
        slope *= cast(float, header.normalization) / 1e3
        for y in iter_unpack('<L', file_content):
            value = slope * sqrt(y[0] - noise) if y[0] > noise else 0.0
            signal.append(DaqPoint(date, value))
            date += 1.0 / sampling
        return [signal]

    return []


def load_signal(file_path: Union[str, Path]) -> List[List[float]]:
    """Loads DAQ signals from an acquisition file (single mode)

    Parameters
    ----------
    file_path : str or Path
        Acquisition file

    Returns
    -------
    list(list(float))
        List of signals loaded from acquisition file (in V, ° or dimensionless)
    """
    warn('load_signal replaced by load_signals',
         FutureWarning, 2)
    result = []
    signals = load_signals(file_path)
    for signal in signals:
        result.append([pt.y for pt in signal])
    return result


@unique
class DaqChannel(IntEnum):
    """Channel Selection"""
    CH_1_SMA = 0
    CH_1_BNC = 1
    CH_2_SMA = 2
    CH_2_BNC = 3


@unique
class DaqRange(IntEnum):
    """Range Selection"""
    RANGE_1000 = 1000
    RANGE_2000 = 2000
    RANGE_10000 = 10000


@unique
class DaqNCTerm(IntEnum):
    """DAQ Non-Connected Termination"""
    NCT_50O = 50
    NCT_OPEN = 1000000


def Daq_SetChannel(channel: DaqChannel, enabled: bool,
                   voltage_range: DaqRange,
                   nc_term: DaqNCTerm = DaqNCTerm.NCT_50O) -> None:
    """Selects and configures a channel

    Parameters
    ----------
    channel : DaqChannel
        Channel number and connector
    enabled : bool
        True to enable the channel
    voltage_range : DaqRange
        Range to use
    nc_term : DaqNCTerm, optional
        Termination impedance on the unused connector
    """
    if not isinstance(channel, DaqChannel):
        raise TypeError('channel must be an instance of DaqChannel IntEnum')
    if enabled and not isinstance(voltage_range, DaqRange):
        raise TypeError('voltage_range must be an instance of '
                        'DaqRange IntEnum')
    if not isinstance(nc_term, DaqNCTerm):
        raise TypeError('nc_term must be an instance of DaqNCTerm IntEnum')
    CTS3Exception._check_error(_MPuLib.Daq_SetChannel(
        c_uint8(channel),
        c_bool(enabled),
        c_uint16(voltage_range) if enabled else c_uint16(0),
        c_uint32(0),
        c_uint32(nc_term),
        c_uint8(0)))


def Daq_GetChannel(channel: DaqChannel) \
        -> Dict[str, Union[bool, DaqRange, DaqNCTerm, None]]:
    """Gets channel configuration

    Parameters
    ----------
    channel : DaqChannel
        Channel number and connector

    Returns
    -------
    dict
        'enabled' (bool) : Channel enabled
        'voltage_range' (DaqRange) : Channel range
        'nc_term' (DaqNCTerm) : Termination impedance on the unused connector
    """
    if not isinstance(channel, DaqChannel):
        raise TypeError('channel must be an instance of DaqChannel IntEnum')
    enabled = c_bool()
    range_mV = c_uint16()
    impedance = c_uint32()
    term = c_uint32()
    rfu = c_uint8()
    CTS3Exception._check_error(_MPuLib.Daq_GetChannel(
        c_uint8(channel),
        byref(enabled),
        byref(range_mV),
        byref(impedance),
        byref(term),
        byref(rfu)))
    if enabled.value:
        return {'enabled': True,
                'voltage_range': DaqRange(range_mV.value),
                'nc_term': DaqNCTerm(term.value)}
    else:
        return {'enabled': False,
                'voltage_range': None,
                'nc_term': None}


@unique
class DaqSamplingClk(IntEnum):
    """DAQ Sampling Clock"""
    SCLK_150MHZ = 0
    SCLK_EXT = 1


def Daq_SetTimeBase(sampling_rate: DaqSamplingClk = DaqSamplingClk.SCLK_150MHZ,
                    points_number: int = 0x10000000) -> None:
    """Configures the sampling rates and the number of points to acquire
    on the enabled channels

    Parameters
    ----------
    sampling_rate : DaqSamplingClk, optional
        Sampling clock source
    points_number : int, optional
        Number of points to acquire
    """
    if not isinstance(sampling_rate, DaqSamplingClk):
        raise TypeError('sampling_rate must be an instance of '
                        'DaqSamplingClk IntEnum')
    _check_limits(c_uint32, points_number, 'points_number')
    CTS3Exception._check_error(_MPuLib.Daq_SetTimeBase(
        c_uint8(sampling_rate),
        c_uint32(points_number)))


@unique
class DaqTrigSource(IntEnum):
    """DAQ Trigger Source"""
    TRIG_INT = 0
    TRIG_EXT = 1
    TRIG_CH1 = 2
    TRIG_CH2 = 3
    TRIG_IMMEDIATE = 4


@unique
class DaqTrigDir(IntEnum):
    """DAQ Trigger direction"""
    DIR_FALLING_EDGE = 0
    DIR_RISING_EDGE = 1
    DIR_BOTH_EDGES = 2


def Daq_SetTrigger(trigger_source: DaqTrigSource, level: float = 0,
                   direction: DaqTrigDir = DaqTrigDir.DIR_BOTH_EDGES,
                   delay: int = 0) -> None:
    """Configures the trigger on enabled channels

    Parameters
    ----------
    trigger_source : DaqTrigSource
        Trigger source
    level : float, optional
        Trigger level in V (only if trigger source is TRIG_CH1 or TRIG_CH2)
    direction : DaqTrigDir, optional
        Trigger direction (only if trigger source is TRIG_EXT, TRIG_CH1 or
        TRIG_CH2)
    delay : int, optional
        Samples number between the trigger and the beginning of the acquisition
    """
    if not isinstance(trigger_source, DaqTrigSource):
        raise TypeError('trigger_source must be an instance of '
                        'DaqTrigSource IntEnum')
    level_mV = round(level * 1e3)
    _check_limits(c_int16, level_mV, 'level')
    if not isinstance(direction, DaqTrigDir):
        raise TypeError('direction must be an instance of DaqTrigDir IntEnum')
    _check_limits(c_int32, delay, 'delay')
    CTS3Exception._check_error(_MPuLib.Daq_SetTrigger(
        c_uint8(trigger_source),
        c_int16(level_mV),
        c_uint8(direction),
        c_int32(delay)))


@unique
class DaqAcqMode(IntEnum):
    """DAQ Acquisition mode"""
    MODE_STOP = 0
    MODE_SINGLE = 1
    MODE_NORMAL = 2


@unique
class DaqDownloadMode(IntEnum):
    """DAQ Download mode"""
    MODE_DOWNLOAD = 0
    MODE_FILESYSTEM = 1


@unique
class DaqDataFormat(IntEnum):
    """Deprecated DAQ Data Format mode"""
    FORMAT_RAW_16BITS = 0


def Daq_StartStopAcq(acq_mode: DaqAcqMode,
                     download_mode: DaqDownloadMode =
                     DaqDownloadMode.MODE_DOWNLOAD,
                     data_format: Optional[DaqDataFormat] = None,
                     file_name: Union[str, Path] = '') -> None:
    """Starts/Stops the acquisition

    Parameters
    ----------
    acq_mode : DaqAcqMode
        Acquisition mode
    download_mode : DaqDownloadMode, optional
        Download mode (only if acq_mode is MODE_SINGLE or MODE_RUN)
    data_format : DaqDataFormat, optional
        Not used
    file_name : str or Path, optional
        File name (only if acq_mode is MODE_SINGLE or MODE_RUN)
    """
    if not isinstance(acq_mode, DaqAcqMode):
        raise TypeError('acq_mode must be an instance of DaqAcqMode IntEnum')
    if not isinstance(download_mode, DaqDownloadMode):
        raise TypeError('download_mode must be an instance of '
                        'DaqAcqMode IntEnum')
    if data_format is not None:
        warn("deprecated 'data_format' parameter",
             FutureWarning, 2)
    if _MPuLib_variadic is None:
        func_pointer = _MPuLib.Daq_StartStopAcq
    else:
        func_pointer = _MPuLib_variadic.Daq_StartStopAcq
    if isinstance(file_name, Path):
        if str(file_name) != '.':
            file = str(file_name).encode('ascii')
        else:
            file = ''.encode('ascii')
    else:
        file = file_name.encode('ascii')
    CTS3Exception._check_error(func_pointer(
        c_uint32(acq_mode),
        c_uint32(download_mode),
        c_uint32(0),
        file))


@unique
class DaqStatus(IntEnum):
    """DAQ trigger status"""
    STATUS_NONE = 0
    STATUS_WAITING_TRIGGER = 1
    STATUS_TRIGGERED = 2
    STATUS_EOC = 3
    STATUS_FILE_AVAILABLE = 4
    STATUS_OVERFLOW = 5
    STATUS_OVERRANGE = 6
    STATUS_OVERVOLTAGE = 7


def Daq_GetStatus() -> DaqStatus:
    """Gets DAQ board acquisition status

    Returns
    -------
    DaqStatus
        Current trigger status
    """
    status = c_uint8()
    CTS3Exception._check_error(_MPuLib.Daq_GetStatus(
        byref(status)))
    return DaqStatus(status.value)


def Daq_GetInfo() -> str:
    """Gets DAQ board version

    Returns
    -------
    str
        FPGA version
    """
    year = c_uint8()
    version = c_uint8()
    revision = c_uint8()
    rfu = c_uint8()
    CTS3Exception._check_error(_MPuLib.Daq_GetInfo(
        byref(year),
        byref(version),
        byref(revision),
        byref(rfu)))
    return str(year.value) + '.' + str(version.value) + '.' + \
        str(revision.value)


@unique
class DaqFilter(IntEnum):
    """DAQ Filters"""
    DAQ_FILTER_LOW_PASS = 1
    VDC_FILTER = 3


def Daq_SetFilter(filter: DaqFilter, enabled: bool) -> None:
    """Enables DAQ filter

    Parameters
    ----------
    filter : DaqFilter
        Filter to enable
    enabled : bool
        True to enable filter
    """
    if not isinstance(filter, DaqFilter):
        raise TypeError('filter must be an instance of DaqFilter IntEnum')
    CTS3Exception._check_error(_MPuLib.Daq_SetFilter(
        c_uint32(filter),
        c_bool(enabled)))


# region Probe Management


def Daq_ProbeCompensation(channel: int, label: Optional[str]) -> None:
    """Performs active probe compensation

    Parameters
    ----------
    channel : int
        Channel used to perform the probe compensation
    label : str
        Probe identifier
    """
    _check_limits(c_uint8, channel, 'channel')
    if label is None:
        CTS3Exception._check_error(_MPuLib.Daq_ProbeCompensation(
            c_uint8(channel),
            c_uint32(0),
            None))
    else:
        CTS3Exception._check_error(_MPuLib.Daq_ProbeCompensation(
            c_uint8(channel),
            c_uint32(0),
            label.encode('ascii')))


def Daq_LoadProbe(label: Optional[str], channel: int) -> None:
    """Loads probe compensation information

    Parameters
    ----------
    label : str
        Probe identifier
    channel : int
        Channel connected to the probe
    """
    _check_limits(c_uint8, channel, 'channel')
    if label is None:
        CTS3Exception._check_error(_MPuLib.Daq_LoadProbe(
            None,
            c_uint8(channel)))
    else:
        CTS3Exception._check_error(_MPuLib.Daq_LoadProbe(
            label.encode('ascii'),
            c_uint8(channel)))


def Daq_ListProbes() -> List[str]:
    """Lists available probe compensations information

    Returns
    -------
    list(str)
        Compensation identifiers list
    """
    cables_list = create_string_buffer(0xFFFF)
    CTS3Exception._check_error(_MPuLib.Daq_ListProbes(
        cables_list))
    list_string = cables_list.value.decode('ascii')
    return list_string.split(';') if len(list_string) else []


def Daq_DeleteProbe(label: str) -> None:
    """Removes probe compensation information from database

    Parameters
    ----------
    label : str
        Compensation identifier
    """
    CTS3Exception._check_error(_MPuLib.Daq_DeleteProbe(
        label.encode('ascii')))

# endregion

# region Self-test


@unique
class DaqAutotestId(IntEnum):
    """DAQ self-test type"""
    TEST_DAQ_ALL = -1
    TEST_DAQ_REF = 300


def MPS_DaqAutoTest(test_id: DaqAutotestId = DaqAutotestId.TEST_DAQ_ALL) \
        -> List[List[str]]:
    """Performs DAQ self-test

    Parameters
    ----------
    test_id : DaqAutotestId, optional
        Self-test identifier

    Returns
    -------
    list(list(str))
        Test result
    """
    if not isinstance(test_id, DaqAutotestId):
        raise TypeError('test_id must be an instance of DaqAutotestId IntEnum')
    result = c_char_p()
    ret = CTS3ErrorCode(_MPuLib.MPS_DaqAutoTest(
        c_uint32(test_id),
        c_bool(True),
        c_uint32(0),
        byref(result)))
    if (ret >= CTS3ErrorCode.RET_FAIL and ret <= CTS3ErrorCode.RET_WARNING) \
            or ret == CTS3ErrorCode.RET_OK:
        if result.value is None:
            return [['']]
        else:
            tests_result = ''.join(map(chr, result.value)).strip().split('\n')
            return [test.split('\t') for test in tests_result]
    else:
        raise CTS3Exception(ret)

# endregion
