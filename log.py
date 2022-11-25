#!/usr/bin/env python3

LOG_LVL_INFO = 0
LOG_LVL_WARN = 1
LOG_LVL_FATAL = 2


def log(level: int, msg: str) -> None:
    level_str = {
        LOG_LVL_INFO: "INFO",
        LOG_LVL_WARN: "WARN",
        LOG_LVL_FATAL: "FATAL",
    }

    print(f"[{level_str[level]}] - {msg}")


def info(msg: str) -> None:
    log(LOG_LVL_INFO, msg)


def warn(msg: str) -> None:
    log(LOG_LVL_WARN, msg)


def error(msg: str) -> None:
    log(LOG_LVL_FATAL, msg)
