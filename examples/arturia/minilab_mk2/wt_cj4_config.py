# -*- coding: utf-8 -*-
"""
midi2sim configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MIDI controller:    Arturia MiniLab mkII
Aircraft:           Working Title Cessna Citation CJ4
SimConnect backend: MobiFlight-SimConnect
Preset file for MIDI controller: midi2sim.minilabmk2
"""

import math

from midi2sim import midi, simc
from midi2sim.utils import arturia
from midi2sim import config

# MIDI device for this configuration
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MIDI_PORTS_IN = ["Arturia MiniLab mkII 0"]

# Some basics  for making life easier
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Knobs section
# ----------------

# Main encoder mode to use for this configuration
# (Relative 1)
AMK2_KNOB_MODE = arturia.ENC_MODE_REL_1

# Knobs 1 and 9 are special, not only can they turn,
# they also can be pushed and can be configured to send
# different MIDI signals with the SHIFT key pressed and held

# CCs sent by knobs 1 and 9 (shift)
AMK2_KNOB_01_SHIFT = midi.CC_041
AMK2_KNOB_09_SHIFT = midi.CC_042

# Notes assigned to knobs 1 and 9 when pressed
AMK2_KNOB_01_SWITCH = midi.NOTE_113
AMK2_KNOB_09_SWITCH = midi.NOTE_115

# CCs for all other knobs
AMK2_KNOB_01 = midi.CC_021
AMK2_KNOB_02 = midi.CC_022
AMK2_KNOB_03 = midi.CC_023
AMK2_KNOB_04 = midi.CC_024
AMK2_KNOB_05 = midi.CC_025
AMK2_KNOB_06 = midi.CC_026
AMK2_KNOB_07 = midi.CC_027
AMK2_KNOB_08 = midi.CC_028
AMK2_KNOB_09 = midi.CC_029
AMK2_KNOB_10 = midi.CC_030
AMK2_KNOB_11 = midi.CC_031
AMK2_KNOB_12 = midi.CC_032
AMK2_KNOB_13 = midi.CC_033
AMK2_KNOB_14 = midi.CC_034
AMK2_KNOB_15 = midi.CC_035
AMK2_KNOB_16 = midi.CC_036

# MIDI notes for all drum pads
AMK2_PAD_01 = midi.NOTE_036
AMK2_PAD_02 = midi.NOTE_037
AMK2_PAD_03 = midi.NOTE_038
AMK2_PAD_04 = midi.NOTE_039
AMK2_PAD_05 = midi.NOTE_040
AMK2_PAD_06 = midi.NOTE_041
AMK2_PAD_07 = midi.NOTE_042
AMK2_PAD_08 = midi.NOTE_043
AMK2_PAD_09 = midi.NOTE_044
AMK2_PAD_10 = midi.NOTE_045
AMK2_PAD_11 = midi.NOTE_046
AMK2_PAD_12 = midi.NOTE_047
AMK2_PAD_13 = midi.NOTE_048
AMK2_PAD_14 = midi.NOTE_049
AMK2_PAD_15 = midi.NOTE_050
AMK2_PAD_16 = midi.NOTE_051

