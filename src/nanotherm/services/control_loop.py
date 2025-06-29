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
        self._timer_thread = None  # Timer thread for "interrupts"
        self._control_thread = None  # Thread for control loop execution
        self._simulation = simulating
        self._run_event = threading.Event()  # Event to trigger _run execution
        self._start_time = 0.0
        self.__measurement = 0.0

    def start(self) -> None:
        """Start the control loop execution with interrupt-like timing."""
        if (self._timer_thread is None or not self._timer_thread.is_alive()) and \
           (self._control_thread is None or not self._control_thread.is_alive()):
            
            self._stop_event.clear()
            self._start_time = time.monotonic()
            self.__measurement = 0.0
            
            # Start the control thread that waits for "interrupts"
            self._control_thread = threading.Thread(
                target=self._control_worker,
                name='ControlWorkerThread',
                daemon=True
            )
            self._control_thread.start()
            
            # Start the timer thread that generates "interrupts"
            self._timer_thread = threading.Thread(
                target=self._timer_worker,
                name='TimerInterruptThread',
                daemon=True
            )
            self._timer_thread.start()
            
            log.info(f'Control loop started with {self.sample_time*1000:.1f}ms interrupt interval')

    def stop(self) -> None:
        """Stop the control loop execution and wait for threads to finish."""
        self._stop_event.set()
        self._run_event.set()  # Wake up control thread if waiting
        
        if self._timer_thread is not None:
            self._timer_thread.join(timeout=1.0)
            self._timer_thread = None
            
        if self._control_thread is not None:
            self._control_thread.join(timeout=1.0)
            self._control_thread = None
            
        log.info('Control loop terminated.')
            
    def _internal_stop(self) -> None:
        """Internal method to stop the control loop."""
        self._stop_event.set()
        self._run_event.set()  # Wake up control thread
        log.info('Control loop stopped internally.')
        
    def thread_is_alive(self) -> bool:
        """Check if the control loop threads are still running."""
        timer_alive = self._timer_thread is not None and self._timer_thread.is_alive()
        control_alive = self._control_thread is not None and self._control_thread.is_alive()
        return timer_alive and control_alive
    
    def wait_for_completion(self):
        """Wait for the control loop threads to finish."""
        if self._timer_thread is not None:
            self._timer_thread.join()
        if self._control_thread is not None:
            self._control_thread.join()

    def _timer_worker(self) -> None:
        """Timer thread that generates periodic 'interrupts' to trigger control loop execution."""
        log.info(f"Timer interrupt thread started: {threading.current_thread().name}")
        
        next_time = time.monotonic()
        
        while not self._stop_event.is_set():
            next_time += self.sample_time
            
            # Sleep until next interrupt time
            sleep_time = next_time - time.monotonic()
            if sleep_time > 0:
                if self._stop_event.wait(timeout=sleep_time):
                    break  # Stop event was set during sleep
            
            # Generate "interrupt" - signal the control thread to run
            if not self._stop_event.is_set():
                self._run_event.set()
        
        log.info("Timer interrupt thread stopped")

    def _control_worker(self) -> None:
        """Control thread that waits for timer 'interrupts' and executes control logic."""
        log.info(f"Control worker thread started: {threading.current_thread().name}")
        
        while not self._stop_event.is_set():
            # Wait for "interrupt" from timer thread
            if self._run_event.wait(timeout=1.0):  # 1 second timeout to check stop event
                if self._stop_event.is_set():
                    break
                    
                self._run_event.clear()  # Clear the event for next interrupt
                self._run()  # Execute control logic
        
        log.info("Control worker thread stopped")

    def _run(self) -> None:
        """Main control loop execution - called on each 'interrupt'."""
        if self._stop_event.is_set():
            return

        try:
            # Compute control action
            timestamp = time.monotonic() - self._start_time
            control_action = self.controller.compute(self.__measurement, timestamp)
            self.__measurement = control_action**2 / self.hal.read_value()

            # Check simulation end
            if self._simulation and getattr(self.hal, 'reach_end', False):
                log.info('End of simulated data reached. Stopping control loop.')
                self._internal_stop()
                return

        except Exception as e:
            log.error(f"Error in control loop: {e}")
            self._internal_stop()
            return