# coding=utf-8
"""The logging module provides print function with color (or label) and logging"""
import logging
import sys
import traceback
from functools import wraps
from pprint import pprint
from typing import Callable
from contextlib import contextmanager

from maxoptics.core.utils import decohints
from maxoptics.config import Config, BASEDIR

Color = Config.Color

logging.basicConfig(
    handlers=[
        logging.FileHandler(
            (BASEDIR / "var" / "log" / "maxoptics.log"), "a", "utf-8"
        )
    ],
    format="%(asctime)s:: %(levelname)s: %(message)s",
    datefmt="%m-%dikt %H:%M",
)
logger = logging.getLogger("maxoptics.sdk")


class LoggerCapturer:
    """Capture Exception and logging"""

    def __enter__(self):
        return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.error("Error", exc_info=True)


@decohints
def logging_error(func: Callable):
    """A decorator. Error in the function will be logged.

    Args:
        func (Callable[[...], T): any func.

    Returns:
        Callable[[...], T
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        with LoggerCapturer():
            ret = func(*args, **kwargs)

        return ret

    return wrapper


@decohints
def logging_error_method(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # with LoggerCapturer():
        try:
            ret = func(*args, **kwargs)
        finally:
            traceback.print_exc()
            if all(sys.exc_info()):
                logger.error("Exception Recoding:", exc_info=True)
        return ret

    return classmethod(wrapper)


@contextmanager
def inc_print_level(end="\n", **kwargs):
    """Increase #indentation when 'enter'. Recover when 'exit'.
    Do layered printing.

    Args:
        end(str): If end is "", the #indentation are temporarily set as 0.

    Yields:
        The current #indentation.
    """

    print_level_record = Config.__print_level__
    try:
        if end == "":
            Config.__print_level__ = 0
        else:
            Config.__print_level__ += 1

        yield Config.__print_level__
    finally:
        Config.__print_level__ = print_level_record


def success_print(txt, *args, **kargs):
    """Print a SUCCESS message. If Color is True, printing will be light green."""
    txt = "  " * Config.__print_level__ + txt
    if Color:
        print("\033[32m%s\033[0m" % txt, *args, **kargs)
    else:
        print("SUCCESS: %s  " % txt, *args, **kargs)
    return inc_print_level(**kargs)


def error_print(txt, *args, **kargs):
    """Print a ERROR message. If Color is True, printing will be red."""
    txt = "  " * Config.__print_level__ + txt
    if Color:
        print("\033[31m%s\033[0m" % txt, *args, **kargs)
    else:
        print("ERROR: %s  " % txt, *args, **kargs)
    logger.error(txt)
    return inc_print_level(**kargs)


def info_print(txt, *args, **kargs):
    """Print a INFO message. If Color is True, printing will be azure."""
    txt = "  " * Config.__print_level__ + txt
    if Color:
        print("\033[36m%s\033[0m" % txt, *args, **kargs)
    else:
        print("INFO: %s  " % txt, *args, **kargs)
    logger.info(txt)
    return inc_print_level(**kargs)


def warn_print(txt, *args, **kargs):
    """Print a WARNING message. If Color is True, printing will be orange."""
    txt = "  " * Config.__print_level__ + txt
    if Color:
        print("\033[35m%s\033[0m" % txt, *args, **kargs)
    else:
        print("WARNING: %s  " % txt, *args, **kargs)
    logger.warning(txt)
    return inc_print_level(**kargs)


def debug_print(*args, **kwargs):
    """Print messages when Debug is True"""
    if Config.Debug:
        print("\033[35m")
        print(*args, **kwargs)
        print("\033[0m")


def debug_pprint(*args, **kwargs):
    """Pretty print messages when Debug is True"""
    if Config.Debug:
        print("\033[35m")
        pprint(*args, **kwargs)
        print("\033[0m")