# SimVars and events used for this aircraft
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# source: https://github.com/MobiFlight/MobiFlight-WASM-Module/blob/main/src/Sources/Code/events.txt#L4641
# official docs about the Working title Cj4 here:
# https://www.workingtitle.aero/packages/cj4/guides/simvars
simevents = {
    "ap_toggle": "AP_MASTER",
    "ap_hdg_inc": "MobiFlight.WT_CJ4_AP_HDG_INC",
    "ap_hdg_dec": "MobiFlight.WT_CJ4_AP_HDG_DEC",
    "ap_hdg_sync": "MobiFlight.WT_CJ4_AP_HDG_SYNC",
    "ap_hdg_toggle": "MobiFlight.WT_CJ4_AP_HDG_PRESSED",
    "ap_alt_inc": "AP_ALT_VAR_INC",
    "ap_alt_dec": "AP_ALT_VAR_DEC",
    "ap_alt_toggle": "MobiFlight.WT_CJ4_AP_ALT_PRESSED",
    "ap_vs_toggle": "MobiFlight.WT_CJ4_AP_VS_PRESSED",
    "ap_vs_inc": "MobiFlight.WT_CJ4_AP_VS_INC",
    "ap_vs_dec": "MobiFlight.WT_CJ4_AP_VS_DEC",
    "ap_flc_toggle": "MobiFlight.WT_CJ4_AP_FLC_PRESSED",
    "ap_flc_inc": "AP_SPD_VAR_INC",
    "ap_flc_dec": "AP_SPD_VAR_DEC",
    "yawdamper_toggle": "YAWDAMPER_TOGGLE",
    "ap_lnav_toggle": "MobiFlight.WT_CJ4_AP_NAV_PRESSED",
    "ap_vnav_toggle": "MobiFlight.WT_CJ4_AP_LNAV_PRESSED",
    "ap_appr_toggle": "MobiFlight.WT_CJ4_AP_APPR_PRESSED",
    "lights_panel_inc": "MobiFlight.WT_CJ4_PANEL_LIGHTS_INC",
    "lights_panel_dec": "MobiFlight.WT_CJ4_PANEL_LIGHTS_DEC",
    "lights_cabin_inc": "MobiFlight.WT_CJ4_CABIN1_LIGHT_INC",
    "lights_cabin_dec": "MobiFlight.WT_CJ4_CABIN1_LIGHT_DEC",
    "lights_flood_inc": "MobiFlight.WT_CJ4_FLOOD_LIGHT_INC",
    "lights_flood_dec": "MobiFlight.WT_CJ4_FLOOD_LIGHT_DEC",
    "lights_mfd1_inc": "MobiFlight.WT_CJ4_MFD1_LIGHT_INC",
    "lights_mfd1_dec": "MobiFlight.WT_CJ4_MFD1_LIGHT_DEC",
    "lights_mfd2_inc": "MobiFlight.WT_CJ4_MFD2_LIGHT_INC",
    "lights_mfd2_dec": "MobiFlight.WT_CJ4_MFD2_LIGHT_DEC",
    "lights_pfd1_inc": "MobiFlight.WT_CJ4_PFD1_LIGHT_INC",
    "lights_pfd1_dec": "MobiFlight.WT_CJ4_PFD1_LIGHT_DEC",
    "lights_pfd2_inc": "MobiFlight.WT_CJ4_PFD2_LIGHT_INC",
    "lights_pfd2_dec": "MobiFlight.WT_CJ4_PFD2_LIGHT_DEC",
    "baro1_inc": "MobiFlight.WT_CJ4_BARO1_INC",
    "baro1_dec": "MobiFlight.WT_CJ4_BARO1_DEC",
    "baro1_std_push": "MobiFlight.WT_CJ4_BARO1_STD_PUSH",
    "baro2_inc": "MobiFlight.WT_CJ4_BARO2_INC",
    "baro2_dec": "MobiFlight.WT_CJ4_BARO2_DEC",
    "baro2_std_push": "MobiFlight.WT_CJ4_BARO2_STD_PUSH",
    "baro3_inc": "MobiFlight.WT_CJ4_BARO3_INC",
    "baro3_dec": "MobiFlight.WT_CJ4_BARO3_DEC",
}
simvars = {"ap_master": "(A:AUTOPILOT MASTER,Bool)"}


# MIDI CC and NOTE handlers used on this aircraft
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def ap_hdg_incdec(m):
    """Heading bug (+/-)"""

    arturia.send_evt_on_encoder_rotation(
        m.value,
        evt_cw=simevents["ap_hdg_inc"],
        evt_ccw=simevents["ap_hdg_dec"],
        mode=AMK2_KNOB_MODE,
    )


