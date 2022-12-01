# -*- coding: utf-8 -*-
"""
A dedicated module of utilities for using midi2sim
on an Arturia MiniLab mkII
"""

from ..simc import send_event as simc_send_evt

ENC_MODE_ABS = 0x0
ENC_MODE_REL_2 = 0x2
ENC_MODE_REL_3 = 0x3

ENC_MODE_ABS_MIN = 0x00
ENC_MODE_ABS_MAX = 0x7F

ENC_MODE_REL_1 = 0x1
ENC_MODE_REL_1_CW_MIN = 0x41  # 65
ENC_MODE_REL_1_CW_MAX = 0x43  # 67
ENC_MODE_REL_1_CW_RANGE = range(ENC_MODE_REL_1_CW_MIN, ENC_MODE_REL_1_CW_MAX + 1)

ENC_MODE_REL_1_CCW_MIN = 0x3D  # 61
ENC_MODE_REL_1_CCW_MAX = 0x3F  # 63
ENC_MODE_REL_1_CCW_RANGE = range(ENC_MODE_REL_1_CCW_MIN, ENC_MODE_REL_1_CCW_MAX + 1)

ENC_MODE_REL_2_CW_MIN = 0x01  # 1
ENC_MODE_REL_2_CW_MAX = 0x03  # 3
ENC_MODE_REL_2_CW_RANGE = range(ENC_MODE_REL_1_CW_MIN, ENC_MODE_REL_1_CW_MAX + 1)

ENC_MODE_REL_2_CCW_MIN = 0x7D  # 125
ENC_MODE_REL_2_CCW_MAX = 0x7F  # 127
ENC_MODE_REL_2_CCW_RANGE = range(ENC_MODE_REL_1_CCW_MIN, ENC_MODE_REL_1_CCW_MAX + 1)

ENC_MODE_REL_3_CW_MIN = 0x41  # 17
ENC_MODE_REL_3_CW_MAX = 0x43  # 19
ENC_MODE_REL_3_CW_RANGE = range(ENC_MODE_REL_1_CW_MIN, ENC_MODE_REL_1_CW_MAX + 1)

ENC_MODE_REL_3_CCW_MIN = 0x3D  # 13
ENC_MODE_REL_3_CCW_MAX = 0x3F  # 15
ENC_MODE_REL_3_CCW_RANGE = range(ENC_MODE_REL_1_CCW_MIN, ENC_MODE_REL_1_CCW_MAX + 1)


def __get_rotation(value, range_cw, range_ccw):
    if value in range_cw:
        return range_cw.stop - value + 1
    elif value in range_ccw:
        return -(range_ccw.stop - value + 1)
    return 0


def get_encoder_rotation(value: int, *, mode=ENC_MODE_REL_1):
    """
    In encoders with relative modes set to 1, 2 or 3,
    this will tell you whether they're being rotated and in
    which direction.

    For a CC value assigned on an encoder, it returns a
    negative number if it's being rotated counter-clockwise,
    a positive number if it's being rotated clockwise and
    zero (0) if it's not being rotated at all.
    """

    if mode == ENC_MODE_REL_1:
        return __get_rotation(value, ENC_MODE_REL_1_CW_RANGE, ENC_MODE_REL_1_CCW_RANGE)
    if mode == ENC_MODE_REL_2:
        return __get_rotation(value, ENC_MODE_REL_2_CW_RANGE, ENC_MODE_REL_2_CCW_RANGE)
    if mode == ENC_MODE_REL_3:
        return __get_rotation(value, ENC_MODE_REL_3_CW_RANGE, ENC_MODE_REL_3_CCW_RANGE)

    return 0


def __send_evt(e):
    if isinstance(e, tuple):
        simc_send_evt(*e)
    else:
        simc_send_evt(e)


def send_evt_on_encoder_rotation(cc_value, *, evt_cw, evt_ccw, mode):
    """
    Send event based on encoder rotation

    On relative modes, this function will detect whether your Arturia
    MIDI controller is doing a clockwise or a counter-clockwise rotation.
    In each case, it'll send a SimEvent of your choice.
    """

    er = get_encoder_rotation(cc_value, mode=mode)
    if er > 0:
        __send_evt(evt_cw)
    elif er < 0:
        __send_evt(evt_ccw)


def send_evt_on_note_toggle(note, *, evt_on, evt_off):
    """
    Send event based on whether a note has been set on or off
    """

    if note.on:
        __send_evt(evt_on)
    else:
        __send_evt(evt_off)
