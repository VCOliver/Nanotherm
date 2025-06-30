#  Copyright 2025 Metala Nanofluidos
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0

from abc import ABC, abstractmethod
from typing import Optional

class I_HALGateway(ABC):
    """
    Interface for a Hardware Abstraction Layer (HAL) Gateway.

    This abstract base class defines the contract for reading input values and writing output values
    to hardware devices or their software representations. Implementations should provide concrete
    methods for interacting with specific hardware or simulation environments.
    """

    @abstractmethod
    def read_value(self, index_: Optional[int] = None, input_id: str | int = ...) -> float:
        """
        Read a value from a hardware input or from a specified index.

        Args:
            index_ (Optional[int]): The index of the input to read. 
            input_id (Optional[str]): The id of the column to be read

        Returns:
            float: The value read from the hardware input or its software representation.
        """
        pass

    @abstractmethod
    def write_value(self, output_id: str, value: float) -> None:
        """
        Write a value to a hardware output.

        Args:
            output_id (str): The identifier of the output to write to.
            value (float): The value to write to the output.

        Returns:
            None
        """
        pass