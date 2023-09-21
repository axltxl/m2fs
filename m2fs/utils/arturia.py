# -*- coding: utf-8 -*-
"""
A dedicated module of utilities for using m2fs
on Arturia devices
"""

from ..utils import encoder

ENC_MODE_ABS = 0x0

ENC_MODE_ABS_MIN = 0x00
ENC_MODE_ABS_MAX = 0x7F

ENC_MODE_REL_1 = 0x1
ENC_MODE_REL_1_CW_MIN = 0x41  # 65
ENC_MODE_REL_1_CW_MAX = 0x43  # 67
ENC_MODE_REL_1_CW_RANGE = range(ENC_MODE_REL_1_CW_MIN, ENC_MODE_REL_1_CW_MAX + 1)

ENC_MODE_REL_1_CCW_MIN = 0x3D  # 61
ENC_MODE_REL_1_CCW_MAX = 0x3F  # 63
ENC_MODE_REL_1_CCW_RANGE = range(ENC_MODE_REL_1_CCW_MIN, ENC_MODE_REL_1_CCW_MAX + 1)

ENC_MODE_REL_2 = 0x2
ENC_MODE_REL_2_CW_MIN = 0x01  # 1
ENC_MODE_REL_2_CW_MAX = 0x03  # 3
ENC_MODE_REL_2_CW_RANGE = range(ENC_MODE_REL_1_CW_MIN, ENC_MODE_REL_1_CW_MAX + 1)

ENC_MODE_REL_2_CCW_MIN = 0x7D  # 125
ENC_MODE_REL_2_CCW_MAX = 0x7F  # 127
ENC_MODE_REL_2_CCW_RANGE = range(ENC_MODE_REL_1_CCW_MIN, ENC_MODE_REL_1_CCW_MAX + 1)

ENC_MODE_REL_3 = 0x3
ENC_MODE_REL_3_CW_MIN = 0x41  # 17
ENC_MODE_REL_3_CW_MAX = 0x43  # 19
ENC_MODE_REL_3_CW_RANGE = range(ENC_MODE_REL_1_CW_MIN, ENC_MODE_REL_1_CW_MAX + 1)

ENC_MODE_REL_3_CCW_MIN = 0x3D  # 13
ENC_MODE_REL_3_CCW_MAX = 0x3F  # 15
ENC_MODE_REL_3_CCW_RANGE = range(ENC_MODE_REL_1_CCW_MIN, ENC_MODE_REL_1_CCW_MAX + 1)


def get_encoder_rotation(cc_value: int, *, mode=ENC_MODE_REL_1):
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
        return encoder.get_rotation(
            cc_value, ENC_MODE_REL_1_CW_RANGE, ENC_MODE_REL_1_CCW_RANGE
        )
    if mode == ENC_MODE_REL_2:
        return encoder.get_rotation(
            cc_value, ENC_MODE_REL_2_CW_RANGE, ENC_MODE_REL_2_CCW_RANGE
        )
    if mode == ENC_MODE_REL_3:
        return encoder.get_rotation(
            cc_value, ENC_MODE_REL_3_CW_RANGE, ENC_MODE_REL_3_CCW_RANGE
        )

    return 0


def send_event_on_encoder_rotation(
    cc_value: int, *, evt_cw: int, evt_ccw: int, mode: int
):
    """Send event based on encoder rotation"""

    return encoder.send_event_on_rotation(
        get_encoder_rotation(cc_value, mode=mode), evt_cw=evt_cw, evt_ccw=evt_ccw
    )
