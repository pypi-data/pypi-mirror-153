from warnings import warn
from pathlib import Path
from typing import Dict, Union, Optional, List, Tuple, Callable, overload
from enum import IntEnum, IntFlag, unique
from . import _MPuLib, _MPuLib_variadic, _check_limits, _get_connection_string
from .MPStatus import CTS3ErrorCode
from .MPException import CTS3Exception, CTS3MifareException
from ctypes import c_uint8, c_int16, c_uint16, c_int32, c_uint32, c_uint64
from ctypes import c_bool, c_char, c_char_p, c_int, c_float, c_double
from ctypes import byref, POINTER, CFUNCTYPE, Structure
from ctypes import Union as C_Union


_callback_dict: Dict[str, Optional[Callable[[int,
                                   int,
                                   POINTER(c_uint8),  # type: ignore[misc]
                                   int], int]]] = {}


class EventHeader(Structure):
    """Protocol analyzer event header structure definition"""
    _pack_ = 1
    _fields_ = [('identifier', c_char * 4),
                ('data_format', c_uint16),
                ('file_version', c_uint16),
                ('device_id', c_char * 32),
                ('device_version', c_char * 32),
                ('time_base_ns', c_uint16),
                ('rfu1', c_uint32),
                ('trace_type', c_uint8),
                ('rfu2', c_uint8),
                ('event_number', c_uint32),
                ('rfu3', c_uint16),
                ('event_mask', c_uint32),
                ('rfu4', c_uint8 * 38)]


class AnalogHeader(Structure):
    """Protocol analyzer analog Measurement header structure definition"""
    _pack_ = 1
    _fields_ = [('identifier', c_char * 4),
                ('data_format', c_uint16),
                ('file_version', c_uint16),
                ('device_id', c_char * 16),
                ('probe_id', c_char * 16),
                ('device_version', c_char * 32),
                ('time_base_ns', c_uint16),
                ('normalization', c_float),
                ('trace_type', c_uint8),
                ('source', c_uint8),
                ('event_number', c_uint32),
                ('rfu', c_uint8 * 6),
                ('range_mV', c_uint16),
                ('frequency_kHz', c_uint32),
                ('delay_ns', c_int32),
                ('date_ns', c_uint64),
                ('impedance_ohm', c_uint32),
                ('offset', c_double),
                ('slope', c_double)]


class Header(C_Union):
    """Protocol analyzer header structure definition"""
    _fields_ = [('events', EventHeader),
                ('analog', AnalogHeader)]

    def get_bytes(self) -> bytes:
        """Converts header into bytes

        Returns
        -------
        bytes
            Bytes representation of header
        """
        return bytearray(self)


@unique
class NfcUnit(IntEnum):
    """Timing units"""
    UNIT_S = 1
    UNIT_MS = 2
    UNIT_US = 3
    UNIT_NS = 4
    UNIT_CARRIER = 6
    UNIT_10_CARRIER = 7
    UNIT_SAMPLES = 8


def _unit_autoselect(unit: NfcUnit, values: List[float]) \
        -> Tuple[NfcUnit, List[int]]:
    """Converts float values to best-fitted 32-bit integer values and unit

    Parameters
    ----------
    unit : NfcUnit
        Values unit
    values : list(float)
        Values to convert

    Returns
    -------
    tuple(NfcUnit, list(int))
        Best unit and converted values
    """
    if unit == NfcUnit.UNIT_NS:
        value_ns = [round(i) for i in values]
        value_us = [round(i / 1e3) for i in values]
        value_ms = [round(i / 1e6) for i in values]
        value_s = [round(i / 1e9) for i in values]
    elif unit == NfcUnit.UNIT_US:
        value_ns = [round(i * 1e3) for i in values]
        value_us = [round(i) for i in values]
        value_ms = [round(i / 1e3) for i in values]
        value_s = [round(i / 1e6) for i in values]
    elif unit == NfcUnit.UNIT_MS:
        value_ns = [round(i * 1e6) for i in values]
        value_us = [round(i * 1e3) for i in values]
        value_ms = [round(i) for i in values]
        value_s = [round(i / 1e3) for i in values]
    elif unit == NfcUnit.UNIT_S:
        value_ns = [round(i * 1e9) for i in values]
        value_us = [round(i * 1e6) for i in values]
        value_ms = [round(i * 1e3) for i in values]
        value_s = [round(i) for i in values]
    else:
        return unit, [round(i) for i in values]

    if max(value_ns) <= 0xFFFFFFFF:
        return NfcUnit.UNIT_NS, [i for i in value_ns]
    if max(value_us) <= 0xFFFFFFFF:
        return NfcUnit.UNIT_US, [i for i in value_us]
    if max(value_ms) <= 0xFFFFFFFF:
        return NfcUnit.UNIT_MS, [i for i in value_ms]
    return NfcUnit.UNIT_S, [i for i in value_s]

# region All Types


@unique
class TechnologyType(IntEnum):
    """Communication technology type"""
    TYPE_A = 1
    TYPE_B = 2
    TYPE_MIFARE = 3
    TYPE_VICINITY = 4
    TYPE_FELICA = 5
    TYPE_FELICA_424 = 7
    TYPE_FELICA_212 = 8


def MPC_SelectType(card_type: TechnologyType) -> None:
    """Selects the PICC technology type

    Parameters
    ----------
    card_type : TechnologyType
        Technology type
    """
    if not isinstance(card_type, TechnologyType):
        raise TypeError('card_type must be an instance of '
                        'TechnologyType IntEnum')
    CTS3Exception._check_error(_MPuLib.MPC_SelectType(
        c_uint8(0),
        c_uint8(card_type)))


def MPC_SelectModulationASK(ask: float) -> None:
    """Selects ASK modulation index

    Parameters
    ----------
    ask : float
        ASK modulation in %
    """
    ask_pm = round(ask * 1e1)
    _check_limits(c_uint16, ask_pm, 'ask')
    CTS3Exception._check_error(_MPuLib.MPC_SelectModulationASKpt(
        c_uint8(0),
        c_uint16(ask_pm)))


@unique
class FieldUnit(IntEnum):
    """Field strength unit"""
    UNIT_PER_CENT = 1
    APPLY_DEFAULT_VALUE = 3
    UNIT_PER_MILLE = 4
    UNIT_MV_RANGE_2V5 = 8
    UNIT_MV_RANGE_18V = 9
    UNIT_MV_RANGE_25V = 10
    UNIT_MV_RANGE_30V = 11
    UNIT_DBM_RANGE_11DBM = 12
    UNIT_DBM_RANGE_29DBM = 13
    UNIT_DBM_RANGE_31DBM = 14
    UNIT_DBM_RANGE_33DBM = 15


def MPC_SelectFieldStrength(unit: FieldUnit, value: float,
                            max_duration: Optional[float] = None) -> None:
    """Applies a field on the Tx connector

    Parameters
    ----------
    unit : FieldUnit
        Field strength unit
    value : float
        Field strength in mVpp, dBm, % or ‰
        (ignored if unit is APPLY_DEFAULT_VALUE)
    max_duration : float, optional
        Maximum duration of the field in s, or None to let the field applied
    """
    if not isinstance(unit, FieldUnit):
        raise TypeError('unit must be an instance of FieldUnit IntEnum')
    max_duration_ms = 0
    if max_duration:
        max_duration_ms = round(max_duration * 1e3)
        _check_limits(c_uint32, max_duration_ms, 'max_duration')

    if unit == FieldUnit.APPLY_DEFAULT_VALUE:
        CTS3Exception._check_error(_MPuLib.MPC_SelectFieldStrengthEx(
            c_uint8(0),
            c_uint8(unit),
            c_int16(0),
            c_uint32(max_duration_ms)))
    elif unit == FieldUnit.UNIT_PER_CENT:
        value_pm = round(value * 1e1)
        _check_limits(c_int16, value_pm, 'value')
        CTS3Exception._check_error(_MPuLib.MPC_SelectFieldStrengthEx(
            c_uint8(0),
            c_uint8(FieldUnit.UNIT_PER_MILLE),
            c_int16(value_pm),
            c_uint32(max_duration_ms)))
    elif unit == FieldUnit.UNIT_PER_MILLE or \
            unit == FieldUnit.UNIT_DBM_RANGE_11DBM or \
            unit == FieldUnit.UNIT_DBM_RANGE_29DBM or \
            unit == FieldUnit.UNIT_DBM_RANGE_31DBM or \
            unit == FieldUnit.UNIT_DBM_RANGE_33DBM:
        value_pm = round(value)
        _check_limits(c_int16, value_pm, 'value')
        CTS3Exception._check_error(_MPuLib.MPC_SelectFieldStrengthEx(
            c_uint8(0),
            c_uint8(unit),
            c_int16(value_pm),
            c_uint32(max_duration_ms)))
    else:  # mV
        value_mV = round(value)
        _check_limits(c_int16, value_mV, 'value')
        CTS3Exception._check_error(_MPuLib.MPC_SelectFieldStrengthEx(
            c_uint8(0),
            c_uint8(unit),
            c_int16(value_mV),
            c_uint32(max_duration_ms)))


def MPC_SetupFindFieldStrength(expected_voltage: float) \
        -> Dict[str, Union[float, int]]:
    """Reaches Vov by adjusting RF field strength

    Parameters
    ----------
    expected_voltage : float
        Vdc value to reach in V

    Returns
    -------
    dict
        'voltage_reached' (float): Reached Vdc in V
        'field_per_mille' (int): Reached field strength in ‰
    """
    expected_voltage_mV = round(expected_voltage * 1e3)
    _check_limits(c_uint32, expected_voltage_mV, 'expected_voltage')
    voltage = c_uint32()
    field = c_uint16()
    CTS3Exception._check_error(_MPuLib.MPC_SetupFindFieldStrength(
        c_uint8(0),
        c_uint32(0),
        c_uint32(expected_voltage_mV),
        byref(field),
        byref(voltage)))
    return {'voltage_reached': voltage.value / 1e3,
            'field_per_mille': field.value}


def MPC_SelectCarrier(frequency: float) -> None:
    """Selects the carrier frequency

    Parameters
    ----------
    frequency : float
        Carrier frequency in Hz
    """
    MPC_SelectCarrierExt(frequency)


def MPC_SelectCarrierExt(frequency: float) -> None:
    """Selects the carrier frequency

    Parameters
    ----------
    frequency : float
        Carrier frequency in Hz
    """
    CTS3Exception._check_error(_MPuLib.MPC_SelectCarrierExt(
        c_uint8(0),
        c_double(frequency)))


def MPC_SelectFallAndRiseTime(falling_time: float,
                              rising_time: float) -> None:
    """Selects modulation rising and falling time

    Parameters
    ----------
    falling_time : float
        Falling time in s
    rising_time : float
        Rising time in s
    """
    falling_time_ns = round(falling_time * 1e9)
    _check_limits(c_uint16, falling_time_ns, 'falling_time')
    rising_time_ns = round(rising_time * 1e9)
    _check_limits(c_uint16, rising_time_ns, 'rising_time')
    CTS3Exception._check_error(_MPuLib.MPC_SelectFallAndRiseTime(
        c_uint8(0),
        c_uint16(falling_time_ns),
        c_uint16(rising_time_ns)))


def MPC_SelectFieldRiseTime(rising_time: float) -> None:
    """Selects the RF field rising time

    Parameters
    ----------
    rising_time : float
        Field rising time in s
    """
    rising_time_us = round(rising_time * 1e6)
    _check_limits(c_uint32, rising_time_us, 'rising_time')
    CTS3Exception._check_error(_MPuLib.MPC_SelectFieldRiseTime(
        c_uint8(0),
        c_uint32(rising_time_us)))


def MPC_PiccResetSlow(falling_time: float, low_time: float,
                      rising_time: float, delay: float,
                      tx_frame: bytes,
                      tx_bits_number: Optional[int] = None) \
        -> Dict[str, Union[int, bytes]]:
    """Performs an RF field reset and then exchanges command

    Parameters
    ----------
    falling_time : float
        RF field falling time in s
    low_time : float
        Delay between Reset and Power On in s
    rising_time : float
        RF field rising time in s
    delay : float
        Delay between Reset and Power On and frame transmission in s
    tx_frame : bytes
        Frame to send
    tx_bits_number : int, optional
        Number of bits to send (8 × tx_frame length if None)

    Returns
    -------
    dict
        'rx_frame' (bytes): Received frame
        'rx_bits_number' (int): Number of received bits
    """
    falling_time_ms = round(falling_time * 1e3)
    _check_limits(c_uint32, falling_time_ms, 'falling_time')
    low_time_us = round(low_time * 1e6)
    _check_limits(c_uint32, low_time_us, 'low_time')
    rising_time_ms = round(rising_time * 1e3)
    _check_limits(c_uint32, rising_time_ms, 'rising_time')
    delay_us = round(delay * 1e6)
    _check_limits(c_uint32, delay_us, 'delay')
    if not isinstance(tx_frame, bytes):
        raise TypeError('tx_frame must be an instance of bytes')
    data = bytes(1000)
    rx_bits = c_uint32()
    if tx_frame:
        if tx_bits_number is None:
            tx_bits_number = 8 * len(tx_frame)
        _check_limits(c_uint32, tx_bits_number, 'tx_bits_number')
        CTS3Exception._check_error(_MPuLib.MPC_PiccResetSlow(
            c_uint8(0),
            c_uint32(falling_time_ms),
            c_uint32(low_time_us),
            c_uint32(rising_time_ms),
            c_uint32(delay_us),
            tx_frame,
            c_uint32(tx_bits_number),
            data,
            byref(rx_bits)))
    else:
        CTS3Exception._check_error(_MPuLib.MPC_PiccResetSlow(
            c_uint8(0),
            c_uint32(falling_time_ms),
            c_uint32(low_time_us),
            c_uint32(rising_time_ms),
            c_uint32(delay_us),
            None,
            c_uint32(0),
            data,
            byref(rx_bits)))
    bytes_number = int(rx_bits.value / 8)
    if rx_bits.value % 8 > 0:
        bytes_number += 1
    return {'rx_frame': data[:bytes_number],
            'rx_bits_number': rx_bits.value}


def MPC_ForceModulationASK(activate: bool) -> None:
    """Sets the field value to its ASK modulated state

    Parameters
    ----------
    activate : bool
        True to set the field to its modulated state
    """
    CTS3Exception._check_error(_MPuLib.MPC_ForceModulationASK(
        c_uint8(0),
        c_bool(activate)))


def MPC_SetFWTETU(fwt_etu: int) -> None:
    """Sets Frame Waiting Time duration

    Parameters
    ----------
    fwt_etu : int
        FWT in etu
    """
    _check_limits(c_uint32, fwt_etu, 'fwt_etu')
    CTS3Exception._check_error(_MPuLib.MPC_SetFWTETU(
        c_uint8(0),
        c_uint32(fwt_etu)))


def MPC_SetFWTus(fwt: float) -> None:
    """Sets Frame Waiting Time duration

    Parameters
    ----------
    fwt : float
        FWT in s
    """
    fwt_us = round(fwt * 1e6)
    _check_limits(c_uint32, fwt_us, 'fwt')
    CTS3Exception._check_error(_MPuLib.MPC_SetFWTus(
        c_uint8(0),
        c_uint32(fwt_us)))


@unique
class DataRate(IntEnum):
    """Data rate"""
    DATARATE_106KB = 106
    DATARATE_212KB = 212
    DATARATE_424KB = 424
    DATARATE_848KB = 848
    DATARATE_1695KB = 1695
    DATARATE_3390KB = 3390
    DATARATE_6780KB = 6780


def MPC_SelectDataRate(pcd_data_rate: DataRate,
                       picc_data_rate: DataRate) -> None:
    """Selects data rate

    Parameters
    ----------
    pcd_data_rate : DataRate
        PCD to PICC data rate
    picc_data_rate : DataRate
        PICC to PCD data rate
    """
    if not isinstance(pcd_data_rate, DataRate):
        raise TypeError('pcd_data_rate must be an instance of '
                        'DataRate IntEnum')
    if not isinstance(picc_data_rate, DataRate):
        raise TypeError('picc_data_rate must be an instance of '
                        'DataRate IntEnum')
    CTS3Exception._check_error(_MPuLib.MPC_SelectDataRate(
        c_uint8(0),
        c_uint16(pcd_data_rate),
        c_uint16(picc_data_rate)))


def MPC_ExchangeCmd(tx_frame: bytes,
                    tx_bits_number: Optional[int] = None) \
        -> Dict[str, Union[bytes, int]]:
    """Exchanges a low level command

    Parameters
    ----------
    tx_frame : bytes
        Frame to transmit
    tx_bits_number : int, optional
        Number of bits to transmit (8 × tx_frame length if None)

    Returns
    -------
    dict
        'rx_frame' (bytes): Received frame
        'rx_bits_number' (int): Number of received bits
    """
    if tx_frame and not isinstance(tx_frame, bytes):
        raise TypeError('tx_frame must be an instance of bytes')
    data = bytes(5000)
    rx_bits = c_uint32()
    if tx_frame:
        if tx_bits_number is None:
            tx_bits_number = 8 * len(tx_frame)
        _check_limits(c_uint32, tx_bits_number, 'tx_bits_number')
        CTS3Exception._check_error(_MPuLib.MPC_ExchangeCmd(
            c_uint8(0),
            tx_frame,
            c_uint32(tx_bits_number),
            data,
            byref(rx_bits)))
    else:
        CTS3Exception._check_error(_MPuLib.MPC_ExchangeCmd(
            c_uint8(0),
            None,
            c_uint32(0),
            data,
            byref(rx_bits)))
    bytes_number = int(rx_bits.value / 8)
    if rx_bits.value % 8 > 0:
        bytes_number += 1
    return {'rx_frame': data[:bytes_number],
            'rx_bits_number': rx_bits.value}


def MPC_DeselectSequence() -> None:
    """Performs a deselect sequence"""
    CTS3Exception._check_error(_MPuLib.MPC_DeselectSequence(
        c_uint8(0)))


def MPC_SendFrameProtocol(tx_frame: bytes) -> bytes:
    """Exchanges an ISO14443-4 frame

    Parameters
    ----------
    tx_frame : bytes
        Frame to transmit

    Returns
    -------
    bytes
        Received frame
    """
    data = bytes(0xFFFF)
    length = c_uint32()
    if not isinstance(tx_frame, bytes):
        raise TypeError('tx_frame must be an instance of bytes')
    _check_limits(c_uint32, len(tx_frame), 'tx_frame')
    CTS3Exception._check_error(_MPuLib.MPC_SendFrameProtocol(
        c_uint8(0),
        tx_frame,
        c_uint32(len(tx_frame)),
        data,
        byref(length)))
    return data[:length.value]


def MPC_SendAPDU(header: Union[bytes, int], lc_field: Optional[bytes] = None,
                 le: Optional[int] = 0) -> Dict[str, Union[bytes, int]]:
    """Sends an Application Protocol Data Unit command

    Parameters
    ----------
    header : bytes or int
        4-byte APDU header
    lc_field : bytes, optional
        Data to send
    le : int, optional
        Expected data size

    Returns
    -------
    dict
        'le_field' (bytes): Received data
        'status_word' (int): PICC status word
    """
    if isinstance(header, bytes):
        if len(header) != 4:
            raise TypeError('header must be an instance of 4 bytes')
        header_value = header[0] << 24
        header_value |= header[1] << 16
        header_value |= header[2] << 8
        header_value |= header[3]
    elif isinstance(header, int):
        _check_limits(c_uint32, header, 'header')
        header_value = header
    else:
        raise TypeError('header must be an instance of int or 4 bytes')
    if lc_field:
        if not isinstance(lc_field, bytes):
            raise TypeError('lc_field must be an instance of bytes')
        if len(lc_field) > 0xFFFF:
            # LC_EXTENDED
            _check_limits(c_uint32, 0x40000000 | len(lc_field), 'lc_field')
            lc = c_uint32(0x40000000 | len(lc_field))
        else:
            _check_limits(c_uint32, len(lc_field), 'lc_field')
            lc = c_uint32(len(lc_field))
    else:
        lc = c_uint32(0x80000000)  # NO_LC
    data = bytes(0xFFFF)
    le_len = c_uint32()
    status_word = c_uint16()
    if le is not None:
        if le == 0:
            computed_le = c_uint32(256)
        elif le > 256:
            # LE_EXTENDED
            _check_limits(c_uint32, 0x40000000 | le, 'le')
            computed_le = c_uint32(0x40000000 | le)
        else:
            _check_limits(c_uint32, le, 'le')
            computed_le = c_uint32(le)
    else:
        computed_le = c_uint32(0x80000000)  # NO_LE
    CTS3Exception._check_error(_MPuLib.MPC_SendAPDU(
        c_uint8(0),
        c_uint32(header_value),
        lc,
        lc_field,
        computed_le,
        data,
        byref(le_len),
        byref(status_word)))
    return {'le_field': data[:le_len.value],
            'status_word': status_word.value}


def MPC_SendSBlockParameters(tx_frame: bytes) -> bytes:
    """Sends an S(PARAMETERS) block

    Parameters
    ----------
    tx_frame : bytes
        INF field of S(PARAMETERS) block to send (without CRC)

    Returns
    -------
    bytes
        INF field of S(PARAMETERS) block answered
    """
    if not isinstance(tx_frame, bytes):
        raise TypeError('tx_frame must be an instance of bytes')
    _check_limits(c_uint16, len(tx_frame), 'tx_frame')
    data = bytes(550)
    length = c_uint16()
    CTS3Exception._check_error(_MPuLib.MPC_SendSBlockParameters(
        c_uint8(0),
        tx_frame,
        c_uint16(len(tx_frame)),
        data,
        byref(length)))
    return data[:length.value]


