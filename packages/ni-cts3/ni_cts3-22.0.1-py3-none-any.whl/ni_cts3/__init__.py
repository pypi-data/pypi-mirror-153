import sys
from platform import processor, architecture
from pathlib import Path
from time import sleep
from atexit import register
from subprocess import Popen, PIPE, DEVNULL
from shlex import split
from threading import Thread, Event
from ipaddress import IPv4Address, IPv4Interface
from typing import List, Dict, Type, Union, Optional, Callable, cast
from enum import IntEnum, IntFlag, unique
from xml.dom.minidom import parseString
from datetime import datetime
from ctypes import c_char, c_char_p, c_uint8, c_int16, c_uint16
from ctypes import c_bool, c_int32, c_uint32, c_double
from ctypes import sizeof, byref, create_string_buffer
from ctypes import CDLL, Structure, CFUNCTYPE
from .MPStatus import CTS3ErrorCode

if sys.version_info < (3, 6):
    raise Exception('Requires Python ≥ 3.6')
if sys.version_info >= (3, 9):
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
if sys.platform == 'win32':
    from ctypes import WinDLL


__version__ = '22.0.1'
__author__ = 'NI'
__copyright__ = f'Copyright 20{__version__[:2]}, NI'
__license__ = 'MIT'


class MpDll(CDLL):
    _func_restype_ = c_int16  # type: ignore[assignment]


# Load MPuLib from local path
_lib_sys: Optional[Path] = None
_lib_name: Optional[str] = None
_lib_path = Path(__file__).resolve().parent.joinpath('.lib')
if sys.platform == 'win32':
    class MpWinDll(WinDLL):
        _func_restype_ = c_int16  # type: ignore[assignment]

    _lib_path = _lib_path.joinpath('Windows')
    if architecture()[0] == '32bit':
        _lib_name = 'MPuLib-win32.dll'
    else:
        _lib_name = 'MPuLib-win64.dll'
elif sys.platform == 'cygwin':
    _lib_path = _lib_path.joinpath('Windows')
    if architecture()[0] == '64bit':
        _lib_name = 'MPuLib-win64.dll'
    else:
        raise NotImplementedError('Unsupported cygwin architecture')
else:
    if sys.platform == 'darwin':
        _lib_path = _lib_path.joinpath('macOS')
        _lib_name = 'libMPuLib.dylib'
    elif sys.platform == 'linux':
        if processor().startswith('armv7'):
            # CTS3 embedded library
            _lib_path = _lib_path.joinpath('Arm')
        else:
            _lib_path = _lib_path.joinpath('Linux')
            if architecture()[0] == '32bit':
                _lib_path = _lib_path.joinpath('x86')
            else:
                _lib_path = _lib_path.joinpath('x64')
        _lib_name = 'libMPuLib.so'
    else:
        raise NotImplementedError(f'Unsupported platform: {sys.platform}')
    _lib_sys = Path('/usr', 'lib', _lib_name)

# Locate library
_lib_path = _lib_path.joinpath(_lib_name)
if not _lib_path.is_file():
    if _lib_sys and _lib_sys.is_file():
        # Use library located in system path
        _lib_path = _lib_sys
    else:
        raise FileNotFoundError(f'Library "{_lib_path}" not found')

# Load library
if sys.platform == 'win32':
    _MPuLib: MpWinDll = MpWinDll(str(_lib_path))
else:
    _MPuLib: MpDll = MpDll(str(_lib_path))
_MPuLib_variadic: Optional[MpDll] = None
if sys.platform == 'win32' and architecture()[0] == '32bit':
    # Load library for variadic functions
    _MPuLib_variadic = MpDll(str(_lib_path))


class _FirmwareLog(Thread):
    """Firmware log listening thread

    Attributes
    ----------
    host : str
        Connection string
    started : Event
        Event raised when log redirection is established or failed
    running : bool
        True if thread is running
    log : Popen
        Log redirection subprocess
    """

    def __init__(self, host: str, started: Event):
        """Inits _FirmwareLog Thread

        Parameters
        ----------
        host : str
            Connection string
        started : Event
            Event raised when log redirection is established or failed
        """
        if sys.platform == 'linux' and processor().startswith('armv7'):
            # Running from CTS3 embedded environment
            self.host = 'localhost'
        else:
            self.host = host
        self.started = started
        self.running = False
        Thread.__init__(self, daemon=True)

    def run(self) -> None:
        """Starts log redirection"""
        # Follow log and read last entry
        log_cmd = 'journalctl --unit=tgapp --follow --lines=1 --output=cat'
        try:
            try:
                if sys.platform == 'linux' and processor().startswith('armv7'):
                    # Running from CTS3 embedded environment
                    self.log = Popen(log_cmd,
                                     bufsize=1,
                                     universal_newlines=True,
                                     encoding='ascii',
                                     shell=True,
                                     stdout=PIPE,
                                     stderr=DEVNULL)
                else:
                    # Running from remote environment, open SSH connection
                    ssh_cmd = 'ssh -Tnq -l default -o ' + \
                              'StrictHostKeyChecking=no ' + self.host
                    self.log = Popen(split(ssh_cmd + ' ' + log_cmd),
                                     bufsize=1,
                                     universal_newlines=True,
                                     encoding='ascii',
                                     stdout=PIPE,
                                     stderr=DEVNULL)
                self.running = True
                # Read last log entry to ensure link is established
                if self.log.stdout is not None:
                    self.log.stdout.readline()
            finally:
                self.started.set()
            while self.running:
                if self.log.stdout is not None:
                    log = self.log.stdout.readline()
                    if len(log) > 0:
                        sys.stderr.write(f'{{{self.host}}}\t{log}')
        except Exception:
            self.running = False

    def stop(self) -> None:
        """Stops log redirection"""
        if self.running:
            self.running = False
            self.log.terminate()
            self.log.wait()
            Thread.join(self)


def _check_limits(c_type: Union[Type[c_uint8], Type[c_uint16], Type[c_uint32],
                                Type[c_int16], Type[c_int32]],
                  int_value: int, var_name: str) -> None:
    """Checks if integer value is within C type integer range

    Parameters
    ----------
    c_type : type
        C integer type
    int_value : int
        Value to check against C type
    var_name : str
        Variable name
    """
    signed = c_type(-1).value < c_type(0).value
    bit_size = sizeof(c_type) * 8
    signed_limit = 2 ** (bit_size - 1)
    if signed:
        if int_value < -signed_limit or int_value > signed_limit - 1:
            raise OverflowError(var_name + ' is out of range')
    else:
        if int_value < 0 or int_value > 2 * signed_limit - 1:
            raise OverflowError(var_name + ' is out of range')


