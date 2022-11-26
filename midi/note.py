# -*- coding: utf-8 -*-

import log
from .message import Message

# List of note handlers (functions)
__note_message_handlers = {}


def __null_note_message_handler(msg: dict):
    """Default note handler"""
    log.info(f'NOTE {msg.id}: no handler set')


# List of all MIDI notes
# Source: https://www.inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies
NOTE_000 = 0
NOTE_001 = 1
NOTE_002 = 2
NOTE_003 = 3
NOTE_004 = 4
NOTE_005 = 5
NOTE_006 = 6
NOTE_007 = 7
NOTE_008 = 8
NOTE_009 = 9
NOTE_010 = 10
NOTE_011 = 11
NOTE_012 = 12
NOTE_013 = 13
NOTE_014 = 14
NOTE_015 = 15
NOTE_016 = 16
NOTE_017 = 17
NOTE_018 = 18
NOTE_019 = 19
NOTE_020 = 20
NOTE_021 = 21  # A0
NOTE_022 = 22
NOTE_023 = 23
NOTE_024 = 24
NOTE_025 = 25
NOTE_026 = 26
NOTE_027 = 27
NOTE_028 = 28
NOTE_029 = 29
NOTE_030 = 30
NOTE_031 = 31
NOTE_032 = 32
NOTE_033 = 33
NOTE_034 = 34
NOTE_035 = 35
NOTE_036 = 36
NOTE_037 = 37
NOTE_038 = 38
NOTE_039 = 39
NOTE_040 = 40
NOTE_041 = 41
NOTE_042 = 42
NOTE_043 = 43
NOTE_044 = 44
NOTE_045 = 45
NOTE_046 = 46
NOTE_047 = 47
NOTE_048 = 48
NOTE_049 = 49
NOTE_050 = 50
NOTE_051 = 51
NOTE_052 = 52
NOTE_053 = 53
NOTE_054 = 54
NOTE_055 = 55
NOTE_056 = 56
NOTE_057 = 57
NOTE_058 = 58
NOTE_059 = 59
NOTE_060 = 60
NOTE_061 = 61
NOTE_062 = 62
NOTE_063 = 63
NOTE_064 = 64
NOTE_065 = 65
NOTE_066 = 66
NOTE_067 = 67
NOTE_068 = 68
NOTE_069 = 69
NOTE_070 = 70
NOTE_071 = 71
NOTE_072 = 72
NOTE_073 = 73
NOTE_074 = 74
NOTE_075 = 75
NOTE_076 = 76
NOTE_077 = 77
NOTE_078 = 78
NOTE_079 = 79
NOTE_080 = 80
NOTE_081 = 81
NOTE_082 = 82
NOTE_083 = 83
NOTE_084 = 84
NOTE_085 = 85
NOTE_086 = 86
NOTE_087 = 87
NOTE_088 = 88
NOTE_089 = 89
NOTE_090 = 90
NOTE_091 = 91
NOTE_092 = 92
NOTE_093 = 93
NOTE_094 = 94
NOTE_095 = 95
NOTE_096 = 96
NOTE_097 = 97
NOTE_098 = 98
NOTE_099 = 99
NOTE_100 = 100
NOTE_101 = 101
NOTE_102 = 102
NOTE_103 = 103
NOTE_104 = 104
NOTE_105 = 105
NOTE_106 = 106
NOTE_107 = 107
NOTE_108 = 108
NOTE_109 = 109
NOTE_110 = 110
NOTE_111 = 111
NOTE_112 = 112
NOTE_113 = 113
NOTE_114 = 114
NOTE_115 = 115
NOTE_116 = 116
NOTE_117 = 117
NOTE_118 = 118
NOTE_119 = 119
NOTE_120 = 120
NOTE_121 = 121
NOTE_122 = 122
NOTE_123 = 123
NOTE_124 = 124
NOTE_125 = 125
NOTE_126 = 126
NOTE_127 = 127  # G9
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
        return f'NoteMessage(id={self.id}, velocity={self.velocity}, channel={self.channel}, on={self.on})'


def get_handler(*, note):
    """ Get a handler for a particular MIDI note """

    return __note_message_handlers[note]


def bootstrap() -> None:
    """Bootstrap CC-related things, mostly initializing handlers"""

    for note in range(NOTE_MIN, NOTE_MAX + 1):
        log.info(f'Setting default handler for MIDI note # {note} ...')
        subscribe(note=note, handler=__null_note_message_handler)


def subscribe(*, note: int, handler):
    """Map a handler to changes done on a CC"""

    log.info(f'NOTE: subscribing handler [{note}] -> {handler.__name__}')

    # Decorator pattern is used mostly
    # for logging calls to a handler by default
    def wrapper(msg):
        log.info(msg)
        handler(msg)

    __note_message_handlers[note] = wrapper
