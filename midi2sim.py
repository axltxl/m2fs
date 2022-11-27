# -*- coding: utf-8 -*-
import sys
import os
import traceback

from docopt import docopt

import config
import flightsim
import log
import midi

PKG_VERSION = "0.1.0"


def __log_ports(ports: list[str]) -> None:
    """Log MIDI port(s) currently connected"""

    if len(ports):
        for port in ports:
            log.info(f"\t => {port}")
    else:
        log.warn("No device found :(")


def __cmd_simget(variable: str) -> None:
    """CLI command to get variable from flight sim"""

    flightsim.connect()  # Connect to flight sim
    simvar = flightsim.get_variable(variable)
    if simvar is not None:
        log.info(f"SimConnect: {variable} = {simvar}")


def __cleanup():
    """Housekeeping is done here"""

    # Stop polling
    flightsim.poll_stop()

    # Disconnect from simulator
    flightsim.disconnect()


def __cmd_ls() -> None:
    """Process command argument"""

    log.info("Listing MIDI port(s) ...")
    ports = midi.list_ports()
    log.info("List of MIDI input port(s) found:")
    __log_ports(ports["input"])
    log.info("List of MIDI output port(s) found:")
    __log_ports(ports["output"])
    log.info("List of MIDI I/O port(s) found:")
    __log_ports(ports["io"])


def __parse_args(argv: list[str]) -> dict:
    """midi2sim

    Usage:
        midi2sim
        midi2sim midi [(list)]
        midi2sim sim var get <variable>
    """

    return docopt(__parse_args.__doc__, argv=argv, version=PKG_VERSION)


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


def event_loop() -> None:
    """
    Main event loop

    This will basically do the magic, namely,
    process MIDI messages and do as it pleases
    with them
    """

    # Read config
    log.info(f"MIDI input port in use: {config.MIDI_PORT}")

    # Start polling for flightsim changes ... (does not block)
    flightsim.poll_start()

    # Start processing MIDI messages already
    log.info("Listening for MIDI messages ... ")
    midi.message_pump(port_name=config.MIDI_PORT, setup_func=config.on_init)


def main(options: dict):
    """Main entrypoint"""

    try:
        # Get command from command line
        # (already parsed to options)
        # if command is not None:

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
                    __cmd_simget(options["<variable>"])

        # If no command is provided, it's gonna
        # do its thing and run the event loop
        else:
            event_loop()
            return 0

    except Exception as e:
        return __handle_except(e)
    finally:
        __cleanup()


if __name__ == "__main__":
    sys.exit(main(__parse_args(sys.argv[1:])))