def GetErrorMessageFromCode(error_code: int) -> str:
    """Converts an error code into an error message

    Parameters
    ----------
    error_code : int
        Error code to convert

    Returns
    -------
    str
        Error message
    """
    _check_limits(c_int16, error_code, 'error_code')
    _MPuLib.GetErrorMessageFromCode.restype = c_char_p
    message = cast(bytes, _MPuLib.GetErrorMessageFromCode(
        c_uint16(error_code))).decode('ascii')
    if len(message) > 0:
        return message
    return f'Unknown error code 0x{error_code:04X}'


def GetMifareErrorMessageFromCode(error_code: int) -> str:
    """Converts a MIFARE error code into an error message

    Parameters
    ----------
    error_code : int
        Error code to convert

    Returns
    -------
    str
        Error message
    """
    _check_limits(c_int32, error_code, 'error_code')
    _MPuLib.GetMifareErrorMessageFromCode.restype = c_char_p
    message = cast(bytes, _MPuLib.GetMifareErrorMessageFromCode(
        c_int32(error_code))).decode('ascii')
    if len(message) > 0:
        return message
    return f'Unknown error code 0x{error_code:02X}'


from .MPException import CTS3Exception  # noqa: E402


_logs_dict: Dict[str, _FirmwareLog] = {}


def _get_connection_string() -> str:
    """Gets communication channel connection string

    Returns
    -------
    str
        Connection string
    """
    host_name = create_string_buffer(128)
    ret = CTS3ErrorCode(_MPuLib.GetConnectionString(host_name))
    if ret == CTS3ErrorCode.RET_OK:
        return host_name.value.decode('ascii')
    return ''


def _log_start() -> None:
    """Starts firwmare log redirection to stderr"""
    global _logs_dict
    host = _get_connection_string()
    if len(host) > 0 and host not in _logs_dict:
        log_started = Event()
        log_thread = _FirmwareLog(host, log_started)
        log_thread.start()
        log_started.wait()
        if log_thread.running:
            _logs_dict[host] = log_thread


def _log_stop() -> None:
    """Stops firmware log redirection to stderr"""
    global _logs_dict
    host = _get_connection_string()
    if len(host) > 0 and host in _logs_dict:
        sleep(0.5)  # Journal flush delay
        _logs_dict[host].stop()
        _logs_dict.pop(host)


def _logs_cleanup() -> None:
    """Stops all firmware log redirections"""
    global _logs_dict
    for log in _logs_dict.values():
        log.stop()


register(_logs_cleanup)

# region Resource management


@unique
class ResourceType(IntEnum):
    """CTS3 resources identifier"""
    CTS3_NFC_RESOURCE_ID = 250
    CTS3_DAQ_RESOURCE_ID = 251


@unique
class ResourceBlockingMode(IntEnum):
    """Resource allocation mode"""
    NOT_BLOCKING = 0
    BLOCKING = 1
    OVERRIDE = 3


def MPOS_OpenResource(resource_id: Union[int, ResourceType, None] = None,
                      blocking_mode: ResourceBlockingMode =
                      ResourceBlockingMode.NOT_BLOCKING) -> None:
    """Opens a resource

    Parameters
    ----------
    resource_id : int or ResourceType, optional
        Resource identifier
    blocking_mode : ResourceBlockingMode, optional
        Resource allocation mode
    """
    if not isinstance(blocking_mode, ResourceBlockingMode):
        raise TypeError('blocking_mode must be an instance of '
                        'ResourceBlockingMode IntEnum')
    if resource_id is None:
        # Open both resources
        ret_code = _MPuLib.MPOS_OpenResource(
            c_uint32(ResourceType.CTS3_DAQ_RESOURCE_ID),
            c_uint8(0),
            c_uint32(blocking_mode))
        if ret_code != 27:  # For compatiblity with MP500
            CTS3Exception._check_error(ret_code)
        ret_code = _MPuLib.MPOS_OpenResource(
            c_uint32(MPOS_GetResourceID()),
            c_uint8(0),
            c_uint32(blocking_mode))
        if ret_code == 3901:  # For compatiblity with MP500
            CTS3Exception._check_error(CTS3ErrorCode.RET_RESOURCE_ALREADY_OPEN)
        else:
            CTS3Exception._check_error(ret_code)
    else:
        _check_limits(c_uint32, resource_id, 'resource_id')
        CTS3Exception._check_error(_MPuLib.MPOS_OpenResource(
            c_uint32(resource_id),
            c_uint8(0),
            c_uint32(blocking_mode)))


def MPOS_CloseResource(resource_id: Union[int, ResourceType, None] =
                       None) -> None:
    """Closes a resource

    Parameters
    ----------
    resource_id : int or ResourceType, optional
        Resource identifier
    """
    if resource_id is None:
        # Close both resources
        ret = CTS3ErrorCode(_MPuLib.MPOS_CloseResource(
            c_uint32(MPOS_GetResourceID()),
            c_uint8(0)))
        if ret != CTS3ErrorCode.RET_OK and \
                ret != CTS3ErrorCode.RET_RESOURCE_NOT_OPEN:
            raise CTS3Exception(ret)
        ret = CTS3ErrorCode(_MPuLib.MPOS_CloseResource(
            c_uint32(ResourceType.CTS3_DAQ_RESOURCE_ID),
            c_uint8(0)))
        if ret != CTS3ErrorCode.RET_OK and \
                ret != CTS3ErrorCode.RET_RESOURCE_INVALID_ID and \
                ret != CTS3ErrorCode.RET_RESOURCE_NOT_OPEN:
            raise CTS3Exception(ret)
    else:
        _check_limits(c_uint32, resource_id, 'resource_id')
        ret = CTS3ErrorCode(_MPuLib.MPOS_CloseResource(
            c_uint32(resource_id),
            c_uint8(0)))
        if ret != CTS3ErrorCode.RET_OK and \
                ret != CTS3ErrorCode.RET_RESOURCE_NOT_OPEN:
            raise CTS3Exception(ret)


def MPOS_GetResourceID() -> Union[int, ResourceType]:
    """Gets the resource identifier

    Returns
    -------
    int or ResourceType
        Resource identifier
    """
    resource_id = c_uint32()
    CTS3Exception._check_error(_MPuLib.MPOS_GetResourceID(
        c_uint8(0),
        byref(resource_id)))
    try:
        return ResourceType(resource_id.value)
    except ValueError:
        return resource_id.value

