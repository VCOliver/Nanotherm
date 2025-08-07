#  Copyright 2025 Metala Nanofluidos
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0

"""
Raspberry Pi Hardware Abstraction Layer (HAL) Gateway.

This module provides the hardware interface for Raspberry Pi platforms,
implementing GPIO control, ADC/DAC operations, and other Pi-specific functionality
for radiofrequency ablation control systems.
"""

import logging
import time
import math
from typing import Optional, Union, Dict, Any
from nanotherm.core.entities.inputGateway import I_HALGateway

log = logging.getLogger(__name__)

try:
    import RPi.GPIO as GPIO
    import board
    import busio
    import adafruit_ads1x15.ads1115 as ADS
    from adafruit_ads1x15.analog_in import AnalogIn
    import adafruit_pcf8591
    HAS_GPIO = True
    log.debug("RPi.GPIO, ADS1115, and PCF8591 libraries imported successfully")
except ImportError as e:
    HAS_GPIO = False
    log.warning(f"RPi.GPIO, ADS1115, or PCF8591 libraries not available: {e}")
    log.warning("Running in mock mode - GPIO operations will be simulated")


class RaspberryPiHALGateway(I_HALGateway):
    """
    Raspberry Pi Hardware Abstraction Layer Gateway.
    
    This class provides hardware interface for Raspberry Pi platforms,
    including GPIO control, ADC reading, and DAC writing for RFA control systems.
    
    For RFA applications, this typically handles:
    - Reading impedance/temperature sensors via ADC
    - Controlling RF power output via DAC/PWM
    - GPIO control for system status indicators
    """
    
    def __init__(self, 
                 voltage_channel: int = 0,
                 current_channel: int = 1,
                 power_control_pin: int = 18,
                 status_led_pin: int = 24,
                 ads1115_address: int = 0x48,
                 pcf8591_address: int = 0x49,
                 reference_voltage: float = 5.0,
                 adc_gain: int = 1,
                 mock_mode: bool = False):
        """
        Initialize the Raspberry Pi HAL Gateway with ADS1115 ADC and PCF8591 DAC.
        
        Args:
            voltage_channel: ADS1115 channel for voltage reading (A0 = 0, default: 0)
            current_channel: ADS1115 channel for current reading (A1 = 1, default: 1)
            power_control_pin: GPIO pin for RF power control (default: 18)
            status_led_pin: GPIO pin for status LED (default: 24)
            ads1115_address: I2C address of ADS1115 ADC (default: 0x48)
            pcf8591_address: I2C address of PCF8591 DAC (default: 0x49)
            reference_voltage: ADC reference voltage for ADS1115 (default: 5.0V)
            adc_gain: ADS1115 gain setting (1=±4.096V, 2=±2.048V, etc.)
            mock_mode: Force mock mode even if GPIO is available (default: False)
        """
        self.voltage_channel = voltage_channel
        self.current_channel = current_channel
        self.power_control_pin = power_control_pin
        self.status_led_pin = status_led_pin
        self.ads1115_address = ads1115_address
        self.pcf8591_address = pcf8591_address
        self.reference_voltage = reference_voltage
        self.adc_gain = adc_gain
        
        # Determine if we should run in mock mode
        self.mock_mode = mock_mode or not HAS_GPIO
        
        if self.mock_mode:
            log.warning("Running Raspberry Pi HAL in MOCK MODE")
            self._initialize_mock_mode()
        else:
            self._initialize_gpio()
            self._initialize_i2c()  # For ADS1115 and PCF8591
            
        log.info(f"Raspberry Pi HAL initialized (mock_mode={self.mock_mode})")
    
    def _initialize_gpio(self) -> None:
        """Initialize GPIO pins for hardware control."""
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            
            # Setup power control pin as output
            GPIO.setup(self.power_control_pin, GPIO.OUT)
            GPIO.output(self.power_control_pin, GPIO.LOW)
            
            # Setup status LED pin as output
            GPIO.setup(self.status_led_pin, GPIO.OUT)
            GPIO.output(self.status_led_pin, GPIO.LOW)
            
            log.debug("GPIO pins initialized successfully")
            
        except Exception as e:
            log.error(f"Failed to initialize GPIO: {e}")
            self.mock_mode = True
            self._initialize_mock_mode()
    
    def _initialize_i2c(self) -> None:
        """Initialize I2C interface for ADS1115 ADC and PCF8591 DAC communication."""
        try:
            # Initialize I2C bus
            self.i2c = busio.I2C(board.SCL, board.SDA)
            
            # Initialize ADS1115 ADC
            self.ads = ADS.ADS1115(self.i2c, address=self.ads1115_address)
            self.ads.gain = self.adc_gain
            
            # Create analog input channels for voltage and current
            self.voltage_input = AnalogIn(self.ads, getattr(ADS, f'P{self.voltage_channel}'))
            self.current_input = AnalogIn(self.ads, getattr(ADS, f'P{self.current_channel}'))
            
            # Initialize PCF8591 DAC
            self.pcf8591 = adafruit_pcf8591.PCF8591(self.i2c, address=self.pcf8591_address)
            
            log.debug(f"ADS1115 ADC initialized successfully on I2C address 0x{self.ads1115_address:02x}")
            log.debug(f"ADS1115 configured: Voltage channel {self.voltage_channel}, Current channel {self.current_channel}, Gain {self.adc_gain}")
            log.debug(f"PCF8591 DAC initialized successfully on I2C address 0x{self.pcf8591_address:02x}")
            
        except Exception as e:
            log.error(f"Failed to initialize ADS1115 ADC or PCF8591 DAC: {e}")
            self.mock_mode = True
            self._initialize_mock_mode()
    
    def _initialize_mock_mode(self) -> None:
        """Initialize mock mode with simulated values."""
        self._mock_voltage = 2.5  # Simulated voltage in V
        self._mock_current = 1.0  # Simulated current in A
        self._mock_power_output = 0.0
        self._mock_timestamp = time.time()
        log.debug("Mock mode initialized with default values")
    
    def read_value(self, 
                   index_: Optional[int] = None, 
                   input_id: Union[str, int] = 'Impedancia') -> float:
        """
        Read a value from the hardware sensors (ADS1115).
        
        For RFA applications, this reads voltage and current from sensors 
        and can calculate derived values like impedance and power.
        
        Args:
            index_: Not used in hardware mode (compatibility with simulation)
            input_id: Sensor identifier ('Impedancia', 'Voltage', 'Current', 'Power', etc.)
            
        Returns:
            float: The sensor reading or calculated value
        """
        if self.mock_mode:
            return self._read_mock_value(input_id)
        else:
            return self._read_sensor_value(input_id)
    
    def _read_mock_value(self, input_id: Union[str, int]) -> float:
        """Read a simulated sensor value for testing."""
        current_time = time.time()
        time_delta = current_time - self._mock_timestamp
        
        if input_id in ['Voltage', 'voltage', 0]:
            # Simulate voltage changing over time
            base_voltage = 2.5
            variation = 0.5 * (0.5 + 0.5 * math.sin(time_delta * 0.1))
            value = base_voltage + variation
            
        elif input_id in ['Current', 'current', 1]:
            # Simulate current changing over time
            base_current = 1.0
            variation = 0.2 * (0.5 + 0.5 * math.sin(time_delta * 0.15))
            value = base_current + variation
            
        elif input_id in ['Impedancia', 'impedance', 'Impedance']:
            # Calculate impedance from mock voltage and current
            voltage = self._read_mock_value('Voltage')
            current = self._read_mock_value('Current')
            value = voltage / current if current > 0.001 else 9999.0
            
        elif input_id in ['Power', 'power']:
            # Calculate power from mock voltage and current
            voltage = self._read_mock_value('Voltage')
            current = self._read_mock_value('Current')
            value = voltage * current
            
        elif input_id in ['Temperature', 'temperature', 2]:
            # Simulate temperature reading
            base_temp = 37.0  # Body temperature
            heating = 30.0 * min(1.0, time_delta / 60.0)  # Heat up over 1 minute
            value = base_temp + heating
            
        else:
            log.warning(f"Unknown input_id: {input_id}, returning default value")
            value = 0.0
            
        log.debug(f"Mock reading {input_id}: {value}")
        return value
    
    def _read_sensor_value(self, input_id: Union[str, int]) -> float:
        """Read actual sensor value from I2C devices."""
        try:
            if input_id in ['Voltage', 'voltage', 0]:
                # Read voltage from ADS1115 channel A0
                chan = AnalogIn(self.ads, ADS.P0)
                voltage = chan.voltage
                log.debug(f"ADS1115 A0 voltage: {voltage:.3f}V")
                return voltage
                
            elif input_id in ['Current', 'current', 1]:
                # Read current from ADS1115 channel A1
                chan = AnalogIn(self.ads, ADS.P1)
                # Convert voltage to current based on sensor characteristics
                # Assuming current sensor outputs voltage proportional to current
                voltage = chan.voltage
                # Example: if 1V = 1A (adjust based on actual sensor specs)
                current = voltage  # Adjust this conversion factor as needed
                log.debug(f"ADS1115 A1 current: {current:.3f}A (from {voltage:.3f}V)")
                return current
                
            elif input_id in ['Impedancia', 'impedance', 'Impedance']:
                # Calculate impedance from voltage and current
                voltage = self._read_sensor_value('Voltage')
                current = self._read_sensor_value('Current')
                
                if current > 0.001:  # Avoid division by zero
                    impedance = voltage / current
                else:
                    impedance = 9999.0  # High impedance when no current
                    
                log.debug(f"Calculated impedance: {impedance:.3f}Ω")
                return impedance
                
            elif input_id in ['Power', 'power']:
                # Calculate power from voltage and current
                voltage = self._read_sensor_value('Voltage')
                current = self._read_sensor_value('Current')
                power = voltage * current
                log.debug(f"Calculated power: {power:.3f}W")
                return power
                
            elif input_id in ['Temperature', 'temperature', 2]:
                # Temperature could be read from additional ADC channel if available
                # For now, use A2 if connected, otherwise return room temperature
                try:
                    chan = AnalogIn(self.ads, ADS.P2)
                    voltage = chan.voltage
                    # Convert voltage to temperature based on sensor type
                    # Example for LM35: 10mV/°C
                    temperature = voltage * 100.0  # Adjust based on actual sensor
                    log.debug(f"Temperature sensor: {temperature:.1f}°C")
                    return temperature
                except:
                    log.warning("Temperature sensor not available, returning room temperature")
                    return 25.0  # Room temperature fallback
                    
            else:
                log.warning(f"Unknown input_id: {input_id}, returning 0.0")
                return 0.0
                
        except Exception as e:
            log.error(f"Error reading sensor {input_id}: {e}")
            return 0.0
    
    def write_value(self, output_id: str, value: float) -> None:
        """
        Write a control value to hardware output.
        
        For RFA applications, this controls RF power output, typically
        through DAC or PWM signals.
        
        Args:
            output_id: Output identifier ('power', 'rf_enable', 'led_status', etc.)
            value: Control value (e.g., power level 0-100%)
        """
        if self.mock_mode:
            self._write_mock_value(output_id, value)
        else:
            self._write_hardware_value(output_id, value)
    
    def _write_mock_value(self, output_id: str, value: float) -> None:
        """Write a simulated control value for testing."""
        self._mock_power_output = value
        log.info(f"Mock writing {value} to: {output_id}")
    
    def _write_hardware_value(self, output_id: str, value: float) -> None:
        """Write actual control value to hardware."""
        try:
            if output_id.lower() in ['power', 'rf_power', 'control_action']:
                self._set_rf_power(value)
                
            elif output_id.lower() in ['led_status', 'status_led']:
                self._set_status_led(value > 0)
                
            elif output_id.lower() in ['rf_enable', 'power_enable']:
                self._set_power_enable(value > 0)
                
            else:
                log.warning(f"Unknown output_id: {output_id}")
                
        except Exception as e:
            log.error(f"Failed to write hardware value: {e}")
    
    def _set_rf_power(self, power_percent: float) -> None:
        """Set RF power output via PCF8591 DAC."""
        # Clamp power to safe range
        power_percent = max(0.0, min(power_percent, 100.0))
        
        try:
            if self.mock_mode:
                log.debug(f"Mock mode: RF power set to {power_percent}%")
                return
                
            # Convert percentage to DAC value (0-255 for 8-bit PCF8591 DAC)
            dac_value = int((power_percent / 100.0) * 255)
            
            # Set DAC output using PCF8591
            self.pcf8591.dac_value = dac_value
            
            log.debug(f"RF power set to {power_percent}% (DAC value: {dac_value}/255)")
            
        except Exception as e:
            log.error(f"Failed to set RF power via PCF8591: {e}")
    
    def _set_status_led(self, state: bool) -> None:
        """Control status LED."""
        try:
            GPIO.output(self.status_led_pin, GPIO.HIGH if state else GPIO.LOW)
            log.debug(f"Status LED: {'ON' if state else 'OFF'}")
        except Exception as e:
            log.error(f"Failed to control status LED: {e}")
    
    def _set_power_enable(self, enabled: bool) -> None:
        """Enable/disable RF power output."""
        try:
            GPIO.output(self.power_control_pin, GPIO.HIGH if enabled else GPIO.LOW)
            log.info(f"RF Power: {'ENABLED' if enabled else 'DISABLED'}")
        except Exception as e:
            log.error(f"Failed to control power enable: {e}")
    
    def cleanup(self) -> None:
        """Clean up GPIO and I2C resources."""
        if not self.mock_mode and HAS_GPIO:
            try:
                GPIO.cleanup()
                log.debug("GPIO resources cleaned up")
            except Exception as e:
                log.error(f"Error during GPIO cleanup: {e}")
    
    def __del__(self) -> None:
        """Destructor to ensure cleanup."""
        self.cleanup()
