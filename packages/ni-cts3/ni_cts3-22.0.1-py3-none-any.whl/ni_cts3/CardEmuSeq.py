from enum import IntEnum, unique
from ctypes import c_uint8, c_uint16, c_int32, c_uint32
from ctypes import Structure, byref
from typing import Union, List, Optional, overload
from warnings import warn
from . import _MPuLib, _MPuLib_variadic, _check_limits
from .Measurement import VoltmeterRange
from .Nfc import TechnologyType, NfcTrigger, DataRate
from .Nfc import VicinityDataRate, VicinitySubCarrier
from .MPException import CTS3Exception


def MPC_OpenScenarioPcd() -> int:
    """Opens a scenario instance

    Returns
    -------
    int
        Scenario instance identifier
    """
    scenario_id = c_uint32()
    CTS3Exception._check_error(_MPuLib.MPC_OpenScenarioPcd(
        c_uint8(0),
        byref(scenario_id),
        c_uint32(0)))
    return scenario_id.value


@unique
class CardEmuSeqAction(IntEnum):
    """Card emulation sequencer actions"""
    TSCN_PARAM_SOF_LOW = 2
    TSCN_PARAM_SOF_HIGH = 3
    TSCN_PARAM_EGT = 4
    TSCN_PARAM_EOF = 5
    TSCN_DO_TEMPO = 19
    TSCN_DO_EXCHANGE = 22
    TSCN_DO_PARITY_ERROR = 23
    TSCN_DO_CHANGE_DATA_RATE = 24
    TSCN_DO_USER_EVENT = 25
    TSCN_DO_TRIGGER_OUT = 26
    TSCN_PARAM_TR0 = 27
    TSCN_PARAM_TR1 = 28
    TSCN_PARAM_TRF = 29
    TSCN_PARAM_FDT1_PICC = 30
    TSCN_PARAM_FDT2_PICC = 31
    TSCN_DO_SEQUENCE_ERROR = 32
    TSCN_DO_EMD = 33
    TSCN_DO_CHANGE_VC_DATA_RATE = 34
    TSCN_DO_COMPLETE_ANTICOLLISION = 35
    TSCN_DO_WAIT_VC_EOF_ONLY = 36
    TSCN_EMD_SUBCARRIER = 37
    TSCN_SET_PCD_MASK = 38
    TSCN_DO_EXCHANGE_RAW_TYPEA = 39
    TSCN_DO_TRIGGER_OUT_RX_ON = 41
    TSCN_DO_TRIGGER_OUT_EMD_GENERATION = 42
    TSCN_DO_WAIT_TYPEA106_SEND_BITS = 43
    TSCN_PARAM_TR0_NS = 50
    TSCN_PARAM_FDT1_PICC_NS = 51
    TSCN_PARAM_FDT2_PICC_NS = 52
    TSCN_PARAM_EGT_BEFORE_EOF = 53
    TSCN_PARAM_FELICA_BIT_CODING_REVERSE = 57
    TSCN_DO_CHANGE_FELICA_DUTY_CYCLE = 58
    TSCN_DO_WAIT_VC_SEND_SOF_ONLY = 63
    TSCN_DO_CE_TRIGGER = 65
    TSCN_DO_START_RF_MEASURE = 67
    TSCN_DO_SELECT_VOLTMETER_RANGE = 69
    TSCN_DO_EXCHANGE_EBF = 70
    TSCN_DO_NEGATIVE_MODULATION = 71
    TSCN_SET_LMA_CARD_EMULATION = 72
    TSCN_DO_VICINITY_COLLISION = 75
    TSCN_PARAM_AUTOMATIC_ATN_RESPONSE = 76
    TSCN_DO_EXCHANGE_ACTIVE_TARGET = 77
    TSCN_PARAM_NFC_ACTIVE_TIMINGS = 78
    TSCN_PARAM_ACTIVE_FDT_MODE = 80
    TSCN_PARAM_ACTIVE_TIMINGS = 82


@unique
class SequenceError(IntEnum):
    """Type A sequence error"""
    SEQUENCE_ERROR_C = 1
    SEQUENCE_ERROR_D = 2
    SEQUENCE_ERROR_E = 7


@unique
class EmdSubCarrier(IntEnum):
    """EMD sub-carriers"""
    EMD_64_PERIODS = 212
    EMD_424_PERIODS = 424
    EMD_848_PERIODS = 848
    EMD_1695_PERIODS = 1695
    EMD_3390_PERIODS = 3390
    EMD_6780_PERIODS = 6780


class _S_emd(Structure):
    """EMD structure definition"""
    _pack_ = 1
    _fields_ = [('nb_pattern', c_uint16),
                ('pattern', c_uint16)]


@unique
class S_emd_pattern(IntEnum):
    """EMD pattern"""
    high_state = 0    # ‾‾‾
    rising_edge = 1   # _|‾
    falling_edge = 2  # ‾|_
    low_state = 3     # ___