def MPC_SetTxDelay(tx_delay: float, unit: NfcUnit) -> None:
    """Selects delay between Rx frame and following Tx frame

    Parameters
    ----------
    tx_delay : float
        Delay to apply
    unit : NfcUnit
        Delay unit
    """
    if not isinstance(unit, NfcUnit):
        raise TypeError('unit must be an instance of NfcUnit IntEnum')
    # Unit auto-selection
    computed_unit, [computed_delay] = _unit_autoselect(unit, [tx_delay])
    _check_limits(c_uint32, computed_delay, 'tx_delay')
    CTS3Exception._check_error(_MPuLib.MPC_SetTxDelay(
        c_uint8(0),
        c_uint16(0) if tx_delay == 0 else c_uint16(1),
        c_uint32(computed_delay),
        c_uint32(computed_unit)))


def MPC_SendOneModulation() -> None:
    """Sends a single modulation"""
    CTS3Exception._check_error(_MPuLib.MPC_SendOneModulation(
        c_uint8(0)))

# endregion

# region Type A


def MPC_SelectPauseWidth(pause: float) -> None:
    """Selects Type A pause width

    Parameters
    ----------
    pause : float
        Pause duration in s
    """
    pause_ns = round(pause * 1e9)
    _check_limits(c_uint16, pause_ns, 'pause')
    CTS3Exception._check_error(_MPuLib.MPC_SelectPauseWidth(
        c_uint8(0),
        c_uint16(pause_ns)))


def MPC_RequestA() -> bytes:
    """Sends a Type A REQ command

    Returns
    -------
    bytes
        Answer to REQA
    """
    atqa = c_uint16()
    CTS3Exception._check_error(_MPuLib.MPC_RequestA(
        c_uint8(0),
        byref(atqa)))
    return bytes([atqa.value & 0xFF, atqa.value >> 8])


def MPC_WakeUpA() -> bytes:
    """Sends a Type A WUP command

    Returns
    -------
    bytes
        Answer to WUPA
    """
    atqa = c_uint16()
    CTS3Exception._check_error(_MPuLib.MPC_WakeUpA(
        c_uint8(0),
        byref(atqa)))
    return bytes([atqa.value & 0xFF, atqa.value >> 8])


def MPC_AnticollA() -> Dict[str, bytes]:
    """Performs Type A anti-collision

    Returns
    -------
    dict
        'uid' (bytes): PICC UID
        'sak' (bytes): PICC SAK
    """
    uid = bytes(12)
    sak = c_uint8()
    length = c_uint16()
    CTS3Exception._check_error(_MPuLib.MPC_AnticollA(
        c_uint8(0),
        uid,
        byref(length),
        byref(sak)))
    return {'uid': uid[:length.value], 'sak': bytes([sak.value])}


def MPC_SelectCardA(uid: bytes) -> bytes:
    """Selects a Type A PICC based on its UID

    Parameters
    ----------
    uid : bytes
        PICC UID

    Returns
    -------
    bytes
        PICC SAK
    """
    if not isinstance(uid, bytes):
        raise TypeError('uid must be an instance of bytes')
    _check_limits(c_uint16, len(uid), 'uid')
    sak = c_uint8()
    CTS3Exception._check_error(_MPuLib.MPC_SelectCardA(
        c_uint8(0),
        uid,
        c_uint16(len(uid)),
        byref(sak)))
    return bytes([sak.value])


def MPC_GetPosColl() -> int:
    """Gets collision position

    Returns
    -------
    int
        Collision position
    """
    position = c_uint32()
    CTS3Exception._check_error(_MPuLib.MPC_GetPosColl(
        c_uint8(0),
        byref(position)))
    return position.value


def MPC_HaltA() -> None:
    """Sends a Type A HLT command"""
    CTS3Exception._check_error(_MPuLib.MPC_HaltA(
        c_uint8(0)))


def MPC_SendRATS(rats: Optional[bytes] = None) -> bytes:
    """Sends an RATS command

    Parameters
    ----------
    rats : bytes, optional
        RATS command (default RATS if None)

    Returns
    -------
    bytes
        PICC ATS
    """
    data = bytes(550)
    length = c_uint16()
    if rats:
        if not isinstance(rats, bytes):
            raise TypeError('snr must be an instance of bytes')
        _check_limits(c_uint16, len(rats), 'rats')
        CTS3Exception._check_error(_MPuLib.MPC_SendRATSFree(
            c_uint8(0),
            rats,
            c_uint16(len(rats)),
            data,
            byref(length)))
    else:
        CTS3Exception._check_error(_MPuLib.MPC_SendRATS(
            c_uint8(0),
            data,
            byref(length)))
    return data[:length.value]


def MPC_SendPPS(cid: Union[int, bytes], dri: Union[int, bytes],
                dsi: Union[int, bytes]) -> None:
    """Sends a PPS command

    Parameters
    ----------
    cid : bytes or int
        Card identifier
    dri : bytes or int
        Divisor Receive Integer
    dsi : bytes or int
        Divisor Send Integer
    """
    if isinstance(cid, bytes):
        if len(cid) != 1:
            raise TypeError('cid must be an instance of 1 byte')
        cid_value = cid[0]
    elif isinstance(cid, int):
        _check_limits(c_uint8, cid, 'cid')
        cid_value = cid
    else:
        raise TypeError('cid must be an instance of int or 1 byte')
    if isinstance(dri, bytes):
        if len(dri) != 1:
            raise TypeError('dri must be an instance of 1 byte')
        dri_value = dri[0]
    elif isinstance(dri, int):
        _check_limits(c_uint8, dri, 'dri')
        dri_value = dri
    else:
        raise TypeError('dri must be an instance of int or 1 byte')
    if isinstance(dsi, bytes):
        if len(dsi) != 1:
            raise TypeError('dsi must be an instance of 1 byte')
        dsi_value = dsi[0]
    elif isinstance(dsi, int):
        _check_limits(c_uint8, dsi, 'dsi')
        dsi_value = dsi
    else:
        raise TypeError('dsi must be an instance of int or 1 byte')
    CTS3Exception._check_error(_MPuLib.MPC_SendPPS(
        c_uint8(0),
        c_uint8(cid_value),
        c_uint8(dri_value),
        c_uint8(dsi_value)))


def MPC_ExchangeCmdRawA(tx_frame: Optional[bytes],
                        tx_bits_number: Optional[int] = None) \
        -> Dict[str, Union[bytes, int]]:
    """Exchanges 106 kb/s sequences

    Parameters
    ----------
    tx_frame : bytes
        Frame to send
    tx_bits_number : int, optional
        Number of bits to send (8 × tx_frame length if None)

    Returns
    -------
    dict
        'rx_frame' (bytes): Received frame
        'rx_bits_number' (int): Number of received sequences
    """
    if tx_frame is None:
        tx_bits_number = 0
    else:
        if not isinstance(tx_frame, bytes):
            raise TypeError('tx_frame must be an instance of bytes')
        if tx_bits_number is None:
            tx_bits_number = 8 * len(tx_frame)
        _check_limits(c_uint32, tx_bits_number, 'tx_bits_number')
    data = bytes(1000)
    rx_bits = c_uint32()
    CTS3Exception._check_error(_MPuLib.MPC_ExchangeCmdRawA(
        c_uint8(0),
        tx_frame,
        c_uint32(tx_bits_number),
        data,
        byref(rx_bits)))
    bytes_number = int(rx_bits.value / 8)
    if rx_bits.value % 8 > 0:
        bytes_number += 1
    return {'rx_frame': data[:bytes_number],
            'rx_bits_number': rx_bits.value}


def MPC_PowerOnGetFrameFromSpecialTagA(unit: FieldUnit, value: int,
                                       timeout: float, nb_id_to_get: int) \
        -> Dict[str, Union[bytes, int]]:
    """Switches the RF field on and gets the data transmitted
    by an NFC tag in read-only TTF mode

    Parameters
    ----------
    unit : FieldUnit
        Field strength unit
    value : float
        Field strength in mV, dBm, % or ‰
    timeout : float
        Timeout in s
    nb_id_to_get : int
        Number of codes to read

    Returns
    -------
    dict
        'rx_frame' (bytes): Received frame
        'rx_bits_number' (int): Number of received bits
    """
    if not isinstance(unit, FieldUnit):
        raise TypeError('unit must be an instance of FieldUnit IntEnum')
    timeout_ms = round(timeout * 1e3)
    _check_limits(c_uint32, timeout_ms, 'timeout')
    _check_limits(c_uint32, nb_id_to_get, 'nb_id_to_get')
    data = bytes(10240)
    rx_bits = c_uint32()
    if unit == FieldUnit.UNIT_PER_CENT:
        value_pm = round(value * 1e1)
        _check_limits(c_int16, value_pm, 'value')
        CTS3Exception._check_error(_MPuLib.MPC_PowerOnGetFrameFromSpecialTagA(
            c_uint8(0),
            c_uint8(FieldUnit.UNIT_PER_MILLE),
            c_int16(value_pm),
            c_uint32(timeout_ms),
            c_uint32(nb_id_to_get),
            data,
            byref(rx_bits)))
    elif unit == FieldUnit.UNIT_PER_MILLE or \
            unit == FieldUnit.UNIT_DBM_RANGE_11DBM or \
            unit == FieldUnit.UNIT_DBM_RANGE_29DBM or \
            unit == FieldUnit.UNIT_DBM_RANGE_31DBM or \
            unit == FieldUnit.UNIT_DBM_RANGE_33DBM:
        value_pm = round(value)
        _check_limits(c_int16, value_pm, 'value')
        CTS3Exception._check_error(_MPuLib.MPC_PowerOnGetFrameFromSpecialTagA(
            c_uint8(0),
            c_uint8(unit),
            c_int16(value_pm),
            c_uint32(timeout_ms),
            c_uint32(nb_id_to_get),
            data,
            byref(rx_bits)))
    else:  # mV
        value_mV = round(value)
        _check_limits(c_int16, value_mV, 'value')
        CTS3Exception._check_error(_MPuLib.MPC_PowerOnGetFrameFromSpecialTagA(
            c_uint8(0),
            c_uint8(unit),
            c_int16(value_mV),
            c_uint32(timeout_ms),
            c_uint32(nb_id_to_get),
            data,
            byref(rx_bits)))

    bytes_number = int(rx_bits.value / 8)
    if rx_bits.value % 8 > 0:
        bytes_number += 1
    return {'rx_frame': data[:bytes_number],
            'rx_bits_number': rx_bits.value}

# endregion

# region Type B


def MPC_RequestB(slots_number: int) -> bytes:
    """Sends a Type B REQ command

    Parameters
    ----------
    slots_number : int
        Number of slots

    Returns
    -------
    bytes
        Answer to REQB
    """
    _check_limits(c_uint8, slots_number, 'slots_number')
    data = bytes(550)
    length = c_uint16()
    CTS3Exception._check_error(_MPuLib.MPC_RequestB(
        c_uint8(0),
        c_uint8(slots_number),
        data,
        byref(length)))
    return data[:length.value]


def MPC_RequestBFree(reqb: bytes) -> bytes:
    """Sends a Type B REQ command

    Parameters
    ----------
    reqb : bytes
        REQB command

    Returns
    -------
    bytes
        Answer to REQB
    """
    if not isinstance(reqb, bytes):
        raise TypeError('reqb must be an instance of bytes')
    _check_limits(c_uint16, len(reqb), 'reqb')
    data = bytes(550)
    length = c_uint16()
    CTS3Exception._check_error(_MPuLib.MPC_RequestBFree(
        c_uint8(0),
        reqb,
        c_uint16(len(reqb)),
        data,
        byref(length)))
    return data[:length.value]


def MPC_WakeUpB(slots_number: int) -> bytes:
    """Sends a Type B WUP command

    Parameters
    ----------
    slots_number : int
        Number of slots

    Returns
    -------
    bytes
        Answer to WUPB
    """
    _check_limits(c_uint8, slots_number, 'slots_number')
    data = bytes(550)
    length = c_uint16()
    CTS3Exception._check_error(_MPuLib.MPC_WakeUpB(
        c_uint8(0),
        c_uint8(slots_number),
        data,
        byref(length)))
    return data[:length.value]


def MPC_SlotMarkerCmd(slot_number: int) -> bytes:
    """Sends a Type B Slot-MARKER command

    Parameters
    ----------
    slot_number : int
        Slot number to check

    Returns
    -------
    bytes
        Answer to WUPB
    """
    _check_limits(c_uint8, slot_number, 'slot_number')
    data = bytes(550)
    length = c_uint16()
    CTS3Exception._check_error(_MPuLib.MPC_SlotMarkerCmd(
        c_uint8(0),
        c_uint8(slot_number),
        data,
        byref(length)))
    return data[:length.value]


def MPC_HaltB(identifier: bytes) -> None:
    """Sends a Type B HLT command

    Parameters
    ----------
    identifier : bytes
        4-byte PICC identifier
    """
    if not isinstance(identifier, bytes) or len(identifier) != 4:
        raise TypeError('identifier must be an instance of 4 bytes')
    CTS3Exception._check_error(_MPuLib.MPC_HaltB(
        c_uint8(0),
        identifier))


def MPC_SendATTRIB(attrib: bytes) -> bytes:
    """Sends a Type B ATTRIB command

    Parameters
    ----------
    attrib : int
        ATTRIB command

    Returns
    -------
    bytes
        Answer to ATTRIB
    """
    if not isinstance(attrib, bytes):
        raise TypeError('attrib must be an instance of bytes')
    _check_limits(c_uint16, len(attrib), 'attrib')
    data = bytes(512)
    length = c_uint16()
    CTS3Exception._check_error(_MPuLib.MPC_SendATTRIB(
        c_uint8(0),
        attrib,
        c_uint16(len(attrib)),
        data,
        byref(length)))
    return data[:length.value]


def MPC_SelectETUWidthTX(etu_logic_0: int, etu_logic_1: int) -> None:
    """Selects the duration of logic '0' and '1' states for all Type B bits

    Parameters
    ----------
    etu_logic_0 : int
        Logic '0' duration in carrier periods
    etu_logic_1 : int
        Logic '1' duration in carrier periods
    """
    _check_limits(c_uint16, etu_logic_0, 'etu_logic_0')
    _check_limits(c_uint16, etu_logic_1, 'etu_logic_1')
    CTS3Exception._check_error(_MPuLib.MPC_SelectETUWidthTX(
        c_uint8(0),
        c_uint16(etu_logic_0),
        c_uint16(etu_logic_1)))

# endregion

# region FeliCa


def MPC_FelicaPolling(system_code: Union[bytes, int],
                      request_code: Union[bytes, int],
                      time_slot: Union[bytes, int]) -> bytes:
    """Performs a polling request

    Parameters
    ----------
    system_code : bytes or int
        2-byte card system identifier
    request_code : bytes or int
        Request code byte
    time_slot : bytes or int
        Time slot byte

    Returns
    -------
    bytes
        PICC answer
    """
    if isinstance(system_code, bytes):
        if len(system_code) != 2:
            raise TypeError('system_code must be an instance of 2 bytes')
        sc_value = system_code[0] << 8
        sc_value |= system_code[1]
    elif isinstance(system_code, int):
        _check_limits(c_uint16, system_code, 'system_code')
        sc_value = system_code
    else:
        raise TypeError('system_code must be an instance of int or 2 bytes')
    if isinstance(request_code, bytes):
        if len(request_code) != 1:
            raise TypeError('request_code must be an instance of 1 byte')
        rc_value = request_code[0]
    elif isinstance(request_code, int):
        _check_limits(c_uint8, request_code, 'request_code')
        rc_value = request_code
    else:
        raise TypeError('request_code must be an instance of int or 1 byte')
    if isinstance(time_slot, bytes):
        if len(time_slot) != 1:
            raise TypeError('time_slot must be an instance of 1 byte')
        ts_value = time_slot[0]
    elif isinstance(time_slot, int):
        _check_limits(c_uint8, time_slot, 'time_slot')
        ts_value = time_slot
    else:
        raise TypeError('time_slot must be an instance of int or 1 byte')

    data = bytes(550)
    length = c_uint16()
    CTS3Exception._check_error(_MPuLib.MPC_FelicaPolling(
        c_uint8(0),
        c_uint16(sc_value),
        c_uint8(rc_value),
        c_uint8(ts_value),
        data,
        byref(length)))
    return data[:length.value]


def MPC_FELICA_Polling(system_code: Union[bytes, int],
                       request_code: Union[bytes, int],
                       time_slot: Union[bytes, int]) -> bytes:
    """Performs a polling request

    Parameters
    ----------
    system_code : bytes or int
        2-byte card system identifier
    request_code : bytes or int
        Request code byte
    time_slot : bytes or int
        Time slot byte

    Returns
    -------
    bytes
        PICC answer
    """
    warn('MPC_FELICA_Polling renamed as MPC_FelicaPolling',
         FutureWarning, 2)
    return MPC_FelicaPolling(system_code, request_code, time_slot)


class FelicaService():
    """FeliCa Service Code

    Attributes
    ----------
    service_number : int
        Service number
    access_attribute : int
        Access Attribute
    """

    def __init__(self, service_number: int, access_attribute: int):
        """Inits FelicaService

        Parameters
        ----------
        service_number : int
            Service number
        access_attribute : int
            Access Attribute
        """
        if service_number > 0x3FF:
            raise OverflowError('service_number is out of range')
        if access_attribute > 0x3F:
            raise OverflowError('access_attribute is out of range')
        self.service_number = service_number
        self.access_attribute = access_attribute

    def _get_int(self) -> int:
        """Converts FelicaService to 16-bit integer

        Returns
        -------
        int
            Integer representation of FelicaService
        """
        val = (self.service_number >> 2) & 0xFF
        val |= (self.service_number << 14) & 0xC000
        val |= self.access_attribute << 8
        return val


class FelicaBlock():
    """FeliCa Block List Element

    Attributes
    ----------
    len : bool
        Len bit
    access_mode : int
        Access Mode
    service_order : int
        Service Code List Order
    block_number : int
        Block Number
    """

    def __init__(self, access_mode: int, service_order: int,
                 block_number: int,
                 two_byte_block: Optional[bool] = None):
        """Inits FelicaBlock

        Parameters
        ----------
        access_mode : int
            Access Mode
        service_order : int
            Service Code List Order
        block_number : int
            Block Number
        two_byte_block : bool, optional
            True if Block List Element is two-byte long,
            None to use three-byte only if required by Block Number
        """
        if access_mode > 0x07:
            raise OverflowError('access_mode is out of range')
        if service_order > 0x0F:
            raise OverflowError('service_order is out of range')
        if block_number > 0xFFFF:
            raise OverflowError('block_number is out of range')
        if two_byte_block is None:
            self.two_byte_block = block_number < 0x100
        else:
            if two_byte_block and block_number > 0xFF:
                raise OverflowError('two-byte block_number is out of range')
            self.two_byte_block = two_byte_block
        self.access_mode = access_mode
        self.service_order = service_order
        self.block_number = block_number

    def _get_int(self) -> int:
        """Converts FelicaBlock to 32-bit integer

        Returns
        -------
        int
            Integer representation of FelicaBlock
        """
        val = (self.access_mode & 0x07) << 4
        val |= self.service_order & 0x0F
        if self.two_byte_block:
            val |= 0x80
            val |= (self.block_number & 0xFF) << 8
        else:
            val |= (self.block_number >> 8) << 16
            val |= (self.block_number & 0xFF) << 8
        return val


@overload
def MPC_FelicaCheck(idm: bytes, service_codes: List[FelicaService],
                    blocks: List[FelicaBlock]) \
        -> Dict[str, Union[bytes, int, List[bytes]]]:
    ...


@overload
def MPC_FelicaCheck(idm: bytes, service_codes: List[int],
                    blocks: List[int]) \
        -> Dict[str, Union[bytes, int, List[bytes]]]:
    ...


