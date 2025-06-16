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

from dataclasses import dataclass

@dataclass(frozen=True)
class PIDParams:
    """
    Holds the proportional, integral, and derivative gains
    for a PID controller.
    """
    kp: float
    ki: float
    kd: float