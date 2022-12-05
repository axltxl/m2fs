# -*- coding: utf-8 -*-

import threading

from .log import log
from .message import BaseMessage
from .message import TYPE_PITCHWHEEL


__pitchwheel_message_handler = None

# FIXME: doc me
__pitchwheel_message_handler_mutex = threading.Lock()


class PitchWheelMessage(BaseMessage):
    """
    MIDI PITCHWHEEL message as a class

    It contains the usual, plus a value pertaining to what the pitch wheel is set to
    """

    def __init__(self, *, value=0, channel=0):
        super().__init__(type=TYPE_PITCHWHEEL, value=value, channel=channel)
        self.value = value

    def __str__(self) -> str:
        return f"PitchWheelMessage(value={self.value}, channel={self.channel})"


def get_handler():
    """Get current pitch wheel handler"""

    global __pitchwheel_message_handler, __pitchwheel_message_handler_mutex

    # FIXME: needs mutex
    with __pitchwheel_message_handler_mutex:
        return __pitchwheel_message_handler


def bootstrap() -> None:
    """Bootstrap pitch wheel-related things"""

    subscribe(handler=__null_pitchwheel_message_handler)


def subscribe(*, handler):
    """Map a handler to pitch wheel changes"""

    global __pitchwheel_message_handler, __pitchwheel_message_handler_mutex

    log.debug(f"PITCHWHEEL: subscribing handler -> {handler.__name__}")

    # Decorator pattern is used mostly
    # for logging calls to a handler by default
    def wrapper(msg):
        log.debug(msg)
        handler(msg)

    # FIXME: needs mutex
    with __pitchwheel_message_handler_mutex:
        __pitchwheel_message_handler = wrapper


def __null_pitchwheel_message_handler(msg: PitchWheelMessage):
    """Default pitch wheel handler"""

    log.info(f"PITCHWHEEL [{msg.value:>5}]: no handler set")
