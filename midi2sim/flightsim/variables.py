# -*- coding: utf-8 -*-

import threading

import SimConnect

from .log import log
from .sim import connect


class SimVarException(Exception):
    """SimVar error"""

    pass


# For how long is Python-SimConnect caching
# local SimVar data?
SIMCONNECT_CACHE_TICK_RATE_HZ = 33
SIMCONNECT_CACHE_TTL_MS = 1000.0 / SIMCONNECT_CACHE_TICK_RATE_HZ

# SimConnect.AircraftRequests object goes in here
# Once created, it'll update its SimVars' data from
# SimConnect every SIMCONNECT_CACHE_TTL_MS
__simvar_aq = None

# Mutex lock is needed to have access to the
# AircraftRequests instance (used to read/write variables)
# since the __poll thread is also accessing this data constantly
# (SIMCONNECT_CACHE_TICK_RATE_HZ times per second to be exact)
__simvar_aq_mutex = threading.Lock()


def __get_aq() -> SimConnect.AircraftRequests:
    # NOTE: critical section shared with __poll thread
    # SEE: poll.py
    with __simvar_aq_mutex:
        global __simvar_aq
        if __simvar_aq is None:
            __simvar_aq = SimConnect.AircraftRequests(
                connect(), _time=SIMCONNECT_CACHE_TTL_MS
            )
        return __simvar_aq


class SimVar:
    """SimVar with class ;)"""

    def __init__(self, *, name: str, description: str, value: any):
        self.name = name
        self.description = description
        self.value = value

    def __str__(self) -> str:
        return f"SimVar(name={self.name}, description={self.description}, value={self.value}"


def get_variable(name: str) -> (SimVar | None):
    """Get SimVar from flight sim"""

    v = __get_aq().find(name)
    if v is not None:
        value = v.get()
        log.verbose(f"SimVar GET {name} => {value}")
        return SimVar(name=name, description=v.description, value=value)

    # NOTE: Unfortunately, not all SimVars are supported out of the box
    # Only the ones supported by PySimConnect, which are a lot indeed and
    # will do much for you, but still, do not expect to get just any SimVar
    raise SimVarException(
        f"SimVar GET {name}: couldn't find it. SimVar does not exist or likely not supported by PySimConnect library! :("
    )


def set_variable(name: str, value: any) -> None:
    """Set SimVar on flight sim :)"""

    log.verbose(f"SimVar SET {name} => {value}")
    v = __get_aq().find(name)
    if v is not None:
        v.set(value)
    else:
        # NOTE: Unfortunately, not all SimVars are supported out of the box
        # Only the ones supported by PySimConnect, which are a lot indeed and
        # will do much for you, but still, do not expect to get just any SimVar
        raise SimVarException(
            f"SimVar SET {name}: couldn't find it. SimVar does not exist or likely not supported by PySimConnect library! :("
        )
