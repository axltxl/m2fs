# -*- coding: utf-8 -*-

# This client will try for up to 5 minutes
# before giving up in connect to the flight sim
SIMCONNECT_TIMEOUT_SECONDS = 300

# For how long is Python-SimConnect caching
# local SimVar data?
SIMCONNECT_CACHE_TICK_RATE_HZ = 33
SIMCONNECT_CACHE_TTL_MS = 1000.0 / SIMCONNECT_CACHE_TICK_RATE_HZ

# SimConnect client backends
SIMCONNECT_BACKEND_DEFAULT = 0
SIMCONNECT_BACKEND_MOBIFLIGHT = 1
SIMCONNECT_BACKEND_DEFAULT_NAME = "Python-SimConnect"
SIMCONNECT_BACKEND_MOBIFLIGHT_NAME = "MobiFlight-SimConnect"
