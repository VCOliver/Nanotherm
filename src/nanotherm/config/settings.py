#  Copyright 2025 Metala Nanofluidos
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#

"""
Pydantic settings configuration for nanotherm.

This module defines the application configuration using Pydantic models
with support for environment variables, .env files, and TOML configuration.

This module serves as the main entry point for all configuration-related functionality,
re-exporting platform utilities and logger functions for convenience.
"""

from pathlib import Path
from typing import List, Literal, TYPE_CHECKING
from pydantic import BaseModel, Field, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict

# Re-export platform utilities
from nanotherm.config.platform import HardwareType, Platform, HardwareError

# Import logger function for re-export
if TYPE_CHECKING:
    from nanotherm.config.logger import LoggingSettings as _LoggingSettings


class LoggingSettings(BaseModel):
    """Configuration for logging system."""
    
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "deploy"] = Field(
        default="DEBUG",
        description="Logging level"
    )
    format: str = Field(
        default="%(asctime)s [%(levelname)s] %(module)s: %(message)s",
        description="Log message format"
    )
    date_format: str = Field(
        default="%d-%m-%Y %H:%M:%S",
        description="Date format for log messages"
    )


class PIDSettings(BaseModel):
    """Configuration for PID controller parameters."""
    
    kp: float = Field(
        default=1.2,
        description="Proportional gain",
        gt=0
    )
    ki: float = Field(
        default=0.14,
        description="Integral gain",
        ge=0
    )
    kd: float = Field(
        default=0.2,
        description="Derivative gain",
        ge=0
    )


class LiverTransferFunctionSettings(BaseModel):
    """Configuration for liver transfer function."""
    
    num: List[float] = Field(
        default=[0.1632, -0.1561],
        description="Numerator coefficients of the transfer function"
    )
    den: List[float] = Field(
        default=[1.0, -1.837, 0.8442],
        description="Denominator coefficients of the transfer function"
    )


class ControlSystemSettings(BaseModel):
    """Configuration for control system parameters."""
    
    setpoint: float = Field(
        default=5.0,
        description="Control system setpoint",
        ge=0
    )
    sampling_time: float = Field(
        default=2.0,
        description="Sampling time in seconds",
        gt=0
    )


class PlotsSettings(BaseModel):
    """Configuration for plots output."""
    
    output_dir: str = Field(
        default="plots",
        description="Output directory for plots"
    )


class NanothermSettings(BaseSettings):
    """Main configuration settings for the nanotherm application."""
    
    model_config = SettingsConfigDict(
        # Read from TOML file
        toml_file='config.toml',
        # Also support environment variables with NANOTHERM_ prefix
        env_prefix='NANOTHERM_',
        # Allow nested environment variables (e.g., NANOTHERM_PID__KP)
        env_nested_delimiter='__',
        # Case sensitivity
        case_sensitive=False,
        # Read from .env file if present
        env_file='.env',
        env_file_encoding='utf-8',
        # Extra fields handling
        extra='forbid'
    )
    
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    pid: PIDSettings = Field(default_factory=PIDSettings)
    liver_tf: LiverTransferFunctionSettings = Field(default_factory=LiverTransferFunctionSettings)
    control_system: ControlSystemSettings = Field(default_factory=ControlSystemSettings)
    plots: PlotsSettings = Field(default_factory=PlotsSettings)
    
    # Platform will be set programmatically
    platform: HardwareType = Field(default=HardwareType.DESKTOP, description="Hardware platform type")


def load_settings(platform: HardwareType, config_file_path: Path | None = None) -> NanothermSettings:
    """
    Load application settings from configuration sources.
    
    Args:
        platform: The hardware platform type
        config_file_path: Optional path to configuration file
        
    Returns:
        NanothermSettings: Loaded and validated configuration
    """
    # If a specific config file path is provided, use it
    if config_file_path:
        # Create a temporary settings class with custom toml_file
        class CustomSettings(NanothermSettings):
            model_config = SettingsConfigDict(
                toml_file=str(config_file_path),
                env_prefix='NANOTHERM_',
                env_nested_delimiter='__',
                case_sensitive=False,
                env_file='.env',
                env_file_encoding='utf-8',
                extra='forbid'
            )
        
        settings = CustomSettings()
    else:
        # Look for config.toml in standard locations
        config_paths = [
            Path("config.toml"),
            Path("src/nanotherm/config.toml"),
            Path(__file__).parent / "config.toml"
        ]
        
        settings = None
        for config_path in config_paths:
            if config_path.exists():
                class CustomSettings(NanothermSettings):
                    model_config = SettingsConfigDict(
                        toml_file=str(config_path),
                        env_prefix='NANOTHERM_',
                        env_nested_delimiter='__',
                        case_sensitive=False,
                        env_file='.env',
                        env_file_encoding='utf-8',
                        extra='forbid'
                    )
                
                settings = CustomSettings()
                break
        
        # Fallback to default settings if no config file found
        if settings is None:
            settings = NanothermSettings()
    
    # Set the platform
    settings.platform = platform
    
    return settings


# Re-export logger function for convenience
def setup_logging_from_settings(logging_settings: "LoggingSettings") -> None:
    """Configure the application's logging system using Pydantic settings."""
    from nanotherm.config.logger import setup_logging_from_settings as _setup_logging
    return _setup_logging(logging_settings)
