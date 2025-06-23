#  Copyright 2025 Metala Nanofluidos
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0

"""
Control loop service implementation.
"""

import time
from typing import Protocol
from nanotherm.infrastructure.controllers import PIDController

class ControlLoop:
    """
    Main control loop service.
    
    Handles the execution of the control loop including timing,
    measurement acquisition, and actuation.
    """
    
    def __init__(self, controller: PIDController, sample_time: float):
        self.controller = controller
        self.sample_time = sample_time
        self._running = False
        
    def start(self) -> None:
        """Start the control loop execution."""
        self._running = True
        self._run()
        
    def stop(self) -> None:
        """Stop the control loop execution."""
        self._running = False
        
    def _run(self) -> None:
        """Main control loop."""
        while self._running:
            loop_start = time.monotonic()
            
            # Read measurement
            measurement = self.plant.measure()
            
            # Compute control action
            control_action = self.controller.compute(measurement)
            
            # Apply control action
            self.plant.actuate(control_action)
            
            # Wait for next sample
            elapsed = time.monotonic() - loop_start
            if elapsed < self.sample_time:
                time.sleep(self.sample_time - elapsed)
