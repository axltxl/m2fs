# -*- coding: utf-8 -*-
"""
General MIDI note utilities
"""

from ..simc import send_event as simc_send_evt
from . import event

def send_evt_on_note_toggle(note, *, evt_on, evt_off):
    """
    Send event based on whether a note has been set on or off
    """

    if note.on:
        event.send(evt_on)
    else:
        event.send(evt_off)
