#  Copyright 2025 Metala Nanofluidos
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0

"""Platform detection module for hardware and operating system identification.

This module provides enums and utility classes to detect and identify the current
hardware platform and operating system the code is running on.
"""

from enum import Enum
import platform
from typing import Final

class HardwareType(Enum):
    """Enum representing different types of hardware platforms."""
    RASPBERRY_PI: Final[str] = "raspberry"
    DESKTOP: Final[str] = "desktop"
    MCU: Final[str] = "mcu"
    UNKNOWN: Final[str] = "unknown"

class SystemPlatform(Enum):
    """Enum representing different operating system platforms."""
    LINUX: Final[str] = "linux"
    WINDOWS: Final[str] = "windows"
    UNKNOWN: Final[str] = "unknown"

class Platform:
    """Utility class for platform detection and identification."""

    @staticmethod
    def get_system() -> SystemPlatform:
        """Detect the current operating system.

        Returns:
            SystemPlatform: The detected operating system platform.
        """
        system = platform.system().lower()
        if system == "linux":
            return SystemPlatform.LINUX
        elif system == "windows":
            return SystemPlatform.WINDOWS
        return SystemPlatform.UNKNOWN

    @staticmethod
    def get_hardware_type() -> HardwareType:
        """Detect the current hardware platform.

        Returns:
            HardwareType: The detected hardware platform type.
        """
        node = platform.node().lower()
        machine = platform.machine().lower()
        
        # Check for Raspberry Pi based on node and machine
        if "raspberrypi" in node and  machine in ("arm", "aarch64"):
            return HardwareType.RASPBERRY_PI
        elif Platform.get_system() in [SystemPlatform.LINUX, SystemPlatform.WINDOWS]:
            return HardwareType.DESKTOP
        elif "mcu" in node:
            return HardwareType.MCU
        return HardwareType.UNKNOWN