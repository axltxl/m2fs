# -*- coding: utf-8 -*-

import math
import midi
import flightsim
import arturia

# MIDI device for this configuration
MIDI_PORT = "Arturia MiniLab mkII 0"
ARTURIA_ENC_MODE = arturia.ENC_MODE_REL_1


def __send_evt_on_encoder_rotation(cc_value, evt_cw, evt_ccw):
    er = arturia.get_encoder_rotation(cc_value, mode=ARTURIA_ENC_MODE)
    if er > 0:
        flightsim.send_event(evt_cw)
    elif er < 0:
        flightsim.send_event(evt_ccw)


def __send_evt_on_note_toggle(note, evt_on, evt_off):
    if note.on:
        flightsim.send_event(evt_on)
    else:
        flightsim.send_event(evt_off)


def ap_hdg_incdec(m: midi.ControlChangeMessage) -> None:
    """Heading bug (+/-)"""

    __send_evt_on_encoder_rotation(m.value, "HEADING_BUG_INC", "HEADING_BUG_DEC")


def ap_hdg_set(m: midi.NoteMessage) -> None:
    """Heading bug set"""

    current_heading = int(
        math.degrees(flightsim.get_variable("HEADING_INDICATOR").value)
    )
    flightsim.send_event("HEADING_BUG_SET", current_heading)


def ap_hdg_mode_toggle(m: midi.NoteMessage) -> None:
    """Heading mode toggle"""

    flightsim.send_event("MobiFlight.WT_CJ4_AP_HDG_PRESSED")


def ap_alt_incdec(m: midi.ControlChangeMessage) -> None:
    """AP Altitude bug (+/-)"""

    __send_evt_on_encoder_rotation(m.value, "AP_ALT_VAR_INC", "AP_ALT_VAR_DEC")


def ap_vs_toggle(m: midi.NoteMessage):
    """Toggle VS mode"""

    flightsim.send_event("MobiFlight.WT_CJ4_AP_VS_PRESSED")


def ap_vs_incdec(m: midi.ControlChangeMessage) -> None:
    """VS Mode knob (+/-)"""

    __send_evt_on_encoder_rotation(
        m.value, "MobiFlight.WT_CJ4_AP_VS_INC", "MobiFlight.WT_CJ4_AP_VS_DEC"
    )


def ap_toggle(m: midi.NoteMessage):
    """Toggle autopilot"""

    __send_evt_on_note_toggle(m, "AUTOPILOT_ON", "AUTOPILOT_OFF")


def yawdamper_toggle(m: midi.NoteMessage) -> None:
    """Toggle yaw damper"""

    flightsim.send_event("YAW_DAMPER_TOGGLE")


def on_init() -> None:
    # CC handlers
    midi.subscribe_to_cc(cc=midi.CC_112, handler=ap_hdg_incdec)
    midi.subscribe_to_cc(cc=midi.CC_074, handler=ap_alt_incdec)
    midi.subscribe_to_cc(cc=midi.CC_018, handler=ap_vs_incdec)

    # Note handlers
    midi.subscribe_to_note(note=midi.NOTE_113, handler=ap_hdg_set)
    midi.subscribe_to_note(note=midi.NOTE_037, handler=ap_vs_toggle)
    midi.subscribe_to_note(note=midi.NOTE_042, handler=yawdamper_toggle)
    midi.subscribe_to_note(note=midi.NOTE_043, handler=ap_toggle)
    midi.subscribe_to_note(note=midi.NOTE_036, handler=ap_hdg_mode_toggle)
