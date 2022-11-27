#!/usr/bin/env python3

LOG_LVL_VERBOSE = -1
LOG_LVL_DEBUG = 0
LOG_LVL_INFO = 1
LOG_LVL_WARN = 2
LOG_LVL_FATAL = 3
LOG_LVL = LOG_LVL_DEBUG  # FIXME: hardcoded (for now)

LEVEL_STR = {
    LOG_LVL_DEBUG: "VERBOSE",
    LOG_LVL_DEBUG: "DEBUG",
    LOG_LVL_INFO: "INFO",
    LOG_LVL_WARN: "WARN",
    LOG_LVL_FATAL: "FATAL",
}


def log(level: int, msg: str) -> None:
    if level >= LOG_LVL:
        print(f"[{LEVEL_STR[level]}] - {msg}")


def verbose(msg: str):
    log(LOG_LVL_VERBOSE, msg)


def debug(msg: str):
    log(LOG_LVL_DEBUG, msg)


def info(msg: str) -> None:
    log(LOG_LVL_INFO, msg)


def warn(msg: str) -> None:
    log(LOG_LVL_WARN, msg)


def error(msg: str) -> None:
    log(LOG_LVL_FATAL, msg)
