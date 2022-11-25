# -*- coding: utf-8 -*-

import log
from .message import Message, MIDI_MSG_SUCCESS

# List of CC handlers (functions)
__cc_message_handlers = {}


def __null_cc_message_handler(msg: dict):
    """Default CC handler"""
    log.info(f'CC {msg.id}: no handler set')
    return (MIDI_MSG_SUCCESS, "")


# List of all MIDI CCs
CC_000 = 0
CC_001 = 1
CC_002 = 2
CC_003 = 3
CC_004 = 4
CC_005 = 5
CC_006 = 6
CC_007 = 7
CC_008 = 8
CC_009 = 9
CC_010 = 10
CC_011 = 11
CC_012 = 12
CC_013 = 13
CC_014 = 14
CC_015 = 15
CC_016 = 16
CC_017 = 17
CC_018 = 18
CC_019 = 19
CC_020 = 20
CC_021 = 21
CC_022 = 22
CC_023 = 23
CC_024 = 24
CC_025 = 25
CC_026 = 26
CC_027 = 27
CC_028 = 28
CC_029 = 29
CC_030 = 30
CC_031 = 31
CC_032 = 32
CC_033 = 33
CC_034 = 34
CC_035 = 35
CC_036 = 36
CC_037 = 37
CC_038 = 38
CC_039 = 39
CC_040 = 40
CC_041 = 41
CC_042 = 42
CC_043 = 43
CC_044 = 44
CC_045 = 45
CC_046 = 46
CC_047 = 47
CC_048 = 48
CC_049 = 49
CC_050 = 50
CC_051 = 51
CC_052 = 52
CC_053 = 53
CC_054 = 54
CC_055 = 55
CC_056 = 56
CC_057 = 57
CC_058 = 58
CC_059 = 59
CC_060 = 60
CC_061 = 61
CC_062 = 62
CC_063 = 63
CC_064 = 64
CC_065 = 65
CC_066 = 66
CC_067 = 67
CC_068 = 68
CC_069 = 69
CC_070 = 70
CC_071 = 71
CC_072 = 72
CC_073 = 73
CC_074 = 74
CC_075 = 75
CC_076 = 76
CC_077 = 77
CC_078 = 78
CC_079 = 79
CC_080 = 80
CC_081 = 81
CC_082 = 82
CC_083 = 83
CC_084 = 84
CC_085 = 85
CC_086 = 86
CC_087 = 87
CC_088 = 88
CC_089 = 89
CC_090 = 90
CC_091 = 91
CC_092 = 92
CC_093 = 93
CC_094 = 94
CC_095 = 95
CC_096 = 96
CC_097 = 97
CC_098 = 98
CC_099 = 99
CC_100 = 100
CC_101 = 101
CC_102 = 102
CC_103 = 103
CC_104 = 104
CC_105 = 105
CC_106 = 106
CC_107 = 107
CC_108 = 108
CC_109 = 109
CC_110 = 110
CC_111 = 111
CC_112 = 112
CC_113 = 113
CC_114 = 114
CC_115 = 115
CC_116 = 116
CC_117 = 117
CC_118 = 118
CC_119 = 119
CC_120 = 120
CC_121 = 121
CC_122 = 122
CC_123 = 123
CC_124 = 124
CC_125 = 125
CC_126 = 126
CC_127 = 127
CC_MIN = CC_000
CC_MAX = CC_127


class ControlChangeMessage(Message):
    """
    MIDI CC as a class

    It contains the usual, plus a value pertaining to a CC
    """

    def __init__(self, *, id=0, value=0, channel=0):
        super().__init__(type=Message.TYPE_CC, id=id, value=value, channel=channel)
        self.value = value

    def __str__(self) -> str:
        return f'ControlChangeMessage(id={self.id}, value={self.value}, channel={self.channel})'


def get_handler(*, cc):
    """ Get a handler for a particular CC """

    return __cc_message_handlers[cc]


def bootstrap() -> None:
    """Bootstrap CC-related things, mostly initializing handlers"""

    for cc in range(CC_MIN, CC_MAX + 1):
        log.info(f'Setting default handler for MIDI CC # {cc} ...')
        set_handler(cc=cc, handler=__null_cc_message_handler)


def set_handler(*, cc: int, handler):
    """Map a handler to changes done on a CC"""

    # Decorator pattern is used mostly
    # for logging calls to a handler by default
    def wrapper(msg):
        log.info(msg)
        result, reason = handler(msg)
        if result != 0:
            log.warn(
                f'[CC#{cc}] - handler did not return successfully: {reason}')
        return result

    __cc_message_handlers[cc] = wrapper
