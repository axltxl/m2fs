# -*- coding: utf-8 -*-
"""
m2fs configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MIDI controller:    Behringer X-Touch Mini
Aircraft:           Cessna Citation CJ4 (AAU1)
SimConnect backend: MobiFlight-SimConnect
Preset file for MIDI controller: m2fs.minilabmk2
"""

import math

from m2fs import midi, simc

from m2fs.utils import behringer
from m2fs import config

# MIDI device for this configuration
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MIDI_PORTS_IN = ["X-TOUCH MINI 0"]  # TODO: change me
MIDI_PORT_CHANNEL = 10  # 0-based, so actually 11
MIDI_PORT_OUT = "X-TOUCH MINI 1"  # FIXME

# Some basics  for making life easier
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Knobs section
# ----------------

# Layer A
# -------

# knobs
KNOB_A_01 = midi.CC_001
KNOB_A_02 = midi.CC_002
KNOB_A_03 = midi.CC_003
KNOB_A_04 = midi.CC_004
KNOB_A_05 = midi.CC_005
KNOB_A_06 = midi.CC_006
KNOB_A_07 = midi.CC_007
KNOB_A_08 = midi.CC_008

# knob buttons
KNOB_A_BT01 = midi.NOTE_000
KNOB_A_BT02 = midi.NOTE_001
KNOB_A_BT03 = midi.NOTE_002
KNOB_A_BT04 = midi.NOTE_003
KNOB_A_BT05 = midi.NOTE_004
KNOB_A_BT06 = midi.NOTE_005
KNOB_A_BT07 = midi.NOTE_006
KNOB_A_BT08 = midi.NOTE_007

# Buttons panel
BT_A_01 = midi.NOTE_008
BT_A_02 = midi.NOTE_009
BT_A_03 = midi.NOTE_010
BT_A_04 = midi.NOTE_011
BT_A_05 = midi.NOTE_012
BT_A_06 = midi.NOTE_013
BT_A_07 = midi.NOTE_014
BT_A_08 = midi.NOTE_015
BT_A_09 = midi.NOTE_016
BT_A_10 = midi.NOTE_017
BT_A_11 = midi.NOTE_018
BT_A_12 = midi.NOTE_019
BT_A_13 = midi.NOTE_020
BT_A_14 = midi.NOTE_021
BT_A_15 = midi.NOTE_022
BT_A_16 = midi.NOTE_023

# Layer B
# -------

# knobs
KNOB_B_01 = midi.CC_011
KNOB_B_02 = midi.CC_012
KNOB_B_03 = midi.CC_013
KNOB_B_04 = midi.CC_014
KNOB_B_05 = midi.CC_015
KNOB_B_06 = midi.CC_016
KNOB_B_07 = midi.CC_017
KNOB_B_08 = midi.CC_018

# knob buttons (when pressed down)
KNOB_B_BT01 = midi.CC_031
KNOB_B_BT02 = midi.CC_032
KNOB_B_BT03 = midi.CC_033
KNOB_B_BT04 = midi.CC_034
KNOB_B_BT05 = midi.CC_035
KNOB_B_BT06 = midi.CC_036
KNOB_B_BT07 = midi.CC_037
KNOB_B_BT08 = midi.CC_038

# Buttons panel
BT_B_01 = midi.NOTE_032
BT_B_02 = midi.NOTE_033
BT_B_03 = midi.NOTE_034
BT_B_04 = midi.NOTE_035
BT_B_05 = midi.NOTE_036
BT_B_06 = midi.NOTE_037
BT_B_07 = midi.NOTE_038
BT_B_08 = midi.NOTE_039
BT_B_09 = midi.NOTE_040
BT_B_10 = midi.NOTE_041
BT_B_11 = midi.NOTE_042
BT_B_12 = midi.NOTE_043
BT_B_13 = midi.NOTE_044
BT_B_14 = midi.NOTE_045
BT_B_15 = midi.NOTE_046
BT_B_16 = midi.NOTE_047

#############################
# Easy logical bindings
# so I don't have to hardcode
# CCs/notes into config.setup
#############################
# Master button for hot reload (Layer B)
CONFIG_RELOAD_BT = BT_B_16

# Main knob mode (I have chosen Relative 1 for all of my knobs)
KNOB_MODE = behringer.ENC_MODE_REL_1

# Autopilot master
AP_MASTER_BT = BT_A_13

# Heading bug (HDG)
AP_HDG_INCDEC_KNOB = KNOB_A_05
AP_HDG_SYNC_BT = KNOB_A_BT05
AP_HDG_MODE_BT = BT_A_05  # heading mode (AP)

