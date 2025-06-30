# Application Reference

This page documents the core application components of Nanotherm.

## Overview

The `app` module contains the main application class that orchestrates:
- Component lifecycle management
- Control loop execution
- Error handling and shutdown procedures

## Module Documentation

::: nanotherm.app.app

---

**Imports:**
- [PIDParams](core/domain/pid_params.md)
- [Discrete Transfer Function](core/entities/DTransferFunction.md)
- [PID Controller](core/infrastructure/pid_controller.md)
- [Simulation Gateway](core/infrastructure/simulation_gateway.md)
- [Control Loop](core/services/control_loop.md)