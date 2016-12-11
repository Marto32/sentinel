"""
This module houses functions that help to set loggers in any script being run
on mm_platform. This works in tandum with the logging configuration file. For
more information on logging configuration, see the docs at

Config Setup: https://docs.python.org/3.5/library/logging.config.html
Config Parser: https://docs.python.org/3.5/library/configparser.html
"""
import logging
import logging.config
import os


def get_logger(logger_name):
    """
    Retrieves a logger from the environment's logging configuration file.
    This file is defined by the environment variable "LOGCONFIG"

    :param logger_name: string, the name of the logger to retrieve
    :returns: logger object
    """
    try:
        logging_config_file = os.environ['LOGCONFIG']
    except KeyError:
        raise Exception("There is no LOGCONFIG variable set in this os "
            "environment. Set this variable to point to the logging "
            "configuration file.")

    logging.config.fileConfig(logging_config_file)
    return logging.getLogger(logger_name)