# Barometer bug (BARO)
BARO_INCDEC_KNOB = KNOB_A_01
BARO_STD_BT = KNOB_A_BT01


# SimVars and events used for this aircraft
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# source: https://github.com/MobiFlight/MobiFlight-WASM-Module/blob/main/src/Sources/Code/events.txt#L4641
# official docs about the Working title Cj4 here:
# https://www.workingtitle.aero/packages/cj4/guides/simvars
simevents = {
    "ap_toggle": "AP_MASTER",
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
    "baro1_inc": "KOHLSMAN_INC",
    "baro1_dec": "KOHLSMAN_DEC",
    "baro1_std_push": "BAROMETRIC_STD_PRESSURE",
}


# MIDI CC and NOTE handlers used on this aircraft
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def ap_hdg_incdec(m):
    """Heading bug (+/-)"""

    behringer.send_event_on_encoder_rotation(
        m.value,
        evt_cw="HEADING_BUG_INC",
        evt_ccw="HEADING_BUG_DEC",
        mode=KNOB_MODE,
    )


def ap_hdg_set(m):
    """Heading bug set"""

    hdg_radians = simc.get_variable("HEADING_INDICATOR").value
    hdg_degrees = int(math.degrees(hdg_radians))
    simc.send_event("HEADING_BUG_SET", hdg_degrees)


def ap_hdg_toggle(m):
    """Heading mode toggle"""

    if m.on:
        simc.send_event("AP_PANEL_HEADING_ON")
    else:
        simc.send_event("AP_PANEL_HEADING_OFF")


def ap_alt_incdec(m):
    """AP Altitude bug (+/-)"""

    pass
    # FIXME
    # arturia.send_evt_on_encoder_rotation(
    #     m.value,
    #     evt_cw=simevents["ap_alt_inc"],
    #     evt_ccw=simevents["ap_alt_dec"],
    #     mode=KNOB_MODE,
    # )


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

    pass
    # FIXME
    # arturia.send_evt_on_encoder_rotation(
    #     m.value,
    #     mode=KNOB_MODE,
    #     evt_cw=simevents["ap_vs_inc"],
    #     evt_ccw=simevents["ap_vs_dec"],
    # )


def ap_flc_toggle(m):
    """Toggle flc mode"""

    if m.on:
        simc.send_event(simevents["ap_flc_toggle"])


def ap_flc_incdec(m):
    """flc Mode knob (+/-)"""

    pass
    # FIXME
    # arturia.send_evt_on_encoder_rotation(
    #     m.value,
    #     mode=KNOB_MODE,
    #     evt_cw=simevents["ap_flc_inc"],
    #     evt_ccw=simevents["ap_flc_dec"],
    # )


def ap_toggle(m):
    """Toggle autopilot"""

    if m.on:
        simc.send_event("AUTOPILOT_ON")
    else:
        simc.send_event("AUTOPILOT_OFF")


def yawdamper_toggle(m):
    """Toggle yaw damper"""

    if m.on:
        simc.send_event(simevents["yawdamper_toggle"])


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
        simc.send_event("BAROMETRIC_STD_PRESSURE")


def baro1_incdec(m):
    """Barometer 1 knob (+/-)"""

    behringer.send_event_on_encoder_rotation(
        m.value,
        mode=KNOB_MODE,
        evt_cw="KOHLSMAN_INC",
        evt_ccw="KOHLSMAN_DEC",
    )


def config_reload(m):
    """Hot configuration reload"""

    config.reload()


# Proceed to start up the engines
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
config.setup(
    simconnect_backend=simc.SIMCONNECT_BACKEND_DEFAULT,
    midi_input_ports=MIDI_PORTS_IN,
    midi_cc_handlers=[
        # AP Panel handlers
        # ----------------------
        # BARO
        (BARO_INCDEC_KNOB, baro1_incdec),  # PFD barometer
        # HDG
        (AP_HDG_INCDEC_KNOB, ap_hdg_incdec),  # HDG bug
    ],
    midi_note_handlers=[
        # FIXME
        # AP Panel handlers
        # ----------------------
        # AP master
        (AP_MASTER_BT, ap_toggle),
        # Barometers
        (BARO_STD_BT, baro1_std_push),  # Barometer 1 STD switch
        # HDG
        (AP_HDG_SYNC_BT, ap_hdg_set),
        (AP_HDG_MODE_BT, ap_hdg_toggle),  # AP HDG mode toggle
        # Reload config
        # ----------------------
        (CONFIG_RELOAD_BT, config_reload),
    ],
)