def MPC_FelicaCheck(idm,  # type: ignore[no-untyped-def]
                    service_codes, blocks):
    """Reads FeliCa memory blocks

    Parameters
    ----------
    idm : bytes
        8-byte manufacturer identifier
    service_codes : list(FelicaService) or list(int)
        Services list
    blocks : list(FelicaBlock) or list(int)
        Blocks list

    Returns
    -------
    dict
        'idm2' (bytes): Answered manufacturer 8-byte identifier
        'status1' (int): Status flag 1
        'status2' (int): Status flag 2
        'data' (list(bytes)): Read 16-byte blocks
    """
    if not isinstance(idm, bytes) or len(idm) != 8:
        raise TypeError('idm must be an instance of 8 bytes')
    if not isinstance(service_codes, list):
        raise TypeError('service_codes must be an instance of '
                        'FelicaService list or int list')
    _check_limits(c_uint8, len(service_codes), 'service_codes')
    if not isinstance(blocks, list):
        raise TypeError('blocks must be an instance of '
                        'FelicaBlock list or int list')
    _check_limits(c_uint8, len(blocks), 'blocks')

    services_list = (c_uint16 * len(service_codes))()
    for i in range(len(service_codes)):
        if isinstance(service_codes[i], FelicaService):
            services_list[i] = c_uint16(service_codes[i]._get_int())
        elif isinstance(service_codes[i], int):
            _check_limits(c_uint16, service_codes[i], 'service_codes')
            services_list[i] = c_uint16(service_codes[i])
        else:
            raise TypeError('service_codes must be an instance of '
                            'FelicaService list or int list')
    blocks_list = (c_uint32 * len(blocks))()
    for i in range(len(blocks)):
        if isinstance(blocks[i], FelicaBlock):
            blocks_list[i] = c_uint32(blocks[i]._get_int())
        elif isinstance(blocks[i], int):
            _check_limits(c_uint32, blocks[i], 'blocks')
            blocks_list[i] = c_uint32(blocks[i])
        else:
            raise TypeError('blocks must be an instance of '
                            'FelicaBlock list or int list')

    data = bytes(16 * len(blocks))
    idm2 = bytes(8)
    length = c_uint8()
    status1 = c_uint8()
    status2 = c_uint8()
    CTS3Exception._check_error(_MPuLib.MPC_FelicaCheck(
        c_uint8(0),
        idm,
        c_uint8(len(service_codes)),
        services_list,
        c_uint8(len(blocks)),
        blocks_list, idm2,
        byref(status1),
        byref(status2),
        byref(length),
        data))
    data_list = []
    for i in range(0, length.value * 16, 16):
        data_list.append(data[i:i+16])
    return {'idm2': idm2,
            'status1': status1.value,
            'status2': status2.value,
            'data': data_list}


def MPC_FELICA_Read_Without_Encryption(idm: bytes, service_codes: List[int],
                                       blocks: List[int]) \
        -> Dict[str, Union[bytes, int, List[bytes]]]:
    """Reads FeliCa memory blocks

    Parameters
    ----------
    idm : bytes
        8-byte manufacturer identifier
    service_codes : list(FelicaService) or list(int)
        Services list
    blocks : list(FelicaBlock) or list(int)
        Blocks list

    Returns
    -------
    dict
        'idm2' (bytes): Answered manufacturer 8-byte identifier
        'status1' (int): Status flag 1
        'status2' (int): Status flag 2
        'data' (list(bytes)): Read 16-byte blocks
    """
    warn('MPC_FELICA_Read_Without_Encryption renamed as MPC_FelicaCheck',
         FutureWarning, 2)
    return MPC_FelicaCheck(idm, service_codes, blocks)


@overload
def MPC_FelicaUpdate(idm: bytes, service_codes: List[FelicaService],
                     blocks: List[FelicaBlock],
                     data: List[bytes]) -> Dict[str, Union[bytes, int]]:
    ...


@overload
def MPC_FelicaUpdate(idm: bytes, service_codes: List[int], blocks: List[int],
                     data: List[bytes]) -> Dict[str, Union[bytes, int]]:
    ...


def MPC_FelicaUpdate(idm,  # type: ignore[no-untyped-def]
                     service_codes, blocks, data):
    """Writes FeliCa memory blocks

    Parameters
    ----------
    idm : bytes
        8-byte manufacturer identifier
    service_codes : list(FelicaService) or list(int)
        Services list
    blocks : list(FelicaBlock) or list(int)
        Blocks list
    data : list(bytes)
        16-byte blocks to write

    Returns
    -------
    dict
        'idm2' (bytes): Answered manufacturer 8-byte identifier
        'status1' (int): Status flag 1
        'status2' (int): Status flag 2
    """
    if not isinstance(idm, bytes) or len(idm) != 8:
        raise TypeError('idm must be an instance of 8 bytes')
    if not isinstance(service_codes, list):
        raise TypeError('service_codes must be an instance of '
                        'FelicaService list or int list')
    _check_limits(c_uint8, len(service_codes), 'service_codes')
    if not isinstance(blocks, list):
        raise TypeError('blocks must be an instance of '
                        'FelicaBlock list or int list')
    _check_limits(c_uint8, len(blocks), 'blocks')
    if not isinstance(data, list) or \
            any(not isinstance(i, bytes) or len(i) != 16 for i in data):
        raise TypeError('blocks_data must be an instance of 16-byte list')

    services_list = (c_uint16 * len(service_codes))()
    for i in range(len(service_codes)):
        if isinstance(service_codes[i], FelicaService):
            services_list[i] = c_uint16(service_codes[i]._get_int())
        elif isinstance(service_codes[i], int):
            _check_limits(c_uint16, service_codes[i], 'service_codes')
            services_list[i] = c_uint16(service_codes[i])
        else:
            raise TypeError('service_codes must be an instance of '
                            'FelicaService list or int list')
    blocks_list = (c_uint32 * len(blocks))()
    for i in range(len(blocks)):
        if isinstance(blocks[i], FelicaBlock):
            blocks_list[i] = c_uint32(blocks[i]._get_int())
        elif isinstance(blocks[i], int):
            _check_limits(c_uint32, blocks[i], 'blocks')
            blocks_list[i] = c_uint32(blocks[i])
        else:
            raise TypeError('blocks must be an instance of '
                            'FelicaBlock list or int list')

    idm2 = bytes(8)
    status1 = c_uint8()
    status2 = c_uint8()
    CTS3Exception._check_error(_MPuLib.MPC_FelicaUpdate(
        c_uint8(0),
        idm,
        c_uint8(len(service_codes)),
        services_list,
        c_uint8(len(blocks)),
        blocks_list,
        b''.join(data),
        idm2,
        byref(status1),
        byref(status2)))
    return {'idm2': idm2,
            'status1': status1.value,
            'status2': status2.value}


def MPC_FELICA_Write_Without_Encryption(idm: bytes,
                                        service_codes: List[int],
                                        blocks: List[int],
                                        data: List[bytes]) \
        -> Dict[str, Union[bytes, int]]:
    """Writes FeliCa memory blocks

    Parameters
    ----------
    idm : bytes
        8-byte manufacturer identifier
    service_codes : list(FelicaService) or list(int)
        Services list
    blocks : list(FelicaBlock) or list(int)
        Blocks list
    data : list(bytes)
        16-byte blocks to write

    Returns
    -------
    dict
        'idm2' (bytes): Answered manufacturer 8-byte identifier
        'status1' (int): Status flag 1
        'status2' (int): Status flag 2
    """
    warn('MPC_FELICA_Write_Without_Encryption renamed as MPC_FelicaUpdate',
         FutureWarning, 2)
    return MPC_FelicaUpdate(idm, service_codes, blocks, data)

# endregion

# region MIFARE Ultralight


def MPC_MFULReadPage(page_number: int) -> bytes:
    """Reads MIFARE UltraLight C page content

    Parameters
    ----------
    page_number : int
        Page number

    Returns
    -------
    bytes
        16-byte read data
    """
    _check_limits(c_uint32, page_number, 'page_number')
    data = bytes(16)
    CTS3Exception._check_error(_MPuLib.MPC_MFULReadPage(
        c_uint8(0),
        c_uint32(page_number),
        data))
    return data


def MPC_MFULWritePage(page_number: int, page_content: bytes) -> None:
    """Writes MIFARE UltraLight C page content

    Parameters
    ----------
    page_number : int
        Page number
    page_content : bytes
        4-byte data to write
    """
    _check_limits(c_uint32, page_number, 'page_number')
    if not isinstance(page_content, bytes) or len(page_content) != 4:
        raise TypeError('page_content must be an instance of 4 bytes')
    CTS3Exception._check_error(_MPuLib.MPC_MFULWritePage(
        c_uint8(0),
        c_uint32(page_number),
        page_content))


def MPC_MFULCAuthenticate(key1: bytes, key2: bytes) -> None:
    """Authenticates a MIFARE UltraLight C

    Parameters
    ----------
    key1 : bytes
        8-byte first key
    key2 : bytes
        8-byte second key
    """
    if not isinstance(key1, bytes) or len(key1) != 8:
        raise TypeError('key1 must be an instance of 8 bytes')
    if not isinstance(key2, bytes) or len(key2) != 8:
        raise TypeError('key2 must be an instance of 8 bytes')
    CTS3Exception._check_error(_MPuLib.MPC_MFULCAuthenticate(
        c_uint8(0),
        key1,
        key2,
        c_uint32(0)))


def MPC_MFULCWriteKey(key1: bytes, key2: bytes) -> None:
    """Updates MIFARE UltraLight C keys

    Parameters
    ----------
    key1 : bytes
        8-byte first key
    key2 : bytes
        8-byte second key
    """
    if not isinstance(key1, bytes) or len(key1) != 8:
        raise TypeError('key1 must be an instance of 8 bytes')
    if not isinstance(key2, bytes) or len(key2) != 8:
        raise TypeError('key2 must be an instance of 8 bytes')
    CTS3Exception._check_error(_MPuLib.MPC_MFULCWriteKey(
        c_uint8(0),
        key1,
        key2))

# endregion

# region MIFARE


@unique
class MifareKey(IntEnum):
    """MIFARE key"""
    KEYA = 0
    KEYB = 1


def CLP_Authentication_2(key_mode: MifareKey, sector: int,
                         key_address: int) -> None:
    """Performs authentication sequence

    Parameters
    ----------
    key_mode : MifareKey
        Key to be used
    sector : int
        Sector number
    key_address : int
        Key block address
    """
    if not isinstance(key_mode, MifareKey):
        raise TypeError('key_mode must be an instance of '
                        'MifareKey IntEnum')
    _check_limits(c_uint8, sector, 'sector')
    _check_limits(c_uint8, key_address, 'key_address')
    _MPuLib.CLP_Authentication_2.restype = c_int32
    CTS3MifareException._check_error(_MPuLib.CLP_Authentication_2(
        c_uint8(0),
        c_uint8(key_mode),
        c_uint8(sector),
        c_uint8(key_address)))


def CLP_Halt() -> None:
    """Halts MIFARE chip"""
    _MPuLib.CLP_Halt.restype = c_int32
    CTS3MifareException._check_error(_MPuLib.CLP_Halt(
        c_uint8(0)))


def CLP_Read(block_number: int) -> bytes:
    """Reads a block

    Parameters
    ----------
    block_number : int
        Block number

    Returns
    -------
    bytes
        16-byte block content
    """
    _check_limits(c_uint8, block_number, 'block_number')
    data = bytes(16)
    _MPuLib.CLP_Read.restype = c_int32
    CTS3MifareException._check_error(_MPuLib.CLP_Read(
        c_uint8(0),
        c_uint8(block_number),
        data))
    return data


def CLP_Write(block_number: int, data: bytes) -> None:
    """Writes a block

    Parameters
    ----------
    block_number : int
        Block number
    data : bytes
        16-byte block content
    """
    _check_limits(c_uint8, block_number, 'block_number')
    if not isinstance(data, bytes) or len(data) != 16:
        raise TypeError('data must be an instance of 16 bytes')
    _MPuLib.CLP_Write.restype = c_int32
    CTS3MifareException._check_error(_MPuLib.CLP_Write(
        c_uint8(0),
        c_uint8(block_number),
        data))


def CLP_Increment(block_number: int, value: int) -> None:
    """Increments block value in register

    Parameters
    ----------
    block_number : int
        Block number
    value : int
        Increment value
    """
    _check_limits(c_uint8, block_number, 'block_number')
    _check_limits(c_uint32, value, 'value')
    _MPuLib.CLP_Increment.restype = c_int32
    CTS3MifareException._check_error(_MPuLib.CLP_Increment(
        c_uint8(0),
        c_uint8(block_number),
        c_uint32(value)))


def CLP_Decrement(block_number: int, value: int) -> None:
    """Decrements block value in register

    Parameters
    ----------
    block_number : int
        Block number
    value : int
        Decrement value
    """
    _check_limits(c_uint8, block_number, 'block_number')
    _check_limits(c_uint32, value, 'value')
    _MPuLib.CLP_Decrement.restype = c_int32
    CTS3MifareException._check_error(_MPuLib.CLP_Decrement(
        c_uint8(0),
        c_uint8(block_number),
        c_uint32(value)))


def CLP_Decrement_Transfer(block_number: int, value: int) -> None:
    """Decrements block value and updates block content

    Parameters
    ----------
    block_number : int
        Block number
    value : int
        Decrement value
    """
    _check_limits(c_uint8, block_number, 'block_number')
    _check_limits(c_uint32, value, 'value')
    _MPuLib.CLP_Decrement_Transfer.restype = c_int32
    CTS3MifareException._check_error(_MPuLib.CLP_Decrement_Transfer(
        c_uint8(0),
        c_uint8(block_number),
        c_uint32(value)))


def CLP_Restore(block_number: int) -> None:
    """Restores register value with block content

    Parameters
    ----------
    block_number : int
        Block number
    """
    _check_limits(c_uint8, block_number, 'block_number')
    _MPuLib.CLP_Restore.restype = c_int32
    CTS3MifareException._check_error(_MPuLib.CLP_Restore(
        c_uint8(0),
        c_uint8(block_number)))


def CLP_Transfer(block_number: int) -> None:
    """Transfers register content to specific block

    Parameters
    ----------
    block_number : int
        Block number
    """
    _check_limits(c_uint8, block_number, 'block_number')
    _MPuLib.CLP_Transfer.restype = c_int32
    CTS3MifareException._check_error(_MPuLib.CLP_Transfer(
        c_uint8(0),
        c_uint8(block_number)))


def CLP_LoadKey(key_mode: MifareKey, sector: int, key: bytes) -> None:
    """Loads keys

    Parameters
    ----------
    key_mode : MifareKey
        Key to be used
    sector : int
        Sector number
    key : bytes
        6-byte key
    """
    if not isinstance(key_mode, MifareKey):
        raise TypeError('key_mode must be an instance of '
                        'MifareKey IntEnum')
    _check_limits(c_uint8, sector, 'sector')
    if not isinstance(key, bytes):
        raise TypeError('key must be an instance of 6 bytes')
    str_key = ''.join(map('{:02X}'.format, key[:6]))
    _MPuLib.CLP_LoadKey.restype = c_int32
    CTS3MifareException._check_error(_MPuLib.CLP_LoadKey(
        c_uint8(0),
        c_uint8(key_mode),
        c_uint8(sector),
        str_key.encode('ascii')))


def CLP_Authentication_3(key_mode: MifareKey, sector: int,
                         key_address: int, snr: bytes) -> None:
    """Performs authentication sequence when chip UID is known

    Parameters
    ----------
    key_mode : MifareKey
        Key to be used
    sector : int
        Sector number
    key_address : int
        Key block address
    snr : bytes
        Serial number
    """
    if not isinstance(key_mode, MifareKey):
        raise TypeError('key_mode must be an instance of '
                        'MifareKey IntEnum')
    _check_limits(c_uint8, sector, 'sector')
    _check_limits(c_uint8, key_address, 'key_address')
    if not isinstance(snr, bytes):
        raise TypeError('snr must be an instance of bytes')
    snr32 = c_uint32(snr[0] << 24 | snr[1] << 16 | snr[2] << 8 | snr[3])
    _MPuLib.CLP_Authentication_3.restype = c_int32
    CTS3MifareException._check_error(_MPuLib.CLP_Authentication_3(
        c_uint8(0),
        c_uint8(key_mode),
        c_uint8(sector),
        c_uint8(key_address),
        snr32))


@unique
class MifareUidOption(IntEnum):
    """MIFARE UID usage option"""
    UIDF0 = 0x00
    UIDF1 = 0x40
    UIDF2 = 0x20
    UIDF3 = 0x60


def CLP_PersonalizeUIDUsage(option: MifareUidOption) -> None:
    """Selects UID option for personalization

    Parameters
    ----------
    option : MifareUidOption
        UID usage option
    """
    if not isinstance(option, MifareUidOption):
        raise TypeError('option must be an instance of '
                        'MifareUidOption IntEnum')
    _MPuLib.CLP_PersonalizeUIDUsage.restype = c_int32
    CTS3MifareException._check_error(_MPuLib.CLP_PersonalizeUIDUsage(
        c_uint8(0),
        c_uint8(option)))

# endregion

# region Vicinity


@unique
class VicinityCodingMode(IntEnum):
    """VCD coding mode"""
    ONE_OUTOF_4 = 1
    ONE_OUTOF_256 = 2


@unique
class VicinityDataRate(IntEnum):
    """VICC data rate"""
    LOW_DATA_RATE = 0
    HIGH_DATA_RATE = 1
    HIGH_DATA_RATE_X2 = 2
    HIGH_DATA_RATE_X4 = 3
    HIGH_DATA_RATE_X8 = 4


@unique
class VicinitySubCarrier(IntEnum):
    """VICC sub-carriers"""
    ONE_SUBCARRIER = 1
    TWO_SUBCARRIERS = 2


def MPC_SelectVCCommunication(mode: VicinityCodingMode,
                              data_rate: VicinityDataRate,
                              sub_carrier: VicinitySubCarrier) -> None:
    """Selects Vicinity data rate

    Parameters
    ----------
    mode : VicinityCodingMode
        VCD coding mode
    data_rate : VicinityDataRate
        VICC data rate
    sub_carrier : VicinitySubCarrier
        Number of VICC sub-carriers
    """
    if not isinstance(mode, VicinityCodingMode):
        raise TypeError('mode must be an instance of '
                        'VicinityCodingMode IntEnum')
    if not isinstance(data_rate, VicinityDataRate):
        raise TypeError('data_rate must be an instance of '
                        'VicinityDataRate IntEnum')
    if not isinstance(sub_carrier, VicinitySubCarrier):
        raise TypeError('sub_carrier must be an instance of '
                        'VicinitySubCarrier IntEnum')
    CTS3Exception._check_error(_MPuLib.MPC_SelectVCCommunication(
        c_uint8(0),
        c_uint8(mode),
        c_uint8(data_rate),
        c_uint8(sub_carrier)))


def MPC_SelectPauseWidthVicinity(pause: float) -> None:
    """Selects Vicinity pause width

    Parameters
    ----------
    pause : float
        Pause duration in s
    """
    pause_ns = round(pause * 1e9)
    _check_limits(c_uint16, pause_ns, 'pause')
    CTS3Exception._check_error(_MPuLib.MPC_SelectPauseWidthVicinity(
        c_uint8(0),
        c_uint16(pause_ns)))


def MPC_ExchangeCmdVicinity(tx_frame: bytes) -> bytes:
    """Exchanges a Vicinity frame

    Parameters
    ----------
    tx_frame : bytes
        Frame to send

    Returns
    -------
    bytes
        Received frame
    """
    if not isinstance(tx_frame, bytes):
        raise TypeError('tx_frame must be an instance of bytes')
    _check_limits(c_uint16, len(tx_frame), 'tx_frame')
    data = bytes(5000)
    length = c_uint16()
    CTS3Exception._check_error(_MPuLib.MPC_ExchangeCmdVicinity(
        c_uint8(0),
        tx_frame,
        c_uint16(len(tx_frame)),
        data,
        byref(length)))
    return data[:length.value]


def MPC_VcInventory(slot: int, afi: Optional[Union[bytes, int]],
                    mask: bytes) -> Dict[str, Union[bytes, int]]:
    """Sends an inventory command

    Parameters
    ----------
    slot : int
        Number of slots
    afi : bytes or int
        Application family identifier byte (None not to send AFI)
    mask : bytes
        Mask value

    Returns
    -------
    dict
        'uid' (bytes): 8-byte VICC Unique ID
        'response_flag' (int): VICC response flag
    """
    _check_limits(c_uint8, slot, 'slot')
    if afi is not None:
        if isinstance(afi, bytes):
            if len(afi) != 1:
                raise TypeError('afi must be an instance of 1 byte')
            afi_value = afi[0]
        elif isinstance(afi, int):
            _check_limits(c_uint8, afi, 'afi')
            afi_value = afi
        else:
            raise TypeError('sak must be an instance of int or 1 byte')
    else:
        afi_value = 0
    if not isinstance(mask, bytes):
        raise TypeError('mask must be an instance of bytes')
    _check_limits(c_uint8, len(mask), 'mask')
    uid = bytes(8)
    response_flag = c_uint8()
    CTS3Exception._check_error(_MPuLib.MPC_VcInventory(
        c_uint8(0),
        c_uint8(slot),
        c_bool(False) if afi is None else c_bool(True),
        c_uint8(afi_value),
        c_uint8(len(mask)),
        mask,
        uid,
        byref(response_flag)))
    return {'uid': uid, 'response_flag': response_flag.value}


def MPC_VcStayQuiet() -> None:
    """Sends a Stay Quiet request"""
    CTS3Exception._check_error(_MPuLib.MPC_VcStayQuiet(
        c_uint8(0)))


def MPC_VcSelect() -> int:
    """Sends a Select command

    Returns
    -------
    int
        Response flag
    """
    response_flag = c_uint8()
    CTS3Exception._check_error(_MPuLib.MPC_VcSelect(
        c_uint8(0),
        byref(response_flag)))
    return response_flag.value


@unique
class VicinityFlag(IntFlag):
    """Vicinity request flags"""
    PROTOCOL_EXTENSION_FLAG = 0x08
    SELECT_FLAG = 0x10
    ADDRESS_FLAG = 0x20
    OPTION_FLAG = 0x40


@unique
class VicinityOption(IntEnum):
    """Vicinity command option"""
    VicinityOptionDefault = 0
    VicinityOptionDelayedEof = 1


