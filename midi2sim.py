#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import traceback

import config
import log
import midi

CMD_LS = "ls"


def __log_ports(ports: list[str]) -> None:
    """Log MIDI port(s) currently connected"""

    if len(ports):
        for port in ports:
            log.info(f'\t => {port}')
    else:
        log.warn("No device found :(")


def __cmd_ls() -> None:
    """Process command argument"""

    log.info("Listing MIDI port(s) ...")
    ports = midi.ls_ports()
    log.info("List of MIDI input port(s) found:")
    __log_ports(ports['input'])
    log.info("List of MIDI output port(s) found:")
    __log_ports(ports['output'])
    log.info("List of MIDI I/O port(s) found:")
    __log_ports(ports['io'])


def __parse_args(argv: list[str]) -> dict:
    """Parse arguments"""

    options = {
        "command": None
    }

    try:
        options["command"] = argv[0]
    except IndexError:
        pass
    return options


def __handle_except(e):
    """
    Handle (log) any exception
    """
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    log.error("Unhandled {e} at {file}:{line}: '{msg}'"
              .format(e=exc_type.__name__, file=fname,
                      line=exc_tb.tb_lineno,  msg=e))
    log.error(traceback.format_exc())
    log.error("An error has occurred!. "
              "For more details, review the logs.")
    return -1


def config_bootstrap():
    """Setup handlers and more from config :) """

    # Read from config and get which port (MIDI controller or device)
    # is it gonna read messages from
    midi.set_port(config.MIDI_PORT)

    log.info("Setting MIDI handlers from config ...")
    log.info(f'{len(config.MIDI_CC_HANDLERS)} CC handler(s) found on config ...')
    log.info(
        f'{len(config.MIDI_NOTE_HANDLERS)} NOTE handler(s) found on config ...')

    # Set CC handlers from config
    # They are expected to be located within the MIDI_CC_HANDLERS dictionary
    for cc, handler in config.MIDI_CC_HANDLERS.items():
        log.info(f'CC # {cc}: found handler: {handler.__name__}')
        midi.set_cc_handler(cc=cc, handler=handler)

    # Set NOTE handlers from config
    # They are expected to be located within the MIDI_NOTE_HANDLERS dictionary
    for note, handler in config.MIDI_NOTE_HANDLERS.items():
        log.info(f'NOTE # {note}: found handler: {handler.__name__}')
        midi.set_note_handler(note=note, handler=handler)


def event_loop() -> None:
    """
    Main event loop

    This will basically do the magic, namely,
    process MIDI messages and do as it pleases
    with them
    """

    # Initialize MIDI, first of all
    midi.bootstrap()

    # Read config
    config_bootstrap()

    # Initialize the MIDI message pump
    log.info(f'MIDI device = {config.MIDI_PORT} ...')
    log.info("Listening for messages ... ")
    midi.message_pump()


def main(options: dict):
    """Main entrypoint"""

    try:
        command = options['command']

        # Get command from command line
        # (already parsed to options)
        if command is not None:
            if command == CMD_LS:
                __cmd_ls()

        # If no command is provided, it's gonna
        # do its thing and run the event loop
        else:
            event_loop()
            return 0

    except Exception as e:
        return __handle_except(e)


if __name__ == "__main__":
    sys.exit(main(__parse_args(sys.argv[1:])))
