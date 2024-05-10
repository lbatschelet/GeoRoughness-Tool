"""
log_config.py
-----------
Version: 1.0.9
Author: Lukas Batschelet
Date: 08.05.2024
-----------
This module sets up the logging for the application.
"""

import logging
import os


def setup_logging():
    log_directory = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_directory, exist_ok=True)

    levels = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    handlers = {}
    for level_name, level in levels.items():
        handler = logging.FileHandler(os.path.join(log_directory, f'{level_name}.log'), 'w')  # Open in write mode
        handler.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        handlers[level_name] = handler

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    for handler in handlers.values():
        logger.addHandler(handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)

# Brief description of logging levels:
# DEBUG: Detailed information, typically of interest only when diagnosing problems.
# INFO: Confirmation that things are working as expected.
# WARNING: An indication that something unexpected happened, or indicative of some problem in the near future (e.g. 'disk space low'). The software is still working as expected.
# ERROR: Due to a more serious problem, the software has not been able to perform some function.
# CRITICAL: A serious error, indicating that the program itself may be unable to continue running.
