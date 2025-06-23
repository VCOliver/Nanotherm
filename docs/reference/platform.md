# Platform Detection Module

This module provides enums and utility classes to detect and identify the current hardware platform and operating system the code is running on.

## Source Reference

::: nanotherm.config.platform

## Usage Example

```python
from nanotherm.config.platform import Platform

system = Platform.get_system()
hardware = Platform.get_hardware_type()

print(f"System platform: {system}")
print(f"Hardware type: {hardware}")
```

## Enums

- `HardwareType`: Types of hardware platforms (e.g., Raspberry Pi, Desktop, MCU, Unknown)
- `SystemPlatform`: Types of operating systems (e.g., Linux, Windows, Unknown)

## Classes

- `Platform`: Utility class for platform detection and identification.