class S_emd():
    """EMD definition

    Attributes
    ----------
    number : int
        Patterns number to send
    type : S_emd_pattern
        EMD waveform pattern
    """

    def __init__(self, patterns_number: int, pattern_type: S_emd_pattern):
        """Inits S_emd

        Parameters
        ----------
        pattern_number : int
            Patterns number to send
        pattern_type : S_emd_pattern
            EMD waveform pattern
        """
        _check_limits(c_uint16, patterns_number, 'patterns_number')
        if not isinstance(pattern_type, S_emd_pattern):
            raise TypeError('pattern_type must be an instance of '
                            'S_emd_pattern IntEnum')
        self.number = patterns_number
        self.type = pattern_type


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         param1: Union[int, bool, float, EmdSubCarrier,
                                       VoltmeterRange]) -> None:
    # TSCN_PARAM_SOF_LOW, TSCN_PARAM_SOF_HIGH, TSCN_PARAM_EGT, TSCN_PARAM_EOF,
    # TSCN_DO_PARITY_ERROR, TSCN_DO_USER_EVENT, TSCN_PARAM_TR0, TSCN_PARAM_TR1,
    # TSCN_PARAM_TRF, TSCN_PARAM_FDT1_PICC, TSCN_PARAM_FDT2_PICC,
    # TSCN_PARAM_EGT_BEFORE_EOF,
    # TSCN_DO_TRIGGER_OUT_RX_ON, TSCN_DO_TRIGGER_OUT_EMD_GENERATION,
    # TSCN_PARAM_AUTOMATIC_ATN_RESPONSE,
    # TSCN_PARAM_FELICA_BIT_CODING_REVERSE, TSCN_PARAM_ACTIVE_FDT_MODE,
    # TSCN_DO_WAIT_VC_EOF_ONLY,
    # TSCN_DO_TEMPO, TSCN_PARAM_TR0_NS, TSCN_PARAM_FDT1_PICC_NS,
    # TSCN_PARAM_FDT2_PICC_NS,
    # TSCN_EMD_SUBCARRIER,
    # TSCN_DO_SELECT_VOLTMETER_RANGE
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         param1: Union[int, bool, VicinityDataRate, DataRate],
                         param2: Union[int, bool, VicinitySubCarrier,
                                       DataRate]) -> None:
    # TSCN_DO_CHANGE_FELICA_DUTY_CYCLE, TSCN_DO_VICINITY_COLLISION,
    # TSCN_DO_TRIGGER_OUT, TSCN_DO_COMPLETE_ANTICOLLISION,
    # TSCN_DO_CHANGE_VC_DATA_RATE,
    # TSCN_DO_CHANGE_DATA_RATE,
    # TSCN_DO_NEGATIVE_MODULATION
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         param1: bool, param2: int,
                         param3: int) -> None:
    # TSCN_DO_NEGATIVE_MODULATION
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         param1: int, param2: Union[int, NfcTrigger],
                         param3: Union[int, bool, SequenceError]) -> None:
    # TSCN_PARAM_NFC_ACTIVE_TIMINGS,
    # TSCN_DO_CE_TRIGGER,
    # TSCN_DO_SEQUENCE_ERROR
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         tadt: int, tarfg: int,
                         toff: int, tmute: int) -> None:
    # TSCN_PARAM_ACTIVE_TIMINGS
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         param1: Union[float, NfcTrigger],
                         param2: float) -> None:
    # TSCN_SET_LMA_CARD_EMULATION,
    # TSCN_DO_START_RF_MEASURE
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         fdt: int, emd: List[S_emd]) -> None:
    # TSCN_DO_EMD
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         picc_crc: bool, pcd_type: TechnologyType,
                         synchro: bool, picc_frame: bytes) -> None:
    # TSCN_DO_EXCHANGE
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         pcd_crc: bool, picc_crc: bool,
                         pcd_type: TechnologyType, synchro: bool,
                         pcd_frame: Optional[bytes],
                         picc_frame: Optional[bytes]) -> None:
    # TSCN_DO_EXCHANGE, TSCN_DO_EXCHANGE_ACTIVE_TARGET
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         param1: bool, picc_frame: bytes) -> None:
    # TSCN_DO_WAIT_VC_EOF_ONLY
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         pcd_type: TechnologyType, mask: bytes) -> None:
    # TSCN_SET_PCD_MASK
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         synchro: bool, pcd_frame: str,
                         picc_frame: str) -> None:
    # TSCN_DO_EXCHANGE_RAW_TYPEA
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         vcd_crc: bool, synchro: bool,
                         vcd_frame: bytes) -> None:
    # TSCN_DO_WAIT_VC_SEND_SOF_ONLY
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         synchro: bool, picc_bits_number: int,
                         picc_frame: bytes) -> None:
    # TSCN_DO_WAIT_TYPEA106_SEND_BITS
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         pcd_crc: bool, synchro: bool,
                         pcd_frame: Optional[bytes]) -> None:
    # TSCN_DO_WAIT_TYPEA106_SEND_BITS
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         pcd_crc: bool, synchro: bool,
                         pcd_frame: Optional[bytes], picc_bits_number: int,
                         picc_frame: bytes) -> None:
    # TSCN_DO_WAIT_TYPEA106_SEND_BITS
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         picc_ebf: bool, picc_pcd_option: int,
                         picc_crc: bool, pcd_type: TechnologyType,
                         synchro: bool, picc_frame: bytes) -> None:
    # TSCN_DO_EXCHANGE_EBF
    ...


@overload
def MPC_AddToScenarioPcd(scenario_id: int, action: CardEmuSeqAction,
                         pcd_ebf: bool, picc_ebf: bool,
                         pcd_picc_option: int, picc_pcd_option: int,
                         pcd_crc: bool, picc_crc: bool,
                         pcd_type: TechnologyType, synchro: bool,
                         pcd_frame: Optional[bytes],
                         picc_frame: Optional[bytes]) -> None:
    # TSCN_DO_EXCHANGE_EBF
    ...


