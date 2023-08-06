from enum import IntEnum, unique
from ctypes import c_uint8, c_int32, c_uint32, byref
from typing import Union, Optional, overload
from warnings import warn
from . import _MPuLib, _MPuLib_variadic, _check_limits
from .Measurement import VoltmeterRange
from .Nfc import TechnologyType, NfcTriggerId, NfcTrigger, DataRate
from .Nfc import VicinityCodingMode, VicinityDataRate, VicinitySubCarrier
from .MPException import CTS3Exception


def MPC_OpenScenarioPicc() -> int:
    """Opens a scenario instance

    Returns
    -------
    int
        Scenario instance identifier
    """
    scenario_id = c_uint32()
    CTS3Exception._check_error(_MPuLib.MPC_OpenScenarioPicc(
        c_uint8(0),
        byref(scenario_id),
        c_uint32(0),
        c_uint32(0)))
    return scenario_id.value


@unique
class TermEmuSeqAction(IntEnum):
    """Terminal emulation sequencer actions"""
    TSCN_PARAM_CARD_TYPE = 1
    TSCN_PARAM_SOF_LOW = 2
    TSCN_PARAM_SOF_HIGH = 3
    TSCN_PARAM_EGT = 4
    TSCN_PARAM_EOF = 5
    TSCN_PARAM_START_BIT = 6
    TSCN_PARAM_B1 = 7
    TSCN_PARAM_B2 = 8
    TSCN_PARAM_B3 = 9
    TSCN_PARAM_B4 = 10
    TSCN_PARAM_B5 = 11
    TSCN_PARAM_B6 = 12
    TSCN_PARAM_B7 = 13
    TSCN_PARAM_B8 = 14
    TSCN_PARAM_STOP_BIT = 15
    TSCN_PARAM_PAUSE_WIDTH = 16
    TSCN_PARAM_FWT = 17
    TSCN_PARAM_FDT_PCD = 18
    TSCN_DO_TEMPO = 19
    TSCN_DO_RF_FIELD_STRENGTH = 20
    TSCN_DO_RF_RESET = 21
    TSCN_DO_EXCHANGE = 22
    TSCN_DO_PARITY_ERROR = 23
    TSCN_DO_CHANGE_DATA_RATE = 24
    TSCN_DO_USER_EVENT = 25
    TSCN_DO_TRIGGER_OUT = 26
    TSCN_DO_CHANGE_VC_COMMUNICATION = 35
    TSCN_PARAM_PAUSE_WIDTH_VICINITY = 36
    TSCN_DO_RF_RESET_CMD = 40
    TSCN_DO_TRIGGER_OUT_RX_ON = 41
    TSCN_PARAM_AUTOMATIC_SWTX_RESPONSE = 42
    TSCN_DO_TRIGGER = 43
    TSCN_DO_TON_EXCHANGE_AFTER_DELAY_TOFF = 54
    TSCN_DO_TX_PARITY = 55
    TSCN_PARAM_MODULATION_ASK_PT = 56
    TSCN_DO_EOF_VICINITY = 59
    TSCN_DO_RF_FIELD_STRENGTH_PER_MILLE = 60
    TSCN_DO_ANTICOLL_CLN = 61
    TSCN_DO_REQUESTB_ATTRIB = 62
    TSCN_DO_SEND_SELECT_CLN = 63
    TSCN_DO_REQUESTB_HALTB = 64
    TSCN_DO_MODE_NO_EOF = 66
    TSCN_DO_START_RF_MEASURE = 67
    TSCN_DO_SEND_TWO_FRAMES = 68
    TSCN_DO_SELECT_VOLTMETER_RANGE = 69
    TSCN_DO_EMV_POLLING = 71
    TSCN_DO_SEND_RAW_A106_FRAME = 72
    TSCN_PARAM_AUTOMATIC_RTOX_RESPONSE = 73
    TSCN_DO_REQUESTB_ATTRIB_FDT = 74
    TSCN_PARAM_NFC_ACTIVE_TIMINGS = 78
    TSCN_DO_EXCHANGE_ACTIVE_INITIATOR = 79
    TSCN_PARAM_ACTIVE_FDT_MODE = 80
    TSCN_DO_EXCHANGE_PATTERN = 81
    TSCN_PARAM_ACTIVE_TIMINGS = 82


@unique
class AutoSwtxMgt(IntEnum):
    """S(WTX) management"""
    AUTO_SWTX_DISABLED = 0
    AUTO_SWTX_NO_CID = 1
    AUTO_SWTX_CID = 2
    AUTO_SWTX_ENABLED = 3


@unique
class SequencerDataFlag(IntEnum):
    """Reception behavior"""
    EXCHANGE_WAIT_RX = 1
    EXCHANGE_NO_WAIT_RX = 2
    EXCHANGE_IGNORE_RX = 3
    EXCHANGE_ACTIVE_NO_FIELD = 4


