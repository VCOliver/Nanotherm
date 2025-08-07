#  Copyright 2025 Metala Nanofluidos
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0

"""
Gateway module for hardware abstraction layer implementations.

This module provides platform-specific gateway implementations for different
hardware platforms including desktop simulation and Raspberry Pi hardware.
"""

from .data_gateway import GatewayFactory, get_platform_gateway
from .simul_data_gateway import CSV_HALGateway

# Raspberry Pi gateway is only available if RPi.GPIO is installed
try:
    from .raspi_gateway import RaspberryPiHALGateway
    __all__ = [
        "GatewayFactory",
        "get_platform_gateway", 
        "CSV_HALGateway",
        "RaspberryPiHALGateway"
    ]
except ImportError:
    __all__ = [
        "GatewayFactory",
        "get_platform_gateway", 
        "CSV_HALGateway"
    ]