def MPC_VcGenericCommand(timeout: float, flag: VicinityFlag,
                         option: VicinityOption, command: Union[bytes, int],
                         tx_data: bytes) -> Dict[str, Union[bytes, int]]:
    """Sends a Vicinity command

    Parameters
    ----------
    timeout : float
        Communication timeout in s
    flag : VicinityFlag
        Vicinity request flag
    option : VicinityOption
        Command option
    command : bytes or int
        Command code byte
    tx_data : bytes
        Data to send

    Returns
    -------
    dict
        'data' (bytes): Received data
        'response_flag' (int): VICC response flag
    """
    timeout_ms = round(timeout * 1e3)
    _check_limits(c_uint16, timeout_ms, 'timeout')
    if not isinstance(flag, VicinityFlag):
        raise TypeError('flag must be an instance of VicinityFlag IntFlag')
    if not isinstance(option, VicinityOption):
        raise TypeError('option must be an instance of VicinityOption IntEnum')
    if isinstance(command, bytes):
        if len(command) != 1:
            raise TypeError('command must be an instance of 1 byte')
        cmd_value = command[0]
    elif isinstance(command, int):
        _check_limits(c_uint8, command, 'command')
        cmd_value = command
    else:
        raise TypeError('command must be an instance of int or 1 byte')
    if not isinstance(tx_data, bytes):
        raise TypeError('tx_data must be an instance of bytes')
    _check_limits(c_uint16, len(tx_data), 'tx_data')
    response_flag = c_uint8()
    data = bytes(256)
    length = c_uint16()
    CTS3Exception._check_error(_MPuLib.MPC_VcGenericCommand(
        c_uint8(0),
        c_uint16(timeout_ms),
        c_uint8(flag),
        c_uint32(option),
        c_uint8(cmd_value),
        tx_data,
        c_uint16(len(tx_data)),
        data,
        byref(length),
        byref(response_flag)))
    return {'data': data[:length.value],
            'response_flag': response_flag.value}


def MPC_VcReadSingleBlock(flag: VicinityFlag, block_number: int) \
        -> Dict[str, Union[bytes, int]]:
    """Sends a Read Single Block command

    Parameters
    ----------
    flag : VicinityFlag
        Vicinity request flag
    block_number : int
        Block number

    Returns
    -------
    dict
        'block_security_status' (int): VICC Block Security Status
                                      (if OPTION_FLAG was set in flag)
        'data' (bytes): Received data
        'response_flag' (int): VICC response flag
    """
    if not isinstance(flag, VicinityFlag):
        raise TypeError('flag must be an instance of VicinityFlag IntFlag')
    _check_limits(c_uint8, block_number, 'block_number')
    response_flag = c_uint8()
    security = c_uint8()
    data = bytes(256)
    length = c_uint16()
    CTS3Exception._check_error(_MPuLib.MPC_VcReadSingleBlock(
        c_uint8(0),
        c_uint8(flag),
        c_uint8(block_number),
        byref(security),
        data,
        byref(length),
        byref(response_flag)))
    return {'block_security_status': security.value,
            'data': data[:length.value],
            'response_flag': response_flag.value}


def MPC_VcExtendedReadSingleBlock(flag: VicinityFlag, block_number: int) \
        -> Dict[str, Union[bytes, int]]:
    """Sends an Extended Read Single Block command

    Parameters
    ----------
    flag : VicinityFlag
        Vicinity request flag
    block_number : int
        Block number

    Returns
    -------
    dict
        'block_security_status' (int): VICC Block Security Status
                                      (if OPTION_FLAG was set in flag)
        'data' (bytes): Received data
        'response_flag' (int): VICC response flag
    """
    if not isinstance(flag, VicinityFlag):
        raise TypeError('flag must be an instance of VicinityFlag IntFlag')
    _check_limits(c_uint16, block_number, 'block_number')
    response_flag = c_uint8()
    security = c_uint8()
    data = bytes(256)
    length = c_uint16()
    CTS3Exception._check_error(_MPuLib.MPC_VcExtendedReadSingleBlock(
        c_uint8(0),
        c_uint8(flag),
        c_uint16(block_number),
        byref(security),
        data,
        byref(length),
        byref(response_flag)))
    return {'block_security_status': security.value,
            'data': data[:length.value],
            'response_flag': response_flag.value}


def MPC_VcReadMultipleBlock(flag: VicinityFlag, first_block_number: int,
                            blocks_number: int) \
        -> Dict[str, Union[bytes, int, List[int]]]:
    """Sends a Read Multiple blocks command

    Parameters
    ----------
    flag : VicinityFlag
        Vicinity request flag
    first_block_number : int
        Number of first block to read
    blocks_number : int
        Number of blocks to read (in addition to first_block_number)

    Returns
    -------
    dict
        'block_security_status' list(int): VICC Block Security Status
                                           (if OPTION_FLAG was set in flag)
        'data' (bytes): Received data
        'response_flag' (int): VICC response flag
    """
    if not isinstance(flag, VicinityFlag):
        raise TypeError('flag must be an instance of VicinityFlag IntFlag')
    _check_limits(c_uint8, first_block_number, 'first_block_number')
    _check_limits(c_uint8, blocks_number, 'blocks_number')
    response_flag = c_uint8()
    security = bytes(blocks_number + 1)
    data = bytes(256)
    block_num = c_uint16()
    block_size = c_uint16()
    CTS3Exception._check_error(_MPuLib.MPC_VcReadMultipleBlock(
        c_uint8(0),
        c_uint8(flag),
        c_uint8(first_block_number),
        c_uint8(blocks_number),
        security,
        data,
        byref(block_num),
        byref(block_size),
        byref(response_flag)))
    return {'block_security_status': list(security),
            'data': data[:block_num.value * block_size.value],
            'response_flag': response_flag.value}


def MPC_VcExtendedReadMultipleBlock(flag: VicinityFlag,
                                    first_block_number: int,
                                    blocks_number: int) \
        -> Dict[str, Union[bytes, int, List[int]]]:
    """Sends an Extended Read Multiple Blocks command

    Parameters
    ----------
    flag : VicinityFlag
        Vicinity request flag
    first_block_number : int
        Number of first block to read
    blocks_number : int
        Number of blocks to read (in addition to first_block_number)

    Returns
    -------
    dict
        'block_security_status' list(int): VICC Block Security Status
                                           (if OPTION_FLAG was set in flag)
        'data' (bytes): Received data
        'response_flag' (int): VICC response flag
    """
    if not isinstance(flag, VicinityFlag):
        raise TypeError('flag must be an instance of VicinityFlag IntFlag')
    _check_limits(c_uint16, first_block_number, 'first_block_number')
    _check_limits(c_uint16, blocks_number, 'blocks_number')
    response_flag = c_uint8()
    security = bytes(blocks_number + 1)
    data = bytes(256)
    block_num = c_uint16()
    block_size = c_uint16()
    CTS3Exception._check_error(_MPuLib.MPC_VcExtendedReadMultipleBlock(
        c_uint8(0),
        c_uint8(flag),
        c_uint16(first_block_number),
        c_uint16(blocks_number),
        security,
        data,
        byref(block_num),
        byref(block_size),
        byref(response_flag)))
    return {'block_security_status': list(security),
            'data': data[:block_num.value * block_size.value],
            'response_flag': response_flag.value}


def MPC_VcWriteSingleBlock(flag: VicinityFlag, block_number: int,
                           data: bytes) -> int:
    """Sends a Write Single Block command

    Parameters
    ----------
    flag : VicinityFlag
        Vicinity request flag
    block_number : int
        Block number
    data : bytes
        Data to write

    Returns
    -------
    int
        VICC response flag
    """
    if not isinstance(flag, VicinityFlag):
        raise TypeError('flag must be an instance of VicinityFlag IntFlag')
    _check_limits(c_uint8, block_number, 'block_number')
    if not isinstance(data, bytes):
        raise TypeError('data must be an instance of bytes')
    _check_limits(c_uint16, len(data), 'data')
    response_flag = c_uint8()
    CTS3Exception._check_error(_MPuLib.MPC_VcWriteSingleBlock(
        c_uint8(0),
        c_uint8(flag),
        c_uint16(len(data)),
        c_uint8(block_number),
        data,
        byref(response_flag)))
    return response_flag.value


def MPC_VcWriteExtendedSingleBlock(flag: VicinityFlag, block_number: int,
                                   data: bytes) -> int:
    """Sends an Extended Write Single Block command

    Parameters
    ----------
    flag : VicinityFlag
        Vicinity request flag
    block_number : int
        Block number
    data : bytes
        Block to write

    Returns
    -------
    int
        VICC response flag
    """
    if not isinstance(flag, VicinityFlag):
        raise TypeError('flag must be an instance of VicinityFlag IntFlag')
    _check_limits(c_uint16, block_number, 'block_number')
    if not isinstance(data, bytes):
        raise TypeError('data must be an instance of bytes')
    _check_limits(c_uint16, len(data), 'data')
    response_flag = c_uint8()
    CTS3Exception._check_error(_MPuLib.MPC_VcWriteExtendedSingleBlock(
        c_uint8(0),
        c_uint8(flag),
        c_uint16(len(data)),
        c_uint16(block_number),
        data,
        byref(response_flag)))
    return response_flag.value


def MPC_VcLockSingleBlock(flag: VicinityFlag, block_number: int) -> int:
    """Sends a Lock Single Block command

    Parameters
    ----------
    flag : VicinityFlag
        Vicinity request flag
    block_number : int
        Block number

    Returns
    -------
    int
        VICC response flag
    """
    if not isinstance(flag, VicinityFlag):
        raise TypeError('flag must be an instance of VicinityFlag IntFlag')
    _check_limits(c_uint8, block_number, 'block_number')
    response_flag = c_uint8()
    CTS3Exception._check_error(_MPuLib.MPC_VcLockSingleBlock(
        c_uint8(0),
        c_uint8(flag),
        c_uint8(block_number),
        byref(response_flag)))
    return response_flag.value


def MPC_VcExtendedLockSingleBlock(flag: VicinityFlag, block_number: int) \
        -> int:
    """Sends an Extended Lock Single Block command

    Parameters
    ----------
    flag : VicinityFlag
        Vicinity request flag
    block_number : int
        Block number

    Returns
    -------
    int
        VICC response flag
    """
    if not isinstance(flag, VicinityFlag):
        raise TypeError('flag must be an instance of VicinityFlag IntFlag')
    _check_limits(c_uint16, block_number, 'block_number')
    response_flag = c_uint8()
    CTS3Exception._check_error(_MPuLib.MPC_VcExtendedLockSingleBlock(
        c_uint8(0),
        c_uint8(flag),
        c_uint16(block_number),
        byref(response_flag)))
    return response_flag.value


def MPC_VcResetToReady(flag: VicinityFlag) -> int:
    """Sends a Reset To Ready command

    Parameters
    ----------
    flag : VicinityFlag
        Vicinity request flag

    Returns
    -------
    int
        VICC response flag
    """
    if not isinstance(flag, VicinityFlag):
        raise TypeError('flag must be an instance of VicinityFlag IntFlag')
    response_flag = c_uint8()
    CTS3Exception._check_error(_MPuLib.MPC_VcResetToReady(
        c_uint8(0),
        c_uint8(flag),
        byref(response_flag)))
    return response_flag.value


def MPC_VcGetLastErrorCode() -> int:
    """Gets the last VICC error code

    Returns
    -------
    int
        Last error code field
    """
    err_code = c_uint8()
    CTS3Exception._check_error(_MPuLib.MPC_VcGetLastErrorCode(
        c_uint8(0),
        byref(err_code)))
    return err_code.value


def MPC_VcGetLastAnswer() -> bytes:
    """Gets the last VICC answer

    Returns
    -------
    bytes
        Last answer (including CRC)
    """
    data = bytes(10000)
    length = c_uint16()
    CTS3Exception._check_error(_MPuLib.MPC_VcGetLastAnswer(
        c_uint8(0),
        data,
        byref(length)))
    return data[:length.value]


# endregion

# region Modulation shape


def MPC_SetModulationShape(pattern_index: int,
                           falling_edge_per_mille: List[int],
                           rising_edge_per_mille: List[int]) -> None:
    """Loads custom rising and falling edges

    Parameters
    ----------
    pattern_index : int
        Pattern index
    falling_edge_per_mille : list(int)
        Falling edge points
    rising_edge_per_mille : list(int)
        Rising edge points
    """
    _check_limits(c_uint8, pattern_index, 'pattern_index')
    if not isinstance(falling_edge_per_mille, list) or \
            any(not isinstance(i, int) for i in falling_edge_per_mille):
        raise TypeError('falling_edge_per_mille must be an instance of'
                        ' integers list')
    if not isinstance(rising_edge_per_mille, list) or \
            any(not isinstance(i, int) for i in rising_edge_per_mille):
        raise TypeError('rising_edge_per_mille must be an instance of'
                        ' integers list')
    falling = (c_uint16 * len(falling_edge_per_mille))()
    for i in range(len(falling_edge_per_mille)):
        _check_limits(c_uint16, falling_edge_per_mille[i],
                      'falling_edge_per_mille')
        falling[i] = c_uint16(falling_edge_per_mille[i])
    rising = (c_uint16 * len(rising_edge_per_mille))()
    for i in range(len(rising_edge_per_mille)):
        _check_limits(c_uint16, rising_edge_per_mille[i],
                      'rising_edge_per_mille')
        rising[i] = c_uint16(rising_edge_per_mille[i])
    CTS3Exception._check_error(_MPuLib.MPC_SetModulationShape(
        c_uint8(pattern_index),
        c_uint32(len(falling_edge_per_mille)),
        falling,
        c_uint32(len(rising_edge_per_mille)),
        rising))


@unique
class ModulationShapeMode(IntEnum):
    """Modulation mode"""
    LINEAR_MODULATION = 1
    CUSTOMIZED_MOD_150_MHZ = 5


def MPC_SelectModulationGeneration(pattern_index: int,
                                   mode: ModulationShapeMode) -> None:
    """Selects the customizable modulation mode or the classical linear mode

    Parameters
    ----------
    pattern_index : int
        Pattern index
    mode : ModulationShapeMode
        Modulation mode
    """
    _check_limits(c_uint8, pattern_index, 'pattern_index')
    if not isinstance(mode, ModulationShapeMode):
        raise TypeError('mode must be an instance of '
                        'ModulationShapeMode IntEnum')
    CTS3Exception._check_error(_MPuLib.MPC_SelectModulationGeneration(
        c_uint8(pattern_index),
        c_uint8(mode)))


@unique
class ModulationItem(IntEnum):
    """Modulation item type"""
    PATTERN_MODULATION = 0
    PATTERN_CHARACTER = 1


def MPC_SelectModulationPattern(item_type: ModulationItem, pattern_index: int,
                                start: int, duration: int) -> None:
    """Applies a modulation edge shape
    Parameters
    ----------
    item_type : ModulationItem
        Modulation pattern item type
    pattern_index : int
        Pattern index
    start : int
        Transmitted frame items number which will trigger
        modulation shape application
    duration : int
        Duration of modulation shape in items count
    """
    if not isinstance(item_type, ModulationItem):
        raise TypeError('item_type must be an instance of '
                        'ModulationItem IntEnum')
    _check_limits(c_uint8, pattern_index, 'pattern_index')
    _check_limits(c_uint32, start, 'start')
    _check_limits(c_uint32, duration, 'duration')
    CTS3Exception._check_error(_MPuLib.MPC_SelectModulationPattern(
        c_uint8(item_type),
        c_uint8(pattern_index),
        c_uint32(start),
        c_uint32(duration)))


def MPC_FastFallingEdge(delay_fc: float, duration_fc: float) -> None:
    """Inverts sine wave signal to improve falling edge duration

    Parameters
    ----------
    delay_fc : float
        Delay between falling edge start and sine wave inversion
        in carrier periods
    duration_fc : float
        Duration of the sine wave inversion in carrier periods
    """
    delay_10fc = round(delay_fc * 1e1)
    _check_limits(c_uint32, delay_10fc, 'delay_fc')
    duration_10fc = round(duration_fc * 1e1)
    _check_limits(c_uint32, duration_10fc, 'duration_fc')
    CTS3Exception._check_error(_MPuLib.MPC_FastFallingEdge(
        c_uint8(0),
        c_uint32(delay_10fc),
        c_uint32(duration_10fc)))

# endregion

# region Deaf time


def MPC_SetDeafTime(deaf_time: float) -> None:
    """Sets the deaf time

    Parameters
    ----------
    deaf_time : float
        Deaf time in s
    """
    deaf_time_us = round(deaf_time * 1e6)
    _check_limits(c_uint32, deaf_time_us, 'deaf_time')
    CTS3Exception._check_error(_MPuLib.MPC_SetDeafTime(
        c_uint8(0),
        c_uint32(deaf_time_us)))

# endregion

# region Anti tearing


def MPS_AntiTearing(clock_count: int) -> None:
    """Deactivates RF field during communication

    Parameters
    ----------
    clock_count : int
        Carrier periods before RF field off
    """
    _check_limits(c_uint32, clock_count, 'clock_count')
    CTS3Exception._check_error(_MPuLib.MPS_AntiTearing(
        c_uint8(0),
        c_uint32(clock_count)))


def MPS_AntiTearing2() -> None:
    """Deactivates RF field during communication upon
    rising edge on SYNC connector"""
    CTS3Exception._check_error(_MPuLib.MPS_AntiTearing2(
        c_uint8(0),
        c_uint32(2),
        c_uint32(0)))

# endregion

# region Changing protocol parameters


@unique
class ProtocolParameters(IntEnum):
    """Protocol parameters"""
    CPP_CID = 1
    CPP_NAD = 2
    CPP_FRAME_TYPE_B = 3
    CPP_FRAME_TYPE_B_CLK = 4
    CPP_FRAME_FDT = 5
    CPP_PROTOCOL_ERROR_MANAGEMENT = 6
    CPP_PROTOCOL_STOP_TIMEOUT = 7
    CPP_NB_RETRANSMISSION = 9
    CPP_TX_PARITY = 10
    CPP_RX_PARITY = 11
    CPP_CREATE_PARITY_ERROR = 12
    CPP_CURRENT_CID = 13
    CPP_CURRENT_NAD = 14
    CPP_CURRENT_BLOCK_NUMBER = 18
    CPP_ANTI_EMD = 20
    CPP_CONFIG_ANTI_EMD = 21
    CPP_VERIFY_PICC_14443_TIMING = 24
    CPP_MSK_RFU_TO_ADD_TO_PCB_IBLOCK = 25
    CPP_EXTRA_FWT_ETU = 26
    CPP_SFGT = 27
    CPP_FRAME_WITH_ERROR_CORRECTION = 29
    CPP_EGT_BEFORE_EOF_CLK = 31
    CPP_FRAME_FELICA_OPTION = 32
    CPP_FORCE_PICC_14443_MAX_FRAME_SIZE = 34
    CPP_POWER_ON_TRIGGER_IN = 36
    CPP_CE_REVERSE_POLARITY = 37
    CPP_ACTIVE_TARGET_MUTE_BEHAVIOR = 38
    CPP_CHANGE_BIT_BOUNDARY = 40
    CPP_FELICA_BIT_CODING_REVERSE = 42
    CPP_RF_FIELD_STRENGTH_COMPATIBILITY = 44
    CPP_CE_SET_IQLM_ENABLE = 45
    CPP_NB_DESELECT = 47
    CPP_MODE_NO_EOF = 48
    CPP_DISABLE_I_OR_Q_DEMODULATION = 51
    CPP_REJECT_INVERTED_MODULATION = 52
    CPP_ALLOW_TA1_RFU = 53
    CPP_DISABLE_ATQA_CHECK = 54
    CPP_RF_FIELD_LOCK_ANTENNA = 55
    CPP_NFC_ACTIVE_FDT_MODE = 61
    CPP_PLI_STEP = 62
    CPP_DAQ_AUTORANGE = 63
    CPP_FRAME_TYPE_F_CLK = 64
    CPP_ANALOG_IN_AUTORANGE = 65
    CPP_ASK_FILTER_106 = 66
    CPP_TX_FIRST_BUFFER_SIZE = 67
    CPP_NFC_MAX_LR_VALUE_NFCFORUM = 68
    CPP_LMA_OUTPUT = 69
    CPP_VDC_INPUT = 70
    CPP_DEMOD_AUTOTHRESHOLD = 71
    CPP_AUTORANGE_MARGIN = 72


@unique
class ConnectorState(IntEnum):
    """VDC or LMA connector"""
    CONNECTOR_AUTOMATIC = 0
    CONNECTOR_HDMI = 1
    CONNECTOR_SMA = 2


