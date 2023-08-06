#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import logging.handlers
import os
import sys


def get_logger(logger_name: str, log_file: str = "file.log", log_dir: str = "logs",
               log_to_console: bool = False, log_to_file: bool = False, size: int = 20_048_576) -> logging.Logger:
    """ Create and return custom logger to use in modules of the miRMag project.
        This logger can write data to the console, to the files, and both to the console and the files at the same time.

    :param logger_name: Name of the logger object.
    :param log_file: Name of the file with the logs.
    :param log_dir: Full path to the directory with the log-files.
    :param log_to_console: True (write logs to console), False (do not).
    :param log_to_file: True (write logs to file), False (do not).
    :param size: Size of one log-file.
    :return: Custom python object logging.Logger.
    """

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)              # set default maximum logging level!

    if log_to_console:
        logger.addHandler(logging.StreamHandler(sys.stdout))

    if log_to_file:
        os.makedirs(log_dir, exist_ok=True)
        formatter = logging.Formatter("[%(levelname).1s] [%(asctime)s] — line:%(lineno)d — %(message)s")
        handler_file = logging.handlers.RotatingFileHandler(filename=os.path.join(log_dir, log_file), maxBytes=size, backupCount=10, encoding="utf-8")
        handler_file.setFormatter(formatter)
        logger.addHandler(handler_file)

    return logger


if __name__ == "__main__":
    """ Examples / Use cases. """

    # Init custom loggers
    test_logger1 = get_logger(logger_name="name1", log_file=r"test.log", log_dir=r"logs/dir", log_to_console=True, log_to_file=True, size=256)
    test_logger2 = get_logger(logger_name="name2", log_to_console=True, log_to_file=False)

    # Logging the messages
    test_logger1.debug("Debug error1.")
    test_logger2.debug("Debug error2.")

    test_logger1.info("Info message1.")
    test_logger2.info("Info message2.")

    test_logger1.warning("Warning error1.")
    test_logger2.warning("Warning error2.")

    test_logger1.error("Simple error1.")
    test_logger2.error("Simple error2.")

    test_logger1.fatal("Fatal error1.")
    test_logger2.fatal("Fatal error2.")

    test_logger1.critical("Critical error1.")
    test_logger2.critical("Critical error2.")

    try:
        1 / 0
    except ZeroDivisionError as e:
        test_logger1.exception("Exception error1.")

    try:
        1 / 0
    except ZeroDivisionError as e:
        test_logger2.exception("Exception error2.")

    # flush data, close handlers and shutdown the loggers
    logging.shutdown()