def ap_hdg_set(m):
    """Heading bug set"""

    simc.send_event(simevents["ap_hdg_sync"])


def ap_hdg_toggle(m):
    """Heading mode toggle"""

    if m.on:
        simc.send_event(simevents["ap_hdg_toggle"])


def ap_alt_incdec(m):
    """AP Altitude bug (+/-)"""

    arturia.send_evt_on_encoder_rotation(
        m.value,
        evt_cw=simevents["ap_alt_inc"],
        evt_ccw=simevents["ap_alt_dec"],
        mode=AMK2_KNOB_MODE,
    )


def ap_alt_toggle(m):
    """Toggle ALT HOLD mode"""

    if m.on:
        simc.send_event(simevents["ap_alt_toggle"])


def ap_vs_toggle(m):
    """Toggle VS mode"""

    if m.on:
        simc.send_event(simevents["ap_vs_toggle"])


def ap_vs_incdec(m):
    """VS Mode knob (+/-)"""

    arturia.send_evt_on_encoder_rotation(
        m.value,
        mode=AMK2_KNOB_MODE,
        evt_cw=simevents["ap_vs_inc"],
        evt_ccw=simevents["ap_vs_dec"],
    )


def ap_flc_toggle(m):
    """Toggle flc mode"""

    if m.on:
        simc.send_event(simevents["ap_flc_toggle"])


def ap_flc_incdec(m):
    """flc Mode knob (+/-)"""

    arturia.send_evt_on_encoder_rotation(
        m.value,
        mode=AMK2_KNOB_MODE,
        evt_cw=simevents["ap_flc_inc"],
        evt_ccw=simevents["ap_flc_dec"],
    )


def ap_toggle(m):
    """Toggle autopilot"""

    if m.on:
        simc.send_event(simevents["ap_toggle"])


def yawdamper_toggle(m):
    """Toggle yaw damper"""

    if m.on:
        simc.send_event(simevents["yawdamper_toggle"])


def lights_panel_incdec(m):
    """Panel lights potentiometer"""

    arturia.send_evt_on_encoder_rotation(
        m.value,
        mode=AMK2_KNOB_MODE,
        evt_cw=simevents["lights_panel_inc"],
        evt_ccw=simevents["lights_panel_dec"],
    )


def lights_cabin_incdec(m):
    """Panel lights potentiometer"""

    arturia.send_evt_on_encoder_rotation(
        m.value,
        mode=AMK2_KNOB_MODE,
        evt_cw=simevents["lights_cabin_inc"],
        evt_ccw=simevents["lights_cabin_dec"],
    )


def lights_flood_incdec(m):
    """Flood lights potentiometer"""

    arturia.send_evt_on_encoder_rotation(
        m.value,
        mode=AMK2_KNOB_MODE,
        evt_cw=simevents["lights_flood_inc"],
        evt_ccw=simevents["lights_flood_dec"],
    )


def lights_displays_incdec(m):
    """Display lights potentiometer (MFD and PFD)"""

    light_events = [
        ("lights_mfd1_inc", "lights_mfd1_dec"),
        ("lights_mfd2_inc", "lights_mfd2_dec"),
        ("lights_pfd1_inc", "lights_pfd1_dec"),
        ("lights_pfd2_inc", "lights_pfd2_dec"),
    ]

    for event in light_events:
        arturia.send_evt_on_encoder_rotation(
            m.value,
            mode=AMK2_KNOB_MODE,
            evt_cw=simevents[event[0]],
            evt_ccw=simevents[event[1]],
        )


def ap_lnav_toggle(m):
    """Toggle LNAV mode"""

    if m.on:
        simc.send_event(simevents["ap_lnav_toggle"])


def ap_vnav_toggle(m):
    """Toggle VNAV mode"""

    if m.on:
        simc.send_event(simevents["ap_vnav_toggle"])


