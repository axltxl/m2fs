# -*- coding: utf-8 -*-
"""
Configuration file entrypoint: setup()
"""

import os
import sys
import importlib
import importlib.util

from .midi import (
    subscribe_to_cc as midi_subscribe_to_cc,
    subscribe_to_note as midi_subscribe_to_note,
    subscribe_to_pitchwheel as midi_subscribe_to_pitchwheel,
    connect_input_port as midi_connect_input_port,
    reset as midi_reset,
    message_pump_start as midi_message_pump_start,
)
from .simc import (
    connect as simc_connect,
    disconnect as simc_disconnect,
    subscribe_to_simvar as simc_subscribe_to_simvar,
    poll_start as simc_poll_start,
    reset as simc_reset,
)
from .simc import SIMCONNECT_BACKEND_DEFAULT
from .simc.poll import poll_reset


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


# FIXME
__config_module = None
__config_module_abs_path = ""

CONFIG_MODULE_SPEC_NAME = "m2fs.usr_config"


def load(config_file: str) -> None:
    """
    Append configuration file directory to sys.path

    This will make it possible to import a configuration file
    set by the user
    """

    global __config_module, __config_module_abs_path

    # FIXME
    try:
        del sys.modules[CONFIG_MODULE_SPEC_NAME]
    except KeyError:
        pass

    __config_module_abs_path = os.path.expanduser(os.path.realpath(config_file))

    # # FIXME
    # spec = importlib.util.spec_from_file_location(
    #     CONFIG_MODULE_NAME, config_file_abs_path
    # )
    # __config_module = importlib.util.module_from_spec(spec)
    # sys.modules[CONFIG_MODULE_NAME] = __config_module
    # spec.loader.exec_module(__config_module)

    # specify the module that needs to be
    # imported relative to the path of the
    # module
    spec = importlib.util.spec_from_file_location(
        CONFIG_MODULE_SPEC_NAME, __config_module_abs_path
    )

    # creates a new module based on spec
    __config_module = importlib.util.module_from_spec(spec)

    # Add module to sys.modules
    sys.modules[CONFIG_MODULE_SPEC_NAME] = __config_module

    # executes the module in its own namespace
    # when a module is imported or reloaded.
    spec.loader.exec_module(__config_module)


# FIXME
def reload() -> None:
    global __config_module_abs_path

    # close all MIDI inputs and outputs
    # reset all MIDI subscriptions
    # CONTINUEHERE: CC, note and pitchwheel handlers need a mutex
    midi_reset()

    # FIXME
    simc_reset()

    # https://stackoverflow.com/questions/437589/how-do-i-unload-reload-a-python-module
    # FIXME: doc me
    # load(config_file)
    load(config_file=__config_module_abs_path)


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

    # FIXME: doc me
    simc_poll_start()  # Start polling for simc changes ... (does not block)
    midi_message_pump_start()  # Start rolling those MIDI messages
