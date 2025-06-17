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
        gains = list(self.config['pid'].values())[:3]
        pid_params = PIDParams(*gains)
        log.debug(f'PID gains set to {pid_params}')
        
        controller = PIDController(pid_params)
        controller.plot_step_response(60, save=True)
        
        