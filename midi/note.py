# -*- coding: utf-8 -*-

import mido
import log
from .message import Message

# List of note handlers (functions)
__note_message_handlers = {}


def __null_note_message_handler(msg: dict):
    """Default note handler"""
    log.info(f"NOTE {msg.id}: no handler set")


# List of all MIDI notes
# Source: https://www.inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies
NOTE_000 = 0x00
NOTE_001 = 0x01
NOTE_002 = 0x02
NOTE_003 = 0x03
NOTE_004 = 0x04
NOTE_005 = 0x05
NOTE_006 = 0x06
NOTE_007 = 0x07
NOTE_008 = 0x08
NOTE_009 = 0x09
NOTE_010 = 0x0A
NOTE_011 = 0x0B
NOTE_012 = 0x0C
NOTE_013 = 0x0D
NOTE_014 = 0x0E
NOTE_015 = 0x0F
NOTE_016 = 0x10
NOTE_017 = 0x11
NOTE_018 = 0x12
NOTE_019 = 0x13
NOTE_020 = 0x14
NOTE_021 = 0x15  # A0
NOTE_022 = 0x16
NOTE_023 = 0x17
NOTE_024 = 0x18
NOTE_025 = 0x19
NOTE_026 = 0x1A
NOTE_027 = 0x1B
NOTE_028 = 0x1C
NOTE_029 = 0x1D
NOTE_030 = 0x1E
NOTE_031 = 0x1F
NOTE_032 = 0x20
NOTE_033 = 0x21
NOTE_034 = 0x22
NOTE_035 = 0x23
NOTE_036 = 0x24
NOTE_037 = 0x25
NOTE_038 = 0x26
NOTE_039 = 0x27
NOTE_040 = 0x28
NOTE_041 = 0x29
NOTE_042 = 0x2A
NOTE_043 = 0x2B
NOTE_044 = 0x2C
NOTE_045 = 0x2D
NOTE_046 = 0x2E
NOTE_047 = 0x2F
NOTE_048 = 0x30
NOTE_049 = 0x31
NOTE_050 = 0x32
NOTE_051 = 0x33
NOTE_052 = 0x34
NOTE_053 = 0x35
NOTE_054 = 0x36
NOTE_055 = 0x37
NOTE_056 = 0x38
NOTE_057 = 0x39
NOTE_058 = 0x3A
NOTE_059 = 0x3B
NOTE_060 = 0x3C
NOTE_061 = 0x3D
NOTE_062 = 0x3E
NOTE_063 = 0x3F
NOTE_064 = 0x40
NOTE_065 = 0x41
NOTE_066 = 0x42
NOTE_067 = 0x43
NOTE_068 = 0x44
NOTE_069 = 0x45
NOTE_070 = 0x46
NOTE_071 = 0x47
NOTE_072 = 0x48
NOTE_073 = 0x49
NOTE_074 = 0x4A
NOTE_075 = 0x4B
NOTE_076 = 0x4C
NOTE_077 = 0x4D
NOTE_078 = 0x4E
NOTE_079 = 0x4F
NOTE_080 = 0x50
NOTE_081 = 0x51
NOTE_082 = 0x52
NOTE_083 = 0x53
NOTE_084 = 0x54
NOTE_085 = 0x55
NOTE_086 = 0x56
NOTE_087 = 0x57
NOTE_088 = 0x58
NOTE_089 = 0x59
NOTE_090 = 0x5A
NOTE_091 = 0x5B
NOTE_092 = 0x5C
NOTE_093 = 0x5D
NOTE_094 = 0x5E
NOTE_095 = 0x5F
NOTE_096 = 0x60
NOTE_097 = 0x61
NOTE_098 = 0x62
NOTE_099 = 0x63
NOTE_100 = 0x64
NOTE_101 = 0x65
NOTE_102 = 0x66
NOTE_103 = 0x67
NOTE_104 = 0x68
NOTE_105 = 0x69
NOTE_106 = 0x6A
NOTE_107 = 0x6B
NOTE_108 = 0x6C
NOTE_109 = 0x6D
NOTE_110 = 0x6E
NOTE_111 = 0x6F
NOTE_112 = 0x70
NOTE_113 = 0x71
NOTE_114 = 0x72
NOTE_115 = 0x73
NOTE_116 = 0x74
NOTE_117 = 0x75
NOTE_118 = 0x76
NOTE_119 = 0x77
NOTE_120 = 0x78
NOTE_121 = 0x79
NOTE_122 = 0x7A
NOTE_123 = 0x7B
NOTE_124 = 0x7C
NOTE_125 = 0x7D
NOTE_126 = 0x7E
NOTE_127 = 0x7F  # G9
NOTE_MIN = NOTE_000
NOTE_MAX = NOTE_127


class NoteMessage(Message):
    """
    A MIDI note message as a class.
    It covers both note_on, and note_off messages
    """

    def __init__(self, *, on=False, id=0, value=0, channel=0, velocity=0):
        super().__init__(type=Message.TYPE_NOTE, id=id, value=value, channel=channel)
        self.on = on
        self.velocity = velocity

    @property
    def off(self) -> bool:
        return not self.on

    def __str__(self) -> str:
        return f"NoteMessage(id={self.id}, velocity={self.velocity}, channel={self.channel}, on={self.on})"


def get_handler(*, note):
    """Get a handler for a particular MIDI note"""

    return __note_message_handlers[note]


def bootstrap() -> None:
    """Bootstrap CC-related things, mostly initializing handlers"""

    for note in range(NOTE_MIN, NOTE_MAX + 1):
        log.debug(f"Setting default handler for MIDI note # {note} ...")
        subscribe(note=note, handler=__null_note_message_handler)


def subscribe(*, note: int, handler):
    """Map a handler to changes done on a CC"""

    log.debug(f"NOTE: subscribing handler [{note}] -> {handler.__name__}")

    # Decorator pattern is used mostly
    # for logging calls to a handler by default
    def wrapper(msg):
        log.info(msg)
        handler(msg)

    __note_message_handlers[note] = wrapper
