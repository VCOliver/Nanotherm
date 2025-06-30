#  Copyright 2025 Metala Nanofluidos
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0

"""
Control loop service implementation with interrupt-like timing.
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
    
    Handles the execution of the control loop with interrupt-like timing,
    measurement acquisition, and actuation.
    """
    
    def __init__(self, controller: PIDController, sample_time: float, gateway: I_HALGateway, simulating: bool = False) -> None:
        self.controller = controller
        self.sample_time = sample_time
        self.hal = gateway
        self._stop_event = threading.Event()
        self._timer_thread = None  # Timer thread that directly calls _run()
        self._simulation = simulating
        self._start_time = 0.0
        self._measurement = 0.0
        self._simulation_data = []  # Store simulation results

    def start(self) -> None:
        """Start the control loop execution with interrupt-like timing."""
        if self._timer_thread is None or not self._timer_thread.is_alive():
            
            self._stop_event.clear()
            self._start_time = time.monotonic() if not self._simulation else 0.0
            self._measurement = 0.0
            self._timestamp = 0.0
            
            # Start the timer thread that directly calls _run()
            self._timer_thread = threading.Thread(
                target=self._timer_worker,
                name='ControlTimerThread',
                daemon=True
            )
            self._timer_thread.start()
            
            log.info(f'Control loop started with {self.sample_time*1000:.1f}ms interrupt interval')

    def stop(self) -> None:
        """Stop the control loop execution and wait for thread to finish."""
        self._stop_event.set()
        
        if self._timer_thread is not None:
            self._timer_thread.join(timeout=1.0)
            self._timer_thread = None
            
        log.info('Control loop terminated.')
            
    def _internal_stop(self) -> None:
        """Internal method to stop the control loop."""
        self._stop_event.set()
        log.info('Control loop stopped internally.')
        
    def thread_is_alive(self) -> bool:
        """Check if the control loop thread is still running."""
        return self._timer_thread is not None and self._timer_thread.is_alive()
    
    def wait_for_completion(self):
        """Wait for the control loop thread to finish."""
        if self._timer_thread is not None:
            self._timer_thread.join()

    def get_simulation_data(self):
        """Get the collected simulation data."""
        return self._simulation_data.copy()
    
    def clear_simulation_data(self):
        """Clear the simulation data."""
        self._simulation_data.clear()

    def _timer_worker(self) -> None:
        """Timer thread that periodically calls the control loop directly."""
        log.info(f"Timer thread started: {threading.current_thread().name}")
        
        next_time = time.monotonic()
        
        while not self._stop_event.is_set():
            next_time += self.sample_time
            
            # Sleep until next execution time
            sleep_time = next_time - time.monotonic()
            if sleep_time > 0:
                if self._stop_event.wait(timeout=sleep_time):
                    break  # Stop event was set during sleep
            
            if not self._stop_event.is_set():
                self._run()
        
        log.info("Timer thread stopped")

    def _run(self) -> None:
        """Main control loop execution - called on each 'interrupt'."""
        if self._stop_event.is_set():
            return

        try:
            # Compute control action
            timestamp = time.monotonic() - self._start_time
            if self._simulation:
                self._timestamp += self.controller.Ts
            else:
                self._timestamp = timestamp
            control_action = self.controller.compute(self._measurement, self._timestamp)
            resistance = self.hal.read_value()
            self._measurement = control_action**2 / resistance

            # Log simulation data if simulating
            if self._simulation:
                setpoint = self.controller.setpoint
                
                self._simulation_data.append({
                    'timestamp': self._timestamp,
                    'resistence': resistance,
                    'control_action': control_action,
                    'setpoint': setpoint,
                    'measurement': self._measurement,
                })

            # Check simulation end
            if self._simulation and getattr(self.hal, 'reach_end', False):
                log.info('End of simulated data reached. Stopping control loop.')
                self._internal_stop()
                return

        except Exception as e:
            log.error(f"Error in control loop: {e}")
            self._internal_stop()
            return