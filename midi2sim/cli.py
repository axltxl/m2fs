# -*- coding: utf-8 -*-

import os
import sys
import traceback
import importlib.util

from docopt import docopt, DocoptExit

from . import simc, midi
from .logger import Logger

log = Logger(prefix=">> ")

PKG_VERSION = "0.1.0"


def __handle_except(e):
    """
    Handle (log) any exception
    """
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    log.error(
        "Unhandled {e} at {file}:{line}: '{msg}'".format(
            e=exc_type.__name__, file=fname, line=exc_tb.tb_lineno, msg=e
        )
    )
    log.error(traceback.format_exc())
    log.error("An error has occurred!. " "For more details, review the logs.")
    return -1


def __parse_args(argv: list[str]) -> dict:
    """midi2sim

    Usage:
        midi2sim --config <config_file> [--simconnect-backend <simconnect_backend>]
        midi2sim midi [(list)]
        midi2sim sim var get <variable> [--simconnect-backend <simconnect_backend>]
    """

    return docopt(__parse_args.__doc__, argv=argv, version=PKG_VERSION)


def __get_simconnect_backend_id(backend: str) -> int:
    if backend == "default":
        return simc.SIMCONNECT_BACKEND_DEFAULT
    if backend == "mobiflight":
        return simc.SIMCONNECT_BACKEND_MOBIFLIGHT
    return simc.SIMCONNECT_BACKEND_DEFAULT


def main(argv: list[str]) -> int:
    """Main entrypoint"""

    try:
        # Parse arguments
        options = __parse_args(argv)

        # Get command from command line
        # (already parsed to options)

        # MIDI options
        if options["midi"]:
            if options["list"]:
                __cmd_ls()

        # SimConnect options
        elif options["sim"]:

            # SimVar options
            if options["var"]:

                # Get/Set variable
                if options["get"]:
                    __cmd_simget(
                        options["<variable>"],
                        simconnect_backend=__get_simconnect_backend_id(
                            options["<simconnect_backend>"]
                        ),
                    )

        # If no command is provided, it's gonna
        # do its thing and run the event loop
        else:
            event_loop(
                config_file=options["<config_file>"],
                simconnect_backend=__get_simconnect_backend_id(
                    options["<simconnect_backend>"]
                ),
            )
            return 0

    except DocoptExit:
        print(__parse_args.__doc__)
    except Exception as e:
        return __handle_except(e)
    finally:
        __cleanup()


def __log_ports(ports: list[str]) -> None:
    """Log MIDI port(s) currently connected"""

    if len(ports):
        for port in ports:
            log.info(f"\t => {port}")
    else:
        log.warn("No device found :(")


def __cmd_simget(variable: str, simconnect_backend: int) -> None:
    """CLI command to get variable from flight sim"""

    simc.set_backend(simconnect_backend)
    simc.connect()  # Connect to flight sim
    simvar = simc.get_variable(variable)
    if simvar is not None:
        log.info(f"SimConnect: {variable} = {simvar}")


def __cleanup():
    """Housekeeping is done here"""

    # Stop polling
    simc.poll_stop()

    # Disconnect from simulator
    simc.disconnect()

    # Take care of business on the MIDI
    # side of things
    midi.cleanup()


def __cmd_ls() -> None:
    """Process command argument"""

    log.info("Listing MIDI port(s) ...")
    ports = midi.list_ports()
    log.info("List of MIDI input port(s) found:")
    __log_ports(ports["input"])
    log.info("List of MIDI output port(s) found:")
    __log_ports(ports["output"])


def __load_mod_from_file(config_file: str):
    """
    Append configuration file directory to sys.path

    This will make it possible to import a configuration file
    set by the user
    """

    config_file_abs_path = os.path.expanduser(os.path.realpath(config_file))
    module_name = "config"

    log.debug(
        f"Attempting to load config module at: {config_file_abs_path} (module_name={module_name}"
    )

    spec = importlib.util.spec_from_file_location(module_name, config_file_abs_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    log.info(
        f"{module_name}@{config_file_abs_path}: config module successfully loaded!"
    )

    return module


def event_loop(*, config_file: str, simconnect_backend: int) -> None:
    """
    Main event loop

    This will basically do the magic, namely,
    process MIDI messages and do as it pleases
    with them
    """

    # Proceed to connect to simulator
    simc.set_backend(simconnect_backend)
    simc.connect()

    # Start polling for simc changes ... (does not block)
    simc.poll_start()

    # Start processing MIDI messages already
    try:
        config = __load_mod_from_file(config_file)  # Get config as a module
        midi.message_pump(
            setup_func=config.on_init
        )  # Start rolling those MIDI messages
    except ImportError:
        log.error(f"Couldn't load configuration file: {config_file}")
        raise
