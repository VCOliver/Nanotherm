#  Copyright 2025 Metala Nanofluidos
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#

"""
Logging configuration module for nanotherm.

This module provides logging setup functionality with support for different
logging levels, file rotation, and format configuration.
"""

import logging
import colorlog
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from nanotherm.config.settings import LoggingSettings


def setup_logging(config: Dict[str, Any]) -> None:
    """Configure the application's logging system."""
    level = logging.DEBUG if config["level"] == "DEBUG" else logging.INFO
    format = config["format"]
    date_format = config['date_format']
    
    # Silence matplotlib and PIL debug messages
    logging.getLogger('matplotlib').setLevel(logging.WARNING)
    logging.getLogger('PIL').setLevel(logging.WARNING)
    
    # Split format string to insert colors only around levelname
    parts = format.split("[%(levelname)s]")
    colored_format = (
        f"{parts[0]}%(log_color)s[%(levelname)s]%(reset)s{parts[1]}"
    )
    
    # Console handler with colors
    console_handler = logging.StreamHandler()
    console_formatter = colorlog.ColoredFormatter(
        fmt=colored_format,
        datefmt=date_format,
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'white',
            'WARNING': 'yellow',
            'ERROR':    'light_red',
            'CRITICAL': 'light_yellow',
        },
        secondary_log_colors={
            'message': {
                'CRITICAL': 'red'
            }
        }
    )
    console_handler.setFormatter(console_formatter)

    # Direct configuration of root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(console_handler)

    # File handler with plain formatting
    if config["level"] == "DEBUG":
        # write debug logs into project-root/logs/debug.log
        project_root = Path(__file__).parent.parent.parent.parent
        log_dir = project_root / "logs"
        log_dir.mkdir(exist_ok=True)
        debug_log = log_dir / "debug.log"

        file_handler = RotatingFileHandler(
            debug_log,
            maxBytes=1_000_000,
            backupCount=3
        )
        file_handler.setFormatter(logging.Formatter(fmt=format, datefmt=date_format))
        root_logger.addHandler(file_handler)

    elif config["level"] == "deploy":
        # production logging to /var/log/myproj.log
        file_handler = RotatingFileHandler(
            "/var/log/myproj.log",
            maxBytes=1_000_000,
            backupCount=3
        )
        file_handler.setFormatter(logging.Formatter(fmt=format, datefmt=date_format))
        root_logger.addHandler(file_handler)


def setup_logging_from_settings(logging_settings: "LoggingSettings") -> None:
    """Configure the application's logging system using Pydantic settings."""
    setup_logging({
        "level": logging_settings.level,
        "format": logging_settings.format,
        "date_format": logging_settings.date_format
    })
        
def test_setup():
    """
    For testing only
    """
    
    log = logging.getLogger()
    log.info('This is a INFO log')
    log.debug('This is a DEBUG log')
    log.warning('This is a WARNING log')
    log.error('This is a ERROR log')
    log.critical('This is a CRITICAL log')