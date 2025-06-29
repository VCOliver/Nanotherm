#  Copyright 2025 Metala Nanofluidos
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#

"""
Main application module for the nanotherm system.

This module contains the core App class that handles the main application logic
and lifecycle management.
"""

import logging
from typing import Dict, Any
from nanotherm.core.domain.pid_params import PIDParams
from nanotherm.infrastructure.controllers import PIDController
from nanotherm.core.entities.DTransferFunction import DiscreteTransferFunction
from nanotherm.config.platform import Platform, HardwareType, HardwareError
from nanotherm.infrastructure.gateways.simul_data_gateway import CSV_HALGateway
from nanotherm.services.control_loop import ControlLoop

log = logging.getLogger(__name__)

class App:
    """
    Main application class for nanotherm.
    
    Handles initialization and execution of the core application logic.
    
    Attributes:
        config (Dict[str, Any]): Configuration dictionary containing application settings
    """
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """
        Initialize the application with the given configuration.
        
        Args:
            config: Dictionary containing application configuration settings
        """
        self.config = config
        log.info('Starting main application.')
        
    def run(self) -> None:
        """
        Execute the main application logic.
        
        This method starts the main processing loop and handles the core
        application functionality.
        """
        gains = list(self.config['pid'].values())
        pid_params = PIDParams(*gains)
        log.debug(f'PID gains set to {pid_params}')
        Ts = self.config['control_system']['sampling_time']
        
        plant_tf = self.config['liver_tf']
        plant = DiscreteTransferFunction(plant_tf['num'], plant_tf['den'], Ts)
        
        setpoint = self.config['control_system']['setpoint']
        controller = PIDController(pid_params, plant, setpoint=setpoint, Ts=Ts)
        
        platform = Platform.get_hardware_type()
        if platform == HardwareType.DESKTOP:
            hal = CSV_HALGateway('data/input/combined.csv')
        else:
            log.warning('HAL for Raspberry Pi not yet implemented!')
            raise HardwareError('Raspberry Pi not supported yet. Please use a desktop platform.')
        
        # Example: run control loop for a few iterations (or implement a stop condition)
        loop = ControlLoop(controller, sample_time=Ts, gateway=hal, simulating=True)
        loop.start()
        
        # loop.start()  # Uncomment to run the control loop
        controller.plot_step_response(120, save=True)

