# -*- coding: utf-8 -*-

MIDI_MSG_SUCCESS = 0
MIDI_MSG_FAILURE = -1

# FIXME: doc me


class Message:
    TYPE_CC = 0
    TYPE_NOTE = 1

    def __init__(self, *, type, id=0, value=0, channel=0):
        self.type = type
        self.id = id
        self.channel = channel
        self.value = value

    def __str__(self) -> str:
        return f'Message(type={self.type}, id={self.id})'
