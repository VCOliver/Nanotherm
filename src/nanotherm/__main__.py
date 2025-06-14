# !/usr/bin/env python3
#  -*- coding: utf-8 -*-
#
#  Copyright {year} Metala Nanofluidos
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#

"""
Main module for the nanotherm application.

This module handles the application's entry point and logging configuration.
It provides functionality to set up logging based on different running modes
(debug or deployment).
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logging(mode: str) -> None:
    """
    Configure the logging system based on the specified mode.

    Args:
        mode (str): The logging mode to use. Can be either 'debug' or 'deploy'.
            - 'debug': Enables debug level logging and writes to both console and a debug.log file
            - 'deploy': Uses info level logging and writes to both console and system log file

    The function sets up:
        - Console logging for all modes
        - File logging with rotation (max 3 files of 1MB each)
        - Different log paths based on mode
    """
    level = logging.DEBUG if mode == "debug" else logging.INFO
    handlers = [logging.StreamHandler()]

    if mode == "debug":
        # write debug logs into project-root/logs/debug.log
        project_root = Path(__file__).parent.parent.parent
        log_dir = project_root / "logs"
        log_dir.mkdir(exist_ok=True)
        debug_log = log_dir / "debug.log"

        handlers.append(RotatingFileHandler(
            debug_log,
            maxBytes=1_000_000,
            backupCount=3
        ))

    elif mode == "deploy":
        # production logging to /var/log/myproj.log as before
        handlers.append(RotatingFileHandler(
            "/var/log/myproj.log",
            maxBytes=1_000_000,
            backupCount=3
        ))

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=handlers
    )
    
logger = logging.getLogger(__name__)

def main():
    """
    Main entry point for the nanotherm application.
    
    Initializes the application and starts the main processing loop.
    """
    setup_logging('debug')
    logger.info("Nanotherm application started in debug mode.")
    print("Hello, world!")
    
if __name__=='__main__':
    main()