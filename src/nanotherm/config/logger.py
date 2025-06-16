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
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Dict, Any


def setup_logging(config: Dict[str, Any]) -> None:
    """
    Configure the application's logging system.

    Args:
        config: Dictionary containing logging configuration with keys:
            - level: Logging level ("DEBUG" or "INFO")
            - format: Log message format string
            - date_format: Date format string for timestamps

    The function sets up:
        - Console logging for all modes
        - File logging with rotation (max 3 files of 1MB each)
        - Debug logs in project/logs/debug.log for debug mode
        - Production logs in /var/log/myproj.log for deploy mode
    """
    level = logging.DEBUG if config["level"] == "DEBUG" else logging.INFO
    format = config["format"]
    date_format = config['date_format']
    handlers = [logging.StreamHandler()]

    if config["level"] == "DEBUG":
        # write debug logs into project-root/logs/debug.log
        project_root = Path(__file__).parent.parent.parent.parent
        log_dir = project_root / "logs"
        log_dir.mkdir(exist_ok=True)
        debug_log = log_dir / "debug.log"

        handlers.append(RotatingFileHandler(
            debug_log,
            maxBytes=1_000_000,
            backupCount=3
        ))

    elif config["level"] == "deploy":
        # production logging to /var/log/myproj.log as before
        handlers.append(RotatingFileHandler(
            "/var/log/myproj.log",
            maxBytes=1_000_000,
            backupCount=3
        ))

    logging.basicConfig(
        level=level,
        format=format,
        datefmt=date_format,
        handlers=handlers
    )