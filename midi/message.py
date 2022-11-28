# -*- coding: utf-8 -*-


TYPE_CC = 0
TYPE_NOTE = 1
TYPE_PITCHWHEEL = 2


class BaseMessage:
    """Standard MIDI message as a class"""

    def __init__(self, *, type, value=0, channel=0):
        self.type = type
        self.channel = channel
        self.value = value


class IdMessage(BaseMessage):
    """Message with an ID value (such as CCs or notes)"""

    def __init__(self, *, type, id=0, value=0, channel=0):
        super().__init__(type=type, value=value, channel=channel)
        self.id = id