def MPC_ChangeProtocolParameters(param_type: ProtocolParameters,
                                 param_value: Union[int, float, bool,
                                                    ConnectorState,
                                                    List[int],
                                                    List[float]]) -> None:
    """Changes a protocol parameter

    Parameters
    ----------
    param_type : ProtocolParameters
        Parameter to change
    param_value : int, float, bool, ConnectorState,
                      list(int) or list(float)
        Parameter value
    """
    if not isinstance(param_type, ProtocolParameters):
        raise TypeError('param_type must be an instance of '
                        'ProtocolParameters IntEnum')
    if param_type == ProtocolParameters.CPP_CURRENT_CID or \
            param_type == ProtocolParameters.CPP_CURRENT_NAD:
        if not isinstance(param_value, int):
            raise TypeError('param_value must be an instance of int')
        int_val = c_uint32(param_value)
        CTS3Exception._check_error(_MPuLib.MPC_ChangeProtocolParameters(
            c_uint8(0),
            c_uint32(param_type),
            byref(int_val),
            c_uint32(1)))

    # List parameter
    elif param_type == ProtocolParameters.CPP_FRAME_TYPE_B or \
            param_type == ProtocolParameters.CPP_FRAME_FELICA_OPTION or \
            param_type == ProtocolParameters.CPP_FRAME_TYPE_F_CLK:
        if not isinstance(param_value, list) or \
                len(param_value) != 4:
            raise TypeError('param_value must be an instance of'
                            ' 4-int list')
        list_u16_val = (4 * c_uint16)()
        for i in range(4):
            item = param_value[i]
            if not isinstance(item, int):
                raise TypeError('param_value must be an instance of'
                                ' 4-int list')
            _check_limits(c_uint16, item, 'param_value')
            list_u16_val[i] = c_uint16(item)
        CTS3Exception._check_error(_MPuLib.MPC_ChangeProtocolParameters(
            c_uint8(0),
            c_uint32(param_type),
            list_u16_val,
            c_uint32(4)))
    elif param_type == ProtocolParameters.CPP_CHANGE_BIT_BOUNDARY:
        if not isinstance(param_value, list) or len(param_value) != 2:
            raise TypeError('param_value must be an instance of'
                            ' 2-int list')
        list_u16_val = (2 * c_uint16)()
        for i in range(2):
            item = param_value[i]
            if not isinstance(item, int):
                raise TypeError('param_value must be an instance of'
                                ' 2-int list')
            _check_limits(c_uint16, item, 'param_value')
            list_u16_val[i] = c_uint16(item)
        CTS3Exception._check_error(_MPuLib.MPC_ChangeProtocolParameters(
            c_uint8(0),
            c_uint32(param_type),
            list_u16_val,
            c_uint32(2)))
    elif param_type == ProtocolParameters.CPP_FRAME_TYPE_B_CLK:
        if not isinstance(param_value, list) or len(param_value) != 14:
            raise TypeError('param_value must be an instance of'
                            ' 14-int list')
        list_u16_val = (14 * c_uint16)()
        for i in range(14):
            item = param_value[i]
            if not isinstance(item, int):
                raise TypeError('param_value must be an instance of'
                                ' 14-int list')
            _check_limits(c_uint16, item, 'param_value')
            list_u16_val[i] = c_uint16(item)
        CTS3Exception._check_error(_MPuLib.MPC_ChangeProtocolParameters(
            c_uint8(0),
            c_uint32(param_type),
            list_u16_val,
            c_uint32(14)))
    elif param_type == ProtocolParameters.CPP_FRAME_WITH_ERROR_CORRECTION:
        if not isinstance(param_value, list) or len(param_value) != 8:
            raise TypeError('param_value must be an instance of'
                            ' 8-int list')
        list_u16_val = (8 * c_uint16)()
        for i in range(8):
            item = param_value[i]
            if not isinstance(item, int):
                raise TypeError('param_value must be an instance of'
                                ' 8-int list')
            _check_limits(c_uint16, item, 'param_value')
            list_u16_val[i] = c_uint16(item)
        CTS3Exception._check_error(_MPuLib.MPC_ChangeProtocolParameters(
            c_uint8(0),
            c_uint32(param_type),
            list_u16_val,
            c_uint32(8)))
    elif param_type == ProtocolParameters.CPP_POWER_ON_TRIGGER_IN:
        if not isinstance(param_value, list) or len(param_value) != 3:
            raise TypeError('param_value must be an instance of'
                            ' 3-float list')
        list_u32_val = (3 * c_uint32)()
        for i in range(3):
            item = param_value[i]
            if not isinstance(item, float):
                raise TypeError('param_value must be an instance of'
                                ' 3-float list')
            if i == 2:
                _check_limits(c_uint32, round(item * 1e3), 'param_value')
                int_item = round(item * 1e3)
            else:
                _check_limits(c_uint32, round(item * 1e6), 'param_value')
                int_item = round(item * 1e6)
            list_u32_val[i] = c_uint32(int_item)
        CTS3Exception._check_error(_MPuLib.MPC_ChangeProtocolParameters(
            c_uint8(0),
            c_uint32(param_type),
            list_u32_val,
            c_uint32(3)))

    # Boolean parameter
    elif param_type == ProtocolParameters.CPP_CID or \
            param_type == ProtocolParameters.CPP_NAD or \
            param_type == ProtocolParameters.CPP_PROTOCOL_ERROR_MANAGEMENT or \
            param_type == ProtocolParameters.CPP_TX_PARITY or \
            param_type == ProtocolParameters.CPP_RX_PARITY or \
            param_type == ProtocolParameters.CPP_ANTI_EMD or \
            param_type == ProtocolParameters.CPP_CONFIG_ANTI_EMD or \
            param_type == ProtocolParameters.CPP_VERIFY_PICC_14443_TIMING or \
            param_type == ProtocolParameters.CPP_SFGT or \
            param_type == ProtocolParameters.CPP_CE_REVERSE_POLARITY or \
            param_type == ProtocolParameters.\
            CPP_ACTIVE_TARGET_MUTE_BEHAVIOR or \
            param_type == ProtocolParameters.CPP_FELICA_BIT_CODING_REVERSE or \
            param_type == ProtocolParameters.\
            CPP_RF_FIELD_STRENGTH_COMPATIBILITY or \
            param_type == ProtocolParameters.CPP_CE_SET_IQLM_ENABLE or \
            param_type == ProtocolParameters.CPP_MODE_NO_EOF or \
            param_type == ProtocolParameters.\
            CPP_REJECT_INVERTED_MODULATION or \
            param_type == ProtocolParameters.CPP_ALLOW_TA1_RFU or \
            param_type == ProtocolParameters.CPP_DISABLE_ATQA_CHECK or \
            param_type == ProtocolParameters.CPP_RF_FIELD_LOCK_ANTENNA or \
            param_type == ProtocolParameters.CPP_NFC_ACTIVE_FDT_MODE or \
            param_type == ProtocolParameters.CPP_ASK_FILTER_106 or \
            param_type == ProtocolParameters.CPP_NFC_MAX_LR_VALUE_NFCFORUM or \
            param_type == ProtocolParameters.CPP_DEMOD_AUTOTHRESHOLD:
        int_val = c_uint32(1) if param_value else c_uint32(0)
        CTS3Exception._check_error(_MPuLib.MPC_ChangeProtocolParameters(
            c_uint8(0),
            c_uint32(param_type),
            byref(int_val),
            c_uint32(4)))

    # ms/mdB/mV parameter
    elif param_type == ProtocolParameters.CPP_PROTOCOL_STOP_TIMEOUT or \
            param_type == ProtocolParameters.CPP_DAQ_AUTORANGE or \
            param_type == ProtocolParameters.CPP_ANALOG_IN_AUTORANGE or \
            param_type == ProtocolParameters.CPP_PLI_STEP or \
            param_type == ProtocolParameters.CPP_AUTORANGE_MARGIN:
        if isinstance(param_value, list) or \
                not isinstance(param_value, float):
            raise TypeError('param_value must be an instance of float')
        value_ms = round(param_value * 1e3)
        _check_limits(c_uint32, value_ms, 'param_value')
        int_val = c_uint32(value_ms)
        CTS3Exception._check_error(_MPuLib.MPC_ChangeProtocolParameters(
            c_uint8(0),
            c_uint32(param_type),
            byref(int_val),
            c_uint32(4)))

    # µs parameter
    elif param_type == ProtocolParameters.CPP_FRAME_FDT:
        if isinstance(param_value, list) or \
                not isinstance(param_value, float):
            raise TypeError('param_value must be an instance of float')
        value_us = round(param_value * 1e6)
        _check_limits(c_uint32, value_us, 'param_value')
        int_val = c_uint32(value_us)
        CTS3Exception._check_error(_MPuLib.MPC_ChangeProtocolParameters(
            c_uint8(0),
            c_uint32(param_type),
            byref(int_val),
            c_uint32(4)))

    # ConnectorState parameter
    elif param_type == ProtocolParameters.CPP_LMA_OUTPUT or \
            param_type == ProtocolParameters.CPP_VDC_INPUT:
        if not isinstance(param_value, ConnectorState):
            raise TypeError('param_value must be an instance of'
                            ' ConnectorState IntEnum')
        int_val = c_uint32(param_value)
        CTS3Exception._check_error(_MPuLib.MPC_ChangeProtocolParameters(
            c_uint8(0),
            c_uint32(param_type),
            byref(int_val),
            c_uint32(4)))

    # int parameter
    else:
        if not isinstance(param_value, int):
            raise TypeError('param_value must be an instance of int')
        _check_limits(c_uint32, param_value, 'param_value')
        int_val = c_uint32(param_value)
        CTS3Exception._check_error(_MPuLib.MPC_ChangeProtocolParameters(
            c_uint8(0),
            c_uint32(param_type),
            byref(int_val),
            c_uint32(4)))


def MPC_GetProtocolParameters(param_type: ProtocolParameters) \
        -> Union[int, float, bool, ConnectorState, List[int], List[float]]:
    """Gets a protocol parameter

    Parameters
    ----------
    param_type : ProtocolParameters
        Parameter to get

    Returns
    -------
    int, float, bool, ConnectorState, list(int) or list(float)
        Parameter value
    """
    if not isinstance(param_type, ProtocolParameters):
        raise TypeError('param_type must be an instance of '
                        'ProtocolParameters IntEnum')
    param_size = c_uint32()
    if param_type == ProtocolParameters.CPP_CURRENT_CID or \
            param_type == ProtocolParameters.CPP_CURRENT_NAD:
        int8_val = c_uint8()
        CTS3Exception._check_error(_MPuLib.MPC_GetProtocolParameters(
            c_uint8(0),
            c_uint32(param_type),
            byref(int8_val),
            c_uint32(1),
            byref(param_size)))
        return int8_val.value

    # List parameter
    elif param_type == ProtocolParameters.CPP_FRAME_TYPE_B or \
            param_type == ProtocolParameters.CPP_FRAME_FELICA_OPTION or \
            param_type == ProtocolParameters.CPP_FRAME_TYPE_F_CLK:
        list_u16_val = (4 * c_uint16)()
        CTS3Exception._check_error(_MPuLib.MPC_GetProtocolParameters(
            c_uint8(0),
            c_uint32(param_type),
            list_u16_val,
            c_uint32(8),
            byref(param_size)))
        return [list_u16_val[i] for i in range(4)]
    elif param_type == ProtocolParameters.CPP_CHANGE_BIT_BOUNDARY:
        list_u16_val = (2 * c_uint16)()
        CTS3Exception._check_error(_MPuLib.MPC_GetProtocolParameters(
            c_uint8(0),
            c_uint32(param_type),
            list_u16_val,
            c_uint32(4),
            byref(param_size)))
        return [list_u16_val[i] for i in range(2)]
    elif param_type == ProtocolParameters.CPP_FRAME_TYPE_B_CLK:
        list_u16_val = (14 * c_uint16)()
        CTS3Exception._check_error(_MPuLib.MPC_GetProtocolParameters(
            c_uint8(0),
            c_uint32(param_type),
            list_u16_val,
            c_uint32(28),
            byref(param_size)))
        return [list_u16_val[i] for i in range(14)]
    elif param_type == ProtocolParameters.CPP_FRAME_WITH_ERROR_CORRECTION:
        list_u16_val = (8 * c_uint16)()
        CTS3Exception._check_error(_MPuLib.MPC_GetProtocolParameters(
            c_uint8(0),
            c_uint32(param_type),
            list_u16_val,
            c_uint32(16),
            byref(param_size)))
        return [list_u16_val[i] for i in range(8)]
    elif param_type == ProtocolParameters.CPP_POWER_ON_TRIGGER_IN:
        list_u32_val = (3 * c_uint32)()
        CTS3Exception._check_error(_MPuLib.MPC_GetProtocolParameters(
            c_uint8(0),
            c_uint32(param_type),
            list_u32_val,
            c_uint32(12),
            byref(param_size)))
        return [float(list_u32_val[i]) / 1e6 for i in range(3)]

    # Boolean parameter
    elif param_type == ProtocolParameters.CPP_CID or \
            param_type == ProtocolParameters.CPP_NAD or \
            param_type == ProtocolParameters.CPP_PROTOCOL_ERROR_MANAGEMENT or \
            param_type == ProtocolParameters.CPP_TX_PARITY or \
            param_type == ProtocolParameters.CPP_RX_PARITY or \
            param_type == ProtocolParameters.CPP_ANTI_EMD or \
            param_type == ProtocolParameters.CPP_CONFIG_ANTI_EMD or \
            param_type == ProtocolParameters.CPP_VERIFY_PICC_14443_TIMING or \
            param_type == ProtocolParameters.CPP_SFGT or \
            param_type == ProtocolParameters.CPP_CE_REVERSE_POLARITY or \
            param_type == ProtocolParameters.\
            CPP_ACTIVE_TARGET_MUTE_BEHAVIOR or \
            param_type == ProtocolParameters.CPP_FELICA_BIT_CODING_REVERSE or \
            param_type == ProtocolParameters.\
            CPP_RF_FIELD_STRENGTH_COMPATIBILITY or \
            param_type == ProtocolParameters.CPP_CE_SET_IQLM_ENABLE or \
            param_type == ProtocolParameters.CPP_MODE_NO_EOF or \
            param_type == ProtocolParameters.\
            CPP_REJECT_INVERTED_MODULATION or \
            param_type == ProtocolParameters.CPP_ALLOW_TA1_RFU or \
            param_type == ProtocolParameters.CPP_DISABLE_ATQA_CHECK or \
            param_type == ProtocolParameters.CPP_RF_FIELD_LOCK_ANTENNA or \
            param_type == ProtocolParameters.CPP_NFC_ACTIVE_FDT_MODE or \
            param_type == ProtocolParameters.CPP_ASK_FILTER_106 or \
            param_type == ProtocolParameters.CPP_NFC_MAX_LR_VALUE_NFCFORUM or \
            param_type == ProtocolParameters.CPP_DEMOD_AUTOTHRESHOLD:
        int_val = c_uint32()
        CTS3Exception._check_error(_MPuLib.MPC_GetProtocolParameters(
            c_uint8(0),
            c_uint32(param_type),
            byref(int_val),
            c_uint32(1),
            byref(param_size)))
        return int_val.value > 0

    # ms/mdB/mV parameter
    elif param_type == ProtocolParameters.CPP_PROTOCOL_STOP_TIMEOUT or \
            param_type == ProtocolParameters.CPP_DAQ_AUTORANGE or \
            param_type == ProtocolParameters.CPP_ANALOG_IN_AUTORANGE or \
            param_type == ProtocolParameters.CPP_PLI_STEP or \
            param_type == ProtocolParameters.CPP_AUTORANGE_MARGIN:
        int_val = c_uint32()
        CTS3Exception._check_error(_MPuLib.MPC_GetProtocolParameters(
            c_uint8(0),
            c_uint32(param_type),
            byref(int_val),
            c_uint32(1),
            byref(param_size)))
        return float(int_val.value) / 1e3

    # µs parameter
    elif param_type == ProtocolParameters.CPP_FRAME_FDT:
        int_val = c_uint32()
        CTS3Exception._check_error(_MPuLib.MPC_GetProtocolParameters(
            c_uint8(0),
            c_uint32(param_type),
            byref(int_val),
            c_uint32(1),
            byref(param_size)))
        return float(int_val.value) / 1e6

    # ConnectorState parameter
    elif param_type == ProtocolParameters.CPP_LMA_OUTPUT or \
            param_type == ProtocolParameters.CPP_VDC_INPUT:
        int_val = c_uint32()
        CTS3Exception._check_error(_MPuLib.MPC_GetProtocolParameters(
            c_uint8(0),
            c_uint32(param_type),
            byref(int_val),
            c_uint32(1),
            byref(param_size)))
        return ConnectorState(int_val.value)

    # c_uint32 parameter
    else:
        int_val = c_uint32()
        CTS3Exception._check_error(_MPuLib.MPC_GetProtocolParameters(
            c_uint8(0),
            c_uint32(param_type),
            byref(int_val),
            c_uint32(1),
            byref(param_size)))
        return int_val.value

# endregion

# region Rx channel selection


@unique
class RxChannel(IntEnum):
    """Reception channel"""
    RX_CHANNEL_1 = 1
    RX_CHANNEL_2 = 2
    RX_CHANNEL_DAQ_CH1 = 3
    RX_CHANNEL_DAQ_CH2 = 4


def MPC_SelectRxChannel(channel: RxChannel) -> None:
    """Selects the reception channel

    Parameters
    ----------
    channel : RxChannel
        Reception channel
    """
    if not isinstance(channel, RxChannel):
        raise TypeError('channel must be an instance of RxChannel IntEnum')
    CTS3Exception._check_error(_MPuLib.MPC_SelectRxChannel(
        c_uint8(0),
        c_uint16(channel)))


def MPC_AdjustRX_Channel_2() -> None:
    """Triggers reception channel automatic adjustment"""
    CTS3Exception._check_error(_MPuLib.MPC_AdjustRX_Channel_2(
        c_uint8(0)))


@unique
class RxGainType(IntEnum):
    """Rx gain threshold type"""
    RX_GAIN_TYPE_EXTERNAL_GAIN = 0
    RX_GAIN_TYPE_SENSITIVITY_RX_EXT = 1
    RX_GAIN_TYPE_SENSITIVITY_RX_TX = 2


def MPC_SelectRxGainExt(gain_type: RxGainType, value: int) -> None:
    """Changes reception channel gain or sub-carrier detection threshold

    Parameters
    ----------
    gain_type : RxGainType
        Type of gain to be changed
    value : int
        Value to change
    """
    if not isinstance(gain_type, RxGainType):
        raise TypeError('gain_type must be an instance of RxGainType IntEnum')
    _check_limits(c_uint32, value, 'value')
    CTS3Exception._check_error(_MPuLib.MPC_SelectRxGainExt(
        c_uint8(0),
        c_uint32(gain_type),
        c_uint32(value)))


def MPC_GetRxGainExternalRx() -> int:
    """Gets current reception gain

    Returns
    -------
    int
        Reception gain
    """
    gain = c_uint32()
    CTS3Exception._check_error(_MPuLib.MPC_GetRxGainExternalRx(
        c_uint8(0),
        byref(gain)))
    return gain.value


def MPC_GetDemodThreshold() -> Dict[str, int]:
    """Gets current sub-carrier detection threshold

    Returns
    -------
    dict
        'threshold' (int): Sub-carrier detection threshold
        'average' (int): Average modulation level
    """
    threshold = c_uint16()
    average = c_uint16()
    CTS3Exception._check_error(_MPuLib.MPC_GetDemodThreshold(
        c_uint8(0),
        byref(threshold),
        byref(average)))
    return {'threshold': threshold.value,
            'average': average.value}


def MPC_ForceGainExtRx(gain: int) -> None:
    """Sets current reception gain

    Parameters
    ----------
    gain : int
        Reception gain (raw value)
    """
    _check_limits(c_uint32, gain, 'gain')
    CTS3Exception._check_error(_MPuLib.MPC_ForceGainExtRx(
        c_uint8(0),
        c_uint32(gain)))

# endregion

# region Specific tests


@unique
class TestType(IntEnum):
    TEST_REQA_REQB = 1
    TEST_REQB_REQA = 2
    TEST_POWERON_REQA = 3
    TEST_POWERON_REQB = 4
    TEST_REQA_REQA = 5
    TEST_REQB_REQB = 6
    TEST_FDT_PICCPCD_A = 8
    TEST_FDT_PICCPCD_B = 9
    TEST_POWER_OFF_ON_CMD = 15
    TEST_WUPA_WUPB = 16
    TEST_WUPB_WUPA = 17
    TEST_RF_RESET_CMD = 18
    TEST_RF_RESET_CMD_WITH_TRIGGER_IN = 19
    TEST_FDT_PICCPCD_FELICA = 20
    TEST_SPECIAL_GET_ATS = 21
    TEST_TON_EXCHANGE_AFTER_DELAY_TOFF = 22
    TEST_EMV_POLLING = 23


@overload
def MPC_Test(test_type: TestType, delay: float) -> bytes:
    # TEST_REQA_REQB, TEST_REQB_REQA, TEST_POWERON_REQA,
    # TEST_POWERON_REQB, TEST_REQA_REQA, TEST_REQB_REQB,
    # TEST_WUPA_WUPB, TEST_WUPB_WUPA
    ...


@overload
def MPC_Test(test_type: TestType, reset_time: float,
             time_1: float, time_2: float) -> bytes:
    # TEST_SPECIAL_GET_ATS
    ...


@overload
def MPC_Test(test_type: TestType, tx_bits_1: int, tx_frame_1: bytes,
             tx_bits_2: int, tx_frame_2: bytes,
             delay: float) -> Dict[str, Union[int, bytes]]:
    # TEST_FDT_PICCPCD_A, TEST_FDT_PICCPCD_B, TEST_FDT_PICCPCD_FELICA
    ...


@overload
def MPC_Test(test_type: TestType, param: Union[int, float], delay: float,
             tx_bits: int, tx_frame: bytes) -> Dict[str, Union[int, bytes]]:
    # TEST_POWER_OFF_ON_CMD, TEST_TON_EXCHANGE_AFTER_DELAY_TOFF
    ...


@overload
def MPC_Test(test_type: TestType, ask: int, time_1: float, time_2: float,
             tx_bits: int, tx_frame: bytes) -> Dict[str, Union[int, bytes]]:
    # TEST_RF_RESET_CMD
    ...


