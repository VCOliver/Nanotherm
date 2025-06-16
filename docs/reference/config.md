# Configuration Reference

This page documents the configuration system for Nanotherm.

## Configuration Loading

The `config` module handles loading and parsing of application settings from TOML files:

::: nanotherm.config.config

## Logging Configuration

The `logger` module provides logging setup with support for different environments:

::: nanotherm.config.logger

## Configuration Schema

### Logging Section
```toml
[logging]
level = "DEBUG"  # or "deploy"
format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
date_format = "%d-%m-%Y %H:%M:%S"
```

### PID Controller Section
```toml
[pid]
kp = 1.0  # Proportional gain
ki = 0.2  # Integral gain
kd = 0.05 # Derivative gain
```