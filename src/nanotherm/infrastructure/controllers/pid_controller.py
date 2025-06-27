#  Copyright 2025 Metala Nanofluidos
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0

"""
PID controller implementation.

Provides a discrete-time PID controller using transfer function representation.
"""

import control as ctrl
import numpy as np
import matplotlib.pyplot as plt
from nanotherm.core.entities.DTransferFunction import DiscreteTransferFunction
from nanotherm.core.entities.controller import IController
from nanotherm.core.domain.pid_params import PIDParams
import logging
from typing import Tuple
from pathlib import Path
from datetime import datetime

log = logging.getLogger(__name__)

class PIDController(IController):
    """
    A discrete-time PID controller implemented as a transfer function C(z).
    """
    
    def __init__(self, gains: PIDParams, plant: DiscreteTransferFunction, setpoint: float = 1.0, Ts: float = 1.0) -> None:
        self.kp = gains.kp
        self.ki = gains.ki
        self.kd = gains.kd
        self.plant = plant
        self._setpoint = setpoint
        self.Ts = Ts
        self._tf = self._build_tf()
        self._last_error = 0.0
        self._last_time = None 
        self._integral = 0.0
        
        log.debug(f'Controller instance created with setpoint = {self._setpoint} and sampling time = {self.Ts}')
    
    def _build_tf(self) -> ctrl.TransferFunction:
        """
        
            
        Returns:
            The complete discrete-time PID controller transfer function
        """
        # Proportional term
        C_p = ctrl.TransferFunction([self.kp], [1], self.Ts)

        # Integral term: Ki * Ts / (z - 1)
        C_i = ctrl.TransferFunction([self.ki * self.Ts], [1, -1], self.Ts)

        # Derivative term: Kd * (z - 1) / Ts
        C_d = ctrl.TransferFunction([self.kd, -self.kd], [self.Ts, 0], self.Ts)

        Hz = C_p + C_i + C_d # Full PID Transfer Function
        Gz = self.plant.tf   # Plant transfer function

        return ctrl.feedback(Hz * Gz, 1) # type: ignore
    
    @property
    def transferFunction(self) -> ctrl.TransferFunction:
        """
        Get the controller's transfer function representation.
        
        Returns:
            The discrete-time transfer function C(z) of the controller
        """
        return self._tf
    
    @property
    def setpoint(self) -> float:
        """
        Get the current target value for the controlled variable.
        
        Returns:
            The current setpoint value
        """
        return self._setpoint
    
    @setpoint.setter
    def setpoint(self, value: float) -> None:
        """
        Set a new target value and reset internal controller states.
        
        Args:
            value: New setpoint value for the controller
            
        Notes:
            Resets integral and error memory to avoid bumps in control action
        """
        self._setpoint = value
        self._last_error = 0.0
        self._integral = 0.0
        
    def compute(self, measurement: float, timestamp: float) -> float:
        """
        Compute control action based on current measurement.
        
        Args:
            measurement: Current value of the controlled variable
            
        Returns:
            Control action to be applied to the system
            
        Notes:
            Uses the transfer function representation to compute the
            control action from the current error signal
        """
        
        dt = timestamp - self._last_time if self._last_time is not None else self.Ts
        
        error = self.setpoint - measurement
        # Apply control law using transfer function
        u = ctrl.forced_response(self._tf, T=[0, self.Ts], U=[error]) # type: ignore
        return float(u.outputs[-1]) 

    def step_response(self, t_final: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute the step response of the controller.
        
        Args:
            t_final: Final time for the simulation in seconds
            
        Returns:
            A tuple containing:
                - Time points array
                - Controller output response array
                
        Notes:
            Useful for analyzing controller behavior and tuning
        """
        t = np.arange(0, t_final + self._tf.dt, self._tf.dt) # type: ignore
        return ctrl.step_response(self._tf, t) # type: ignore

    def plot_step_response(self, t_final: float, show: bool = True, save: bool = False) -> None:
        """
        Plot and optionally save the step response of the controller.

        Args:
            t_final: Final time for the simulation in seconds
            show: Whether to display the plot immediately (default: True)
            save: Whether to save the plot to file (default: False)
        """
        t, y = self.step_response(t_final)
        
        plt.figure(figsize=(10, 6))
        plt.plot(t, y, 'b-', linewidth=2, label='Controller Output')
        plt.grid(True)
        plt.title(f'PID Controller Step Response (Kp={self.kp}, Ki={self.ki}, Kd={self.kd})')
        plt.xlabel('Time [s]')
        plt.ylabel('Output')
        plt.legend()
        
        if save:
            # Create plots directory in project root
            project_root = Path(__file__).parent.parent.parent.parent.parent
            plots_dir = project_root / "plots"
            plots_dir.mkdir(exist_ok=True)
            
            # Generate filename with timestamp and parameters
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"pid_step_response_{timestamp}.png"
            filepath = plots_dir / filename
            
            plt.savefig(filepath)
            log.info(f"Step response plot saved to: {filepath.relative_to(project_root)}")
        
        if show:
            plt.show()
        
        plt.close()