@overload
def MPC_Test(test_type: TestType, ask: int, time_1: float,
             time_2: float, timeout: float,
             tx_bits: int, tx_frame: bytes) -> Dict[str, Union[int, bytes]]:
    # TEST_RF_RESET_CMD_WITH_TRIGGER_IN
    ...


@overload
def MPC_Test(test_type: TestType, reset_time: float, first_frame_delay: float,
             next_frames_delay: float, type_odd: TechnologyType,
             tx_bits_odd: int, tx_frame_odd: bytes, type_even: TechnologyType,
             tx_bits_even: int, tx_frame_even: bytes, timeout: float) -> None:
    # TEST_EMV_POLLING
    ...


def MPC_Test(test_type, *args):  # type: ignore[no-untyped-def]
    """Performs specific test

    Parameters
    ----------
    test_type : TestType
        Test to perform
    *args
        Test parameters

    Returns
    ----------
    dict
        Test result
    """
    if not isinstance(test_type, TestType):
        raise TypeError('test_type must be an instance of TestType IntEnum')
    if _MPuLib_variadic is None:
        func_pointer = _MPuLib.MPC_Test
    else:
        func_pointer = _MPuLib_variadic.MPC_Test
    if test_type == TestType.TEST_REQA_REQB or \
            test_type == TestType.TEST_WUPA_WUPB or \
            test_type == TestType.TEST_REQB_REQB or \
            test_type == TestType.TEST_POWERON_REQB:
        if len(args) != 1:
            raise TypeError(f'MPC_Test({test_type.name}) takes exactly two '
                            f'arguments ({len(args) + 1} given)')
        if not isinstance(args[0], float) and not isinstance(args[0], int):
            raise TypeError('delay must be an instance of float')
        delay_us = round(args[0] * 1e6)
        _check_limits(c_uint32, delay_us, 'delay')
        data = bytes(550)
        length16 = c_uint16()
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(test_type),
            c_uint32(delay_us),  # Delay_us
            data,  # pRxFrame
            byref(length16)))  # pRxBits
        return data[:length16.value]

    elif test_type == TestType.TEST_REQB_REQA or \
            test_type == TestType.TEST_WUPB_WUPA or \
            test_type == TestType.TEST_REQA_REQA or \
            test_type == TestType.TEST_POWERON_REQA:
        if len(args) != 1:
            raise TypeError(f'MPC_Test({test_type.name}) takes exactly two '
                            f'arguments ({len(args) + 1} given)')
        if not isinstance(args[0], float) and not isinstance(args[0], int):
            raise TypeError('delay must be an instance of float')
        delay_us = round(args[0] * 1e6)
        _check_limits(c_uint32, delay_us, 'delay')
        atqa = c_uint16()
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(test_type),
            c_uint32(delay_us),  # Delay_us
            byref(atqa)))  # pAtqa
        return bytes([atqa.value & 0xFF, atqa.value >> 8])

    elif test_type == TestType.TEST_FDT_PICCPCD_A or \
            test_type == TestType.TEST_FDT_PICCPCD_B or \
            test_type == TestType.TEST_FDT_PICCPCD_FELICA:
        if len(args) != 5:
            raise TypeError(f'MPC_Test({test_type.name}) takes exactly six '
                            f'arguments ({len(args) + 1} given)')
        if not isinstance(args[0], int):
            raise TypeError('tx_bits_1 must be an instance of int')
        _check_limits(c_uint32, args[0], 'tx_bits_1')  # TxBits1
        if not isinstance(args[1], bytes):
            raise TypeError('tx_frame_1 must be an instance of bytes')
        if not isinstance(args[2], int):
            raise TypeError('tx_bits_2 must be an instance of int')
        _check_limits(c_uint32, args[2], 'tx_bits_2')  # TxBits2
        if not isinstance(args[3], bytes):
            raise TypeError('tx_frame_2 must be an instance of bytes')
        if not isinstance(args[4], float) and not isinstance(args[4], int):
            raise TypeError('delay must be an instance of float')
        delay_ns = round(args[4] * 1e9)
        _check_limits(c_uint32, delay_ns, 'delay')
        data = bytes(0xFFFF)
        rx_bits = c_uint32()
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(test_type),
            c_uint32(args[0]),  # TxBits1
            args[1],  # pTxFrame1
            c_uint32(args[2]),  # TxBits2
            args[3],  # pTxFrame2
            c_uint32(delay_ns),  # Delay_ns
            data,  # pRxFrame
            byref(rx_bits)))  # pRxBits
        bytes_number = int(rx_bits.value / 8)
        if rx_bits.value % 8 > 0:
            bytes_number += 1
        return {'rx_frame': data[:bytes_number],
                'rx_bits_number': rx_bits.value}

    elif test_type == TestType.TEST_SPECIAL_GET_ATS:
        if len(args) != 3:
            raise TypeError(f'MPC_Test({test_type.name}) takes exactly four '
                            f'arguments ({len(args) + 1} given)')
        if not isinstance(args[0], float) and not isinstance(args[0], int):
            raise TypeError('reset_time must be an instance of float')
        reset_us = round(args[0] * 1e6)
        _check_limits(c_uint32, reset_us, 'reset_time')
        if not isinstance(args[1], float) and not isinstance(args[1], int):
            raise TypeError('time_1 must be an instance of float')
        time1_us = round(args[1] * 1e6)
        _check_limits(c_uint32, time1_us, 'time_1')
        if not isinstance(args[2], float) and not isinstance(args[2], int):
            raise TypeError('time_2 must be an instance of float')
        time2_us = round(args[2] * 1e6)
        _check_limits(c_uint32, time2_us, 'time_2')
        data = bytes(0xFFFF)
        length = c_uint32()
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(test_type),
            c_uint32(reset_us),  # ResetTime_us
            c_uint32(time1_us),  # Time1_us
            c_uint32(time2_us),  # Time2_us
            data,  # pRxFrame
            byref(length)))  # pRxBytes
        return data[:length.value]

    elif test_type == TestType.TEST_POWER_OFF_ON_CMD:
        if len(args) != 4:
            raise TypeError(f'MPC_Test({test_type.name}) takes exactly five '
                            f'arguments ({len(args) + 1} given)')
        if not isinstance(args[0], float) and not isinstance(args[0], int):
            raise TypeError('param must be an instance of float')
        time1_us = round(args[0] * 1e6)
        _check_limits(c_uint32, time1_us, 'param')
        if not isinstance(args[1], float) and not isinstance(args[1], int):
            raise TypeError('delay must be an instance of float')
        time2_us = round(args[1] * 1e6)
        _check_limits(c_uint32, time2_us, 'delay')
        if not isinstance(args[2], int):
            raise TypeError('tx_bits must be an instance of int')
        _check_limits(c_uint32, args[2], 'tx_bits')  # TxBits
        if not isinstance(args[3], bytes):
            raise TypeError('tx_frame must be an instance of bytes')
        data = bytes(0xFFFF)
        rx_bits = c_uint32()
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(test_type),
            c_uint32(time1_us),  # Time1_us
            c_uint32(time2_us),  # Time2_us
            c_uint32(args[2]),  # TxBits
            args[3],  # pTxFrame
            data,  # pRxFrame
            byref(rx_bits)))  # pRxBits
        bytes_number = int(rx_bits.value / 8)
        if rx_bits.value % 8 > 0:
            bytes_number += 1
        return {'rx_frame': data[:bytes_number],
                'rx_bits_number': rx_bits.value}

    elif test_type == TestType.TEST_TON_EXCHANGE_AFTER_DELAY_TOFF:
        if len(args) != 4:
            raise TypeError(f'MPC_Test({test_type.name}) takes exactly five '
                            f'arguments ({len(args) + 1} given)')
        if not isinstance(args[0], int):
            raise TypeError('param must be an instance of int')
        _check_limits(c_uint32, args[0], 'param')  # TrigNum
        if not isinstance(args[1], float) and not isinstance(args[1], int):
            raise TypeError('delay must be an instance of float')
        delay_us = round(args[1] * 1e6)
        _check_limits(c_uint32, delay_us, 'delay')
        if not isinstance(args[2], int):
            raise TypeError('tx_bits must be an instance of int')
        _check_limits(c_uint32, args[2], 'tx_bits')  # TxBits
        if not isinstance(args[3], bytes):
            raise TypeError('tx_frame must be an instance of bytes')
        data = bytes(0xFFFF)
        rx_bits = c_uint32()
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(test_type),
            c_uint32(args[0]),  # TrigNum
            c_uint32(delay_us),  # Delay_us
            c_uint32(args[2]),  # TxBits
            args[3],  # pTxFrame
            data,  # pRxFrame
            byref(rx_bits)))  # pRxBits
        bytes_number = int(rx_bits.value / 8)
        if rx_bits.value % 8 > 0:
            bytes_number += 1
        return {'rx_frame': data[:bytes_number],
                'rx_bits_number': rx_bits.value}

    elif test_type == TestType.TEST_RF_RESET_CMD:
        if len(args) != 5:
            raise TypeError(f'MPC_Test({test_type.name}) takes exactly six '
                            f'arguments ({len(args) + 1} given)')
        if not isinstance(args[0], int):
            raise TypeError('ask must be an instance of int')
        _check_limits(c_uint32, args[0], 'ask')  # Ask_pm
        if not isinstance(args[1], float) and not isinstance(args[1], int):
            raise TypeError('time_1 must be an instance of float')
        time1_us = round(args[1] * 1e6)
        _check_limits(c_uint32, time1_us, 'time_1')
        if not isinstance(args[2], float) and not isinstance(args[2], int):
            raise TypeError('time_2 must be an instance of float')
        time2_us = round(args[2] * 1e6)
        _check_limits(c_uint32, time2_us, 'time_2')
        if not isinstance(args[3], int):
            raise TypeError('tx_bits must be an instance of int')
        _check_limits(c_uint32, args[3], 'tx_bits')  # TxBits
        if not isinstance(args[4], bytes):
            raise TypeError('tx_frame must be an instance of bytes')
        data = bytes(0xFFFF)
        rx_bits = c_uint32()
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(test_type),
            c_uint32(args[0]),  # Ask_pm
            c_uint32(time1_us),  # Time1_us
            c_uint32(time2_us),  # Time2_us
            c_uint32(args[3]),  # TxBits
            args[4],  # pTxFrame
            data,  # pRxFrame
            byref(rx_bits)))  # pRxBits
        bytes_number = int(rx_bits.value / 8)
        if rx_bits.value % 8 > 0:
            bytes_number += 1
        return {'rx_frame': data[:bytes_number],
                'rx_bits_number': rx_bits.value}

    elif test_type == TestType.TEST_RF_RESET_CMD_WITH_TRIGGER_IN:
        if len(args) != 6:
            raise TypeError(f'MPC_Test({test_type.name}) takes exactly seven '
                            f'arguments ({len(args) + 1} given)')
        if not isinstance(args[0], int):
            raise TypeError('ask must be an instance of int')
        _check_limits(c_uint32, args[0], 'ask')  # Ask_pm
        if not isinstance(args[1], float) and not isinstance(args[1], int):
            raise TypeError('time_1 must be an instance of float')
        time1_us = round(args[1] * 1e6)
        _check_limits(c_uint32, time1_us, 'time_1')
        if not isinstance(args[2], float) and not isinstance(args[2], int):
            raise TypeError('time_2 must be an instance of float')
        time2_us = round(args[2] * 1e6)
        _check_limits(c_uint32, time2_us, 'time_2')
        if not isinstance(args[3], float) and not isinstance(args[3], int):
            raise TypeError('timeout must be an instance of float')
        timeout_triggerin_ms = round(args[3] * 1e3)
        _check_limits(c_uint32, timeout_triggerin_ms, 'timeout')
        if not isinstance(args[4], int):
            raise TypeError('tx_bits must be an instance of int')
        _check_limits(c_uint32, args[4], 'tx_bits')  # TxBits
        if not isinstance(args[5], bytes):
            raise TypeError('tx_frame must be an instance of bytes')
        data = bytes(0xFFFF)
        rx_bits = c_uint32()
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(test_type),
            c_uint32(args[0]),  # Ask_pm
            c_uint32(time1_us),  # Time1_us
            c_uint32(time2_us),  # Time2_us
            c_uint32(timeout_triggerin_ms),  # TimeOutTriggerIn_ms
            c_uint32(args[4]),  # TxBits
            args[5],  # pTxFrame
            data,  # pRxFrame
            byref(rx_bits)))  # pRxBits
        bytes_number = int(rx_bits.value / 8)
        if rx_bits.value % 8 > 0:
            bytes_number += 1
        return {'rx_frame': data[:bytes_number],
                'rx_bits_number': rx_bits.value}

    elif test_type == TestType.TEST_EMV_POLLING:
        if len(args) != 10:
            raise TypeError(f'MPC_Test({test_type.name}) takes exactly eleven '
                            f'arguments ({len(args) + 1} given)')
        if not isinstance(args[0], float) and not isinstance(args[0], int):
            raise TypeError('reset_time must be an instance of float')
        reset_time_us = round(args[0] * 1e6)
        _check_limits(c_uint32, reset_time_us, 'reset_time')
        if not isinstance(args[1], float) and not isinstance(args[1], int):
            raise TypeError('first_frame_delay must be an instance of float')
        first_delay_us = round(args[1] * 1e6)
        _check_limits(c_uint32, first_delay_us, 'first_frame_delay')
        if not isinstance(args[2], float) and not isinstance(args[2], int):
            raise TypeError('next_frames_delay must be an instance of float')
        frames_delay_us = round(args[2] * 1e6)
        _check_limits(c_uint32, frames_delay_us, 'next_frames_delay')
        if not isinstance(args[3], TechnologyType):
            raise TypeError('type_odd must be an instance of '
                            'TechnologyType IntEnum')
        if not isinstance(args[4], int):
            raise TypeError('tx_bits_odd must be an instance of int')
        _check_limits(c_uint32, args[4], 'tx_bits_odd')
        if not isinstance(args[5], bytes):
            raise TypeError('tx_frame_odd must be an instance of bytes')
        if not isinstance(args[6], TechnologyType):
            raise TypeError('type_even must be an instance of '
                            'TechnologyType IntEnum')
        if not isinstance(args[7], int):
            raise TypeError('tx_bits_even must be an instance of int')
        _check_limits(c_uint32, args[7], 'tx_bits_even')
        if not isinstance(args[8], bytes):
            raise TypeError('tx_frame_even must be an instance of bytes')
        if not isinstance(args[9], float) and not isinstance(args[9], int):
            raise TypeError('timeout must be an instance of float')
        timeout_ms = round(args[9] * 1e3)
        _check_limits(c_uint32, timeout_ms, 'timeout')
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(test_type),
            c_uint32(reset_time_us),  # ResetTiming_us
            c_uint32(first_delay_us),  # FirstFrameDelay_us
            c_uint32(frames_delay_us),  # FramesDelay_us
            c_uint32(args[3]),  # FrameType1
            c_uint32(args[4]),  # TxBits1
            args[5],  # pTxFrame1
            c_uint32(args[6]),  # FrameType2
            c_uint32(args[7]),  # TxBits2
            args[8],  # pTxFrame2
            c_uint32(timeout_ms)))  # Timeout_ms
        return None
    else:
        raise TypeError('test_type must be an instance of TestType IntEnum')

# endregion

# region PICC response time


@unique
class ResponseTimeAction(IntEnum):
    """PICC response time measurement action"""
    PRT_ENABLE = 1
    PRT_DISABLE = 2
    PRT_GET_TR1 = 3
    PRT_CLEAR = 4
    PRT_ENABLE2 = 5
    PRT_LAST_APDU = 6
    PRT_GET_FDT = 7


def MPC_PiccResponseTime2(param: ResponseTimeAction, unit: NfcUnit) \
        -> List[int]:
    """Performs PICC timings measurement

    Parameters
    ----------
    param : TestType
        Action to perform
    unit : NfcUnit
        Timings unit

    Returns
    -------
    list(int)
        Timings result
    """
    if not isinstance(param, ResponseTimeAction):
        raise TypeError('param must be an instance of '
                        'ResponseTimeAction IntEnum')
    if not isinstance(unit, NfcUnit):
        raise TypeError('unit must be an instance of NfcUnit IntEnum')
    measurement = (c_uint32 * 10)()
    nb_meas = c_uint32()
    CTS3Exception._check_error(_MPuLib.MPC_PiccResponseTime2(
        c_uint8(0),
        c_uint32(param),
        c_uint32(unit),
        measurement,
        byref(nb_meas)))
    if nb_meas.value:
        return [i for i in measurement][:nb_meas.value]
    else:
        return []

# endregion

# region Trigger


@unique
class InputTriggerNum(IntEnum):
    TRIGGER_IN1 = 1
    TRIGGER_IN2 = 2
    TRIGGER_IN3 = 3
    TRIGGER_IN4 = 4


def MPC_GetTrigger(trigger: InputTriggerNum) -> bool:
    """Gets input trigger voltage level

    Parameters
    ----------
    trigger : InputTriggerNum
        Trigger number

    Returns
    -------
    bool
        Trigger voltage level
    """
    if not isinstance(trigger, InputTriggerNum):
        raise TypeError('trigger must be an instance of '
                        'InputTriggerNum IntEnum')
    status = c_uint32()
    CTS3Exception._check_error(_MPuLib.MPC_GetTrigger(
        c_uint8(0),
        c_uint8(trigger),
        byref(status)))
    return status.value > 0


@unique
class NfcTriggerId(IntFlag):
    TRIGGER_1 = 1
    TRIGGER_2 = 2
    TRIGGER_3 = 4
    TRIGGER_ANALOG = 8
    TRIGGER_DAQ = 16


@unique
class NfcTrigger(IntEnum):
    TRIG_DEACTIVATE = 0
    TRIG_FORCE = 1
    TRIG_TX_ON = 2
    TRIG_TX_OUT = 3
    TRIG_RX_SUBCARRIER = 4
    TRIG_RX_DEMOD = 5
    TRIG_RX_ON = 6
    TRIG_DELAY_AFTER_TX = 7
    TRIG_CARRIER = 8
    TRIG_MODULATION_CARD_EMULATION = 9
    TRIG_CE_SEQZ_DETECTED = 10
    TRIG_CE_PCD_SOF_TYPE_B = 11
    TRIG_TX_OFF = 12
    TRIG_RX_OFF = 13
    TRIG_CE_PCD_SOF_TYPE_V = 14
    TRIG_FS_DETECT_ON = 15
    TRIG_FS_DETECT_OFF = 16
    TRIG_EMD_GENERATION = 17
    TRIG_RX_FIRST_CHAR_PICC = 19
    TRIG_IN = 20
    TRIG_RF_FIELD_OFF = 22
    TRIG_RF_FIELD_ON = 23
    TRIG_PICC_106 = 24
    TRIG_PICC_212 = 25
    TRIG_PICC_424 = 26
    TRIG_PICC_848 = 27
    TRIG_PICC_1695 = 28
    TRIG_PICC_3390 = 29
    TRIG_PICC_6780 = 30
    TRIG_CE_PCD_TYPE_F212 = 32
    TRIG_CE_PCD_TYPE_F424 = 34
    TRIG_CE_PCD_106 = 35
    TRIG_CE_PCD_212 = 36
    TRIG_CE_PCD_424 = 37
    TRIG_CE_PCD_848 = 38
    TRIG_CE_PCD_1695 = 39
    TRIG_CE_PCD_3390 = 40
    TRIG_CE_PCD_6780 = 41
    TRIG_CE_PCD_TX_A = 42
    TRIG_CE_PCD_TX_F_212 = 43
    TRIG_CE_PCD_TX_F_424 = 44
    TRIG_CE_PCD_TX_V_1o4 = 45
    TRIG_CE_PCD_TX_V_1o256 = 46
    TRIG_CE_PDC_CHAR_TYPE_A = 47
    TRIG_CE_PDC_CHAR_TYPE_B = 48
    TRIG_CE_PDC_CHAR_TYPE_F = 49
    TRIG_CE_PDC_CHAR_TYPE_V = 50
    TRIG_RX_FRAME = 59
    TRIG_ON_ERROR = 60
    TRIG_TX_FRAME = 61
    TRIG_PICC_CHAR_TYPE_A = 62
    TRIG_PICC_CHAR_TYPE_B = 63
    TRIG_PICC_CHAR_TYPE_F = 64
    TRIG_PICC_CHAR_TYPE_V = 65


