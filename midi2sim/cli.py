# -*- coding: utf-8 -*-

import os
import sys
import traceback
import importlib.util
import signal
import time

from docopt import docopt, DocoptExit

from .logger import Logger
from .simc import (
    SIMCONNECT_BACKEND_DEFAULT,
    SIMCONNECT_BACKEND_MOBIFLIGHT,
    SIMCONNECT_BACKEND_DEFAULT_NAME,
    SIMCONNECT_BACKEND_MOBIFLIGHT_NAME,
    connect as simc_connect,
    disconnect as simc_disconnect,
    get_variable as simc_get_variable,
    poll_start as simc_poll_start,
    poll_stop as simc_poll_stop,
)
from .midi import (
    list_available_ports as midi_list_available_ports,
    cleanup as midi_cleanup,
    message_pump_start as midi_message_pump_start,
    bootstrap as midi_bootstrap,
)

log = Logger(prefix=">> ")

PKG_VERSION = "0.1.0"
PKG_NAME = "midi2sim"
CLI_DEFAULT_CONFIG_DIR = os.path.join(os.path.expanduser("~"), PKG_NAME)
CLI_DEFAULT_CONFIG_FILE = os.path.join(CLI_DEFAULT_CONFIG_DIR, "config.py")
CLI_DEFAULT_SIMCONNECT_BACKEND = SIMCONNECT_BACKEND_DEFAULT_NAME


def __handle_signal(signum, frame):
    """
    UNIX signal handler
    """
    # Raise a SystemExit exception
    sys.exit(1)


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
    """{pkg_name}

    Usage:
        {pkg_name} [--config FILE]
        {pkg_name} midi [(list)]
        {pkg_name} sim var get <variable> [--simconnect-backend BACKEND]

    Options:
        -h --help                          Show this screen.
        --version                          Show version.
        -c, --config FILE                  Configuration file location [default: {default_config_file}]
        -s, --simconnect-backend BACKEND   SimConnect client backend [default: {default_smc_backend}]
    """

    # __doc__ needs to be formatted first
    __parse_args.__doc__ = __parse_args.__doc__.format(
        pkg_name=PKG_NAME,
        default_config_file=CLI_DEFAULT_CONFIG_FILE,
        default_smc_backend=CLI_DEFAULT_SIMCONNECT_BACKEND,
    )

    return docopt(
        __parse_args.__doc__,
        argv=argv,
        version=PKG_VERSION,
    )


def __get_simconnect_backend_id(backend: str) -> int:
    if backend == SIMCONNECT_BACKEND_DEFAULT_NAME:
        return SIMCONNECT_BACKEND_DEFAULT
    if backend == SIMCONNECT_BACKEND_MOBIFLIGHT_NAME:
        return SIMCONNECT_BACKEND_MOBIFLIGHT
    log.warn(f"{backend}: unrecognized SimConnect backend provided, using default ...")
    return SIMCONNECT_BACKEND_DEFAULT


def main(argv: list[str]) -> int:
    """Main entrypoint"""

    try:
        # Parse arguments
        options = __parse_args(argv)

        # This baby will handle UNIX signals
        signal.signal(signal.SIGINT, __handle_signal)
        signal.signal(signal.SIGTERM, __handle_signal)

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
                            options["--simconnect-backend"]
                        ),
                    )

        # If no command is provided, it's gonna
        # do its thing and run the event loop
        else:
            event_loop(config_file=options["--config"])
            return 0

    except DocoptExit:
        print(__parse_args.__doc__)
    except SystemExit:
        log.warn("Exiting ...")
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

    simc_connect(backend=simconnect_backend)  # Connect to flight sim
    simvar = simc_get_variable(variable)
    if simvar is not None:
        log.info(f"SimConnect: {variable} = {simvar}")


def __cleanup():
    """Housekeeping is done here"""

    # Stop polling
    simc_poll_stop()

    # Disconnect from simulator
    simc_disconnect()

    # Take care of business on the MIDI
    # side of things
    midi_cleanup()


def __cmd_ls() -> None:
    """Process command argument"""

    log.info("Listing MIDI port(s) ...")
    ports = midi_list_available_ports()
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

    log.debug(f"Attempting to load config module at: {config_file_abs_path}")

    spec = importlib.util.spec_from_file_location(module_name, config_file_abs_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    log.info(
        f"{module_name}@{config_file_abs_path}: config module successfully loaded!"
    )

    return module


def event_loop(*, config_file: str) -> None:
    """
    Main event loop

    This will basically do the magic, namely,
    process MIDI messages and do as it pleases
    with them
    """

    try:
        midi_bootstrap()  # Start the MIDI engine
        config = __load_mod_from_file(config_file)  # Get config as a module
        simc_poll_start()  # Start polling for simc changes ... (does not block)
        midi_message_pump_start()  # Start rolling those MIDI messages

        # block until exception
        while True:
            time.sleep(1)
    except ImportError:
        log.error(f"Couldn't load configuration file: {config_file}")
        raise
