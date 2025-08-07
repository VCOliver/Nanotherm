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

"""
Configuration module for nanotherm.

This module provides Pydantic-based configuration management with support
for TOML files, environment variables, and validation.

All configuration-related functionality is available through the settings module.
"""

# Re-export everything from settings for convenience
from .settings import *

__all__ = [
    # Settings classes
    "LoggingSettings",
    "PIDSettings", 
    "LiverTransferFunctionSettings",
    "ControlSystemSettings",
    "PlotsSettings",
    "NanothermSettings",
    # Functions
    "load_settings",
    "setup_logging_from_settings",
    # Platform
    "Platform",
    "HardwareType", 
    "HardwareError",
]