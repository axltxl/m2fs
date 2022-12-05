# -*- coding: utf-8 -*-
"""
backend identification stuff
"""

from .const import (
    SIMCONNECT_BACKEND_DEFAULT,
    SIMCONNECT_BACKEND_MOBIFLIGHT,
    SIMCONNECT_BACKEND_DEFAULT_NAME,
    SIMCONNECT_BACKEND_MOBIFLIGHT_NAME,
)

__sm_backend = SIMCONNECT_BACKEND_DEFAULT


def get_backend() -> int:
    """Get currently chosen backend"""

    global __sm_backend
    return __sm_backend


def set_backend(backend: int) -> None:
    """Set currently chosen backend"""

    global __sm_backend
    __sm_backend = backend


def get_backend_name() -> str:
    """Get backend name as a string"""

    global __sm_backend
    if __sm_backend == SIMCONNECT_BACKEND_MOBIFLIGHT:
        return SIMCONNECT_BACKEND_MOBIFLIGHT_NAME
    return SIMCONNECT_BACKEND_DEFAULT_NAME
