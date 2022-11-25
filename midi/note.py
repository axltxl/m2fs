# -*- coding: utf-8 -*-

from .message import Message


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
        return f'NoteMessage(type=NOTE, id={self.id}, velocity={self.velocity}, channel={self.channel}, on={self.on})'
