#  Copyright 2025 Metala Nanofluidos
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0

"""
Controller interface definition.

This module defines the abstract base class that all controllers must implement.
"""

from abc import ABC, abstractmethod

class IController(ABC):
    """
    Abstract base class for control system implementations.
    
    This interface defines the contract that all controllers must fulfill
    to be usable within the control loop.
    """
    
    @abstractmethod
    def _build_tf(self, ):
        pass
    
    @abstractmethod
    def compute(self, measurement: float) -> float:
        """
        Compute the control action based on current measurement.
        
        Args:
            measurement: Current value of the controlled variable
            
        Returns:
            Control action to be applied to the system
        """
        pass

    @abstractmethod
    def step_response(self, t_final: float):
        """
        Purely for studying purposes
        """
        pass