# endregion

# region Device management


def MPS_GetVersion() -> str:
    """Gets the product name and system version

    Returns
    -------
    str
        Device version
    """
    message = create_string_buffer(128)
    CTS3Exception._check_error(_MPuLib.MPS_GetVersion(
        message))
    return message.value.decode('ascii').strip()


def MPS_GetHardRev() -> Dict[str, Union[str, int]]:
    """Gets the product hardware revision

    Returns
    -------
    dict
        'revision' (str) : Hardware revision
        'variant' (int) : Hardware variant
    """
    rev = c_char()
    var = c_uint8()
    CTS3Exception._check_error(_MPuLib.MPS_GetHardRev(
        byref(rev),
        byref(var)))
    return {'revision': rev.value.decode('ascii'),
            'variant': var.value}


def MPS_GetVersion2() -> str:
    """Gets the product information in XML format

    Returns
    -------
    str
        Device information in XML format
    """
    message = create_string_buffer(1024 * 1024)
    CTS3Exception._check_error(_MPuLib.MPS_GetVersion2(
        message))
    info = message.value.decode('ascii').strip()
    return cast(str, parseString(info).toprettyxml())


@unique
class EEConfig(IntEnum):
    """Configuration type"""
    EEC_AUTO_BOOT = 1
    EEC_DEBUG_PORT = 4
    EEC_TELNET_NEGO = 5
    EEC_WINUSB_DRIVER = 6


def MPS_EESetConfig(config: EEConfig, value: bool) -> None:
    """Sets product configuration

    Parameters
    ----------
    config : EEConfig
        Configuration to set
    value : bool
        Configuration value
    """
    if not isinstance(config, EEConfig):
        raise TypeError('config must be an instance of EEConfig IntEnum')
    CTS3Exception._check_error(_MPuLib.MPS_EESetConfig(
        c_uint8(0),
        c_uint32(config),
        c_uint32(1) if value else c_uint32(0)))


def MPS_EEGetConfig(config: EEConfig) -> bool:
    """Gets product configuration

    Parameters
    ----------
    config : EEConfig
        Configuration to set

    Returns
    -------
    bool
        Configuration value
    """
    if not isinstance(config, EEConfig):
        raise TypeError('config must be an instance of EEConfig IntEnum')
    value = c_uint32()
    CTS3Exception._check_error(_MPuLib.MPS_EESetConfig(
        c_uint8(0),
        c_uint32(config),
        byref(value)))
    return value.value > 0


def MPS_SelectActivePartition(partition: int) -> None:
    """Selects the partition to activate on the next reboot

    Parameters
    ----------
    partition : int
        Partition index
    """
    _check_limits(c_uint8, partition, 'partition')
    CTS3Exception._check_error(_MPuLib.MPS_SelectActivePartition(
        c_uint8(partition)))


def MPS_GetActivePartition() -> int:
    """Gets the partition which will be activated on the next reboot

    Returns
    -------
    int
        Partition index
    """
    partition = c_uint8()
    CTS3Exception._check_error(_MPuLib.MPS_GetActivePartition(
        byref(partition)))
    return partition.value


def MPS_ListVersions(partition: int) -> Dict[str, Union[str, int]]:
    """Reads the firmware version present on a partition

    Parameters
    ----------
    partition : int
        Partition index

    Returns
    -------
    dict
        'active_partition' (int) : Index of the partition currently in use
        'os_version' (str) : OS version
        'application_version' (str) : Application version
        'fpga_version' (str) : FPGA version
        'daq_version' (str) : DAQ version
    """
    _check_limits(c_uint8, partition, 'partition')
    current_partition = c_uint8()
    system = create_string_buffer(64)
    app = create_string_buffer(64)
    fpga = create_string_buffer(64)
    daq = create_string_buffer(64)
    CTS3Exception._check_error(_MPuLib.MPS_ListVersions(
        c_uint8(partition),
        byref(current_partition),
        system,
        app,
        fpga,
        daq))
    if partition > 0:
        return {'active_partition': current_partition.value,
                'os_version': system.value.decode('ascii').strip(),
                'application_version': app.value.decode('ascii').strip(),
                'fpga_version': fpga.value.decode('ascii').strip(),
                'daq_version': daq.value.decode('ascii').strip()}
    else:
        return {'active_partition': current_partition.value}


def UpdateFirmware(path: Union[str, Path], partIndex: int,
                   call_back: Optional[Callable[[int], int]] =
                   None) -> None:
    """Updates the CTS3 firmware

    Parameters
    ----------
    path : str or Path
        Firmware package path
    partIndex : int
        Index of the partition to update
    call_back : Callable, optional
        Update progress call back
    """
    _check_limits(c_uint8, partIndex, 'partIndex')
    if isinstance(path, Path):
        file = str(path).encode('ascii')
    else:
        file = path.encode('ascii')
    if call_back:
        cmp_func = CFUNCTYPE(c_int32, c_int32)

        CTS3Exception._check_error(_MPuLib.UpdateFirmware(
            file,
            c_uint8(partIndex),
            cmp_func(call_back)))
    else:
        CTS3Exception._check_error(_MPuLib.UpdateFirmware(
            file,
            c_uint8(partIndex),
            None))


def ApplyLicenseUpdateFile(path: Union[str, Path]) -> None:
    """Applies a license update file

    Parameters
    ----------
    path : str or Path
        License update file path
    """
    if isinstance(path, Path):
        file = str(path).encode('ascii')
    else:
        file = path.encode('ascii')
    CTS3Exception._check_error(_MPuLib.ApplyLicenseUpdateFile(
        file))


@unique
class CpuAutotestId(IntEnum):
    """CPU self-test type"""
    TEST_CPU_ALL = -1
    TEST_RAM = 1
    TEST_TIMER = 2
    TEST_FLASH = 3
    TEST_CPU_LOAD = 4


