# !/usr/bin/env python3
#  -*- coding: utf-8 -*-
#
#  Copyright 2025 Metala Nanofluidos
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging(config: dict[str]) -> None:
    """
    setup
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
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt=date_format,
        handlers=handlers
    )