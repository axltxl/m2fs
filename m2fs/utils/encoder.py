# -*- coding: utf-8 -*-
"""
General MIDI encoder utilities
"""

from . import event

def get_rotation(
    value: int,
    range_cw: range,
    range_ccw: range,
):
    """
    For a CC value assigned on an encoder, it returns a
    negative number if it's being rotated counter-clockwise,
    a positive number if it's being rotated clockwise and
    zero (0) if it's not being rotated at all.
    """

    if value in range_cw:
        return 1
    elif value in range_ccw:
        return -1
    return 0


def send_event_on_rotation(
    er: int,  # encoder rotation value (must be something returned from a function like get_rotation)
    *,
    evt_cw: str,
    evt_ccw: str,
):
    """
    Send event based on encoder rotation

    On relative modes, this function will detect whether your
    MIDI controller is doing a clockwise or a counter-clockwise rotation.
    In each case, it'll send a SimEvent of your choice.
    """

    if er > 0:
        event.send(evt_cw)
    elif er < 0:
        event.send(evt_ccw)