def MPS_CPUAutoTest(test_id: CpuAutotestId = CpuAutotestId.TEST_CPU_ALL,
                    parameter: int = 0) -> List[List[str]]:
    """Performs CPU self-test

    Parameters
    ----------
    test_id : CpuAutotestId, optional
        Self-test identifier
    parameter : int, optional
        Test-specific parameter

    Returns
    -------
    list(list(str))
        Test result
    """
    global _logs_dict
    if not isinstance(test_id, CpuAutotestId):
        raise TypeError('test_id must be an instance of CpuAutotestId IntEnum')
    _check_limits(c_uint32, parameter, 'parameter')
    restore_log = False
    if test_id == CpuAutotestId.TEST_CPU_ALL or \
            (test_id == CpuAutotestId.TEST_FLASH and
                (parameter & 0xF == 0 or parameter & 0xF == 6)):
        # Close 'default' user connection to allow user data partition analysis
        host = _get_connection_string()
        if len(host) > 0 and host in _logs_dict:
            restore_log = True
            _log_stop()
    result = c_char_p()
    ret = CTS3ErrorCode(_MPuLib.MPS_CPUAutoTest(
        c_uint32(test_id),
        c_bool(True),
        c_uint32(parameter),
        byref(result)))
    if restore_log:
        _log_start()
    if (ret >= CTS3ErrorCode.RET_FAIL and ret <= CTS3ErrorCode.RET_WARNING) \
            or ret == CTS3ErrorCode.RET_OK:
        if result.value is None:
            return [['']]
        else:
            tests_result = ''.join(map(chr, result.value)).strip().split('\n')
            return [test.split('\t') for test in tests_result]
    else:
        raise CTS3Exception(ret)


def MPS_ResetHard(resource_id: Union[int, ResourceType, None] = None) -> None:
    """Resets application to its default state

    Parameters
    ----------
    resource_id : int or ResourceType, optional
        Resource to reset, or any other value to reset currently opened
        resources
    """
    if resource_id is None:
        resource_id = 0
    _check_limits(c_uint8, resource_id, 'resource_id')
    CTS3Exception._check_error(_MPuLib.MPS_ResetHard(
        c_uint8(resource_id)))


def MPS_NetworkGetAddress() -> Dict[str, Union[IPv4Interface, IPv4Address]]:
    """Gets the network configuration

    Returns
    -------
    dict
        'ip_interface' (IPv4Interface) : IP interface
        'gateway_address' (IPv4Address) : Gateway IP address
    """
    ip_address = c_uint32()
    subnet_mask = c_uint32()
    gateway_address = c_uint32()
    CTS3Exception._check_error(_MPuLib.MPS_NetworkGetAddress(
        byref(ip_address),
        byref(subnet_mask),
        byref(gateway_address)))
    interface = IPv4Interface((ip_address.value,
                               str(IPv4Address(subnet_mask.value))))
    return {'ip_interface': interface,
            'gateway_address': IPv4Address(gateway_address.value)}


def MPS_NetworkSetAddress(ip_interface: Optional[IPv4Interface],
                          gateway_address: Optional[IPv4Address] = None) \
                         -> None:
    """Sets the network configuration

    Parameters
    ----------
    ip_address : IPv4Interface (None to select DHCP)
        IP interface
    gateway_address : IPv4Address, optional
        Gateway IP address
    """
    if ip_interface is None:
        CTS3Exception._check_error(_MPuLib.MPS_NetworkSetAddress(
            c_uint32(0),
            c_uint32(0),
            c_uint32(0)))
    else:
        if not isinstance(ip_interface, IPv4Interface):
            raise TypeError('ip_interface must be an instance of '
                            'IPv4Interface')
        if gateway_address is None:
            CTS3Exception._check_error(_MPuLib.MPS_NetworkSetAddress(
                c_uint32(int(ip_interface.ip)),
                c_uint32(int(ip_interface.netmask)),
                c_uint32(0)))
        else:
            if not isinstance(gateway_address, IPv4Address):
                raise TypeError('gateway_address must be an instance of '
                                'IPv4Address')
            CTS3Exception._check_error(_MPuLib.MPS_NetworkSetAddress(
                c_uint32(int(ip_interface.ip)),
                c_uint32(int(ip_interface.netmask)),
                c_uint32(int(gateway_address))))


def MPS_NetworkSetUsbAddress(ip_interface: IPv4Interface) -> None:
    """Sets the USB network base address

    Parameters
    ----------
    ip_interface : IPv4Interface
        IP interface
    """
    if not isinstance(ip_interface, IPv4Interface):
        raise TypeError('ip_interface must be an instance of '
                        'IPv4Interface')
    CTS3Exception._check_error(_MPuLib.MPS_NetworkSetUsbAddress(
        str(ip_interface.ip).encode('ascii')))


@unique
class TemperatureSensor(IntEnum):
    """Temperature sensor location"""
    MotherBoardSensor = 0
    NfcBoardSensor = 1
    DaqBoardSensor = 2


def MPS_ProbeTemperature(sensor: TemperatureSensor) -> float:
    """Gets board temperature

    Parameters
    ----------
    sensor : TemperatureSensor
        Sensor identifier

    Returns
    -------
    float, None
        Temperature in °C
    """
    if not isinstance(sensor, TemperatureSensor):
        raise TypeError('sensor must be an instance of '
                        'TemperatureSensor IntEnum')
    _MPuLib.MPS_ProbeTemperature.restype = c_double
    return cast(float, _MPuLib.MPS_ProbeTemperature(
        c_uint8(sensor)))


def MPS_Beep(duration: float) -> None:
    """Beeps the internal buzzer

    Parameters
    ----------
    duration : float
        Beep duration in s
    """
    duration_ms = round(duration * 1e3)
    _check_limits(c_uint32, duration_ms, 'duration')
    CTS3Exception._check_error(_MPuLib.MPS_Beep(
        c_uint32(duration_ms)))


@unique
class LicenseId(IntEnum):
    """Embedded license"""
    LICENSE_SIMULATOR = 6
    LICENSE_VHBR = 12
    LICENSE_SPECIAL_ATS = 18
    LICENSE_ADVANCED_MEAS = 21
    LICENSE_DAQ = 28
    LICENSE_TERMINAL = 29


def MPS_CouplerCheckLicense(embedded_license: LicenseId) -> bool:
    """Checks embedded license validity

    Parameters
    ----------
    embedded_license : LicenseId
        License to be checked

    Returns
    -------
    bool
        True if license is active
    """
    if not isinstance(embedded_license, LicenseId):
        raise TypeError('embedded_license must be an instance of '
                        'LicenseId IntEnum')
    license_validity = c_uint32()
    CTS3Exception._check_error(_MPuLib.MPS_CouplerCheckLicense(
        c_uint8(0),
        c_uint32(embedded_license),
        byref(license_validity)))
    return license_validity.value == 0xFFFFFFFF


def GetLastSystemErrorMessageEx() -> str:
    """Gets the firmware log

    Returns
    -------
    str
        Firmware log
    """
    max_size = 3 * 1024 * 1024
    message = create_string_buffer(max_size)
    CTS3Exception._check_error(_MPuLib.GetLastSystemErrorMessageEx(
        message,
        c_uint8(0),
        c_uint32(max_size)))
    return message.value.decode('ascii').strip()