def ap_appr_toggle(m):
    """Toggle APPROACH mode"""

    if m.on:
        simc.send_event(simevents["ap_appr_toggle"])


def baro1_std_push(m):
    """Barometer 1 push (set to STD)"""

    if m.on:
        simc.send_event(simevents["baro1_std_push"])


def baro2_std_push(m):
    if m.on:
        simc.send_event(simevents["baro2_std_push"])


def baro1_incdec(m):
    """Barometer 1 knob (+/-)"""

    arturia.send_evt_on_encoder_rotation(
        m.value,
        mode=AMK2_KNOB_MODE,
        evt_cw=simevents["baro1_inc"],
        evt_ccw=simevents["baro1_dec"],
    )


def baro2_incdec(m):
    """Barometer 2 knob (+/-)"""

    arturia.send_evt_on_encoder_rotation(
        m.value,
        mode=AMK2_KNOB_MODE,
        evt_cw=simevents["baro2_inc"],
        evt_ccw=simevents["baro2_dec"],
    )


def baro3_incdec(m):
    """Barometer 3 knob (+/-)"""

    arturia.send_evt_on_encoder_rotation(
        m.value,
        mode=AMK2_KNOB_MODE,
        evt_cw=simevents["baro3_inc"],
        evt_ccw=simevents["baro3_dec"],
    )


def on_ap_master_change(v):
    """Example SimVar change handler"""

    ap_on = bool(math.floor(v.value))


# Proceed to start up the engines
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
config.setup(
    simconnect_backend=simc.SIMCONNECT_BACKEND_MOBIFLIGHT,
    simconnect_var_subs=[(simvars["ap_master"], on_ap_master_change)],
    midi_input_ports=MIDI_PORTS_IN,
    midi_cc_handlers=[
        # AP Panel handlers
        # ----------------------
        # Barometers
        (AMK2_KNOB_01, baro1_incdec),  # PFD barometer
        (AMK2_KNOB_02, baro3_incdec),  # secondary barometer
        # ALT
        (AMK2_KNOB_14, ap_alt_incdec),  # AP ALT inc/dec
        # FLC
        (AMK2_KNOB_13, ap_flc_incdec),  #
        # VS
        (AMK2_KNOB_12, ap_vs_incdec),  # AP VS increment/decrement
        # HDG
        (AMK2_KNOB_09, ap_hdg_incdec),  # AP VS increment/decrement
        # Lights section
        # ----------------------
        # Master lights
        (AMK2_KNOB_08, lights_panel_incdec),  # Lights (panel)
        (AMK2_KNOB_07, lights_cabin_incdec),  # Lights (cabin)
        (AMK2_KNOB_06, lights_flood_incdec),  # Lights (flood lights)
        (AMK2_KNOB_05, lights_displays_incdec),  # Lights (PFD and MFD)
    ],
    midi_note_handlers=[
        # PFD section
        # ----------------------
        # Barometers
        (AMK2_KNOB_01_SWITCH, baro1_std_push),  # Barometer 1 STD switch
        # AP Panel handlers
        # ----------------------
        (AMK2_PAD_08, ap_toggle),  # AP master switch
        (AMK2_PAD_07, yawdamper_toggle),  # Yaw damper toggle
        # ALT
        (AMK2_PAD_06, ap_alt_toggle),  # AP ALT toggle
        # FLC
        (AMK2_PAD_05, ap_flc_toggle),
        # VS
        (AMK2_PAD_04, ap_vs_toggle),  # AP VS toggle
        # HDG
        (AMK2_PAD_01, ap_hdg_toggle),  # AP heading mode toggle
        (AMK2_KNOB_09_SWITCH, ap_hdg_set),  # AP heading mode toggle
        # Navigation
        (AMK2_PAD_09, ap_lnav_toggle),  # LNAV
        (AMK2_PAD_10, ap_vnav_toggle),  # VNAV
        (AMK2_PAD_11, ap_appr_toggle),  # Approach mode
    ],
)