def MPC_TriggerConfig(trigger_id: NfcTriggerId, config: NfcTrigger,
                      value: Union[float, TechnologyType, CTS3ErrorCode,
                                   bool] = 0,
                      frame: Optional[bytes] = None,
                      mask: Optional[bytes] = None) -> None:
    """Configures trigger

    Parameters
    ----------
    trigger_id : NfcTriggerId
        Trigger on which configuration will apply
    config : NfcTrigger
        Trigger configuration
    value : float, TechnologyType, CTS3ErrorCode or bool, optional
        If config is TRIG_FORCE: value to force (bool)
        If config is TRIG_DELAY_AFTER_TX: delay in s (float)
        If config is TRIG_ON_ERROR: error code (CTS3ErrorCode)
        If config is TRIG_RX_FRAME: frame technology (TechnologyType)
        If config is TRIG_TX_FRAME: frame technology (TechnologyType)
    frame : bytes, optional
        Rx frame to match
    mask : bytes, optional
        Rx frame mask
    """
    if not isinstance(trigger_id, NfcTriggerId):
        raise TypeError('trigger_id must be an instance of '
                        'NfcTriggerId IntFlag')
    if not isinstance(config, NfcTrigger):
        raise TypeError('config must be an instance of NfcTrigger IntEnum')
    if frame:
        if not isinstance(frame, bytes):
            raise TypeError('frame must be an instance of bytes')
        _check_limits(c_uint32, len(frame), 'frame')
    if mask and not isinstance(mask, bytes):
        raise TypeError('mask must be an instance of bytes')
    if mask and not frame:
        raise TypeError('frame not defined')
    if frame and not mask:
        mask = b'\xFF' * len(frame)
    if mask and frame and len(mask) != len(frame):
        raise TypeError('frame/mask mismatch')

    if config == NfcTrigger.TRIG_FORCE:
        val = 1 if value else 0
    elif config == NfcTrigger.TRIG_DELAY_AFTER_TX:
        val = round(value * 1e9)
        _check_limits(c_uint32, val, 'value')
    elif config == NfcTrigger.TRIG_ON_ERROR:
        if not isinstance(value, CTS3ErrorCode):
            raise TypeError('value must be an instance of '
                            'CTS3ErrorCode IntEnum')
        val = value.value
    elif config == NfcTrigger.TRIG_RX_FRAME or \
            config == NfcTrigger.TRIG_TX_FRAME:
        if not isinstance(value, TechnologyType):
            raise TypeError('value must be an instance of '
                            'TechnologyType IntEnum')
        val = value.value
    else:
        val = 0

    CTS3Exception._check_error(_MPuLib.MPC_TriggerConfig(
        c_uint8(0),
        c_uint32(trigger_id),
        c_uint32(config),
        c_uint32(val),
        c_uint32(0) if frame is None else c_uint32(len(frame)),
        frame,
        mask))


# endregion

# region Arbitrary disturbance generator


@unique
class DisturbanceOperation(IntEnum):
    """RF signal disturbance operation"""
    SIGNAL_CARRIER_ADD = 0
    SIGNAL_CARRIER_MUL = 1


@unique
class DisturbanceType(IntEnum):
    """RF signal disturbance type"""
    DISTURBANCE_RAMP = 0
    DISTURBANCE_SQUARE = 1
    DISTURBANCE_SINE = 2
    DISTURBANCE_GLITCH = 3
    DISTURBANCE_SINE2 = 4


def MPC_GenerateDisturbance(operation: DisturbanceOperation,
                            disturbance_type: DisturbanceType,
                            amplitude: float, offset: float, duration: float,
                            param: Union[None, bool, int] = None) -> None:
    """Programs an RF disturbance

    Parameters
    ----------
    operation : DisturbanceOperation
        Disturbance operation to be generated
    disturbance_type : DisturbanceType
        Disturbance type
    amplitude : float
        Disturbance amplitude in %
    offset : float
        Disturbance offset in %
    duration : float
        Disturbance duration in s
    param : bool or int, optional
        - True to maintain final field level
          (if disturbance_type is DISTURBANCE_RAMP)
        - Number of signal periods
          (if disturbance_type is DISTURBANCE_SQUARE, DISTURBANCE_SINE
          or DISTURBANCE_SINE2)
    """
    if not isinstance(operation, DisturbanceOperation):
        raise TypeError('operation must be an instance of '
                        'DisturbanceOperation IntEnum')
    if not isinstance(disturbance_type, DisturbanceType):
        raise TypeError('disturbance_type must be an instance of '
                        'DisturbanceType IntEnum')
    amplitude_pm = round(amplitude * 1e1)
    _check_limits(c_int32, amplitude_pm, 'amplitude')
    offset_pm = round(offset * 1e1)
    _check_limits(c_int16, offset_pm, 'offset')
    duration_ns = round(duration * 1e9)
    _check_limits(c_uint32, duration_ns, 'duration')
    if disturbance_type == DisturbanceType.DISTURBANCE_RAMP:
        CTS3Exception._check_error(_MPuLib.MPC_GenerateDisturbance(
            c_uint8(0),
            c_uint8(operation),
            c_uint8(disturbance_type),
            c_int32(amplitude_pm),
            c_int16(offset_pm),
            c_uint32(duration_ns),
            c_uint32(1) if param else c_uint32(0),
            c_uint32(0),
            c_uint32(0),
            c_uint32(0)))
    elif disturbance_type == DisturbanceType.DISTURBANCE_SQUARE or \
            disturbance_type == DisturbanceType.DISTURBANCE_SINE or \
            disturbance_type == DisturbanceType.DISTURBANCE_SINE2:
        periods_number = c_uint32(1)
        if param is not None:
            if not isinstance(param, int):
                raise TypeError('param must be an instance of int')
            _check_limits(c_uint32, param, 'param')
            periods_number = c_uint32(param)
        CTS3Exception._check_error(_MPuLib.MPC_GenerateDisturbance(
            c_uint8(0),
            c_uint8(operation),
            c_uint8(disturbance_type),
            c_int32(amplitude_pm),
            c_int16(offset_pm),
            c_uint32(duration_ns),
            periods_number,
            c_uint32(0),
            c_uint32(0),
            c_uint32(0)))
    else:
        CTS3Exception._check_error(_MPuLib.MPC_GenerateDisturbance(
            c_uint8(0),
            c_uint8(operation),
            c_uint8(disturbance_type),
            c_int32(amplitude_pm),
            c_int16(offset_pm),
            c_uint32(duration_ns),
            c_uint32(0),
            c_uint32(0),
            c_uint32(0),
            c_uint32(0)))


def MPC_LoadDisturbanceWaveshape(operation: DisturbanceOperation,
                                 timebase: int, data: List[float]) -> None:
    """Loads a disturbance signal

    Parameters
    ----------
    operation : DisturbanceOperation
        Disturbance operation to be loaded
    timebase : int
        Signal time base in 1 / (150 MHz)
    data : list(float)
        Disturbing signal in %
    """
    if not isinstance(operation, DisturbanceOperation):
        raise TypeError('operation must be an instance of '
                        'DisturbanceOperation IntEnum')
    _check_limits(c_uint32, timebase, 'timebase')
    if not isinstance(data, list):
        raise TypeError('data must be an instance of integers list')
    _check_limits(c_uint32, len(data), 'data')
    data_array = (c_int16 * len(data))()
    for i in range(len(data)):
        value_pm = round(data[i] * 10)
        _check_limits(c_int16, value_pm, 'data')
        data_array[i] = c_int16(value_pm)
    CTS3Exception._check_error(_MPuLib.MPC_LoadDisturbanceWaveshape(
        c_uint8(0),
        c_uint8(operation),
        c_uint32(timebase),
        c_uint32(len(data)),
        data_array))


def MPC_SetDisturbanceTrigger(operation: DisturbanceOperation,
                              trigger: NfcTrigger, delay: float = 0,
                              count: int = 1) -> None:
    """Selects the trigger condition starting the disturbance

    Parameters
    ----------
    operation : DisturbanceOperation
        Disturbance operation to be triggered
    trigger : NfcTrigger
        Trigger condition
    delay : float, optional
        Delay after trigger in s
    count : int, optional
        Number of times the trigger condition will generate the disturbance
    """
    if not isinstance(operation, DisturbanceOperation):
        raise TypeError('operation must be an instance of '
                        'DisturbanceOperation IntEnum')
    if not isinstance(trigger, NfcTrigger):
        raise TypeError('trigger must be an instance of NfcTrigger IntEnum')
    delay_ns = round(delay * 1e9)
    _check_limits(c_uint32, delay_ns, 'delay')
    _check_limits(c_uint16, count, 'repeat_count')
    CTS3Exception._check_error(_MPuLib.MPC_SetDisturbanceTrigger(
        c_uint8(0),
        c_uint8(operation),
        c_uint32(trigger),
        c_uint32(delay_ns),
        c_uint16(count)))


def MPC_ResetDisturbance() -> None:
    """Resets previously loaded RF disturbances"""
    CTS3Exception._check_error(_MPuLib.MPC_ResetDisturbance(
        c_uint8(0),
        c_uint8(0)))

# endregion

# region Self-test


@unique
class CplAutotestId(IntEnum):
    """NFC self-test type"""
    TEST_CPL_ALL = -1
    TEST_TXCHANNEL = 101
    TEST_RXCHANNEL = 102
    TEST_LMA = 103
    TEST_RFQ_CHANNEL = 104
    TEST_RFOUT_CHANNEL = 105