def GetRemoteHelp(remote: Optional[str] = None) -> Dict[str, str]:
    """Gets remote command help message

    Parameters
    ----------
    remote : str, optional
        Remote command

    Returns
    -------
    dict
        Command/Description pairs
    """
    if remote and (not isinstance(remote, str) or len(remote) != 4):
        raise TypeError('remote must be an instance of 4 characters string')
    max_size = 3 * 1024 * 1024
    message = create_string_buffer(max_size)
    CTS3Exception._check_error(_MPuLib.GetRemoteHelp(
        remote.encode('ascii') if remote else None,
        message))
    help: Dict[str, str] = {}
    for cmd in message.value.decode('ascii').strip().split(';'):
        pair = cmd.split('=')
        if len(pair) == 1 and len(pair[0]):
            help[pair[0]] = ''
        elif len(pair) == 2 and len(pair[0]):
            help[pair[0]] = pair[1]
    return help


def Reboot() -> None:
    """Reboots the device"""
    try:
        _MPuLib.Reboot.restype = c_int32
        CTS3Exception._check_error(_MPuLib.Reboot())
    finally:
        CloseCommunication()


def SoftReboot() -> None:
    """Restarts the device firmware"""
    try:
        _MPuLib.SoftReboot.restype = c_int32
        CTS3Exception._check_error(_MPuLib.SoftReboot())
    finally:
        CloseCommunication()


def Shutdown() -> None:
    """Powers the device off"""
    try:
        _MPuLib.Shutdown.restype = c_int32
        CTS3Exception._check_error(_MPuLib.Shutdown())
    finally:
        CloseCommunication()

# endregion

# region Timers and time delay


def MPS_DoTempo(delay: float) -> None:
    """Waits for a delay

    Parameters
    ----------
    delay : float
        Time to wait in s
    """
    delay_us = round(delay * 1e6)
    _check_limits(c_uint32, delay_us, 'delay')
    CTS3Exception._check_error(_MPuLib.MPS_DoTempo(
        c_uint32(delay_us)))


def MPS_GetTickCount() -> float:
    """Gets time since system startup

    Returns
    -------
    float
        Time in s
    """
    _MPuLib.MPS_GetTickCount.restype = c_uint32
    return cast(int, _MPuLib.MPS_GetTickCount()) / 1e3


class _RTM_Time(Structure):
    """RTM Time structure"""
    _pack_ = 1
    _fields_ = [('Hours', c_uint8),
                ('Minutes', c_uint8),
                ('Seconds', c_uint8)]


class _RTM_Date(Structure):
    """RTM Date structure"""
    _pack_ = 1
    _fields_ = [('DayOfWeek', c_uint8),
                ('DayOfMonth', c_uint8),
                ('Month', c_uint8),
                ('Year', c_uint8)]


def MPS_GetTime() -> datetime:
    """Gets system time

    Returns
    -------
    datetime
        System time
    """
    time = _RTM_Time()
    CTS3Exception._check_error(_MPuLib.MPS_GetTime(
        byref(time)))
    if time.Seconds > 59:
        time.Seconds = 59

    date = _RTM_Date()
    CTS3Exception._check_error(_MPuLib.MPS_GetDate(
        byref(date)))

    local_time = datetime(date.Year + 1900, date.Month, date.DayOfMonth,
                          time.Hours, time.Minutes, time.Seconds)

    if sys.version_info >= (3, 9):
        try:
            tz = ZoneInfo(MPS_GetTimeZone())
            local_time = local_time.replace(tzinfo=tz)
        except ZoneInfoNotFoundError:
            pass

    return local_time


def MPS_SetTime(time: datetime = datetime.now().astimezone()) -> None:
    """Sets system time

    Parameters
    ----------
    time : datetime, optional
        Time to set
    """
    if sys.version_info >= (3, 9):
        try:
            # Try to set local time zone
            MPS_SetTimeZone()
        except (ZoneInfoNotFoundError, ModuleNotFoundError, ValueError):
            pass

    _check_limits(c_uint8, time.year - 1900, 'time')
    c_time = _RTM_Time(time.hour, time.minute, time.second)
    CTS3Exception._check_error(_MPuLib.MPS_SetTime(
        byref(c_time)))

    c_date = _RTM_Date(0, time.day, time.month, time.year - 1900)
    CTS3Exception._check_error(_MPuLib.MPS_SetDate(
        byref(c_date)))


def MPS_GetTimeZone() -> str:
    """Gets time zone

    Returns
    -------
    str
        Current time zone
    """
    time_zone = create_string_buffer(128)
    CTS3Exception._check_error(_MPuLib.MPS_GetTimeZone(
        time_zone))
    return time_zone.value.decode('ascii')


def MPS_SetTimeZone(time_zone: Optional[str] = None) -> None:
    """Sets time zone

    Parameters
    ----------
    time_zone : str, optional
        Time zone to set (None to set local time zone)
    """
    if not time_zone and sys.version_info >= (3, 9):
        if sys.platform == 'win32':
            try:
                from tzlocal import get_localzone  # noqa: E402
                time_zone = str(get_localzone())
            except ModuleNotFoundError:
                pass
        else:
            time_zone = str(ZoneInfo('localtime'))
    if not time_zone:
        raise ValueError('unable to get local time zone')
    CTS3Exception._check_error(_MPuLib.MPS_SetTimeZone(
        time_zone.encode('ascii')))


def MPS_GetDate() -> datetime:
    """Gets system date

    Returns
    -------
    datetime
        System date
    """
    return MPS_GetTime()


def MPS_SetDate(date: datetime = datetime.now().astimezone()) -> None:
    """Sets system date

    Parameters
    ----------
    date : datetime, optional
        Date to set
    """
    MPS_SetTime(date)

# endregion

# region LEDs management


@unique
class LedColor(IntEnum):
    """LED color"""
    LED_RED = 0
    LED_GREEN = 1
    LED_YELLOW = 2
    LED_OFF = 3
    LED_BLUE = 4
    LED_MAGENTA = 5
    LED_WHITE = 6
    LED_CYAN = 7


def MPS_LedOn(color: LedColor) -> None:
    """Switches AUX CPU LED on

    Parameters
    ----------
    color : LedColor
        LED color
    """
    if not isinstance(color, LedColor):
        raise TypeError('color must be an instance of LedColor IntEnum')
    CTS3Exception._check_error(_MPuLib.MPS_LedOn(
        c_uint8(0),
        c_uint8(color)))


