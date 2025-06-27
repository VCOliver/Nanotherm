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
    
    def __init__(self, controller: PIDController, sample_time: float, gateway: I_HALGateway, simulating: bool = False) -> None:
        self.controller = controller
        self.sample_time = sample_time
        self.hal = gateway
        self._stop_event = threading.Event()
        self._thread = None  # Thread for running the control loop
        self._simulation = simulating

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
        log.info('Control loop terminated.')
            
    def _internal_stop(self) -> None:
        """Internal method to stop the control loop."""
        self._stop_event.set()
        log.info('Control loop stopped internally.')
        
    def thread_is_alive(self) -> bool:
        """Check if the control loop thread is still running."""
        return self._thread is not None and self._thread.is_alive()
    
    def wait_for_completion(self):
        """Wait for the control loop thread to finish."""
        if self._thread is not None:
            self._thread.join()

    def _run(self) -> None:
        """
        Main control loop.
        """
        measurement = 0.0
        start_time = time.monotonic()
        simulated_time = 0.0
        def get_time():
            nonlocal simulated_time
            if self._simulation:
                # for example, advance by one sample_time each call
                simulated_time += self.sample_time
                return simulated_time
            else:
                return time.monotonic()
        next_call = start_time
        timestamp = 0.0
        log.info(f"Starting control loop thread: {threading.current_thread().name}")

        while not self._stop_event.is_set():
            now = get_time()
            timestamp = now - start_time

            # Compute control action
            control_action = self.controller.compute(measurement, timestamp)
            measurement = control_action**2 / self.hal.read_value()

            # Check for end of simulation
            if self._simulation and getattr(self.hal, 'reach_end', False):
                log.info('End of simulated data reached. Stopping control loop.')
                self._internal_stop()
                break

            # Schedule next iteration
            sleep_time = 0 if self._simulation else self.sample_time - (now - next_call)
            if sleep_time > 0:
                time.sleep(sleep_time)

