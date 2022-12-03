# -*- coding: utf-8 -*-

from .client import (
    connect,
    disconnect,
)

from .const import (
    SIMCONNECT_BACKEND_DEFAULT,
    SIMCONNECT_BACKEND_MOBIFLIGHT,
    SIMCONNECT_BACKEND_DEFAULT_NAME,
    SIMCONNECT_BACKEND_MOBIFLIGHT_NAME,
)

from .backend import get_backend, set_backend
from .variables import set_variable, get_variable, SimVar
from .events import send_event
from .poll import subscribe_to_simvar, poll_start, poll_stop