def MPS_LedOff() -> None:
    """Switches AUX CPU connector LED off"""
    CTS3Exception._check_error(_MPuLib.MPS_LedOff(
        c_uint8(0)))

# endregion

# region I²C


def MPS_I2cAuxWrite(slave_address: int, data: bytes) -> None:
    """Writes to I²C AUX 2 front connector

    Parameters
    ----------
    slave_address : int
        7-bit I²C slave address (0x1E and 0x77 are reserved)
    data : bytes
        Data to write
    """
    _check_limits(c_uint8, slave_address, 'slave_address')
    if not isinstance(data, bytes):
        raise TypeError('data must be an instance of bytes')
    _check_limits(c_uint8, len(data), 'data')
    CTS3Exception._check_error(_MPuLib.MPS_I2cAuxWrite(
        c_uint8(slave_address),
        c_uint8(len(data)),
        data))


def MPS_I2cAuxRead(slave_address: int, data_length: int) -> bytes:
    """Reads from I²C AUX 2 front connector

    Parameters
    ----------
    slave_address : int
        7 bits I²C slave address (0x1E and 0x77 are reserved)
    data_length : bytes
        Size of data to read

    Returns
    -------
    bytes
        Data read
    """
    _check_limits(c_uint8, slave_address, 'slave_address')
    _check_limits(c_uint8, data_length, 'data_length')
    data = bytes(255)
    size = c_uint8(data_length)
    CTS3Exception._check_error(_MPuLib.MPS_I2cAuxRead(
        c_uint8(slave_address),
        byref(size),
        data))
    return data[:size.value]


def MPS_I2cAux1Write(slave_address: int, data: bytes) -> None:
    """Writes to I²C AUX 1 front connector

    Parameters
    ----------
    slave_address : int
        7-bit I²C slave address (0x1E and 0x77 are reserved)
    data : bytes
        Data to write
    """
    _check_limits(c_uint8, slave_address, 'slave_address')
    if not isinstance(data, bytes):
        raise TypeError('data must be an instance of bytes')
    _check_limits(c_uint8, len(data), 'data')
    CTS3Exception._check_error(_MPuLib.MPS_I2cAux1Write(
        c_uint8(slave_address),
        c_uint8(len(data)),
        data))


def MPS_I2cAux1Read(slave_address: int, data_length: int) -> bytes:
    """Reads from I²C AUX 1 front connector

    Parameters
    ----------
    slave_address : int
        7 bits I²C slave address (0x1E and 0x77 are reserved)
    data_length : bytes
        Size of data to read

    Returns
    -------
    bytes
        Data read
    """
    _check_limits(c_uint8, slave_address, 'slave_address')
    _check_limits(c_uint8, data_length, 'data_length')
    data = bytes(255)
    size = c_uint8(data_length)
    CTS3Exception._check_error(_MPuLib.MPS_I2cAux1Read(
        c_uint8(slave_address),
        byref(size),
        data))
    return data[:size.value]

# endregion

# region Serial port


@unique
class Baudrate(IntEnum):
    """RS-232 baud rate"""
    BAUDS_9600 = 0
    BAUDS_19200 = 1
    BAUDS_38400 = 2
    BAUDS_115200 = 3
    BAUDS_230400 = 4
    BAUDS_524288 = 5


@unique
class SerialParity(IntEnum):
    """RS-232 parity"""
    SERIAL_NOP = 0
    SERIAL_EVENP = 1
    SERIAL_ODDP = 2


def MPS_PortInit(baud_rate: Baudrate = Baudrate.BAUDS_115200,
                 parity: SerialParity = SerialParity.SERIAL_NOP,
                 stop_bits: int = 1,
                 data_bits: int = 8,
                 xon_xoff: bool = False) -> None:
    """Initializes serial port on AUX.CPU front connector

    Parameters
    ----------
    baud_rate : Baudrate, optional
        Device baud rate
    parity : SerialParity, optional
        Parity bits number
    stop_bits : int, optional
        Stop bits number
    data_bits : int, optional
        Data bits number
    xon_xoff : bool, optional
        True to enable flow control
    """
    if not isinstance(baud_rate, Baudrate):
        raise TypeError('baud_rate must be an instance of Baudrate IntEnum')
    if not isinstance(parity, SerialParity):
        raise TypeError('parity must be an instance of SerialParity IntEnum')
    flag = parity.value
    if stop_bits == 2:
        flag |= 0x04
    elif stop_bits != 1:
        raise ValueError('invalid stop_bits value')
    if data_bits == 8:
        flag |= 0x10
    elif data_bits != 7:
        raise ValueError('invalid data_bits value')
    if xon_xoff:
        flag |= 0x08
    CTS3Exception._check_error(_MPuLib.MPS_PortInit(
        c_uint8(3),
        c_uint8(baud_rate),
        c_uint8(flag)))


def MPS_PortSend(tx_frame: bytes) -> None:
    """Sends data over serial port

    Parameters
    ----------
    tx_frame : bytes
        Data to write
    """
    if not isinstance(tx_frame, bytes):
        raise TypeError('tx_frame must be an instance of bytes')
    _check_limits(c_uint16, len(tx_frame), 'tx_frame')
    CTS3Exception._check_error(_MPuLib.MPS_PortSend(
        c_uint8(3),
        tx_frame,
        c_uint16(len(tx_frame))))


def MPS_PortReceive(data_count: Optional[int] = None) -> bytes:
    """Reads data from serial port

    Parameters
    ----------
    data_count : int, optional
        Size of data to read.
        If None, data currently received are returned

    Returns
    -------
    bytes
        Data read
    """
    if data_count:
        _check_limits(c_uint16, data_count, 'data_count')
        data = bytes(data_count)
        CTS3Exception._check_error(_MPuLib.MPS_PortReceive(
            c_uint8(3),
            data,
            c_uint16(data_count)))
    else:
        count = c_uint16()
        CTS3Exception._check_error(_MPuLib.MPS_PortStatus(
            c_uint8(3),
            byref(count)))
        data = bytes(count.value)
        CTS3Exception._check_error(_MPuLib.MPS_PortReceive(
            c_uint8(3),
            data,
            count))
    return data


@unique
class PortStatusType(IntEnum):
    """RS-232 port status"""
    PS_RXBUFF_COUNT = 1
    PS_TXBUFF_COUNT = 2


