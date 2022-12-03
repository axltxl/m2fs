# -*- coding: utf-8 -*-
"""
Configuration file entrypoint: setup()
"""

from .midi import (
    subscribe_to_cc as midi_subscribe_to_cc,
    subscribe_to_note as midi_subscribe_to_note,
    subscribe_to_pitchwheel as midi_subscribe_to_pitchwheel,
    connect_input_port as midi_connect_input_port,
)
from .simc import (
    connect as simc_connect,
    subscribe_to_simvar as simc_subscribe_to_simvar,
)
from .simc import SIMCONNECT_BACKEND_DEFAULT


def ___batch_assign_cc_handlers(h_map: list[tuple[int, callable]]):
    for handle_pair in h_map:
        cc, handler = handle_pair
        midi_subscribe_to_cc(cc=cc, handler=handler)


def ___batch_assign_note_handlers(h_map: list[tuple[int, callable]]):
    for handle_pair in h_map:
        note, handler = handle_pair
        midi_subscribe_to_note(note=note, handler=handler)


def ___batch_subscribe_to_simvars(h_map: list[tuple[str, callable]]):
    for handle_pair in h_map:
        simvar, handler = handle_pair
        simc_subscribe_to_simvar(simvar, handler=handler)


def setup(
    *,
    simconnect_backend: int = SIMCONNECT_BACKEND_DEFAULT,
    simconnect_var_subs: list[tuple[str, callable]] = None,
    midi_input_ports: list[str],
    midi_cc_handlers: list[tuple[int, callable]] = None,
    midi_note_handlers: list[tuple[int, callable]] = None,
    midi_pitchwheel_handler: callable = None,
):
    """
    Set-up entrypoint (mainly thought for configuration files)

    This is meant to be used by configuration files in order to
    get the basics done very easily. This function handles the following:

    * Connection to the simulator via a backend of choice
    * Plug in the MIDI input port of choice
    * MIDI CC handlers (if specified)
    * MIDI note handlers (if specifiec)
    * MIDI pitchwheel handler (if specified)
    * SimVar change handler subscription (if specified)
    """

    # Connect to the flight simulator
    simc_connect(backend=simconnect_backend)

    # MIDI
    # ~~~~~~~~~~~~~~

    # Connect the MIDI input ports
    for ip in midi_input_ports:
        midi_connect_input_port(name=ip)

    # CC handlers
    if midi_cc_handlers is not None:
        ___batch_assign_cc_handlers(midi_cc_handlers)

    # Note handlers
    if midi_note_handlers is not None:
        ___batch_assign_note_handlers(midi_note_handlers)

    # Pitchwheel handler
    if midi_pitchwheel_handler is not None:
        midi_subscribe_to_pitchwheel(handler=midi_pitchwheel_handler)

    # SimVar subscriptions
    if simconnect_var_subs is not None:
        ___batch_subscribe_to_simvars(simconnect_var_subs)