def MPS_CPLAutoTest(test_id: CplAutotestId = CplAutotestId.TEST_CPL_ALL) \
        -> List[List[str]]:
    """Performs NFC self-test

    Parameters
    ----------
    test_id : CplAutotestId, optional
        Self-test identifier

    Returns
    -------
    list(list(str))
        Test result
    """
    if not isinstance(test_id, CplAutotestId):
        raise TypeError('test_id must be an instance of CplAutotestId IntEnum')
    result = c_char_p()
    ret = CTS3ErrorCode(_MPuLib.MPS_CPLAutoTest(
        c_uint8(0),
        c_uint32(test_id),
        c_bool(True),
        c_uint32(0),
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

# region Miscellaneous


def MPC_ComputeCrc(card_type: TechnologyType, frame: bytes) -> bytes:
    """Computes frame CRC

    Parameters
    ----------
    card_type : TechnologyType
        Technology type
    frame : bytes
        Input frame

    Returns
    -------
    bytes
        CRC bytes
    """
    if not isinstance(card_type, TechnologyType):
        raise TypeError('card_type must be an instance of '
                        'TechnologyType IntEnum')
    if not isinstance(frame, bytes):
        raise TypeError('frame must be an instance of bytes')
    _check_limits(c_uint32, len(frame), 'frame')
    crc1 = c_uint8()
    crc2 = c_uint8()
    CTS3Exception._check_error(_MPuLib.MPC_ComputeCrc(
        c_uint8(0),
        c_int32(card_type),
        frame,
        c_uint32(len(frame)),
        byref(crc1),
        byref(crc2)))
    return bytes([crc1.value, crc2.value])


def MPC_CheckCRCFrame(card_type: TechnologyType, frame: bytes) -> bool:
    """Checks frame CRC

    Parameters
    ----------
    card_type : TechnologyType
        Technology type
    frame : bytes
        Input frame

    Returns
    -------
    bool
        True if frame CRC is correct
    """
    if not isinstance(card_type, TechnologyType):
        raise TypeError('card_type must be an instance of '
                        'TechnologyType IntEnum')
    if not isinstance(frame, bytes):
        raise TypeError('frame must be an instance of bytes')
    _check_limits(c_uint32, len(frame), 'frame')
    ret = CTS3ErrorCode(_MPuLib.MPC_CheckCRCFrame(
        c_uint8(0),
        c_int32(card_type),
        frame,
        c_uint32(len(frame))))
    if ret == CTS3ErrorCode.ERR_RX_FRAME_CRCA or \
            ret == CTS3ErrorCode.ERR_RX_FRAME_CRCB or \
            ret == CTS3ErrorCode.ERR_RX_FRAME_CRCF:
        return False
    elif ret == CTS3ErrorCode.RET_OK:
        return True
    else:
        raise CTS3Exception(ret)


@unique
class InputImpedance(IntEnum):
    INPUT_IMPEDANCE_50 = 50
    INPUT_IMPEDANCE_1M = 1000000


def MPC_SelectInputImpedanceAnalogIn(impedance: InputImpedance) -> None:
    """Selects ANALOG IN input impedance

    Parameters
    ----------
    impedance : InputImpedance
        Input impedance
    """
    if not isinstance(impedance, InputImpedance):
        raise TypeError('impedance must be an instance of '
                        'InputImpedance IntEnum')
    CTS3Exception._check_error(_MPuLib.MPC_SelectInputImpedanceAnalogIn(
        c_uint8(0),
        c_uint32(impedance)))


@unique
class CounterCommand(IntEnum):
    COUNTER_RESET = 1
    COUNTER_READ = 2


def MPS_Counter(command: CounterCommand) -> int:
    """Counts protocol errors

    Parameters
    ----------
    command : CounterCommand
        Counter type

    Returns
    -------
    int
        Counter value
    """
    if not isinstance(command, CounterCommand):
        raise TypeError('command must be an instance of '
                        'CounterCommand IntEnum')
    counter = c_uint32()
    CTS3Exception._check_error(_MPuLib.MPS_Counter(
        c_uint8(0),
        c_uint32(command),
        byref(counter)))
    return counter.value

# endregion

# region NFC


@unique
class NfcMode(IntEnum):
    """NFC communication mode"""
    NFC_PASSIVE_MODE = 1
    NFC_ACTIVE_MODE = 2
    NFC_PASSIVE_MODE2 = 3


@unique
class NfcDataRate(IntEnum):
    """NFC communication data rate"""
    NFC_106 = 106
    NFC_212 = 212
    NFC_424 = 424


def MPC_NfcConfiguration(mode: NfcMode, initiator: bool,
                         data_rate: NfcDataRate) -> None:
    """Configures the NFC mode

    Parameters
    ----------
    mode : NfcMode
        NFC mode
    initiator : bool
        True to set Initiator mode
    data_rate : int
        NFC data rate in kb/s
    """
    if not isinstance(mode, NfcMode):
        raise TypeError('mode must be an instance of NfcMode IntEnum')
    if not isinstance(data_rate, NfcDataRate):
        raise TypeError('data_rate must be an instance of NfcDataRate IntEnum')
    CTS3Exception._check_error(_MPuLib.MPC_NfcConfiguration(
        c_uint8(0),
        c_uint8(mode),
        c_uint8(1) if initiator else c_uint8(2),
        c_uint16(data_rate)))


def MPC_SensReq() -> bytes:
    """Sends a SENS_REQ command

    Returns
    -------
    bytes
        Response to SENS_REQ
    """
    sens_res = c_uint16()
    CTS3Exception._check_error(_MPuLib.MPC_SensReq(
        c_uint8(0),
        byref(sens_res)))
    return bytes([sens_res.value & 0xFF, sens_res.value >> 8])


def MPC_AllReq() -> bytes:
    """Sends an ALL_REQ command

    Returns
    -------
    bytes
        Response to ALL_REQ
    """
    sens_res = c_uint16()
    CTS3Exception._check_error(_MPuLib.MPC_AllReq(
        c_uint8(0),
        byref(sens_res)))
    return bytes([sens_res.value & 0xFF, sens_res.value >> 8])


def MPC_Sdd() -> Dict[str, bytes]:
    """Performs a single device detection

    Returns
    -------
    dict
        'sel_res' (bytes): SEL_RES byte
        'nfc_id1' (bytes): Random ID for Single Device Detection
    """
    data = bytes(12)
    length = c_uint16()
    sel_res = c_uint8()
    CTS3Exception._check_error(_MPuLib.MPC_Sdd(
        c_uint8(0),
        data,
        byref(length),
        byref(sel_res)))
    return {'sel_res': bytes([sel_res.value]), 'nfc_id1': data[:length.value]}


def MPC_SelReq(nfc_id1: bytes) -> bytes:
    """Selects a target by its NFCID1

    Parameters
    ----------
    nfc_id1 : bytes
        Random ID for Single Device Detection

    Returns
    -------
    bytes
        SEL_RES byte
    """
    if not isinstance(nfc_id1, bytes):
        raise TypeError('nfc_id1 must be an instance of bytes')
    _check_limits(c_uint16, len(nfc_id1), 'nfc_id1')
    sel_res = c_uint8()
    CTS3Exception._check_error(_MPuLib.MPC_SelReq(
        c_uint8(0),
        nfc_id1,
        c_uint16(len(nfc_id1)),
        byref(sel_res)))
    return bytes([sel_res.value])


def MPC_SlpReq() -> None:
    """Sends a SLP_REQ command"""
    CTS3Exception._check_error(_MPuLib.MPC_SlpReq(
        c_uint8(0)))


def MPC_PollReq(system_code: Union[bytes, int], rc: Union[bytes, int],
                tsn: Union[bytes, int]) -> Dict[str, bytes]:
    """Sends a polling request

    Parameters
    ----------
    system_code : bytes or int
        2-byte System Code
    rc : bytes or int
        Request Code byte
    tsn : bytes or int
        Time Slot Number byte

    Returns
    -------
    dict
        'nfc_id2' (bytes): 8-byte random ID for Single Device Detection
        'pad' (bytes): 8-byte Pad
        'rd' (bytes): RD byte
    """
    if isinstance(system_code, bytes):
        if len(system_code) != 2:
            raise TypeError('system_code must be an instance of 2 bytes')
        sc_value = system_code[0] << 8
        sc_value |= system_code[1]
    elif isinstance(system_code, int):
        _check_limits(c_uint16, system_code, 'system_code')
        sc_value = system_code
    else:
        raise TypeError('system_code must be an instance of int or 2 bytes')
    if isinstance(rc, bytes):
        if len(rc) != 1:
            raise TypeError('rc must be an instance of 1 byte')
        rc_value = rc[0]
    elif isinstance(rc, int):
        _check_limits(c_uint8, rc, 'rc')
        rc_value = rc
    else:
        raise TypeError('rc must be an instance of int or 1 byte')
    if isinstance(tsn, bytes):
        if len(tsn) != 1:
            raise TypeError('tsn must be an instance of 1 byte')
        tsn_value = tsn[0]
    elif isinstance(tsn, int):
        _check_limits(c_uint8, tsn, 'tsn')
        tsn_value = tsn
    else:
        raise TypeError('tsn must be an instance of int or 1 byte')
    nfc_id2 = bytes(8)
    pad = bytes(8)
    rd = c_uint16()
    CTS3Exception._check_error(_MPuLib.MPC_PollReq(
        c_uint8(0),
        c_uint16(sc_value),
        c_uint8(rc_value),
        c_uint8(tsn_value),
        nfc_id2,
        pad,
        byref(rd)))
    return {'nfc_id2': nfc_id2, 'pad': pad, 'rd': bytes([rd.value >> 8,
                                                         rd.value & 0xFF])}


def MPC_AtrReq(atr_req: bytes) -> bytes:
    """Sends an ATR_REQ command

    Parameters
    ----------
    atr_req : bytes
        ATR_REQ command

    Returns
    -------
    bytes
        ATR_RES answer
    """
    if not isinstance(atr_req, bytes):
        raise TypeError('atr_req must be an instance of bytes')
    _check_limits(c_uint16, len(atr_req), 'atr_req')
    data = bytes(512)
    length = c_uint16()
    CTS3Exception._check_error(_MPuLib.MPC_AtrReq(
        c_uint8(0),
        atr_req,
        c_uint16(len(atr_req)),
        data,
        byref(length)))
    return data[:length.value]


def MPC_PslReq(brs: Union[bytes, int], fsl: Union[bytes, int]) -> None:
    """Sends a PSL_REQ command

    Parameters
    ----------
    brs : bytes or int
        BRS byte
    fsl : bytes or int
        FSL byte
    """
    if isinstance(brs, bytes):
        if len(brs) != 1:
            raise TypeError('brs must be an instance of 1 byte')
        brs_value = brs[0]
    elif isinstance(brs, int):
        _check_limits(c_uint8, brs, 'brs')
        brs_value = brs
    else:
        raise TypeError('brs must be an instance of int or 1 byte')
    if isinstance(fsl, bytes):
        if len(fsl) != 1:
            raise TypeError('fsl must be an instance of 1 byte')
        fsl_value = fsl[0]
    elif isinstance(fsl, int):
        _check_limits(c_uint8, fsl, 'fsl')
        fsl_value = fsl
    else:
        raise TypeError('fsl must be an instance of int or 1 byte')
    CTS3Exception._check_error(_MPuLib.MPC_PslReq(
        c_uint8(0),
        c_uint8(brs_value),
        c_uint8(fsl_value)))


def MPC_WakeUpReq(nfc_id3: bytes) -> None:
    """Wakes a target up

    Parameters
    ----------
    nfc_id3 : bytes
        10-byte target NFCID3 identifier
    """
    if not isinstance(nfc_id3, bytes) or len(nfc_id3) != 10:
        raise TypeError('nfc_id3 must be an instance of 10 bytes')
    CTS3Exception._check_error(_MPuLib.MPC_WakeUpReq(
        c_uint8(0),
        nfc_id3))


def MPC_DeselectReq() -> None:
    """Sends a DEP_REQ command"""
    CTS3Exception._check_error(_MPuLib.MPC_DeselectReq(
        c_uint8(0)))


def MPC_ReleaseReq() -> None:
    """Sends a RLS_REQ command"""
    CTS3Exception._check_error(_MPuLib.MPC_ReleaseReq(
        c_uint8(0)))


def MPC_ExchangeNFCData(command: bytes) -> bytes:
    """Exchanges data based on ISO 18092 frame format

    Parameters
    ----------
    command : bytes
        Frame to transmit

    Returns
    -------
    bytes
        Received frame
    """
    if command and not isinstance(command, bytes):
        raise TypeError('command must be an instance of bytes')
    _check_limits(c_uint16, len(command), 'command')
    data = bytes(0xFFFF)
    length = c_uint16()
    if command:
        CTS3Exception._check_error(_MPuLib.MPC_ExchangeNFCData(
            c_uint8(0),
            command,
            c_uint16(len(command)),
            data,
            byref(length)))
    else:
        CTS3Exception._check_error(_MPuLib.MPC_ExchangeNFCData(
            c_uint8(0),
            None,
            c_uint16(0),
            data,
            byref(length)))
    return data[:length.value]


def MPC_DepReq(command: bytes) -> bytes:
    """Exchanges data with a DEP_REQ command

    Parameters
    ----------
    command : bytes
        Data to send

    Returns
    -------
    bytes
        Received data
    """
    if not isinstance(command, bytes):
        raise TypeError('command must be an instance of bytes')
    _check_limits(c_uint32, len(command), 'command')
    data = bytes(0xFFFF)
    length = c_uint32()
    CTS3Exception._check_error(_MPuLib.MPC_DepReq(
        c_uint8(0),
        command,
        c_uint32(len(command)),
        data,
        byref(length)))
    return data[:length.value]


def MPC_NfcWaitAndGetFrameAsTarget(timeout: float) -> bytes:
    """Receives a frame from an NFC active initiator

    Parameters
    ---------
    timeout : float
        Reception timeout in s

    Returns
    -------
    bytes
        Received frame
    """
    timeout_ms = round(timeout * 1e3)
    _check_limits(c_uint32, timeout_ms, 'timeout')
    data = bytes(0xFFFF)
    length = c_uint32()
    CTS3Exception._check_error(_MPuLib.MPC_NfcWaitAndGetFrameAsTarget(
        c_uint8(0),
        c_uint32(timeout_ms),
        data,
        c_uint32(0),
        byref(length)))
    return data[:length.value]


def MPC_NfcRFCollisionAvoidance(unit: FieldUnit, value: float) -> None:
    """Selects field value to be used during NFC active exchanges

    Parameters
    ----------
    unit : FieldUnit
        Field strength unit
    value : float
        Field strength in mV, dBm, % or ‰
        (ignored if unit is APPLY_DEFAULT_VALUE)
    """
    if not isinstance(unit, FieldUnit):
        raise TypeError('unit must be an instance of FieldUnit IntEnum')
    if unit == FieldUnit.APPLY_DEFAULT_VALUE:
        CTS3Exception._check_error(_MPuLib.MPC_NfcRFCollisionAvoidance(
            c_uint8(0),
            c_uint8(unit),
            c_int16(0)))
    elif unit == FieldUnit.UNIT_PER_CENT:
        value_pm = round(value * 1e1)
        _check_limits(c_int16, value_pm, 'value')
        CTS3Exception._check_error(_MPuLib.MPC_NfcRFCollisionAvoidance(
            c_uint8(0),
            c_uint8(FieldUnit.UNIT_PER_MILLE),
            c_int16(value_pm)))
    elif unit == FieldUnit.UNIT_PER_MILLE or \
            unit == FieldUnit.UNIT_DBM_RANGE_11DBM or \
            unit == FieldUnit.UNIT_DBM_RANGE_29DBM or \
            unit == FieldUnit.UNIT_DBM_RANGE_31DBM or \
            unit == FieldUnit.UNIT_DBM_RANGE_33DBM:
        value_pm = round(value)
        _check_limits(c_int16, value_pm, 'value')
        CTS3Exception._check_error(_MPuLib.MPC_NfcRFCollisionAvoidance(
            c_uint8(0),
            c_uint8(unit),
            c_int16(value_pm)))
    else:  # mV
        value_mV = round(value)
        _check_limits(c_int16, value_mV, 'value')
        CTS3Exception._check_error(_MPuLib.MPC_NfcRFCollisionAvoidance(
            c_uint8(0),
            c_uint8(unit),
            c_int16(value_mV)))


def MPC_NfcSendFrameAsTarget(tx_frame: bytes, timeout: float = 0) -> None:
    """Sends a frame to an NFC active initiator

    Parameters
    ---------
    tx_frame : bytes
        Frame to send
    timeout : float, optional
        Transmission timeout in s
    """
    timeout_us = round(timeout * 1e6)
    _check_limits(c_uint32, timeout_us, 'timeout')
    if tx_frame:
        if not isinstance(tx_frame, bytes):
            raise TypeError('tx_frame must be an instance of bytes')
        _check_limits(c_uint32, len(tx_frame), 'tx_frame')
        CTS3Exception._check_error(_MPuLib.MPC_NfcSendFrameAsTarget(
            c_uint8(0),
            c_uint32(timeout_us),
            tx_frame,
            c_uint32(len(tx_frame))))
    else:
        CTS3Exception._check_error(_MPuLib.MPC_NfcSendFrameAsTarget(
            c_uint8(0),
            c_uint32(timeout_us),
            None,
            c_uint32(0)))


def MPC_SetActiveTimings(unit: NfcUnit, t_idt: float = 0, t_irfg: float = 0,
                         t_adt: float = 0, t_arfg: float = 0, t_off: float = 0,
                         t_mute: float = 0) -> None:
    """Sets timings for NFC active mode

    Parameters
    ----------
    unit : NfcUnit
        Timings unit
    t_idt : float, optional
        RF field off initial duration, or 0 to keep previous value
    t_irfg : float, optional
        RF field on initial duration before transmission,
        or 0 to keep previous value
    t_adt : float, optional
        RF field off duration, or 0 to keep previous value
    t_arfg : float, optional
        RF field on duration before transmission, or 0 to keep previous value
    t_off : float, optional
        RF field on duration after transmission, or 0 to keep previous value
    t_mute : float, optional
        Mute answer duration, or 0 to keep previous value
    """
    if not isinstance(unit, NfcUnit):
        raise TypeError('unit must be an instance of NfcUnit IntEnum')
    # Unit auto-selection
    computed_unit, [computed_tidt,
                    computed_tirfg,
                    computed_tadt,
                    computed_tarfg,
                    computed_toff,
                    computed_tmute] = _unit_autoselect(unit,
                                                       [t_idt, t_irfg,
                                                        t_adt, t_arfg,
                                                        t_off, t_mute])
    _check_limits(c_uint32, computed_tidt, 't_idt')
    _check_limits(c_uint32, computed_tirfg, 't_irfg')
    _check_limits(c_uint32, computed_tadt, 't_adt')
    _check_limits(c_uint32, computed_tarfg, 't_arfg')
    _check_limits(c_uint32, computed_toff, 't_off')
    _check_limits(c_uint32, computed_tmute, 't_mute')
    CTS3Exception._check_error(_MPuLib.MPC_SetActiveTimings(
        c_uint8(0),
        c_uint32(computed_unit),
        c_uint32(computed_tidt),
        c_uint32(computed_tirfg),
        c_uint32(computed_tadt),
        c_uint32(computed_tarfg),
        c_uint32(computed_toff),
        c_uint32(computed_tmute)))


def MPC_GetActiveTimings(unit: NfcUnit) -> Dict[str, int]:
    """Gets timings for NFC active mode

    Parameters
    ----------
    unit : NfcUnit
        Timings unit

    Returns
    -------
    dict
        't_idt' (int): RF field off initial duration
        't_irfg' (int): RF field on initial duration before transmission
        't_adt' (int): RF field off duration
        't_arfg' (int): RF field on duration before transmission
        't_off' (int): RF field on duration after transmission
        't_mute' (int): Mute answer duration
    """
    if not isinstance(unit, NfcUnit):
        raise TypeError('unit must be an instance of NfcUnit IntEnum')
    tidt = c_uint32()
    tirfg = c_uint32()
    tadt = c_uint32()
    tarfg = c_uint32()
    toff = c_uint32()
    tmute = c_uint32()
    CTS3Exception._check_error(_MPuLib.MPC_GetActiveTimings(
        c_uint8(0),
        c_uint32(unit),
        byref(tidt),
        byref(tirfg),
        byref(tadt),
        byref(tarfg),
        byref(toff),
        byref(tmute)))
    return {'t_idt': tidt.value,
            't_irfg': tirfg.value,
            't_adt': tadt.value,
            't_arfg': tarfg.value,
            't_off': toff.value,
            't_mute': tmute.value}

# endregion

# region Protocol Analyzer


def MPS_OpenLog() -> None:
    """Starts the events acquisition"""
    CTS3Exception._check_error(_MPuLib.MPS_OpenLog(
        c_uint8(0),
        c_uint32(0),
        c_uint32(0)))


def MPS_CloseLog() -> None:
    """Stops the events acquisition"""
    ret = _MPuLib.MPS_CloseLog(
        c_uint8(0))
    if ret != CTS3ErrorCode.CRET_NO_DOWNLOAD_RUNNING.value:
        CTS3Exception._check_error(ret)


def MPS_FlushLog() -> None:
    """Flushes the events acquisition buffer"""
    CTS3Exception._check_error(_MPuLib.MPS_FlushLog(
        c_uint8(0)))


def MPS_CancelDownload() -> None:
    """Aborts events download"""
    CTS3Exception._check_error(_MPuLib.MPS_CancelDownload(
        c_uint8(0)))


@unique
class SpyParameter(IntEnum):
    CP_SPY_MEMORY_SIZE_MB = 2
    CP_SPY_EMV_TIMINGS = 4
    CP_SPY_DISABLE_PICC_MODULATION = 7
    CP_SPY_DISABLE_PCD_MODULATION = 8
    CP_SPY_TIMEOUT_S = 9
    CP_SPY_BUFFER_SIZE_MB = 10
    CP_SPY_DOWNLOAD_BLOCK_SIZE = 11


def MPS_SpyChangeParameters(param: SpyParameter, value: int) -> None:
    """Changes protocol analyzer parameter

    Parameters
    ----------
    param : SpyParameter
        Parameter type
    value : int
        Parameter value
    """
    if not isinstance(param, SpyParameter):
        raise TypeError('param must be an instance of SpyParameter IntEnum')
    _check_limits(c_uint32, value, 'value')
    CTS3Exception._check_error(_MPuLib.MPS_SpyChangeParameters(
        c_uint8(0),
        c_uint32(param),
        c_uint32(value)))


def MPS_SpyGetParameters(param: SpyParameter) -> int:
    """Gets protocol analyzer parameter

    Parameters
    ----------
    param : SpyParameter
        Parameter type

    Returns
    -------
    int
        Parameter value
    """
    if not isinstance(param, SpyParameter):
        raise TypeError('param must be an instance of SpyParameter IntEnum')
    value = c_uint32()
    CTS3Exception._check_error(_MPuLib.MPS_SpyGetParameters(
        c_uint8(0),
        c_uint32(param),
        byref(value)))
    return value.value


def MPS_SetUserEvent(user_event_number: int) -> None:
    """Adds a user defined event in the acquisition buffer

    Parameters
    ----------
    user_event_number : int
        User defined event
    """
    _check_limits(c_uint8, user_event_number, 'user_event_number')
    CTS3Exception._check_error(_MPuLib.MPS_SetUserEvent(
        c_uint8(0),
        c_uint8(user_event_number)))


def BeginDownload(call_back: Callable[[int,
                                       int,
                                       POINTER(c_uint8),  # type: ignore[misc]
                                       int], int]) -> None:
    """Starts protocol analyzer events download

    Parameters
    ----------
    call_back : Callable
        Events callback
    """
    global _callback_dict
    cmp_func = CFUNCTYPE(c_int32, c_uint32, c_uint32, POINTER(c_uint8), c_int)
    host = _get_connection_string()
    if len(host) > 0:
        _callback_dict[host] = cmp_func(call_back)
        ret = _MPuLib.BeginDownload(
            c_uint8(0),
            _callback_dict[host],
            c_uint32(0),
            c_int(0))
        if ret == CTS3ErrorCode.RET_UNKNOWN_COMMAND.value:
            # For compatibility with MP500
            ret = _MPuLib.StartDownload(
                c_uint8(0),
                _callback_dict[host],
                c_uint32(0),
                c_int(0))
        CTS3Exception._check_error(ret)
    else:
        raise CTS3Exception(CTS3ErrorCode.DLLCOMERROR)


def BeginDownloadTo(path: Union[str, Path]) -> None:
    """Starts protocol analyzer events download

    Parameters
    ----------
    path : str or Path
        mplog file path
    """
    if isinstance(path, Path):
        log_file = str(path).encode('ascii')
    else:
        log_file = path.encode('ascii')
    ret = _MPuLib.BeginDownloadTo(
        c_uint8(0),
        log_file)
    if ret == CTS3ErrorCode.RET_UNKNOWN_COMMAND.value:
        # For compatibility with MP500
        ret = _MPuLib.StartDownloadTo(
            c_uint8(0),
            log_file)
    CTS3Exception._check_error(ret)


def MPS_EndDownload() -> None:
    """Ends protocol analyzer events download"""
    global _callback_dict
    ret = _MPuLib.MPS_EndDownload(
        c_uint8(0))
    host = _get_connection_string()
    if len(host) > 0 and host in _callback_dict:
        _callback_dict.pop(host)
    if ret != CTS3ErrorCode.CRET_NO_DOWNLOAD_RUNNING.value:
        CTS3Exception._check_error(ret)

# endregion

# region Changing default value of parameters


@unique
class DefaultParameterType(IntEnum):
    # Default parameters definition
    DP_MODULATION_FALL_TIME = 1
    DP_MODULATION_RISE_TIME = 2
    DP_MODULATION_ASK = 3
    DP_FIELD_STRENGTH = 4
    DP_FIELD_RISE_TIME = 5
    # Default parameters definition for Type A
    DP_PAUSE_WIDTH_106 = 6
    DP_PAUSE_WIDTH_212 = 7
    DP_PAUSE_WIDTH_424 = 8
    DP_PAUSE_WIDTH_848 = 9
    # Default parameters definition for Type B card
    DP_SOF1_106 = 10
    DP_SOF2_106 = 11
    DP_START_BIT_106 = 12
    DP_BIT0_106 = 13
    DP_BIT1_106 = 14
    DP_BIT2_106 = 15
    DP_BIT3_106 = 16
    DP_BIT4_106 = 17
    DP_BIT5_106 = 18
    DP_BIT6_106 = 19
    DP_BIT7_106 = 20
    DP_EGT_106 = 21
    DP_STOP_BIT_106 = 22
    DP_EOF_106 = 23
    DP_SOF1_212 = 24
    DP_SOF2_212 = 25
    DP_START_BIT_212 = 26
    DP_BIT0_212 = 27
    DP_BIT1_212 = 28
    DP_BIT2_212 = 29
    DP_BIT3_212 = 30
    DP_BIT4_212 = 31
    DP_BIT5_212 = 32
    DP_BIT6_212 = 33
    DP_BIT7_212 = 34
    DP_EGT_212 = 35
    DP_STOP_BIT_212 = 36
    DP_EOF_212 = 37
    DP_SOF1_424 = 38
    DP_SOF2_424 = 39
    DP_START_BIT_424 = 40
    DP_BIT0_424 = 41
    DP_BIT1_424 = 42
    DP_BIT2_424 = 43
    DP_BIT3_424 = 44
    DP_BIT4_424 = 45
    DP_BIT5_424 = 46
    DP_BIT6_424 = 47
    DP_BIT7_424 = 48
    DP_EGT_424 = 49
    DP_STOP_BIT_424 = 50
    DP_EOF_424 = 51
    DP_SOF1_848 = 52
    DP_SOF2_848 = 53
    DP_START_BIT_848 = 54
    DP_BIT0_848 = 55
    DP_BIT1_848 = 56
    DP_BIT2_848 = 57
    DP_BIT3_848 = 58
    DP_BIT4_848 = 59
    DP_BIT5_848 = 60
    DP_BIT6_848 = 61
    DP_BIT7_848 = 62
    DP_EGT_848 = 63
    DP_STOP_BIT_848 = 64
    DP_EOF_848 = 65
    DP_FWT = 66
    # Pause width vicinity
    DP_PAUSE_WIDTH_VICINITY = 67
    # For VHBR
    DP_PAUSE_WIDTH_1695 = 68
    DP_PAUSE_WIDTH_3390 = 69
    DP_PAUSE_WIDTH_6780 = 70
    DP_MODULATION_ASKPT = 71
    DP_CE_LMA_LOW = 72
    DP_CE_LMA_HIGH = 73
    DP_LOAD_ANTENNA = 74
    DP_ANALOG_IN_IMPEDANCE = 75
    DP_EMD_LMA_LOW = 76
    DP_EMD_LMA_HIGH = 77
    DP_FIELD_STRENGTH_PM = 78
    DP_MODULATION_FALL_TIME_ALL_TYPES = 79
    DP_MODULATION_RISE_TIME_ALL_TYPES = 80


def MPC_SetDefaultParameters(card_type: TechnologyType,
                             param_id: DefaultParameterType,
                             param_value: int) -> None:
    """Sets a default parameter value

    Parameters
    ----------
    card_type : TechnologyType
        Technology type
    param_id : DefaultParameterType
        Default parameter to set
    param_value : int
        Default value
    """
    if not isinstance(card_type, TechnologyType):
        raise TypeError('card_type must be an instance of '
                        'TechnologyType IntEnum')
    if not isinstance(param_id, DefaultParameterType):
        raise TypeError('param_id must be an instance of '
                        'DefaultParameterType IntEnum')
    _check_limits(c_uint32, param_value, 'param_value')
    CTS3Exception._check_error(_MPuLib.MPC_SetDefaultParameters(
        c_uint8(0),
        c_uint8(card_type),
        c_uint32(param_id),
        byref(c_uint32(param_value)),
        c_uint32(4)))


def MPC_GetDefaultParameters(card_type: TechnologyType,
                             param_id: DefaultParameterType) -> int:
    """Gets a default parameter value

    Parameters
    ----------
    card_type : TechnologyType
        Technology type
    param_id : DefaultParameterType
        Default parameter to get

    Returns
    -------
    int
        Default value
    """
    if not isinstance(card_type, TechnologyType):
        raise TypeError('card_type must be an instance of '
                        'TechnologyType IntEnum')
    if not isinstance(param_id, DefaultParameterType):
        raise TypeError('param_id must be an instance of '
                        'DefaultParameterType IntEnum')
    param_value = c_uint32()
    size = c_uint32(4)
    CTS3Exception._check_error(_MPuLib.MPC_GetDefaultParameters(
        c_uint8(0),
        c_uint8(card_type),
        c_uint32(param_id),
        byref(param_value),
        byref(size)))
    return param_value.value


@unique
class InternalParameterType(IntEnum):
    INTERNAL_FIELD_STRENGTH = 100
    INTERNAL_MODULATION_ASK = 101
    INTERNAL_FIELD_STRENGTH_PM = 102
    INTERNAL_MODULATION_ASK_PM = 103
    INTERNAL_CARD_TYPE = 104
    INTERNAL_FIELD_STRENGTH_MV = 105
    CONFIG_FIELD_STRENGTH = 200
    CONFIG_MODULATION_ASK_TYPE_A = 201
    CONFIG_MODULATION_ASK_TYPE_B = 202
    CONFIG_MODULATION_ASK_TYPE_FELICA = 203
    CONFIG_MODULATION_ASK_TYPE_VICINITY = 204
    CONFIG_MODULATION_FALL_TIME = 205
    CONFIG_MODULATION_RISE_TIME = 206
    CONFIG_FIELD_RISE_TIME = 207
    CONFIG_FIELD_STRENGTH_PM = 208
    CONFIG_MODULATION_ASK_TYPE_A_PM = 209
    CONFIG_MODULATION_ASK_TYPE_B_PM = 210
    CONFIG_MODULATION_ASK_TYPE_FELICA_PM = 211
    CONFIG_MODULATION_ASK_TYPE_VICINITY_PM = 212


def MPS_GetInternalParameter(param_type: InternalParameterType) -> int:
    """Gets current internal parameter value

    Parameters
    ----------
    param_type : InternalParameterType
        Parameter type

    Returns
    -------
    int
        Parameter value
    """
    if not isinstance(param_type, InternalParameterType):
        raise TypeError('param_type must be an instance of '
                        'InternalParameterType IntEnum')
    param_value = c_uint32()
    CTS3Exception._check_error(_MPuLib.MPS_GetInternalParameter(
        c_uint8(0),
        c_uint32(param_type),
        c_uint32(0),
        byref(param_value)))
    return param_value.value

# endregion

# region Phase drift monitoring


def MPC_SelectPhaseDriftLimits(intra_modulation: float = float('inf'),
                               inter_modulations: float = float('inf'),
                               frame: float = float('inf')) -> None:
    """Selects phase drift monitoring limits

    Parameters
    ----------
    intra_modulation : float, optional
        Phase drift in each modulation upper limit in °
    inter_modulations : float, optional
        Phase drift between modulations upper limit in °
    frame : float, optional
        Phase drift in whole frame upper limit in °
    """
    CTS3Exception._check_error(_MPuLib.MPC_SelectPhaseDriftLimits(
        c_uint8(0),
        c_double(intra_modulation),
        c_double(inter_modulations),
        c_double(frame)))


def MPC_GetPhaseDrifts() -> Dict[str, List[float]]:
    """Gets PICC phase drift measurements

    Returns
    -------
    dict
        'intra' (list(float)): Phase drifts in each modulation in °
        'inter' (list(float)): Phase drifts between modulations in °
        'frame' (list(float)): Phase drifts in whole frame in °
    """
    nb_meas = c_uint32()
    intra = (c_double * 10)()
    inter = (c_double * 10)()
    frame = (c_double * 10)()
    CTS3Exception._check_error(_MPuLib.MPC_GetPhaseDrifts(
        c_uint8(0),
        byref(nb_meas),
        intra,
        inter,
        frame))
    if nb_meas.value:
        return {'intra': [i for i in intra][:nb_meas.value],
                'inter': [i for i in inter][:nb_meas.value],
                'frame': [i for i in frame][:nb_meas.value]}
    else:
        return {'intra': [],
                'inter': [],
                'frame': []}

# endregion
