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

from datetime import datetime
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

import pandas as pd
from nanotherm.core.domain.pid_params import PIDParams
from nanotherm.infrastructure.controllers import PIDController
from nanotherm.core.entities.DTransferFunction import DiscreteTransferFunction
from nanotherm.config.platform import Platform, HardwareType, HardwareError
from nanotherm.config.settings import NanothermSettings
from nanotherm.infrastructure.gateways.simul_data_gateway import CSV_HALGateway
from nanotherm.services.control_loop import ControlLoop

log = logging.getLogger(__name__)

class App:
    """
    Main application class for nanotherm.
    
    Handles initialization and execution of the core application logic.
    
    Attributes:
        settings (NanothermSettings): Pydantic settings containing application configuration.
    """
    
    def __init__(self, settings: NanothermSettings) -> None:
        """
        Initialize the application with the given configuration.
        
        Args:
            settings (NanothermSettings): Pydantic settings containing application configuration.
        """
        self.settings = settings
        log.info('Starting main application.')
        
    def run(self) -> None:
        """
        Execute the main application logic.
        
        This method starts the main processing loop and handles the core
        application functionality, including initializing the control system,
        running the simulation, and saving results.
        """
        gains = [self.settings.pid.kp, self.settings.pid.ki, self.settings.pid.kd]
        pid_params = PIDParams(*gains)
        log.debug(f'PID gains set to {pid_params}')
        Ts = self.settings.control_system.sampling_time
        
        plant_tf = self.settings.liver_tf
        plant = DiscreteTransferFunction(plant_tf.num, plant_tf.den, Ts)
        
        setpoint = self.settings.control_system.setpoint
        controller = PIDController(pid_params, plant, setpoint=setpoint, Ts=Ts)
        
        platform = Platform.get_hardware_type()
        if platform == HardwareType.DESKTOP:
            hal = CSV_HALGateway('data/input/combined.csv')
        else:
            log.warning('HAL for Raspberry Pi not yet implemented!')
            raise HardwareError('Raspberry Pi not supported yet. Please use a desktop platform.')
        
        # Example: run control loop for a few iterations (or implement a stop condition)
        loop = ControlLoop(controller, sample_time=0.01, gateway=hal, simulating=True)
        log.info("Starting control loop simulation...")
        loop.start()
        
        try:
            # Wait for the control loop to complete
            loop.wait_for_completion()
            log.info("Control loop simulation completed successfully")
            
        except KeyboardInterrupt:
            log.info("Simulation interrupted by user")
            loop.stop()

        except Exception as e:
            log.error(f"Error during simulation: {e}")
            loop.stop()
            raise

        finally:
            # Ensure the loop is stopped
            if loop.thread_is_alive():
                loop.stop()
             
        try:   
            simulation_data = loop.get_simulation_data()
            csv_path = self.save_simulation_results(simulation_data)
        
        except Exception as e:
            log.error(f"Failed to save results: {e}")
                

    def save_simulation_results(
        self, 
        simulation_data: List[Dict[str, Any]], 
        output_dir: str = 'data/output'
    ) -> str:
        """
        Save simulation results to a CSV file using pandas.
        
        Args:
            simulation_data (List[Dict[str, Any]]): List of dictionaries containing simulation data.
            output_dir (str, optional): Directory to save the output files. Defaults to 'data/output'.
        
        Returns:
            str: Path to the saved CSV file.
        
        Raises:
            Exception: If saving fails for any reason.
        """
        try:
            # Create output directory if it doesn't exist
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            csv_file = output_path / f"control_loop_results_{timestamp}.csv"
            
            if simulation_data:
                # Create DataFrame from simulation data
                df = pd.DataFrame(simulation_data)
                
                # Calculate basic statistics
                stats_info = {
                    'total_iterations': len(df),
                    'simulation_duration': df['timestamp'].max() if not df.empty else 0,
                    'final_measurement': df['measurement'].iloc[-1] if not df.empty else 0, # type: ignore
                    'avg_output': df['measurement'].mean() if not df.empty else 0,
                    'std_output': df['measurement'].std() if not df.empty else 0,
                    'max_output': df['measurement'].max() if not df.empty else 0,
                    'min_output': df['measurement'].min() if not df.empty else 0,
                }
                
                df_out = df.rename(columns={
                    'timestamp': 'timestamp (s)',
                    'resistence': 'resistance (Ohm)',
                    'control_action': 'control_action (V)',
                    'setpoint': 'setpoint (W)',
                    'measurement': 'measurement (W)',                    
                })
                
                # Save to CSV with proper formatting
                df_out.to_csv(csv_file, index=False, float_format='%.6f')
                
                
                log.info(f"Results saved to CSV: {csv_file}")
                log.debug(f"Simulation Statistics:")
                log.debug(f"  - Total iterations: {stats_info['total_iterations']}")
                log.debug(f"  - Duration: {stats_info['simulation_duration']} seconds")
                log.debug(f"  - Final output: {stats_info['final_measurement']:.6f}")
                log.debug(f"  - Average output: {stats_info['avg_output']:.6f}")
                log.debug(f"  - STD output: {stats_info['std_output']:.6f}")
                log.debug(f"  - Max output: {stats_info['max_output']:.6f}")
                log.debug(f"  - Min output: {stats_info['min_output']:.6f}")
                
            else:
                # Create empty DataFrame with correct columns
                columns = ['timestamp', 'measurement', 'setpoint', 'control_action']
                empty_df = pd.DataFrame(columns=columns)
                empty_df.to_csv(csv_file, index=False)
                
                log.warning("No simulation data collected - saved empty files with headers")
            
            return str(csv_file)
            
        except Exception as e:
            log.error(f"Failed to save simulation results: {e}")
            raise