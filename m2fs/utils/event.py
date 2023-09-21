# -*- coding: utf-8 -*-
"""
SimConnect event utilities
"""

from ..simc import send_event as simc_send_evt


def send(e):
    if isinstance(e, tuple):
        simc_send_evt(*e)
    else:
        simc_send_evt(e)