@overload
def MPC_AddToScenarioPicc(scenario_id: int, action: TermEmuSeqAction,
                          param: Union[int, TechnologyType, VoltmeterRange,
                                       AutoSwtxMgt, float, bool,
                                       SequencerDataFlag]) -> None:
    # TSCN_PARAM_SOF_LOW, TSCN_PARAM_SOF_HIGH, TSCN_PARAM_EGT, TSCN_PARAM_EOF,
    # TSCN_PARAM_START_BIT, TSCN_PARAM_B1, TSCN_PARAM_B2, TSCN_PARAM_B3,
    # TSCN_PARAM_B4, TSCN_PARAM_B5, TSCN_PARAM_B6, TSCN_PARAM_B7,
    # TSCN_PARAM_B8, TSCN_PARAM_STOP_BIT, TSCN_DO_RF_FIELD_STRENGTH,
    # TSCN_DO_PARITY_ERROR, TSCN_DO_USER_EVENT, TSCN_DO_TRIGGER_OUT_RX_ON,
    # TSCN_PARAM_MODULATION_ASK_PT, TSCN_DO_RF_FIELD_STRENGTH_PER_MILLE,
    # TSCN_DO_ANTICOLL_CLN, TSCN_DO_SEND_SELECT_CLN,
    # TSCN_PARAM_CARD_TYPE,
    # TSCN_DO_SELECT_VOLTMETER_RANGE,
    # TSCN_PARAM_AUTOMATIC_SWTX_RESPONSE,
    # TSCN_PARAM_PAUSE_WIDTH, TSCN_PARAM_FWT, TSCN_PARAM_FDT_PCD,
    # TSCN_DO_TEMPO, TSCN_DO_RF_RESET, TSCN_PARAM_PAUSE_WIDTH_VICINITY,
    # TSCN_DO_TX_PARITY, TSCN_DO_MODE_NO_EOF,
    # TSCN_PARAM_AUTOMATIC_RTOX_RESPONSE, TSCN_PARAM_ACTIVE_FDT_MODE,
    # TSCN_DO_EOF_VICINITY
    ...


@overload
def MPC_AddToScenarioPicc(scenario_id: int, action: TermEmuSeqAction,
                          trigger: NfcTrigger, delay: float) -> None:
    # TSCN_DO_START_RF_MEASURE
    ...


@overload
def MPC_AddToScenarioPicc(scenario_id: int, action: TermEmuSeqAction,
                          pcd_datarate: DataRate,
                          picc_datarate: DataRate) -> None:
    # TSCN_DO_CHANGE_DATA_RATE
    ...


@overload
def MPC_AddToScenarioPicc(scenario_id: int, action: TermEmuSeqAction,
                          trigger: int, state: bool) -> None:
    # TSCN_DO_TRIGGER_OUT
    ...


@overload
def MPC_AddToScenarioPicc(scenario_id: int, action: TermEmuSeqAction,
                          coding_mode: VicinityCodingMode,
                          data_rate: VicinityDataRate,
                          sub_carrier: VicinitySubCarrier) -> None:
    # TSCN_DO_CHANGE_VC_COMMUNICATION
    ...


@overload
def MPC_AddToScenarioPicc(scenario_id: int, action: TermEmuSeqAction,
                          trigger: NfcTriggerId, config: NfcTrigger,
                          value: Union[bool, float]) -> None:
    # TSCN_DO_TRIGGER
    ...


@overload
def MPC_AddToScenarioPicc(scenario_id: int, action: TermEmuSeqAction,
                          tadt: int, tarfg: int, toff: int) -> None:
    # TSCN_PARAM_NFC_ACTIVE_TIMINGS
    ...


@overload
def MPC_AddToScenarioPicc(scenario_id: int, action: TermEmuSeqAction,
                          tadt: int, tarfg: int,
                          toff: int, tmute: int) -> None:
    # TSCN_PARAM_ACTIVE_TIMINGS
    ...


@overload
def MPC_AddToScenarioPicc(scenario_id: int, action: TermEmuSeqAction,
                          pcd_crc: bool, tx_bits: Optional[int],
                          tx_frame: bytes, wait: SequencerDataFlag) -> None:
    # TSCN_DO_EXCHANGE, TSCN_DO_EXCHANGE_ACTIVE_INITIATOR
    ...


@overload
def MPC_AddToScenarioPicc(scenario_id: int, action: TermEmuSeqAction,
                          pcd_crc: bool, tx_bits: Optional[int],
                          tx_frame: bytes, rx_pattern: bytes,
                          rx_mask: Optional[bytes] = None) -> None:
    # TSCN_DO_EXCHANGE_PATTERN
    ...


@overload
def MPC_AddToScenarioPicc(scenario_id: int, action: TermEmuSeqAction,
                          pcd_crc: bool, tx_bits: Optional[int],
                          tx_frame: bytes, wait: SequencerDataFlag,
                          timeout: float) -> None:
    # TSCN_DO_EXCHANGE, TSCN_DO_EXCHANGE_ACTIVE_INITIATOR
    ...


@overload
def MPC_AddToScenarioPicc(scenario_id: int, action: TermEmuSeqAction,
                          ask: int, time_1: float, time_2: float,
                          tx_bits: Optional[int], tx_frame: bytes) -> None:
    # TSCN_DO_RF_RESET_CMD
    ...


@overload
def MPC_AddToScenarioPicc(scenario_id: int, action: TermEmuSeqAction,
                          trigger: int, delay: float, pcd_crc: bool,
                          tx_bits: Optional[int], tx_frame: bytes,
                          wait: SequencerDataFlag) -> None:
    # TSCN_DO_TON_EXCHANGE_AFTER_DELAY_TOFF
    ...


@overload
def MPC_AddToScenarioPicc(scenario_id: int, action: TermEmuSeqAction,
                          trigger: int, delay: float, pcd_crc: bool,
                          tx_bits: Optional[int], tx_frame: bytes,
                          wait: SequencerDataFlag, timeout: float) -> None:
    # TSCN_DO_TON_EXCHANGE_AFTER_DELAY_TOFF
    ...


@overload
def MPC_AddToScenarioPicc(scenario_id: int, action: TermEmuSeqAction,
                          param: SequencerDataFlag, timeout: float) -> None:
    # TSCN_DO_EOF_VICINITY
    ...


