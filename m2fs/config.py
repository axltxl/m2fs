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
    subscribe_to_simvar as simc_subscribe_to_simvar,
    poll_start as simc_poll_start,
    reset as simc_reset,
)
from .simc import SIMCONNECT_BACKEND_DEFAULT
from .log import log


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


__config_module = None  # configuration as a python module
__config_module_abs_path = ""  # absolute path to configuration file

CONFIG_MODULE_SPEC_NAME = "m2fs.usr_config"


def load(config_file: str) -> None:
    """
    Append configuration file directory to sys.path

    This will make it possible to import a configuration file
    set by the user
    """

    global __config_module, __config_module_abs_path

    log.debug(f"Attempting to load config module at: {config_file}")

    # Make sure the config module is not a sys.modules already
    try:
        del sys.modules[CONFIG_MODULE_SPEC_NAME]
    except KeyError:
        pass

    __config_module_abs_path = os.path.expanduser(os.path.realpath(config_file))

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

    log.info(f"{config_file}: config module successfully loaded!")


def reload() -> None:
    """
    Reload configuration module

    This will make sure a hot configuration can be done.
    It'll make sure all internal state has been set to defaults
    (any housekeeping, etc.), and then it proceeds to reload
    the config module.
    """

    global __config_module_abs_path

    log.warn("!!! CONFIG RELOAD !!!")

    # Reset MIDI engine
    midi_reset()

    # Reset SimConnect client and data
    simc_reset()

    # Load the configuration file (again)
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

    simc_poll_start()  # Start polling for simc changes ... (does not block)
    midi_message_pump_start()  # Start rolling those MIDI messages