def MPS_PortStatusEx(status_type: PortStatusType) -> int:
    """Gets port buffer status

    Parameters
    ----------
    status_type : PortStatusType
        Buffer type

    Returns
    -------
    int
        Buffer size
    """
    if not isinstance(status_type, PortStatusType):
        raise TypeError('status_type must be an instance of '
                        'PortStatusType IntEnum')
    value = c_uint32()
    CTS3Exception._check_error(_MPuLib.MPS_PortStatusEx(
        c_uint8(3),
        c_uint32(status_type),
        byref(value)))
    return value.value

# endregion

# region Relay Driving


@unique
class AuxRelay(IntEnum):
    """CMOS output"""
    RELAY1 = 1
    RELAY2 = 2
    RELAY3 = 3
    RELAY4 = 4
    RELAY5 = 5


def MPC_SetRelay(relay_number: AuxRelay, state: bool) -> None:
    """Drives a CMOS output on the HDMI connector

    Parameters
    ----------
    relay_number : AuxRelay
        Relay number
    state : bool
        True to output 5V
    """
    if not isinstance(relay_number, AuxRelay):
        raise TypeError('relay_number must be an instance of AuxRelay IntEnum')
    CTS3Exception._check_error(_MPuLib.MPC_SetRelay(
        c_uint8(0),
        c_uint8(relay_number),
        c_bool(state)))

# endregion

# region Embedded applications


@unique
class EmbeddedScriptMode(IntFlag):
    """Embedded script mode"""
    EMBEDDED_NO_OPTION = 0
    EMBEDDED_WAIT_TERMINATION = 1
    EMBEDDED_REMOTE_OUTPUT = 2


def LaunchEmbeddedScript(script_command: str,
                         timeout: float,
                         option: EmbeddedScriptMode =
                         EmbeddedScriptMode.EMBEDDED_WAIT_TERMINATION,
                         call_back: Optional[Callable[[bytes], int]] =
                         None) -> int:
    """Launches an embedded script

    Parameters
    ----------
    script_command : str
        Script to run
    timeout : float
        Execution timeout in s (only if option is configured with
        EMBEDDED_WAIT_TERMINATION)
    option : EmbeddedScriptMode, optional
        Embedded script options
    call_back : Callable, optional
        Script callback function (only if option is configured with
        EMBEDDED_WAIT_TERMINATION)

    Returns
    -------
    int
        Script return code
    """
    timeout_ms = round(timeout * 1e3)
    _check_limits(c_uint32, timeout_ms, 'timeout')
    if not isinstance(option, EmbeddedScriptMode):
        raise TypeError('option must be an instance of '
                        'EmbeddedScriptMode IntFlag')
    retCode = c_uint8(0)
    if call_back:
        cmp_func = CFUNCTYPE(c_int32, c_char_p)
    CTS3Exception._check_error(_MPuLib.LaunchEmbeddedScript(
        script_command.encode('ascii'),
        c_uint32(option),
        c_uint32(timeout_ms),
        byref(retCode),
        cmp_func(call_back) if call_back else None))
    return retCode.value


def StartEmbeddedApplication(application_path: str, args: str,
                             call_back: Optional[Callable[[bytes], int]]
                             = None) -> None:
    """Launches an embedded C program within the firmware environment

    Parameters
    ----------
    application_path : str
        Embedded C program path
    args : str
        Program parameters
    call_back : Callable, optional
        Program callback function
    """
    if call_back:
        cmp_func = CFUNCTYPE(c_int32, c_char_p)
    CTS3Exception._check_error(_MPuLib.StartEmbeddedApplication(
        application_path.encode('ascii'),
        args.encode('ascii') if args else None,
        cmp_func(call_back) if call_back else None))

# endregion

# region MPuLib Specific


def OpenCommunication(host: Union[str, IPv4Address],
                      log: bool = True) -> None:
    """Opens the communication channel to a CTS3

    Parameters
    ----------
    host : str or IPv4Address
        Host name or IP address
    log : bool, optional
        True to output firmware log to stderr
    """
    _MPuLib.OpenCommunication.restype = c_int32
    if isinstance(host, str):
        CTS3Exception._check_error(_MPuLib.OpenCommunication(
            host.encode('ascii')))
    elif isinstance(host, IPv4Address):
        CTS3Exception._check_error(_MPuLib.OpenCommunication(
            str(host).encode('ascii')))
    else:
        raise TypeError('host must be an instance of str or IPv4Interface')
    if log:
        _log_start()


def CloseCommunication() -> None:
    """Closes the communication channel"""
    _log_stop()
    _MPuLib.CloseCommunication.restype = c_int32
    _MPuLib.CloseCommunication()


@unique
class LibraryParameter(IntEnum):
    """MPuLib parameters"""
    TCP_TIMEOUT = 1
    USB_TIMEOUT = 8
    DLL_VERSION = 10
    TCP_CONNECT_TIMEOUT = 12
    SPY_TIMEOUT = 13
    DAQ_TIMEOUT = 14


def SetDLLParameter(param: LibraryParameter, value: float) -> None:
    """Sets MPuLib parameter

    Parameters
    ----------
    param : LibraryParameter
        Parameter to set
    value : float
        Parameter value
    """
    if not isinstance(param, LibraryParameter):
        raise TypeError('param must be an instance of '
                        'LibraryParameter IntEnum')
    value_ms = round(value * 1e3)
    _check_limits(c_uint32, value_ms, 'value')
    CTS3Exception._check_error(_MPuLib.SetDLLParameter(
        c_uint32(param),
        c_uint32(value_ms)))


def GetDLLParameter(param: LibraryParameter) -> Union[str, float]:
    """Gets MPuLib parameter

    Parameters
    ----------
    param : LibraryParameter
        Parameter to get

    Returns
    -------
    str or float
        Parameter value
    """
    if not isinstance(param, LibraryParameter):
        raise TypeError('param must be an instance of '
                        'LibraryParameter IntEnum')
    val = c_uint32()
    CTS3Exception._check_error(_MPuLib.GetDLLParameter(
        c_uint32(param),
        byref(val)))
    if param == LibraryParameter.DLL_VERSION:
        return str(val.value >> 24) + '.' + str((val.value >> 16) & 0xFF) + \
            '.' + str((val.value >> 8) & 0xFF) + '.' + \
            str(val.value & 0xFF)
    else:
        return float(val.value) / 1e3


def SetDLLDebugMode(path: Union[str, Path, None]) -> None:
    """Generates a log file containing remote commands

    Parameters
    ----------
    path : str or Path
        Log file path (None to deactivate)
    """
    if not path:
        file = None
    elif isinstance(path, Path):
        if str(path) != '.':
            file = str(path).encode('ascii')
        else:
            file = None
    else:
        if len(path) == 0:
            file = None
        else:
            file = path.encode('ascii')
    _MPuLib.SetDLLDebugMode.restype = None
    _MPuLib.SetDLLDebugMode(
        c_bool(file is not None),
        file)