@overload
def MPC_AddToScenarioPicc(scenario_id: int, action: TermEmuSeqAction,
                          request: bytes, attrib: bytes, fdt: float) -> None:
    # TSCN_DO_REQUESTB_ATTRIB_FDT
    ...


@overload
def MPC_AddToScenarioPicc(scenario_id: int, action: TermEmuSeqAction,
                          request: bytes, command: bytes) -> None:
    # TSCN_DO_REQUESTB_ATTRIB, TSCN_DO_REQUESTB_HALTB
    ...


@overload
def MPC_AddToScenarioPicc(scenario_id: int, action: TermEmuSeqAction,
                          pcd_crc_1: bool, tx_bits_1: Optional[int],
                          tx_frame_1: bytes, pcd_crc_2: bool,
                          tx_bits_2: Optional[int], tx_frame_2: bytes,
                          delay: int, wait: SequencerDataFlag) -> None:
    # TSCN_DO_SEND_TWO_FRAMES
    ...


@overload
def MPC_AddToScenarioPicc(scenario_id: int, action: TermEmuSeqAction,
                          pcd_crc_1: bool, tx_bits_1: Optional[int],
                          tx_frame_1: bytes, pcd_crc_2: bool,
                          tx_bits_2: Optional[int], tx_frame_2: bytes,
                          delay: int, wait: SequencerDataFlag,
                          timeout: float) -> None:
    # TSCN_DO_SEND_TWO_FRAMES
    ...


@overload
def MPC_AddToScenarioPicc(scenario_id: int, action: TermEmuSeqAction,
                          first_frame_delay: float, next_frames_delay: float,
                          type_odd: TechnologyType, tx_bits_odd: Optional[int],
                          tx_frame_odd: bytes, type_even: TechnologyType,
                          tx_bits_even: Optional[int], tx_frame_even: bytes,
                          timeout: float) -> None:
    # TSCN_DO_EMV_POLLING
    ...


@overload
def MPC_AddToScenarioPicc(scenario_id: int, action: TermEmuSeqAction,
                          tx_bits: int, tx_frame: bytes,
                          wait: SequencerDataFlag) -> None:
    # TSCN_DO_SEND_RAW_A106_FRAME
    ...


@overload
def MPC_AddToScenarioPicc(scenario_id: int, action: TermEmuSeqAction,
                          tx_bits: int, tx_frame: bytes,
                          wait: SequencerDataFlag, timeout: float) -> None:
    # TSCN_DO_SEND_RAW_A106_FRAME
    ...


