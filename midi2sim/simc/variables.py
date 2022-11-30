# -*- coding: utf-8 -*-

import threading

import SimConnect
from .mobiflight import MobiFlightVariableRequests

from .log import log
from .backend import get_backend

from .const import (
    SIMCONNECT_CACHE_TTL_MS,
    SIMCONNECT_BACKEND_MOBIFLIGHT,
)

# SimConnect.AircraftRequests object goes in here
# Once created, it'll update its SimVars' data from
# SimConnect every SIMCONNECT_CACHE_TTL_MS
__simvar_aq = None

# Mutex lock is needed to have access to the
# AircraftRequests instance (used to read/write variables)
# since the __poll thread is also accessing this data constantly
# (SIMCONNECT_CACHE_TICK_RATE_HZ times per second to be exact)
__simvar_aq_mutex = threading.Lock()

# SimConnect client
__simc_client = None


def cleanup():
    """Housekeeping"""

    global __simvar_aq, __simc_client
    __simvar_aq = None
    __simc_client = None


def update_client(client: SimConnect.SimConnect):
    global __simc_client
    # we need to make sure that global objects in variables
    # module have been reset upon changing a client backend
    cleanup()
    __simc_client = client


def __get_aq() -> SimConnect.AircraftRequests:
    # NOTE: critical section shared with __poll thread
    # SEE: poll.py
    global __simvar_aq, __simc_client
    with __simvar_aq_mutex:
        if __simvar_aq is None:
            if get_backend() == SIMCONNECT_BACKEND_MOBIFLIGHT:
                __simvar_aq = MobiFlightVariableRequests(__simc_client)
                __simvar_aq.clear_sim_variables()
            else:
                __simvar_aq = SimConnect.AircraftRequests(
                    __simc_client, _time=SIMCONNECT_CACHE_TTL_MS
                )
        return __simvar_aq


class SimVarException(Exception):
    """SimVar error"""

    pass


class SimVar:
    """SimVar with class ;)"""

    def __init__(self, *, name: str, description: str, value: any):
        self.name = name
        self.description = description
        self.value = value

    def __str__(self) -> str:
        return f"SimVar(name='{self.name}', description='{self.description}', value='{self.value}')"


def __get_variable_default(name: str) -> (SimVar | None):
    """Get SimVar from flight sim"""

    v = __get_aq().find(name)
    if v is not None:
        value = v.get()
        return SimVar(name=name, description=v.description, value=value)

    # NOTE: Unfortunately, not all SimVars are supported out of the box
    raise SimVarException(
        f"SimVar GET {name}: couldn't find it. SimVar does not exist or likely not supported by current SimConnect backend ..."
    )


def __get_variable_mobiflight(name: str) -> (SimVar | None):
    """Get SimVar from flight sim"""

    v = __get_aq()
    if v is not None:
        value = v.get(name)
        return SimVar(name=name, description="", value=value)

    # NOTE: Unfortunately, not all SimVars are supported out of the box
    # Only the ones supported by PySimConnect, which are a lot indeed and
    # will do much for you, but still, do not expect to get just any SimVar
    raise SimVarException(
        f"SimVar GET {name}: couldn't find it. SimVar does not exist or likely not supported by current SimConnect backend ..."
    )


def get_variable(name: str) -> (SimVar | None):
    """Get SimVar from flight sim"""

    # Get proper AircraftRequests object that is
    # correspondent to current backend
    if get_backend() == SIMCONNECT_BACKEND_MOBIFLIGHT:
        v = __get_variable_mobiflight(name)
    else:
        v = __get_variable_default(name)
    log.verbose(f"SimVar GET {name} => {v.value}")
    return v


def set_variable(name: str, value: any) -> None:
    """Set SimVar on flight sim :)"""

    log.verbose(f"SimVar SET {name} => {value}")
    if get_backend() == SIMCONNECT_BACKEND_MOBIFLIGHT:
        v = __get_aq()
    else:
        v = __get_aq().find(name)
    if v is not None:
        # FIXME: explain me
        if get_backend() == SIMCONNECT_BACKEND_MOBIFLIGHT:
            value = str(value)
        v.set(value)
    else:
        # NOTE: Unfortunately, not all SimVars are supported out of the box
        # Only the ones supported by PySimConnect, which are a lot indeed and
        # will do much for you, but still, do not expect to get just any SimVar
        raise SimVarException(
            f"SimVar SET {name}: couldn't find it. SimVar does not exist or likely not supported by current SimConnect backend ..."
        )