def MPC_AddToScenarioPcd(scenario_id,  # type: ignore[no-untyped-def]
                         action, *args):
    """Adds an action to a scenario

    Parameters
    ----------
    scenario_id : int
        Scenario instance identifier
    action : TerminalEmulationSequenceAction
        Scenario action
    *args
        Scenario action parameters
    """
    _check_limits(c_uint32, scenario_id, 'scenario_id')
    if not isinstance(action, CardEmuSeqAction):
        raise TypeError('action must be an instance of '
                        'CardEmuSeqAction IntEnum')
    if _MPuLib_variadic is None:
        func_pointer = _MPuLib.MPC_AddToScenarioPcd
    else:
        func_pointer = _MPuLib_variadic.MPC_AddToScenarioPcd

    # One parameter
    if action == CardEmuSeqAction.TSCN_PARAM_SOF_LOW or \
            action == CardEmuSeqAction.TSCN_PARAM_SOF_HIGH or \
            action == CardEmuSeqAction.TSCN_PARAM_EGT or \
            action == CardEmuSeqAction.TSCN_PARAM_EOF or \
            action == CardEmuSeqAction.TSCN_DO_PARITY_ERROR or \
            action == CardEmuSeqAction.TSCN_PARAM_TR0 or \
            action == CardEmuSeqAction.TSCN_PARAM_TR1 or \
            action == CardEmuSeqAction.TSCN_PARAM_TRF or \
            action == CardEmuSeqAction.TSCN_PARAM_FDT1_PICC or \
            action == CardEmuSeqAction.TSCN_PARAM_FDT2_PICC or \
            action == CardEmuSeqAction.TSCN_PARAM_EGT_BEFORE_EOF or \
            action == CardEmuSeqAction.TSCN_PARAM_AUTOMATIC_ATN_RESPONSE or \
            action == CardEmuSeqAction.TSCN_DO_USER_EVENT:
        if len(args) != 1:
            raise TypeError(f'MPC_AddToScenarioPcd({action.name}) takes '
                            f'exactly three arguments ({len(args) + 2} given)')
        if not isinstance(args[0], int):
            raise TypeError('param1 must be an instance of int')
        _check_limits(c_uint32, args[0], 'param1')
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0])))
    elif action == CardEmuSeqAction.TSCN_PARAM_FELICA_BIT_CODING_REVERSE or \
            action == CardEmuSeqAction.TSCN_PARAM_ACTIVE_FDT_MODE:
        if len(args) != 1:
            raise TypeError(f'MPC_AddToScenarioPcd({action.name}) takes '
                            f'exactly three arguments ({len(args) + 2} given)')
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(1) if args[0] else c_uint32(0)))
    # µs
    elif action == CardEmuSeqAction.TSCN_DO_TEMPO:
        if len(args) != 1:
            raise TypeError(f'MPC_AddToScenarioPcd({action.name}) takes '
                            f'exactly three arguments ({len(args) + 2} given)')
        if not isinstance(args[0], float) and not isinstance(args[0], int):
            raise TypeError('param1 must be an instance of float')
        tempo_us = round(args[0] * 1e6)
        _check_limits(c_uint32, tempo_us, 'param1')
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(tempo_us)))
    # ns
    elif action == CardEmuSeqAction.TSCN_PARAM_TR0_NS or \
            action == CardEmuSeqAction.TSCN_PARAM_FDT1_PICC_NS or \
            action == CardEmuSeqAction.TSCN_PARAM_FDT2_PICC_NS:
        if len(args) != 1:
            raise TypeError(f'MPC_AddToScenarioPcd({action.name}) takes '
                            f'exactly three arguments ({len(args) + 2} given)')
        if not isinstance(args[0], float) and not isinstance(args[0], int):
            raise TypeError('param1 must be an instance of float')
        delay_ns = round(args[0] * 1e9)
        _check_limits(c_uint32, delay_ns, 'param1')
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(delay_ns)))
    elif action == CardEmuSeqAction.TSCN_EMD_SUBCARRIER:
        if len(args) != 1:
            raise TypeError(f'MPC_AddToScenarioPcd({action.name}) takes '
                            f'exactly three arguments ({len(args) + 2} given)')
        if not isinstance(args[0], EmdSubCarrier):
            raise TypeError('param1 must be an instance of '
                            'EmdSubCarrier IntEnum')
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            args[0]))
    elif action == CardEmuSeqAction.TSCN_DO_SELECT_VOLTMETER_RANGE:
        if len(args) != 1:
            raise TypeError(f'MPC_AddToScenarioPcd({action.name}) takes '
                            f'exactly three arguments ({len(args) + 2} given)')
        if not isinstance(args[0], VoltmeterRange):
            raise TypeError('param1 must be an instance of '
                            'VoltmeterRange IntEnum')
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0])))
    elif action == CardEmuSeqAction.TSCN_DO_TRIGGER_OUT_RX_ON or \
            action == CardEmuSeqAction.TSCN_DO_TRIGGER_OUT_EMD_GENERATION:
        if len(args) != 1:
            raise TypeError(f'MPC_AddToScenarioPcd({action.name}) takes '
                            f'exactly three arguments ({len(args) + 2} given)')
        if not isinstance(args[0], int):
            raise TypeError('param1 must be an instance of int')
        _check_limits(c_uint32, args[0], 'param1')  # Trigger
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0]),  # Trigger
            c_uint32(0)))  # Rfu

    # Two parameters
    elif action == CardEmuSeqAction.TSCN_DO_CHANGE_FELICA_DUTY_CYCLE or \
            action == CardEmuSeqAction.TSCN_DO_VICINITY_COLLISION:
        if len(args) != 2:
            raise TypeError(f'MPC_AddToScenarioPcd({action.name}) takes '
                            f'exactly four arguments ({len(args) + 2} given)')
        if not isinstance(args[0], int):
            raise TypeError('param1 must be an instance of int')
        _check_limits(c_uint32, args[0], 'param1')
        if not isinstance(args[1], int):
            raise TypeError('param2 must be an instance of int')
        _check_limits(c_uint32, args[1], 'param2')
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0]),
            c_uint32(args[1])))
    elif action == CardEmuSeqAction.TSCN_DO_TRIGGER_OUT:
        if len(args) != 2:
            raise TypeError(f'MPC_AddToScenarioPcd({action.name}) takes '
                            f'exactly four arguments ({len(args) + 2} given)')
        if not isinstance(args[0], int):
            raise TypeError('param1 must be an instance of int')
        _check_limits(c_uint32, args[0], 'param1')  # Trigger
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0]),  # Trigger
            c_uint32(1) if args[1] else c_uint32(0)))  # State
    elif action == CardEmuSeqAction.TSCN_DO_CHANGE_VC_DATA_RATE:
        if len(args) != 2:
            raise TypeError(f'MPC_AddToScenarioPcd({action.name}) takes '
                            f'exactly four arguments ({len(args) + 2} given)')
        if not isinstance(args[0], VicinityDataRate):
            raise TypeError('param1 must be an instance of '
                            'VicinityDataRate IntEnum')
        if not isinstance(args[1], VicinitySubCarrier):
            raise TypeError('param2 must be an instance of '
                            'VicinitySubCarrier IntEnum')
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0]),  # DataRate
            c_uint32(args[1])))  # SubCarrierNumber
    elif action == CardEmuSeqAction.TSCN_DO_CHANGE_DATA_RATE:
        if len(args) != 2:
            raise TypeError(f'MPC_AddToScenarioPcd({action.name}) takes '
                            f'exactly four arguments ({len(args) + 2} given)')
        if not isinstance(args[0], DataRate):
            raise TypeError('param1 must be an instance of DataRate IntEnum')
        if not isinstance(args[1], DataRate):
            raise TypeError('param2 must be an instance of DataRate IntEnum')
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0]),  # PcdDataRate
            c_uint32(args[1])))  # PiccDataRate
    elif action == CardEmuSeqAction.TSCN_DO_START_RF_MEASURE:
        if len(args) != 2:
            raise TypeError(f'MPC_AddToScenarioPcd({action.name}) takes '
                            f'exactly four arguments ({len(args) + 2} given)')
        if not isinstance(args[0], NfcTrigger):
            raise TypeError('param1 must be an instance of '
                            'NfcTrigger IntEnum')
        if not isinstance(args[1], float) and not isinstance(args[1], int):
            raise TypeError('param2 must be an instance of float')
        delay_ns = round(args[1] * 1e9)
        _check_limits(c_int32, delay_ns, 'param2')
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0]),  # EventMode
            c_int32(delay_ns)))  # Delay_ns
    elif action == CardEmuSeqAction.TSCN_DO_COMPLETE_ANTICOLLISION:
        if len(args) != 2:
            raise TypeError(f'MPC_AddToScenarioPcd({action.name}) takes '
                            f'exactly four arguments ({len(args) + 2} given)')
        if not isinstance(args[1], int):
            raise TypeError('param2 must be an instance of int')
        _check_limits(c_uint32, args[1], 'param2')  # Sak
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(1) if args[0] else c_uint32(0),  # Option
            c_uint32(args[1])))  # Sak
    elif action == CardEmuSeqAction.TSCN_SET_LMA_CARD_EMULATION:
        if len(args) != 2:
            raise TypeError(f'MPC_AddToScenarioPcd({action.name}) takes '
                            f'exactly four arguments ({len(args) + 2} given)')
        if not isinstance(args[0], float) and not isinstance(args[0], int):
            raise TypeError('param1 must be an instance of float')
        low_mV = round(args[0] * 1e3)
        _check_limits(c_int32, low_mV, 'param1')
        if not isinstance(args[1], float) and not isinstance(args[1], int):
            raise TypeError('param2 must be an instance of float')
        high_mV = round(args[1] * 1e3)
        _check_limits(c_int32, high_mV, 'param2')
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_int32(low_mV),  # Low_mV
            c_int32(high_mV)))  # High_mV
    elif action == CardEmuSeqAction.TSCN_SET_PCD_MASK:
        if len(args) != 2:
            raise TypeError(f'MPC_AddToScenarioPcd({action.name}) takes '
                            f'exactly four arguments ({len(args) + 2} given)')
        if not isinstance(args[0], TechnologyType):
            raise TypeError('pcd_type must be an instance of '
                            'TechnologyType IntEnum')
        if not isinstance(args[1], bytes):
            raise TypeError('mask must be an instance of bytes')
        _check_limits(c_uint32, len(args[1]), 'mask')
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0]),  # PcdFrameType
            c_uint32(len(args[1])),  # MaskLength
            args[1]))  # pPcdMask

    # Three parameters
    elif action == CardEmuSeqAction.TSCN_DO_CE_TRIGGER:
        if len(args) != 3:
            raise TypeError(f'MPC_AddToScenarioPcd({action.name}) takes '
                            f'exactly five arguments ({len(args) + 2} given)')
        if not isinstance(args[0], int):
            raise TypeError('param1 must be an instance of int')
        _check_limits(c_uint32, args[0], 'param1')  # Trigger
        if not isinstance(args[1], NfcTrigger):
            raise TypeError('param2 must be an instance of '
                            'NfcTrigger IntEnum')
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0]),  # Trigger
            c_uint32(args[1]),  # Config
            c_uint32(1) if args[2] else c_uint32(0)))  # Value
    elif action == CardEmuSeqAction.TSCN_DO_SEQUENCE_ERROR:
        if len(args) != 3:
            raise TypeError(f'MPC_AddToScenarioPcd({action.name}) takes '
                            f'exactly five arguments ({len(args) + 2} given)')
        if not isinstance(args[0], int):
            raise TypeError('param1 must be an instance of int')
        _check_limits(c_uint32, args[0], 'param1')  # ByteNumber
        if not isinstance(args[1], int):
            raise TypeError('param2 must be an instance of int')
        _check_limits(c_uint32, args[1], 'param2')  # SequenceNumber
        if not isinstance(args[2], SequenceError):
            raise TypeError('param3 must be an instance of '
                            'SequenceError IntEnum')
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0]),  # ByteNumber
            c_uint32(args[1]),  # SequenceNumber
            c_uint32(args[2])))  # Sequence
    elif action == CardEmuSeqAction.TSCN_PARAM_NFC_ACTIVE_TIMINGS:
        if len(args) != 3:
            raise TypeError(f'MPC_AddToScenarioPcd({action.name}) takes '
                            f'exactly five arguments ({len(args) + 2} given)')
        if not isinstance(args[0], int):
            raise TypeError('param1 must be an instance of int')
        _check_limits(c_uint32, args[0], 'param1')  # Tadt
        if not isinstance(args[1], int):
            raise TypeError('param2 must be an instance of int')
        _check_limits(c_uint32, args[1], 'param2')  # Tarfg
        if not isinstance(args[2], int):
            raise TypeError('param3 must be an instance of int')
        _check_limits(c_uint32, args[2], 'param3')  # Toff
        warn("deprecated 'TSCN_PARAM_NFC_ACTIVE_TIMINGS' instruction",
             FutureWarning, 2)
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0]),  # Tadt
            c_uint32(args[1]),  # Tarfg
            c_uint32(args[2])))  # Toff
    elif action == CardEmuSeqAction.TSCN_DO_EXCHANGE_RAW_TYPEA:
        if len(args) != 3:
            raise TypeError(f'MPC_AddToScenarioPcd({action.name}) takes '
                            f'exactly five arguments ({len(args) + 2} given)')
        if not isinstance(args[1], str):
            raise TypeError('pcd_frame must be an instance of str')
        if not isinstance(args[2], str):
            raise TypeError('picc_frame must be an instance of str')
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(TechnologyType.TYPE_A),  # PcdFrameType
            c_uint32(1) if args[0] else c_uint32(0),  # Synchro
            args[1].encode('ascii'),  # pExpectedPcdFrame
            args[2].encode('ascii')))  # pPiccResponse
    elif action == CardEmuSeqAction.TSCN_DO_WAIT_VC_SEND_SOF_ONLY:
        if len(args) != 3:
            raise TypeError(f'MPC_AddToScenarioPcd({action.name}) takes '
                            f'exactly five arguments ({len(args) + 2} given)')
        if not isinstance(args[2], bytes):
            raise TypeError('vcd_frame must be an instance of bytes')
        _check_limits(c_uint32, len(args[2]), 'vcd_frame')
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(1) if args[0] else c_uint32(0),  # VcdCrc
            c_uint32(1) if args[1] else c_uint32(0),  # Synchro
            c_uint32(len(args[2])),  # VcdFrameLength
            args[2]))  # pExpectedVcdFrame

    # Two or three parameters
    elif action == CardEmuSeqAction.TSCN_DO_NEGATIVE_MODULATION:
        if len(args) < 2 or len(args) > 3:
            raise TypeError(f'MPC_AddToScenarioPcd({action.name}) takes '
                            f'four or five arguments ({len(args) + 2} given)')
        if not isinstance(args[1], int):
            raise TypeError('param2 must be an instance of int')
        _check_limits(c_uint32, args[1], 'param2')  # TimeBeforeTload_clk
        if len(args) > 2:
            if not isinstance(args[2], int):
                raise TypeError('param3 must be an instance of int')
            _check_limits(c_uint32, args[2], 'param3')  # TimeBeforeTload_clk2
            CTS3Exception._check_error(func_pointer(
                c_uint8(0),
                c_uint32(scenario_id),
                c_uint32(0x80000000 + action),
                c_uint32(1) if args[0] else c_uint32(0),  # OnOff
                c_uint32(args[1]),  # TimeBeforeTload_clk
                c_uint32(args[2])))  # TimeBeforeTload_clk2
        else:
            CTS3Exception._check_error(func_pointer(
                c_uint8(0),
                c_uint32(scenario_id),
                c_uint32(action),
                c_uint32(1) if args[0] else c_uint32(0),  # OnOff
                c_uint32(args[1])))  # TimeBeforeTload_clk

    # Four parameters
    elif action == CardEmuSeqAction.TSCN_PARAM_ACTIVE_TIMINGS:
        if len(args) != 4:
            raise TypeError(f'MPC_AddToScenarioPcd({action.name}) takes '
                            f'exactly six arguments ({len(args) + 2} given)')
        if not isinstance(args[0], int):
            raise TypeError('tadt must be an instance of int')
        _check_limits(c_uint32, args[0], 'tadt')
        if not isinstance(args[1], int):
            raise TypeError('tarfg must be an instance of int')
        _check_limits(c_uint32, args[1], 'tarfg')
        if not isinstance(args[2], int):
            raise TypeError('toff must be an instance of int')
        _check_limits(c_uint32, args[2], 'toff')
        if not isinstance(args[3], int):
            raise TypeError('tmute must be an instance of int')
        _check_limits(c_uint32, args[3], 'tmute')
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0]),  # Tadt
            c_uint32(args[1]),  # Tarfg
            c_uint32(args[2]),  # Toff
            c_uint32(args[3])))  # Tmute

    # Structure parameter
    elif action == CardEmuSeqAction.TSCN_DO_EMD:
        if len(args) != 2:
            raise TypeError(f'MPC_AddToScenarioPcd({action.name}) takes '
                            f'exactly four arguments ({len(args) + 2} given)')
        if not isinstance(args[0], int):
            raise TypeError('fdt must be an instance of int')
        _check_limits(c_uint32, args[0], 'fdt')  # FdtEmd
        if not isinstance(args[1], list):
            raise TypeError('emd must be an instance of S_emd list')
        emd = (_S_emd * (len(args[1]) + 1))()
        for i in range(len(args[1])):
            if not isinstance(args[1][i], S_emd):
                raise TypeError('emd must be an instance of S_emd list')
            emd[i] = _S_emd(c_uint16(args[1][i].number),
                            c_uint16(args[1][i].type.value))
        emd[len(args[1])] = _S_emd(c_uint16(0), c_uint16(0))
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0]),  # FdtEmd
            c_uint32(0),  # Rfu
            emd))  # pPattern

    elif action == CardEmuSeqAction.TSCN_DO_EXCHANGE:
        if len(args) != 4 and len(args) != 6:
            raise TypeError(f'MPC_AddToScenarioPcd({action.name}) takes '
                            f'six or eight arguments ({len(args) + 2} given)')
        if len(args) > 5:
            if not isinstance(args[2], TechnologyType):
                raise TypeError('pcd_type must be an instance of '
                                'TechnologyType IntEnum')
            if args[4] is None:
                pcd_length = 1000000  # PCD_FRAME_DONT_CARE
                pcd_data = bytes()
            else:
                if not isinstance(args[4], bytes):
                    raise TypeError('pcd_frame must be an instance of bytes')
                _check_limits(c_uint32, len(args[4]), 'pcd_frame')
                pcd_length = len(args[4])
                pcd_data = args[4]
            if args[5] is None:
                picc_length = 0
                picc_data = bytes()
            else:
                if not isinstance(args[5], bytes):
                    raise TypeError('picc_frame must be an instance of bytes')
                _check_limits(c_uint32, len(args[5]), 'picc_frame')
                picc_length = len(args[5])
                picc_data = args[5]
            CTS3Exception._check_error(func_pointer(
                c_uint8(0),
                c_uint32(scenario_id),
                c_uint32(action),
                c_uint32(2) if args[0] else c_uint32(1),  # PcdCrc
                c_uint32(2) if args[1] else c_uint32(1),  # PiccCrc
                c_uint32(args[2]),  # PcdFrameType
                c_uint32(1) if args[3] else c_uint32(0),  # Synchro
                c_uint32(pcd_length),  # PcdFrameLength
                pcd_data,  # pExpectedPcdFrame
                c_uint32(picc_length),  # PiccFrameLength
                picc_data,  # pPiccResponse
                ''.encode('ascii')))
        else:
            if not isinstance(args[1], TechnologyType):
                raise TypeError('pcd_type must be an instance of '
                                'TechnologyType IntEnum')
            if not isinstance(args[3], bytes):
                raise TypeError('picc_frame must be an instance of bytes')
            _check_limits(c_uint32, len(args[3]), 'picc_frame')
            CTS3Exception._check_error(func_pointer(
                c_uint8(0),
                c_uint32(scenario_id),
                c_uint32(action),
                c_uint32(1),  # PcdCrc
                c_uint32(2) if args[0] else c_uint32(1),  # PiccCrc
                c_uint32(args[1]),  # PcdFrameType
                c_uint32(1) if args[2] else c_uint32(0),  # Synchro
                c_uint32(0),  # PcdFrameLength
                bytes(),  # pExpectedPcdFrame
                c_uint32(len(args[3])),  # PiccFrameLength
                args[3],  # pPiccResponse
                ''.encode('ascii')))

    elif action == CardEmuSeqAction.TSCN_DO_EXCHANGE_ACTIVE_TARGET:
        if len(args) != 6:
            raise TypeError(f'MPC_AddToScenarioPcd({action.name}) takes '
                            f'exactly eight arguments ({len(args) + 2} given)')
        if not isinstance(args[2], TechnologyType):
            raise TypeError('pcd_type must be an instance of '
                            'TechnologyType IntEnum')
        if not isinstance(args[4], bytes):
            raise TypeError('pcd_frame must be an instance of bytes')
        _check_limits(c_uint32, len(args[4]), 'pcd_frame')
        if args[5] is None:
            CTS3Exception._check_error(func_pointer(
                c_uint8(0),
                c_uint32(scenario_id),
                c_uint32(action),
                c_uint32(2) if args[0] else c_uint32(1),  # PcdCrc
                c_uint32(2) if args[1] else c_uint32(1),  # PiccCrc
                c_uint32(args[2]),  # PcdFrameType
                c_uint32(1) if args[3] else c_uint32(0),  # Synchro
                c_uint32(len(args[4])),  # PcdFrameLength
                args[4],  # pExpectedPcdFrame
                c_uint32(1000010),  # PiccFrameLength
                bytes()))  # pPiccResponse
        else:
            if args[5] and not isinstance(args[5], bytes):
                raise TypeError('picc_frame must be an instance of bytes')
            _check_limits(c_uint32, len(args[5]), 'picc_frame')
            CTS3Exception._check_error(func_pointer(
                c_uint8(0),
                c_uint32(scenario_id),
                c_uint32(action),
                c_uint32(2) if args[0] else c_uint32(1),  # PcdCrc
                c_uint32(2) if args[1] else c_uint32(1),  # PiccCrc
                c_uint32(args[2]),  # PcdFrameType
                c_uint32(1) if args[3] else c_uint32(0),  # Synchro
                c_uint32(len(args[4])),  # PcdFrameLength
                args[4],  # pExpectedPcdFrame
                c_uint32(len(args[5])),  # PiccFrameLength
                args[5]))  # pPiccResponse

    elif action == CardEmuSeqAction.TSCN_DO_WAIT_VC_EOF_ONLY:
        if len(args) < 1 or len(args) > 2:
            raise TypeError(f'MPC_AddToScenarioPcd({action.name}) takes '
                            f'three or four arguments ({len(args) + 2} given)')
        if len(args) > 1:
            if not isinstance(args[1], bytes):
                raise TypeError('picc_frame must be an instance of bytes')
            _check_limits(c_uint32, len(args[1]), 'picc_frame')
            CTS3Exception._check_error(func_pointer(
                c_uint8(0),
                c_uint32(scenario_id),
                c_uint32(action),
                c_uint32(2) if args[0] else c_uint32(1),  # PiccCrc
                c_uint32(len(args[1])),  # PiccFrameLength
                args[1],  # pAnswer
                c_uint32(0)))  # pRfu
        else:
            CTS3Exception._check_error(func_pointer(
                c_uint8(0),
                c_uint32(scenario_id),
                c_uint32(action),
                c_uint32(2) if args[0] else c_uint32(1),  # PiccCrc
                c_uint32(0),  # PiccFrameLength
                bytes(),  # pAnswer
                c_uint32(0)))  # pRfu

    elif action == CardEmuSeqAction.TSCN_DO_WAIT_TYPEA106_SEND_BITS:
        if len(args) != 3 and len(args) != 5:
            raise TypeError(f'MPC_AddToScenarioPcd({action.name}) takes '
                            f'five or seven arguments ({len(args) + 2} given)')
        if len(args) > 4:
            if not isinstance(args[3], int):
                raise TypeError('picc_bits_number must be an instance of int')
            _check_limits(c_uint32, args[3], 'picc_bits_number')
            if args[3] > 8:
                raise OverflowError('picc_bits_number cannot be higher than 8')
            if not isinstance(args[4], bytes):
                raise TypeError('picc_frame must be an instance of bytes')
            if args[2] is None:
                CTS3Exception._check_error(func_pointer(
                    c_uint8(0),
                    c_uint32(scenario_id),
                    c_uint32(action),
                    c_uint32(1),  # PcdCrc
                    c_uint32(1) if args[1] else c_uint32(0),  # Synchro
                    c_uint32(1000000),  # PCD_FRAME_DONT_CARE
                    bytes(),  # pExpectedPcdFrame
                    c_uint32(args[3]),  # PiccFrameLength
                    args[4]))  # pPiccResponse
            else:
                if not isinstance(args[2], bytes):
                    raise TypeError('pcd_frame must be an instance of bytes')
                _check_limits(c_uint32, len(args[2]), 'pcd_frame')
                CTS3Exception._check_error(func_pointer(
                    c_uint8(0),
                    c_uint32(scenario_id),
                    c_uint32(action),
                    c_uint32(2) if args[0] else c_uint32(1),  # PcdCrc
                    c_uint32(1) if args[1] else c_uint32(0),  # Synchro
                    c_uint32(len(args[2])),  # PcdFrameLength
                    args[2],  # pExpectedPcdFrame
                    c_uint32(args[3]),  # PiccFrameLength
                    args[4]))  # pPiccResponse
        elif isinstance(args[1], int):
            _check_limits(c_uint32, args[1], 'picc_bits_number')
            if not isinstance(args[2], bytes):
                raise TypeError('picc_frame must be an instance of bytes')
            CTS3Exception._check_error(func_pointer(
                c_uint8(0),
                c_uint32(scenario_id),
                c_uint32(action),
                c_uint32(1),  # PcdCrc
                c_uint32(1) if args[0] else c_uint32(0),  # Synchro
                c_uint32(0),  # PcdFrameLength
                bytes(),  # pExpectedPcdFrame
                c_uint32(args[1]),  # PiccFrameLength
                args[2]))  # pPiccResponse
        else:
            if args[2] is None:
                CTS3Exception._check_error(func_pointer(
                    c_uint8(0),
                    c_uint32(scenario_id),
                    c_uint32(action),
                    c_uint32(1),  # PcdCrc
                    c_uint32(1) if args[1] else c_uint32(0),  # Synchro
                    c_uint32(1000000),  # PCD_FRAME_DONT_CARE
                    bytes(),  # pExpectedPcdFrame
                    c_uint32(0),  # PiccFrameLength
                    bytes()))  # pPiccResponse
            else:
                if not isinstance(args[2], bytes):
                    raise TypeError('pcd_frame must be an instance of bytes')
                _check_limits(c_uint32, len(args[2]), 'pcd_frame')
                CTS3Exception._check_error(func_pointer(
                    c_uint8(0),
                    c_uint32(scenario_id),
                    c_uint32(action),
                    c_uint32(2) if args[0] else c_uint32(1),  # PcdCrc
                    c_uint32(1) if args[1] else c_uint32(0),  # Synchro
                    c_uint32(len(args[2])),  # PcdFrameLength
                    args[2],  # pExpectedPcdFrame
                    c_uint32(0),  # PiccFrameLength
                    bytes()))  # pPiccResponse

    elif action == CardEmuSeqAction.TSCN_DO_EXCHANGE_EBF:
        if len(args) != 6 and len(args) != 10:
            raise TypeError(f'MPC_AddToScenarioPcd({action.name}) takes '
                            'eight or twelve arguments '
                            f'({len(args) + 2} given)')
        if len(args) > 9:
            if not isinstance(args[2], int):
                raise TypeError('pcd_picc_option must be an instance of int')
            _check_limits(c_uint32, args[2], 'pcd_picc_option')
            if not isinstance(args[3], int):
                raise TypeError('picc_pcd_option must be an instance of int')
            _check_limits(c_uint32, args[3], 'picc_pcd_option')
            if not isinstance(args[6], TechnologyType):
                raise TypeError('pcd_type must be an instance of '
                                'TechnologyType IntEnum')
            if args[8] is None:
                if args[9] is None:
                    CTS3Exception._check_error(func_pointer(
                        c_uint8(0),
                        c_uint32(scenario_id),
                        c_uint32(action),
                        c_uint32(1) if args[0] else c_uint32(0),  # PcdUseEBF
                        c_uint32(1) if args[1] else c_uint32(0),  # PiccUseEBF
                        c_uint32(args[2]),  # FrameOptionPcdToPicc
                        c_uint32(args[3]),  # FrameOptionPiccToPcd
                        c_uint32(2) if args[4] else c_uint32(1),  # PcdCrc
                        c_uint32(2) if args[5] else c_uint32(1),  # PiccCrc
                        c_uint32(args[6]),  # PcdFrameType
                        c_uint32(1) if args[7] else c_uint32(0),  # Synchro
                        c_uint32(1000000),  # PCD_FRAME_DONT_CARE
                        bytes(),  # pExpectedPcdFrame
                        c_uint32(0),  # PiccFrameLength
                        bytes()))  # pPiccResponse
                else:
                    if not isinstance(args[9], bytes):
                        raise TypeError('picc_frame must be an instance '
                                        'of bytes')
                    _check_limits(c_uint32, len(args[9]), 'picc_frame')
                    CTS3Exception._check_error(func_pointer(
                        c_uint8(0),
                        c_uint32(scenario_id),
                        c_uint32(action),
                        c_uint32(1) if args[0] else c_uint32(0),  # PcdUseEBF
                        c_uint32(1) if args[1] else c_uint32(0),  # PiccUseEBF
                        c_uint32(args[2]),  # FrameOptionPcdToPicc
                        c_uint32(args[3]),  # FrameOptionPiccToPcd
                        c_uint32(2) if args[4] else c_uint32(1),  # PcdCrc
                        c_uint32(2) if args[5] else c_uint32(1),  # PiccCrc
                        c_uint32(args[6]),  # PcdFrameType
                        c_uint32(1) if args[7] else c_uint32(0),  # Synchro
                        c_uint32(1000000),  # PCD_FRAME_DONT_CARE
                        bytes(),  # pExpectedPcdFrame
                        c_uint32(len(args[9])),  # PiccFrameLength
                        args[9]))  # pPiccResponse
            else:
                if not isinstance(args[8], bytes):
                    raise TypeError('pcd_frame must be an instance of bytes')
                _check_limits(c_uint32, len(args[8]), 'pcd_frame')
                if args[9] is None:
                    CTS3Exception._check_error(func_pointer(
                        c_uint8(0),
                        c_uint32(scenario_id),
                        c_uint32(action),
                        c_uint32(1) if args[0] else c_uint32(0),  # PcdUseEBF
                        c_uint32(1) if args[1] else c_uint32(0),  # PiccUseEBF
                        c_uint32(args[2]),  # FrameOptionPcdToPicc
                        c_uint32(args[3]),  # FrameOptionPiccToPcd
                        c_uint32(2) if args[4] else c_uint32(1),  # PcdCrc
                        c_uint32(2) if args[5] else c_uint32(1),  # PiccCrc
                        c_uint32(args[6]),  # PcdFrameType
                        c_uint32(1) if args[7] else c_uint32(0),  # Synchro
                        c_uint32(len(args[8])),  # PcdFrameLength
                        args[8],  # pExpectedPcdFrame
                        c_uint32(0),  # PiccFrameLength
                        bytes()))  # pPiccResponse
                else:
                    if not isinstance(args[9], bytes):
                        raise TypeError('picc_frame must be an instance '
                                        'of bytes')
                    _check_limits(c_uint32, len(args[9]), 'picc_frame')
                    CTS3Exception._check_error(func_pointer(
                        c_uint8(0),
                        c_uint32(scenario_id),
                        c_uint32(action),
                        c_uint32(1) if args[0] else c_uint32(0),  # PcdUseEBF
                        c_uint32(1) if args[1] else c_uint32(0),  # PiccUseEBF
                        c_uint32(args[2]),  # FrameOptionPcdToPicc
                        c_uint32(args[3]),  # FrameOptionPiccToPcd
                        c_uint32(2) if args[4] else c_uint32(1),  # PcdCrc
                        c_uint32(2) if args[5] else c_uint32(1),  # PiccCrc
                        c_uint32(args[6]),  # PcdFrameType
                        c_uint32(1) if args[7] else c_uint32(0),  # Synchro
                        c_uint32(len(args[8])),  # PcdFrameLength
                        args[8],  # pExpectedPcdFrame
                        c_uint32(len(args[9])),  # PiccFrameLength
                        args[9]))  # pPiccResponse
        else:
            if not isinstance(args[1], int):
                raise TypeError('picc_pcd_option must be an instance of int')
            if not isinstance(args[3], TechnologyType):
                raise TypeError('pcd_type must be an instance of '
                                'TechnologyType IntEnum')
            if not isinstance(args[5], bytes):
                raise TypeError('picc_frame must be an instance of bytes')
            _check_limits(c_uint32, len(args[5]), 'picc_frame')
            CTS3Exception._check_error(func_pointer(
                c_uint8(0),
                c_uint32(scenario_id),
                c_uint32(action),
                c_uint32(0),  # PcdUseEBF
                c_uint32(1) if args[1] else c_uint32(0),  # PiccUseEBF
                c_uint32(0),  # FrameOptionPcdToPicc
                c_uint32(args[1]),  # FrameOptionPiccToPcd
                c_uint32(1),  # PcdCrc
                c_uint32(2) if args[2] else c_uint32(1),  # PiccCrc
                c_uint32(args[3]),  # PcdFrameType
                c_uint32(1) if args[4] else c_uint32(0),  # Synchro
                c_uint32(0),  # PcdFrameLength
                bytes(),  # pExpectedPcdFrame
                c_uint32(len(args[5])),  # PiccFrameLength
                args[5]))  # pPiccResponse


def MPC_ExecuteScenarioPcd(scenario_id: int, timeout: float) -> None:
    """Runs a scenario instance

    Parameters
    ----------
    scenario_id : int
        Scenario instance identifier
    timeout : float
        Scenario timeout in s
    """
    _check_limits(c_uint32, scenario_id, 'scenario_id')
    timeout_ms = round(timeout * 1e3)
    _check_limits(c_uint32, timeout_ms, 'timeout')
    CTS3Exception._check_error(_MPuLib.MPC_ExecuteScenarioPcd(
        c_uint8(0),
        c_uint32(scenario_id),
        c_uint32(timeout_ms)))


def MPC_CloseScenarioPcd(scenario_id: int) -> None:
    """Closes a scenario instance

    Parameters
    ----------
    scenario_id : int
        Scenario instance identifier
    """
    _check_limits(c_uint32, scenario_id, 'scenario_id')
    CTS3Exception._check_error(_MPuLib.MPC_CloseScenarioPcd(
        c_uint8(0),
        c_uint32(scenario_id)))
