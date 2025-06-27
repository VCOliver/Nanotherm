#  Copyright 2025 Metala Nanofluidos
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0

import logging
from typing import Optional, Union
import pandas as pd
from nanotherm.core.entities.inputGateway import I_HALGateway

log = logging.getLogger(__file__)

class CSV_HALGateway(I_HALGateway):
    """
    Simulated Hardware Abstraction Layer (HAL) Gateway using CSV data.

    This class reads input values from a CSV file to simulate hardware input for testing and development.
    """

    def __init__(self, path: str) -> None:
        """
        Initialize the simulated HAL gateway.

        Args:
            path (str): Path to the CSV file containing simulation data.
        """
        self.__path = path
        log.info(f"Initializing simulated HAL. Reading inputs from {path}.")
        try:
            simulated_data: pd.DataFrame = pd.read_csv(path)
        except FileNotFoundError:
            log.error(f"Simulated CSV data file not found at {path}!")
            log.warning('Creating empty pd.DataFrame.')
            simulated_data = pd.DataFrame()
            
        if simulated_data.empty:
            log.warning('Simulation data is EMPTY.')
            
        self.__index: int = 0
        self._data_len: int = len(simulated_data)
        self._simul_data: pd.DataFrame = simulated_data
        
    def read_value(
        self, 
        index_: Optional[int] = None, 
        input_id: Union[str, int] = 'Impedancia'
    ) -> float:
        """
        Read a value from the simulated CSV data.

        Args:
            index_ (Optional[int]): The row index to read from. If None, reads the next row.
            input_id (str | int): The column name or index to read from.

        Returns:
            float: The value read from the CSV data.

        Raises:
            AssertionError: If input types are incorrect.
            IndexError: If the index is out of bounds.
        """
        assert index_ is None or isinstance(index_, int), "index_ should be of type 'int' or None"
        assert isinstance(input_id, (str, int)), "input_id should be of type 'str' or 'int'"
        
        if self.__index == self._data_len:
            log.info('No more data to be read from CSV file.')
            log.debug(f'Final index read from {self.__path}: {self.__index}.')
        
        if index_ is None:
            index = self.__index
            self.__index += 1
        else:
            index = index_
            
        if index >= self._data_len:
            log.error(f'Index value [ {index} ] out of data bounds. Data length is {self._data_len}')
            raise IndexError(f'Index {index} out of bounds for data length {self._data_len}')
            
        current_row = self._simul_data.iloc[index]
        value = current_row[input_id] 
        log.debug(f'Value read from index {index}: {value}')
        
        return float(value)
    
    def write_value(self, output_id: str, value: float) -> None:
        """
        Simulate writing a value to a hardware output.

        Args:
            output_id (str): The identifier of the output to write to.
            value (float): The value to write.

        Returns:
            None
        """
        log.info(f"Simulated writing {value} to: {output_id}")



