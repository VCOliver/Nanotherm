#  Copyright 2025 Metala Nanofluidos
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#

"""
Configuration loader module for nanotherm.

This module handles loading and parsing of the application configuration
from TOML files. It provides functionality to read and validate configuration
settings used throughout the application.
"""

from typing import Any, Dict
import logging
import toml
from pathlib import Path
from nanotherm.config.platform import HardwareType

TOML_PATH = Path("src/nanotherm/config.toml")

def load_config(platform: HardwareType) -> Dict[str, Any]:
    """
    Load application configuration from TOML file.

    Returns:
        Dict[str, Any]: Configuration dictionary containing all application settings

    Raises:
        FileNotFoundError: If the config.toml file cannot be found
        toml.TomlDecodeError: If the TOML file contains syntax errors
    """
    # The file is opened in normal text mode, e.g., "r"
    try:
        with open(TOML_PATH, "r") as f:
            config_data = toml.load(f)


        return config_data

    except FileNotFoundError as e:
        #print(e)
        logging.basicConfig(level=logging.CRITICAL)
        log = logging.getLogger(__name__)
        log.critical("Error: config.toml not found.")
        exit(1)
    except toml.TomlDecodeError as e:
        #print(e)
        logging.basicConfig(level=logging.CRITICAL)
        log = logging.getLogger(__name__)
        log.critical("Error: Could not decode the TOML file. Check for syntax errors.")
        exit(1)