def MPC_AddToScenarioPicc(scenario_id,  # type: ignore[no-untyped-def]
                          action, *args):
    """Adds an action to a scenario

    Parameters
    ----------
    scenario_id : int
        Scenario instance identifier
    action : TermEmuSeqAction
        Scenario action
    *args
        Scenario action parameters
    """
    _check_limits(c_uint32, scenario_id, 'scenario_id')
    if not isinstance(action, TermEmuSeqAction):
        raise TypeError('action must be an instance of '
                        'TermEmuSeqAction IntEnum')
    if _MPuLib_variadic is None:
        func_pointer = _MPuLib.MPC_AddToScenarioPicc
    else:
        func_pointer = _MPuLib_variadic.MPC_AddToScenarioPicc

    # One parameter
    if action == TermEmuSeqAction.TSCN_PARAM_SOF_LOW or \
            action == TermEmuSeqAction.TSCN_PARAM_SOF_HIGH or \
            action == TermEmuSeqAction.TSCN_PARAM_EGT or \
            action == TermEmuSeqAction.TSCN_PARAM_EOF or \
            action == TermEmuSeqAction.TSCN_PARAM_START_BIT or \
            action == TermEmuSeqAction.TSCN_PARAM_B1 or \
            action == TermEmuSeqAction.TSCN_PARAM_B2 or \
            action == TermEmuSeqAction.TSCN_PARAM_B3 or \
            action == TermEmuSeqAction.TSCN_PARAM_B4 or \
            action == TermEmuSeqAction.TSCN_PARAM_B5 or \
            action == TermEmuSeqAction.TSCN_PARAM_B6 or \
            action == TermEmuSeqAction.TSCN_PARAM_B7 or \
            action == TermEmuSeqAction.TSCN_PARAM_B8 or \
            action == TermEmuSeqAction.TSCN_PARAM_STOP_BIT or \
            action == TermEmuSeqAction.TSCN_DO_RF_FIELD_STRENGTH or \
            action == TermEmuSeqAction.TSCN_DO_RF_FIELD_STRENGTH_PER_MILLE or \
            action == TermEmuSeqAction.TSCN_DO_PARITY_ERROR or \
            action == TermEmuSeqAction.TSCN_PARAM_MODULATION_ASK_PT or \
            action == TermEmuSeqAction.TSCN_DO_ANTICOLL_CLN or \
            action == TermEmuSeqAction.TSCN_DO_SEND_SELECT_CLN or \
            action == TermEmuSeqAction.TSCN_DO_USER_EVENT:
        if len(args) != 1:
            raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                            f'exactly three arguments ({len(args) + 2} given)')
        if not isinstance(args[0], int):
            raise TypeError('param must be an instance of int')
        _check_limits(c_uint32, args[0], 'param')
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0])))
    elif action == TermEmuSeqAction.TSCN_PARAM_CARD_TYPE:
        if len(args) != 1:
            raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                            f'exactly three arguments ({len(args) + 2} given)')
        if not isinstance(args[0], TechnologyType):
            raise TypeError('param must be an instance of '
                            'TechnologyTypeype IntEnum')
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0])))
    elif action == TermEmuSeqAction.TSCN_DO_SELECT_VOLTMETER_RANGE:
        if len(args) != 1:
            raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                            f'exactly three arguments ({len(args) + 2} given)')
        if not isinstance(args[0], VoltmeterRange):
            raise TypeError('param must be an instance of '
                            'VoltmeterRange IntEnum')
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0])))
    elif action == TermEmuSeqAction.TSCN_PARAM_AUTOMATIC_SWTX_RESPONSE:
        if len(args) != 1:
            raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                            f'exactly three arguments ({len(args) + 2} given)')
        if not isinstance(args[0], AutoSwtxMgt):
            raise TypeError('param must be an instance of '
                            'AutoSwtxMgt IntEnum')
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0])))
    elif action == TermEmuSeqAction.TSCN_DO_TRIGGER_OUT_RX_ON:
        if len(args) != 1:
            raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                            f'exactly three arguments ({len(args) + 2} given)')
        if not isinstance(args[0], int):
            raise TypeError('param must be an instance of int')
        _check_limits(c_uint32, args[0], 'param')  # Trigger
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0]),  # Trigger
            c_uint32(0)))  # Rfu
    # µs
    elif action == TermEmuSeqAction.TSCN_PARAM_FWT or \
            action == TermEmuSeqAction.TSCN_DO_RF_RESET or \
            action == TermEmuSeqAction.TSCN_DO_TEMPO:
        if len(args) != 1:
            raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                            f'exactly three arguments ({len(args) + 2} given)')
        if not isinstance(args[0], float) and not isinstance(args[0], int):
            raise TypeError('param must be an instance of float')
        delay_us = round(args[0] * 1e6)
        _check_limits(c_uint32, delay_us, 'param')
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(delay_us)))
    # ns
    elif action == TermEmuSeqAction.TSCN_PARAM_PAUSE_WIDTH or \
            action == TermEmuSeqAction.TSCN_PARAM_PAUSE_WIDTH_VICINITY or \
            action == TermEmuSeqAction.TSCN_PARAM_FDT_PCD:
        if len(args) != 1:
            raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                            f'exactly three arguments ({len(args) + 2} given)')
        if not isinstance(args[0], float) and not isinstance(args[0], int):
            raise TypeError('param must be an instance of float')
        delay_ns = round(args[0] * 1e9)
        _check_limits(c_uint32, delay_ns, 'param')
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(delay_ns)))
    # boolean
    elif action == TermEmuSeqAction.TSCN_DO_TX_PARITY or \
            action == TermEmuSeqAction.TSCN_DO_MODE_NO_EOF or \
            action == TermEmuSeqAction.TSCN_PARAM_AUTOMATIC_RTOX_RESPONSE or \
            action == TermEmuSeqAction.TSCN_PARAM_ACTIVE_FDT_MODE:
        if len(args) != 1:
            raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                            f'exactly three arguments ({len(args) + 2} given)')
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(1) if args[0] else c_uint32(0)))

    # Two parameters
    elif action == TermEmuSeqAction.TSCN_DO_START_RF_MEASURE:
        if len(args) != 2:
            raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                            f'exactly four arguments ({len(args) + 2} given)')
        if not isinstance(args[0], NfcTrigger):
            raise TypeError('trigger must be an instance of '
                            'NfcTrigger IntEnum')
        if not isinstance(args[1], float) and not isinstance(args[1], int):
            raise TypeError('delay must be an instance of float')
        delay_ns = round(args[1] * 1e9)
        _check_limits(c_int32, delay_ns, 'delay')
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0]),  # EventMode
            c_int32(delay_ns)))  # Delay_ns
    elif action == TermEmuSeqAction.TSCN_DO_CHANGE_DATA_RATE:
        if len(args) != 2:
            raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                            f'exactly four arguments ({len(args) + 2} given)')
        if not isinstance(args[0], DataRate):
            raise TypeError('pcd_datarate must be an instance of '
                            'DataRate IntEnum')
        if not isinstance(args[1], DataRate):
            raise TypeError('picc_datarate must be an instance of '
                            'DataRate IntEnum')
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0]),  # PcdDataRate
            c_uint32(args[1])))  # PiccDataRate
    elif action == TermEmuSeqAction.TSCN_DO_TRIGGER_OUT:
        if len(args) != 2:
            raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                            f'exactly four arguments ({len(args) + 2} given)')
        if not isinstance(args[0], int):
            raise TypeError('trigger must be an instance of int')
        _check_limits(c_uint32, args[0], 'trigger')  # Trigger
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0]),  # Trigger
            c_uint32(1) if args[1] else c_uint32(1)))  # State
    elif action == TermEmuSeqAction.TSCN_DO_REQUESTB_ATTRIB or \
            action == TermEmuSeqAction.TSCN_DO_REQUESTB_HALTB:
        if len(args) != 2:
            raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                            f'exactly four arguments ({len(args) + 2} given)')
        if not isinstance(args[0], bytes):
            raise TypeError('request must be an instance of bytes')
        _check_limits(c_uint32, len(args[0]), 'request')
        if not isinstance(args[1], bytes):
            raise TypeError('command must be an instance of bytes')
        _check_limits(c_uint32, len(args[1]), 'command')
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(len(args[0])),  # NBytesRequest
            args[0],  # pRequest
            c_uint32(len(args[1])),  # NBytesATTRIB/NBytesHALTB
            args[1]))  # pATTRIB/pHALTB

    # Three parameters
    elif action == TermEmuSeqAction.TSCN_DO_CHANGE_VC_COMMUNICATION:
        if len(args) != 3:
            raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                            f'exactly five arguments ({len(args) + 2} given)')
        if not isinstance(args[0], VicinityCodingMode):
            raise TypeError('coding_mode must be an instance of '
                            'VicinityCodingMode IntEnum')
        if not isinstance(args[1], VicinityDataRate):
            raise TypeError('data_rate must be an instance of '
                            'VicinityDataRate IntEnum')
        if not isinstance(args[2], VicinitySubCarrier):
            raise TypeError('sub_carrier must be an instance of '
                            'VicinitySubCarrier IntEnum')
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0]),  # CodingMode
            c_uint32(args[1]),  # DataRateRx
            c_uint32(args[2])))  # NbSubCarrier
    elif action == TermEmuSeqAction.TSCN_DO_TRIGGER:
        if len(args) != 3:
            raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                            f'exactly five arguments ({len(args) + 2} given)')
        if not isinstance(args[0], NfcTriggerId):
            raise TypeError('trigger must be an instance of '
                            'NfcTriggerId Flag')
        if not isinstance(args[1], NfcTrigger):
            raise TypeError('config must be an instance of '
                            'NfcTrigger IntEnum')
        if args[1] == NfcTrigger.TRIG_FORCE:
            CTS3Exception._check_error(func_pointer(
                c_uint8(0),
                c_uint32(scenario_id),
                c_uint32(action),
                c_uint32(args[0]),  # Trigger
                c_uint32(args[1]),  # TRIG_FORCE
                c_uint32(1) if args[2] else c_uint32(0)))  # Value
        else:
            if not isinstance(args[2], float) and not isinstance(args[2], int):
                raise TypeError('value must be an instance of float')
            delay_ns = round(args[2] * 1e9)
            _check_limits(c_uint32, delay_ns, 'value')
            CTS3Exception._check_error(func_pointer(
                c_uint8(0),
                c_uint32(scenario_id),
                c_uint32(action),
                c_uint32(args[0]),  # Trigger
                c_uint32(args[1]),  # Config
                c_uint32(delay_ns)))  # Value
    elif action == TermEmuSeqAction.TSCN_PARAM_NFC_ACTIVE_TIMINGS:
        if len(args) != 3:
            raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                            f'exactly five arguments ({len(args) + 2} given)')
        if not isinstance(args[0], int):
            raise TypeError('tadt must be an instance of int')
        _check_limits(c_uint32, args[0], 'tadt')
        if not isinstance(args[1], int):
            raise TypeError('tarfg must be an instance of int')
        _check_limits(c_uint32, args[1], 'tarfg')
        if not isinstance(args[2], int):
            raise TypeError('toff must be an instance of int')
        _check_limits(c_uint32, args[2], 'toff')
        warn("deprecated 'TSCN_PARAM_NFC_ACTIVE_TIMINGS' instruction",
             FutureWarning, 2)
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0]),  # Tadt
            c_uint32(args[1]),  # Tarfg
            c_uint32(args[2])))  # Toff

    # Four parameters
    elif action == TermEmuSeqAction.TSCN_PARAM_ACTIVE_TIMINGS:
        if len(args) != 4:
            raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
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
            c_uint32(args[0]),  # NtrfwTadt
            c_uint32(args[1]),  # Tarfg
            c_uint32(args[2]),  # Toff
            c_uint32(args[3])))  # Tmute

    elif action == TermEmuSeqAction.TSCN_DO_REQUESTB_ATTRIB_FDT:
        if len(args) != 3:
            raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                            f'exactly five arguments ({len(args) + 2} given)')
        if not isinstance(args[0], bytes):
            raise TypeError('request must be an instance of bytes')
        _check_limits(c_uint32, len(args[0]), 'request')
        if not isinstance(args[1], bytes):
            raise TypeError('attrib must be an instance of bytes')
        _check_limits(c_uint32, len(args[1]), 'attrib')
        if not isinstance(args[2], float) and not isinstance(args[2], int):
            raise TypeError('fdt must be an instance of float')
        fdt_ns = round(args[2] * 1e9)
        _check_limits(c_uint32, fdt_ns, 'fdt')
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(len(args[0])),  # NBytesRequest
            args[0],  # pRequest
            c_uint32(len(args[1])),  # NBytesATTRIB
            args[1],  # pATTRIB
            c_uint32(fdt_ns)))  # Fdt_ns

    elif action == TermEmuSeqAction.TSCN_DO_EXCHANGE or \
            action == TermEmuSeqAction.TSCN_DO_EXCHANGE_ACTIVE_INITIATOR:
        if len(args) < 4:
            raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                            f'six or seven arguments ({len(args) + 2} given)')
        if args[2] and not isinstance(args[2], bytes):
            raise TypeError('tx_frame must be an instance of bytes')
        if args[1] is None:
            tx_bits = 0 if args[2] is None else 8 * len(args[2])
        elif not isinstance(args[1], int):
            raise TypeError('tx_bits must be an instance of int')
        else:
            tx_bits = args[1]
        _check_limits(c_uint32, tx_bits, 'tx_bits')
        if not isinstance(args[3], SequencerDataFlag):
            raise TypeError('wait must be an instance of '
                            'SequencerDataFlag IntEnum')
        if args[3] == SequencerDataFlag.EXCHANGE_WAIT_RX or \
                args[3] == SequencerDataFlag.EXCHANGE_ACTIVE_NO_FIELD:
            if len(args) != 4:
                raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                                'exactly six arguments '
                                f'({len(args) + 2} given)')
            CTS3Exception._check_error(func_pointer(
                c_uint8(0),
                c_uint32(scenario_id),
                c_uint32(action),
                c_uint32(2) if args[0] else c_uint32(1),  # PcdCrc
                c_uint32(tx_bits),  # BitsNumber
                args[2],  # pPcdFrame
                c_uint32(args[3])))  # EXCHANGE_WAIT_RX
        else:
            if len(args) != 5:
                raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                                'exactly seven arguments '
                                f'({len(args) + 2} given)')
            if not isinstance(args[4], float) and not isinstance(args[4], int):
                raise TypeError('timeout must be an instance of float')
            timeout_us = round(args[4] * 1e6)
            _check_limits(c_uint32, timeout_us, 'timeout')
            CTS3Exception._check_error(func_pointer(
                c_uint8(0),
                c_uint32(scenario_id),
                c_uint32(action),
                c_uint32(2) if args[0] else c_uint32(1),  # PcdCrc
                c_uint32(tx_bits),  # BitsNumber
                args[2],  # pPcdFrame
                c_uint32(args[3]),
                c_uint32(timeout_us)))  # RxTimeout_us

    elif action == TermEmuSeqAction.TSCN_DO_EXCHANGE_PATTERN:
        if len(args) != 4 and len(args) != 5:
            raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                            f'six or seven arguments ({len(args) + 2} given)')
        if args[2] and not isinstance(args[2], bytes):
            raise TypeError('tx_frame must be an instance of bytes')
        if args[1] is None:
            tx_bits = 0 if args[2] is None else 8 * len(args[2])
        elif not isinstance(args[1], int):
            raise TypeError('tx_bits must be an instance of int')
        else:
            tx_bits = args[1]
        _check_limits(c_uint32, tx_bits, 'tx_bits')
        if not isinstance(args[3], bytes):
            raise TypeError('rx_pattern must be an instance of bytes')
        _check_limits(c_uint32, len(args[3]), 'rx_pattern')
        if len(args) == 5:
            if args[4] is not None:
                if not isinstance(args[4], bytes):
                    raise TypeError('rx_mask must be an instance of bytes')
                mask = args[4]
            else:
                mask = b'\xFF' * len(args[3])
        else:
            mask = b'\xFF' * len(args[3])
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(2) if args[0] else c_uint32(1),  # PcdCrc
            c_uint32(tx_bits),  # BitsNumber
            args[2],  # pPcdFrame
            c_uint32(len(args[3])),  # RxPatternLength
            args[3],  # pRxPattern
            mask))

    elif action == TermEmuSeqAction.TSCN_DO_RF_RESET_CMD:
        if len(args) != 5:
            raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                            f'exactly seven arguments ({len(args) + 2} given)')
        if not isinstance(args[0], int):
            raise TypeError('ask must be an instance of int')
        _check_limits(c_uint32, args[0], 'ask')
        if not isinstance(args[1], float) and not isinstance(args[1], int):
            raise TypeError('time_1 must be an instance of float')
        time1_us = round(args[1] * 1e6)
        _check_limits(c_uint32, time1_us, 'time_1')
        if not isinstance(args[2], float) and not isinstance(args[2], int):
            raise TypeError('time_2 must be an instance of float')
        time2_us = round(args[2] * 1e6)
        _check_limits(c_uint32, time2_us, 'time_2')
        if not isinstance(args[4], bytes):
            raise TypeError('tx_frame must be an instance of bytes')
        if args[3] is None:
            tx_bits = 8 * len(args[4])
        elif not isinstance(args[3], int):
            raise TypeError('tx_bits must be an instance of int')
        else:
            tx_bits = args[3]
        _check_limits(c_uint32, tx_bits, 'tx_bits')
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(args[0]),  # Ask_pm
            c_uint32(time1_us),  # Time1_us
            c_uint32(time2_us),  # Time2_us
            c_uint32(tx_bits),  # TxBits
            args[4]))  # pTxFrame

    elif action == TermEmuSeqAction.TSCN_DO_TON_EXCHANGE_AFTER_DELAY_TOFF:
        if len(args) < 6:
            raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                            f'eight or nine arguments ({len(args) + 2} given)')
        if not isinstance(args[0], int):
            raise TypeError('trigger must be an instance of int')
        _check_limits(c_uint32, args[0], 'trigger')
        if not isinstance(args[1], float) and not isinstance(args[1], int):
            raise TypeError('delay must be an instance of float')
        delay_us = round(args[1] * 1e6)
        _check_limits(c_uint32, delay_us, 'delay')
        if not isinstance(args[4], bytes):
            raise TypeError('tx_frame must be an instance of bytes')
        if args[3] is None:
            tx_bits = 8 * len(args[4])
        elif not isinstance(args[3], int):
            raise TypeError('tx_bits must be an instance of int')
        else:
            tx_bits = args[3]
        _check_limits(c_uint32, tx_bits, 'tx_bits')
        if not isinstance(args[5], SequencerDataFlag):
            raise TypeError('wait must be an instance of '
                            'SequencerDataFlag IntEnum')
        if args[5] == SequencerDataFlag.EXCHANGE_WAIT_RX:
            if len(args) != 6:
                raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                                'exactly eight arguments '
                                f'({len(args) + 2} given)')
            CTS3Exception._check_error(func_pointer(
                c_uint8(0),
                c_uint32(scenario_id),
                c_uint32(action),
                c_uint32(args[0]),  # TrigNum
                c_uint32(delay_us),  # Delay_us
                c_uint32(2) if args[2] else c_uint32(1),  # PcdCrc
                c_uint32(tx_bits),  # BitsNumber
                args[4],  # pPcdFrame
                c_uint32(args[5])))  # EXCHANGE_WAIT_RX
        else:
            if len(args) != 7:
                raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                                'exactly nine arguments '
                                f'({len(args) + 2} given)')
            if not isinstance(args[6], float) and not isinstance(args[6], int):
                raise TypeError('timeout must be an instance of float')
            timeout_us = round(args[6] * 1e6)
            _check_limits(c_uint32, timeout_us, 'timeout')
            CTS3Exception._check_error(func_pointer(
                c_uint8(0),
                c_uint32(scenario_id),
                c_uint32(action),
                c_uint32(args[0]),  # TrigNum
                c_uint32(round(args[1] * 1e6)),  # Delay_us
                c_uint32(2) if args[2] else c_uint32(1),  # PcdCrc
                c_uint32(tx_bits),  # BitsNumber
                args[4],  # pPcdFrame
                c_uint32(args[5]),
                c_uint32(timeout_us)))  # RxTimeout_us

    elif action == TermEmuSeqAction.TSCN_DO_EOF_VICINITY:
        if len(args) < 1:
            raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                            f'three or four arguments ({len(args) + 2} given)')
        if not isinstance(args[0], SequencerDataFlag):
            raise TypeError('param must be an instance of '
                            'SequencerDataFlag IntEnum')
        if args[0] == SequencerDataFlag.EXCHANGE_WAIT_RX:
            if len(args) != 1:
                raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                                'exactly three arguments '
                                f'({len(args) + 2} given)')
            CTS3Exception._check_error(func_pointer(
                c_uint8(0),
                c_uint32(scenario_id),
                c_uint32(action),
                c_uint32(args[0])))  # EXCHANGE_WAIT_RX
        else:
            if len(args) != 2:
                raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                                'exactly four arguments '
                                f'({len(args) + 2} given)')
            if not isinstance(args[1], float) and not isinstance(args[1], int):
                raise TypeError('timeout must be an instance of float')
            timeout_us = round(args[1] * 1e6)
            _check_limits(c_uint32, timeout_us, 'timeout')
            CTS3Exception._check_error(func_pointer(
                c_uint8(0),
                c_uint32(scenario_id),
                c_uint32(action),
                c_uint32(args[0]),  # Wait
                c_uint32(timeout_us)))  # RxTimeout_us

    elif action == TermEmuSeqAction.TSCN_DO_SEND_TWO_FRAMES:
        if len(args) < 8:
            raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                            f'ten or eleven arguments ({len(args) + 2} given)')
        if not isinstance(args[2], bytes):
            raise TypeError('tx_frame_1 must be an instance of bytes')
        if args[1] is None:
            tx_frame_1 = 8 * len(args[2])
        elif not isinstance(args[1], int):
            raise TypeError('tx_bits_1 must be an instance of int')
        else:
            tx_frame_1 = args[1]
        _check_limits(c_uint32, tx_frame_1, 'tx_bits_1')
        if not isinstance(args[5], bytes):
            raise TypeError('tx_frame_2 must be an instance of bytes')
        if args[4] is None:
            tx_bits_2 = 8 * len(args[5])
        elif not isinstance(args[4], int):
            raise TypeError('tx_bits_2 must be an instance of int')
        else:
            tx_bits_2 = args[4]
        _check_limits(c_uint32, tx_bits_2, 'tx_bits_2')
        if not isinstance(args[6], int):
            raise TypeError('delay must be an instance of int')
        _check_limits(c_uint32, args[6], 'delay')
        if not isinstance(args[7], SequencerDataFlag):
            raise TypeError('wait must be an instance of '
                            'SequencerDataFlag IntEnum')
        if args[7] == SequencerDataFlag.EXCHANGE_WAIT_RX:
            if len(args) != 8:
                raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                                'exactly eleven arguments '
                                f'({len(args) + 2} given)')
            CTS3Exception._check_error(func_pointer(
                c_uint8(0),
                c_uint32(scenario_id),
                c_uint32(action),
                c_uint32(2) if args[0] else c_uint32(1),  # PcdCrc_f1
                c_uint32(tx_frame_1),  # BitsNumber_f1
                args[2],  # pPcdFrame_f1
                c_uint32(2) if args[3] else c_uint32(1),  # PcdCrc_f2
                c_uint32(tx_bits_2),  # BitsNumber_f2
                args[5],  # pPcdFrame_f2
                c_uint32(0),  # Rfu
                c_uint32(args[6]),  # Delay_clk
                c_uint32(args[7])))  # EXCHANGE_WAIT_RX
        else:
            if len(args) != 9:
                raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                                'exactly eleven arguments '
                                f'({len(args) + 2} given)')
            if not isinstance(args[8], float) and not isinstance(args[8], int):
                raise TypeError('timeout must be an instance of float')
            timeout_us = round(args[8] * 1e6)
            _check_limits(c_uint32, timeout_us, 'timeout')
            CTS3Exception._check_error(func_pointer(
                c_uint8(0),
                c_uint32(scenario_id),
                c_uint32(action),
                c_uint32(2) if args[0] else c_uint32(1),  # PcdCrc_f1
                c_uint32(tx_frame_1),  # BitsNumber_f1
                args[2],  # pPcdFrame_f1
                c_uint32(2) if args[3] else c_uint32(1),  # PcdCrc_f2
                c_uint32(tx_bits_2),  # BitsNumber_f2
                args[5],  # pPcdFrame_f2
                c_uint32(0),  # Rfu
                c_uint32(args[6]),  # Delay_clk
                c_uint32(args[7]),
                c_uint32(timeout_us)))  # RxTimeout_us

    elif action == TermEmuSeqAction.TSCN_DO_EMV_POLLING:
        if len(args) != 9:
            raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                            'exactly eleven arguments '
                            f'({len(args) + 2} given)')
        if not isinstance(args[0], float) and not isinstance(args[0], int):
            raise TypeError('first_frame_delay must be an instance of float')
        first_delay_us = round(args[0] * 1e6)
        _check_limits(c_uint32, first_delay_us, 'first_frame_delay')
        if not isinstance(args[1], float) and not isinstance(args[1], int):
            raise TypeError('next_frames_delay must be an instance of float')
        frames_delay_us = round(args[1] * 1e6)
        _check_limits(c_uint32, frames_delay_us, 'next_frames_delay')
        if not isinstance(args[2], TechnologyType):
            raise TypeError('type_odd must be an instance of '
                            'TechnologyType IntEnum')
        if not isinstance(args[4], bytes):
            raise TypeError('tx_frame_odd must be an instance of bytes')
        if args[3] is None:
            tx_bits_odd = 8 * len(args[4])
        elif not isinstance(args[3], int):
            raise TypeError('tx_bits_odd must be an instance of int')
        else:
            tx_bits_odd = args[3]
        _check_limits(c_uint32, tx_bits_odd, 'tx_bits_odd')
        if not isinstance(args[5], TechnologyType):
            raise TypeError('type_even must be an instance of '
                            'TechnologyType IntEnum')
        if not isinstance(args[7], bytes):
            raise TypeError('tx_frame_even must be an instance of bytes')
        if args[6] is None:
            tx_bits_even = 8 * len(args[7])
        elif not isinstance(args[6], int):
            raise TypeError('tx_bits_even must be an instance of int')
        else:
            tx_bits_even = args[6]
        _check_limits(c_uint32, tx_bits_even, 'tx_bits_even')
        if not isinstance(args[8], float) and not isinstance(args[8], int):
            raise TypeError('timeout must be an instance of float')
        timeout_ms = round(args[8] * 1e3)
        _check_limits(c_uint32, timeout_ms, 'timeout')
        CTS3Exception._check_error(func_pointer(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(action),
            c_uint32(first_delay_us),  # FirstFrameDelay_us
            c_uint32(frames_delay_us),  # NextFramesDelay_us
            c_uint32(args[2]),  # OddFramesType
            c_uint32(tx_bits_odd),  # OddFramesBitsNumber
            args[4],  # pPcdOddFrames
            c_uint32(args[5]),  # EvenFramesType
            c_uint32(tx_bits_even), args[7],  # EvenFramesBitsNumber
            c_uint32(timeout_ms)))  # Timeout_ms

    elif action == TermEmuSeqAction.TSCN_DO_SEND_RAW_A106_FRAME:
        if len(args) < 3:
            raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                            f'five or six arguments ({len(args) + 2} given)')
        if not isinstance(args[0], int):
            raise TypeError('tx_bits must be an instance of int')
        _check_limits(c_uint32, args[0], 'tx_bits')
        if not isinstance(args[1], bytes):
            raise TypeError('tx_frame must be an instance of bytes')
        if not isinstance(args[2], SequencerDataFlag):
            raise TypeError('wait must be an instance of '
                            'SequencerDataFlag IntEnum')
        if args[2] == SequencerDataFlag.EXCHANGE_WAIT_RX:
            if len(args) != 3:
                raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                                'exactly five arguments '
                                f'({len(args) + 2} given)')
            CTS3Exception._check_error(func_pointer(
                c_uint8(0),
                c_uint32(scenario_id),
                c_uint32(action),
                c_uint32(args[0]),  # BitsNumber
                args[1],  # pPcdFrame
                c_uint32(args[2])))  # EXCHANGE_WAIT_RX
        else:
            if len(args) != 4:
                raise TypeError(f'MPC_AddToScenarioPicc({action.name}) takes '
                                'exactly six arguments '
                                f'({len(args) + 2} given)')
            if not isinstance(args[3], float) and not isinstance(args[3], int):
                raise TypeError('timeout must be an instance of float')
            timeout_us = round(args[3] * 1e6)
            _check_limits(c_uint32, timeout_us, 'timeout')
            CTS3Exception._check_error(func_pointer(
                c_uint8(0),
                c_uint32(scenario_id),
                c_uint32(action),
                c_uint32(args[0]),  # BitsNumber
                args[1],  # pPcdFrame
                c_uint32(args[2]),
                c_uint32(timeout_us)))  # RxTimeout_us


def MPC_ExecuteScenarioPicc(scenario_id: int,
                            timeout: Optional[float]) -> None:
    """Runs a scenario instance

    Parameters
    ----------
    scenario_id : int
        Scenario instance identifier
    timeout : float
        Scenario timeout in s, or None to compile
        the scenario without executing it
    """
    _check_limits(c_uint32, scenario_id, 'scenario_id')
    if timeout:
        timeout_ms = round(timeout * 1e3)
        _check_limits(c_uint32, timeout_ms, 'timeout')
        CTS3Exception._check_error(_MPuLib.MPC_ExecuteScenarioPicc(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(timeout_ms)))
    else:
        CTS3Exception._check_error(_MPuLib.MPC_ExecuteScenarioPicc(
            c_uint8(0),
            c_uint32(scenario_id),
            c_uint32(0)))


def MPC_CloseScenarioPicc(scenario_id: int) -> None:
    """Closes a scenario instance

    Parameters
    ----------
    scenario_id : int
        Scenario instance identifier
    """
    _check_limits(c_uint32, scenario_id, 'scenario_id')
    CTS3Exception._check_error(_MPuLib.MPC_CloseScenarioPicc(
        c_uint8(0),
        c_uint32(scenario_id)))
