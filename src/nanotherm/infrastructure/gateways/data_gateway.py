#  Copyright 2025 Metala Nanofluidos
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0

"""
Data Gateway interface and implementations for different hardware platforms.

This module provides concrete implementations of the HAL Gateway for different
hardware platforms, with automatic platform detection and selection.
"""

import logging
from typing import Optional, Union

from nanotherm.config.settings import HardwareType, Platform, HardwareError
from nanotherm.core.entities.inputGateway import I_HALGateway

log = logging.getLogger(__name__)


class GatewayFactory:
    """Factory class for creating the appropriate HAL Gateway based on platform."""
    
    @staticmethod
    def create_gateway(platform: HardwareType, **kwargs) -> I_HALGateway:
        """
        Create and return the appropriate HAL Gateway for the detected platform.
        
        Args:
            platform: The hardware platform type
            **kwargs: Additional arguments to pass to the gateway constructor
            
        Returns:
            I_HALGateway: The appropriate gateway implementation
            
        Raises:
            HardwareError: If the platform is not supported
        """
        if platform == HardwareType.DESKTOP:
            from nanotherm.infrastructure.gateways.simul_data_gateway import CSV_HALGateway
            csv_path = kwargs.get('csv_path', 'data/input/combined.csv')
            return CSV_HALGateway(csv_path)
            
        elif platform == HardwareType.RASPBERRY_PI:
            from nanotherm.infrastructure.gateways.raspi_gateway import RaspberryPiHALGateway
            # Filter out arguments that are not relevant for RaspberryPiHALGateway
            raspi_kwargs = {k: v for k, v in kwargs.items() 
                           if k not in ['csv_path']}  # Remove desktop-specific args
            return RaspberryPiHALGateway(**raspi_kwargs)
            
        else:
            raise HardwareError(f"Unsupported hardware platform: {platform}")


def get_platform_gateway(**kwargs) -> I_HALGateway:
    """
    Convenience function to automatically detect platform and create appropriate gateway.
    
    Args:
        **kwargs: Additional arguments to pass to the gateway constructor
        
    Returns:
        I_HALGateway: The appropriate gateway implementation for the current platform
    """
    platform = Platform.get_hardware_type()
    log.info(f"Detected platform: {platform}")
    return GatewayFactory.create_gateway(platform, **kwargs)

