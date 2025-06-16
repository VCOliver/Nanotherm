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

from typing import Any
import toml

TOML_PATH="src/nanotherm/config.toml"

def load_config() -> dict[str, Any]:
    # The file is opened in normal text mode, e.g., "r"
    try:
        with open(TOML_PATH, "r") as f:
            config_data = toml.load(f)

        return config_data

    except FileNotFoundError as e:
        print(e)
        print("Error: config.toml not found.")
    except toml.TomlDecodeError as e:
        print(e)
        print("Error: Could not decode the TOML file. Check for syntax errors.")
