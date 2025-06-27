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
import threading
from logging import getLogger
from nanotherm.infrastructure.controllers import PIDController
from nanotherm.core.entities.inputGateway import I_HALGateway

log = getLogger(__name__)

class ControlLoop:
    """
    Main control loop service.
    
    Handles the execution of the control loop including timing,
    measurement acquisition, and actuation.
    """
    
    def __init__(self, controller: PIDController, sample_time: float, gateway: I_HALGateway):
        self.controller = controller
        self.sample_time = sample_time
        self.hal = gateway
        self._stop_event = threading.Event()
        self._thread = None  # Thread for running the control loop

    def start(self) -> None:
        """Start the control loop execution in a separate thread."""
        if self._thread is None or not self._thread.is_alive():
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._run, name='ControlSysThread', daemon=True)
            self._thread.start()
            log.info('Thread {} created'.format(self._thread.name))

    def stop(self) -> None:
        """Stop the control loop execution and wait for the thread to finish."""
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join()
            self._thread = None

    def _run(self) -> None:
        measurement = 0.0
        elapsed = 0.0
        log.info(f"Starting control loop thread: {threading.current_thread().name}")
        
        """Main control loop."""
        while not self._stop_event.is_set():
            loop_start = time.monotonic() 
            
            # Compute control action
            control_action = self.controller.compute(measurement, elapsed) # Simulated output
            measurement = control_action**2 / self.hal.read_value()
            
            # Wait for next sample
            elapsed = time.monotonic() - loop_start
            if elapsed < self.sample_time:
                time.sleep(self.sample_time - elapsed)
