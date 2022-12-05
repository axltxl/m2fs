# -*- coding: utf-8 -*-

import threading

from .log import log
from .message import IdMessage
from .message import TYPE_CC

# List of CC handlers (functions)
__cc_message_handlers = {}

# FIXME: doc me
__cc_message_handlers_mutex = threading.Lock()

# List of all MIDI CCs
CC_000 = 0x00
CC_001 = 0x01
CC_002 = 0x02
CC_003 = 0x03
CC_004 = 0x04
CC_005 = 0x05
CC_006 = 0x06
CC_007 = 0x07
CC_008 = 0x08
CC_009 = 0x09
CC_010 = 0x0A
CC_011 = 0x0B
CC_012 = 0x0C
CC_013 = 0x0D
CC_014 = 0x0E
CC_015 = 0x0F
CC_016 = 0x10
CC_017 = 0x11
CC_018 = 0x12
CC_019 = 0x13
CC_020 = 0x14
CC_021 = 0x15
CC_022 = 0x16
CC_023 = 0x17
CC_024 = 0x18
CC_025 = 0x19
CC_026 = 0x1A
CC_027 = 0x1B
CC_028 = 0x1C
CC_029 = 0x1D
CC_030 = 0x1E
CC_031 = 0x1F
CC_032 = 0x20
CC_033 = 0x21
CC_034 = 0x22
CC_035 = 0x23
CC_036 = 0x24
CC_037 = 0x25
CC_038 = 0x26
CC_039 = 0x27
CC_040 = 0x28
CC_041 = 0x29
CC_042 = 0x2A
CC_043 = 0x2B
CC_044 = 0x2C
CC_045 = 0x2D
CC_046 = 0x2E
CC_047 = 0x2F
CC_048 = 0x30
CC_049 = 0x31
CC_050 = 0x32
CC_051 = 0x33
CC_052 = 0x34
CC_053 = 0x35
CC_054 = 0x36
CC_055 = 0x37
CC_056 = 0x38
CC_057 = 0x39
CC_058 = 0x3A
CC_059 = 0x3B
CC_060 = 0x3C
CC_061 = 0x3D
CC_062 = 0x3E
CC_063 = 0x3F
CC_064 = 0x40
CC_065 = 0x41
CC_066 = 0x42
CC_067 = 0x43
CC_068 = 0x44
CC_069 = 0x45
CC_070 = 0x46
CC_071 = 0x47
CC_072 = 0x48
CC_073 = 0x49
CC_074 = 0x4A
CC_075 = 0x4B
CC_076 = 0x4C
CC_077 = 0x4D
CC_078 = 0x4E
CC_079 = 0x4F
CC_080 = 0x50
CC_081 = 0x51
CC_082 = 0x52
CC_083 = 0x53
CC_084 = 0x54
CC_085 = 0x55
CC_086 = 0x56
CC_087 = 0x57
CC_088 = 0x58
CC_089 = 0x59
CC_090 = 0x5A
CC_091 = 0x5B
CC_092 = 0x5C
CC_093 = 0x5D
CC_094 = 0x5E
CC_095 = 0x5F
CC_096 = 0x60
CC_097 = 0x61
CC_098 = 0x62
CC_099 = 0x63
CC_100 = 0x64
CC_101 = 0x65
CC_102 = 0x66
CC_103 = 0x67
CC_104 = 0x68
CC_105 = 0x69
CC_106 = 0x6A
CC_107 = 0x6B
CC_108 = 0x6C
CC_109 = 0x6D
CC_110 = 0x6E
CC_111 = 0x6F
CC_112 = 0x70
CC_113 = 0x71
CC_114 = 0x72
CC_115 = 0x73
CC_116 = 0x74
CC_117 = 0x75
CC_118 = 0x76
CC_119 = 0x77
CC_120 = 0x78
CC_121 = 0x79
CC_122 = 0x7A
CC_123 = 0x7B
CC_124 = 0x7C
CC_125 = 0x7D
CC_126 = 0x7E
CC_127 = 0x7F
CC_MIN = CC_000
CC_MAX = CC_127


class ControlChangeMessage(IdMessage):
    """
    MIDI CC as a class

    It contains the usual, plus a value pertaining to a CC
    """

    def __init__(self, *, id=0, value=0, channel=0):
        super().__init__(type=TYPE_CC, id=id, value=value, channel=channel)
        self.value = value

    def __str__(self) -> str:
        return f"ControlChangeMessage(id={self.id}, value={self.value}, channel={self.channel})"


def get_handler(*, cc):
    """Get a handler for a particular CC"""

    global __cc_message_handlers, __cc_message_handlers_mutex

    # FIXME: needs mutex
    # FIXME: it will happen that a handler is no more
    # FIXME: at worst it'll be __null_cc_message_handler
    # FIXME: still, deal with KeyError and return None
    with __cc_message_handlers_mutex:
        return __cc_message_handlers[cc]


def bootstrap() -> None:
    """Bootstrap CC-related things, mostly initializing handlers"""

    for cc in range(CC_MIN, CC_MAX + 1):
        log.debug(f"Setting default handler for MIDI CC # {cc} ...")
        subscribe(cc=cc, handler=__null_cc_message_handler)


def subscribe(*, cc: int, handler):
    """Map a handler to changes done on a CC"""

    global __cc_message_handlers, __cc_message_handlers_mutex

    log.debug(f"CC: subscribing handler [CC#{cc}] -> {handler.__name__}")

    # Decorator pattern is used mostly
    # for logging calls to a handler by default
    def wrapper(msg):
        log.debug(msg)
        handler(msg)

    # FIXME: this variable needs a mutex
    with __cc_message_handlers_mutex:
        __cc_message_handlers[cc] = wrapper


def __null_cc_message_handler(msg: ControlChangeMessage):
    """Default CC handler"""

    log.info(f"CC {msg.id}: no handler set")
