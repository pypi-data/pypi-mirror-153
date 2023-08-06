# Copyright (C) 2019 ETH Zurich,
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher Oct 2019

import logging
import sys


class CustomFormatter(logging.Formatter):
    """
    Class to handle customization of logger output format.
    """

    def __init__(self, colorized=True):
        RED = '\033[91m'
        VIOLET = '\033[95m'
        YELLOW = '\033[93m'
        BOLD = '\033[1m'
        # UNDERLINE = '\033[4m'
        ENDC = '\033[0m'

        format = "%(asctime)s - %(filename)12s:%(lineno)4d" \
            " - %(levelname)7s - %(message)s"

        if colorized:
            self.FORMATS = {
                logging.DEBUG: VIOLET + format + ENDC,
                logging.INFO: format,
                logging.WARNING: BOLD + YELLOW + format + ENDC,
                logging.ERROR: BOLD + RED + format + ENDC,
                logging.CRITICAL: BOLD + RED + format + ENDC
            }
        else:
            self.FORMATS = {
                logging.DEBUG: format,
                logging.INFO: format,
                logging.WARNING: format,
                logging.ERROR: format,
                logging.CRITICAL: format
            }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        new = formatter.format(record)
        return new


def init_logger(name, logging_level=3, colorized=True):
    """
    Initializes a logger instance for a file.
    :param name: The name of the file for which the logging is done.
    :param colorized: If True uses coloring of logger messages.
    :return: Logger instance
    """
    if not isinstance(name, str):
        raise ValueError(f'filepath must be a string not {name}')

    logger = logging.getLogger(name)

    # create console handler with a higher log level
    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setFormatter(CustomFormatter(colorized=colorized))

    # if handlers exist already remove them
    if logger.hasHandlers():
        for hdl in logger.handlers:
            logger.removeHandler(hdl)
    logger.addHandler(ch)

    set_logger_level(logger, logging_level)
    return logger


def set_logger_level(logger, level):
    """
    Sets the global logging level. Meassages with a logging level below will
    not be logged.

    :param logger: A logger instance.
    :param logging_level: The logger severity
                          (critical, error, warning, info or debug)
    """

    logging_levels = {0: logging.CRITICAL,
                      1: logging.ERROR,
                      2: logging.WARNING,
                      3: logging.INFO,
                      4: logging.DEBUG}

    if level not in logging_levels.keys():
        raise ValueError(
            f"Logging level must be an integer from 0 to 4 not {level}")

    logger.setLevel(logging_levels[level])


def vprint(message, logger=None, verbose=False, level='info'):
    """
    DEPRECATED. Only for backward compatibility
    Prints a message if verbose is True.
    Can also redirect output to a logger instance.

    :param message: The message string to print.
    :param logger: Either a logger instance or None
    :param verbose: If True prints the message
    :param level: The severity level of the message (either info, warning,
                  error or debug)
    """
    if logger is not None:
        logger.warning(
            "DEPRECATION WARNING: Use LOGGER.<level>() "
            "interface instead of vprint()")
    else:
        print(
            "DEPRECATION WARNING: "
            "Use LOGGER.<level>() interface instead of vprint()")

    if verbose:
        if logger is not None:
            getattr(logger, level)(message)
        else:
            print('{} : {}'.format(level, message))
    else:
        pass