def SendFrame(command: Optional[str], timeout: int = -1,
              asynchronous_tx: bool = False) -> Optional[str]:
    """Sends a remote command to the connected CTS3

    Parameters
    ----------
    command : str
        Remote command to send
    timeout : int, optional
        Communication timeout in s (-1 to use default value)
    asynchronous_tx : bool, optional
        True to send command to connected CTS3 without waiting for an answer

    Returns
    -------
    str
        CTS3 answer
    """
    if timeout != -1:
        _check_limits(c_uint16, timeout, 'timeout')
    _MPuLib.SendFrame.restype = c_int32
    max_buffer_size = 3 * 1024 * 1024 + 1
    if command is None:
        response = create_string_buffer(max_buffer_size)
        CTS3Exception._check_error(_MPuLib.SendFrame(
            None,
            c_int32(0),
            c_uint16(timeout),
            '',
            response))
        return response.value.decode('ascii').strip()
    else:
        if not asynchronous_tx and not command.endswith('\r'):
            command += '\r'
        if asynchronous_tx:
            CTS3Exception._check_error(_MPuLib.SendFrame(
                byref(c_uint32(1)),
                c_int32(1),
                c_uint16(timeout),
                command.encode('ascii'),
                None))
            return None
        else:
            response = create_string_buffer(max_buffer_size)
            CTS3Exception._check_error(_MPuLib.SendFrame(
                None,
                c_int32(0),
                c_uint16(timeout),
                command.encode('ascii'),
                response))
            return response.value.decode('ascii').strip()


@unique
class LibraryMode(IntEnum):
    """MPuLib mode"""
    MULTITHREADED = 0
    MONOTHREADED = 1
    ADDRESSED = 2


def SetDLLMode(mode: LibraryMode) -> None:
    """Sets MPuLib working mode

    Parameters
    ----------
    mode : LibraryMode
        Working mode
    """
    if not isinstance(mode, LibraryMode):
        raise TypeError('flag must be an instance of LibraryMode IntEnum')
    _MPuLib.SetDLLMode.restype = c_int32
    CTS3Exception._check_error(_MPuLib.SetDLLMode(
        c_uint32(mode)))


def USBEnumerateDevices() -> List[str]:
    """Detects Micropross devices over USB link

    Returns
    -------
    list(str)
        Devices serial number list
    """
    devices_number = c_int32()
    devices_list = create_string_buffer(0xFFFF)
    _MPuLib.USBEnumerateDevices2.restype = c_int32
    CTS3Exception._check_error(_MPuLib.USBEnumerateDevices2(
        byref(devices_number),
        devices_list))
    list_string = devices_list.value.decode('ascii')
    return list_string.splitlines() if len(list_string) else []


def UsbResetInterface(host: Optional[str] = None) -> None:
    """Resets WinUSB driver interface

    Parameters
    ----------
    host : str, optional
        Host name
    """
    if sys.platform == 'win32':
        _MPuLib.UsbResetInterface.restype = None
        if host is None:
            _MPuLib.UsbResetInterface(None, c_uint32(0))
        else:
            _MPuLib.UsbResetInterface(host.encode('ascii'), c_uint32(0))


def TCPEnumerateDevices() -> Dict[str, IPv4Address]:
    """Detects Micropross devices over Ethernet

    Returns
    -------
    dict
        Device serial number (str) : Device IP address (IPv4Address)
    """
    devices_number = c_uint32()
    devices_ip = create_string_buffer(0xFFFF)
    devices_serial = create_string_buffer(0xFFFF)
    _MPuLib.TCPEnumerateDevices.restype = c_int32
    CTS3Exception._check_error(_MPuLib.TCPEnumerateDevices(
        byref(devices_number),
        devices_ip,
        devices_serial))
    list_ip = devices_ip.value.decode('ascii').splitlines()
    list_serial = devices_serial.value.decode('ascii').splitlines()
    if len(list_ip) and len(list_ip) == len(list_serial):
        return {list_serial[i]: IPv4Address(list_ip[i])
                for i in range(len(list_ip))}
    else:
        return {}


def USBEnumerateDevices2() -> List[str]:
    """Detects Micropross devices over USB link

    Returns
    -------
    list(str)
        Devices serial number list
    """
    return USBEnumerateDevices()


def SelectActiveDevice(active_device: int) -> None:
    """Selects the device to send the commands to

    Parameters
    ----------
    active_device : int
        Device identifier
    """
    _check_limits(c_uint32, active_device, 'active_device')
    _MPuLib.SelectActiveDevice.restype = c_int32
    CTS3Exception._check_error(_MPuLib.SelectActiveDevice(
        c_uint32(active_device)))


def AbortCoupler(host: Union[str, IPv4Address]) -> None:
    """Aborts current command execution

    Parameters
    ----------
    host : str or IPv4Address
        Host name or IP address
    """
    if isinstance(host, str):
        _MPuLib.AbortCoupler(
            c_uint8(0),
            host.encode('ascii'))
    elif isinstance(host, IPv4Address):
        _MPuLib.AbortCoupler(
            c_uint8(0),
            str(host).encode('ascii'))
    else:
        raise TypeError('host must be an instance of str or IPv4Interface')


def UploadClientFile(local_path: Union[str, Path], remote_name: str) -> None:
    """Uploads a file to the CTS3 '/home/default/tmp' directory

    Parameters
    ----------
    local_path : str or Path
        Path to file to upload
    remote_name : str
        CTS3 remote file name (will be over-written if already exists)
    """
    if isinstance(local_path, Path):
        file = str(local_path).encode('ascii')
    else:
        file = local_path.encode('ascii')
    CTS3Exception._check_error(_MPuLib.UploadClientFile(
        file,
        remote_name.encode('ascii')))


def DownloadClientFile(remote_name: str, local_path: Union[str, Path]) -> None:
    """Downloads a file from the CTS3 '/home/default/tmp' directory

    Parameters
    ----------
    remote_name : str
        CTS3 remote file name
    local_path : str or Path
        Path to file to be downloaded
    """
    if isinstance(local_path, Path):
        file = str(local_path).encode('ascii')
    else:
        file = local_path.encode('ascii')
    CTS3Exception._check_error(_MPuLib.DownloadClientFile(
        remote_name.encode('ascii'),
        file))

# endregion
