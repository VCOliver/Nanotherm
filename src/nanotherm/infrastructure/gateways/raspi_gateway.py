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
    import spidev
    import board
    import busio
    import adafruit_ads1x15.ads1115 as ADS
    from adafruit_ads1x15.analog_in import AnalogIn
    HAS_GPIO = True
    log.debug("RPi.GPIO, spidev, and ADS1115 libraries imported successfully")
except ImportError as e:
    HAS_GPIO = False
    log.warning(f"RPi.GPIO, spidev, or ADS1115 libraries not available: {e}")
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
                 adc_channel: int = 0,
                 dac_channel: int = 1,
                 power_control_pin: int = 18,
                 status_led_pin: int = 24,
                 spi_bus: int = 0,
                 spi_device: int = 0,
                 ads1115_address: int = 0x48,
                 reference_voltage: float = 5.0,
                 adc_resolution: int = 65536,
                 adc_gain: int = 1,
                 mock_mode: bool = False):
        """
        Initialize the Raspberry Pi HAL Gateway with ADS1115 ADC.
        
        Args:
            adc_channel: ADS1115 ADC channel for reading sensor values (0-3, default: 0)
            dac_channel: SPI DAC channel for power control (default: 1)
            power_control_pin: GPIO pin for RF power control (default: 18)
            status_led_pin: GPIO pin for status LED (default: 24)
            spi_bus: SPI bus number for DAC (default: 0)
            spi_device: SPI device number for DAC (default: 0)
            ads1115_address: I2C address of ADS1115 (default: 0x48)
            reference_voltage: ADC reference voltage for ADS1115 (default: 5.0V)
            adc_resolution: ADC resolution (16-bit ADS1115 = 65536)
            adc_gain: ADS1115 gain setting (1=±4.096V, 2=±2.048V, etc.)
            mock_mode: Force mock mode even if GPIO is available (default: False)
        """
        self.adc_channel = adc_channel
        self.dac_channel = dac_channel
        self.power_control_pin = power_control_pin
        self.status_led_pin = status_led_pin
        self.ads1115_address = ads1115_address
        self.reference_voltage = reference_voltage
        self.adc_resolution = adc_resolution
        self.adc_gain = adc_gain
        
        # Determine if we should run in mock mode
        self.mock_mode = mock_mode or not HAS_GPIO
        
        if self.mock_mode:
            log.warning("Running Raspberry Pi HAL in MOCK MODE")
            self._initialize_mock_mode()
        else:
            self._initialize_gpio()
            self._initialize_i2c()  # For ADS1115
            self._initialize_spi(spi_bus, spi_device)  # For DAC
            
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
        """Initialize I2C interface for ADS1115 ADC communication."""
        try:
            # Initialize I2C bus
            self.i2c = busio.I2C(board.SCL, board.SDA)
            
            # Initialize ADS1115 ADC
            self.ads = ADS.ADS1115(self.i2c, address=self.ads1115_address)
            self.ads.gain = self.adc_gain
            
            # Create analog input channel
            self.adc_input = AnalogIn(self.ads, getattr(ADS, f'P{self.adc_channel}'))
            
            log.debug(f"ADS1115 ADC initialized successfully on I2C address 0x{self.ads1115_address:02x}")
            log.debug(f"ADC configured: Channel {self.adc_channel}, Gain {self.adc_gain}")
            
        except Exception as e:
            log.error(f"Failed to initialize ADS1115 ADC: {e}")
            self.mock_mode = True
            self._initialize_mock_mode()
    
    def _initialize_spi(self, spi_bus: int, spi_device: int) -> None:
        """Initialize SPI interface for ADC/DAC communication."""
        try:
            self.spi = spidev.SpiDev()
            self.spi.open(spi_bus, spi_device)
            self.spi.max_speed_hz = 1000000  # 1MHz
            self.spi.mode = 0
            log.debug("SPI interface initialized successfully")
            
        except Exception as e:
            log.error(f"Failed to initialize SPI: {e}")
            self.mock_mode = True
            self._initialize_mock_mode()
    
    def _initialize_mock_mode(self) -> None:
        """Initialize mock mode with simulated values."""
        self._mock_sensor_value = 500.0  # Simulated impedance value in Ohms
        self._mock_power_output = 0.0
        self._mock_timestamp = time.time()
        log.debug("Mock mode initialized with default values")
    
    def read_value(self, 
                   index_: Optional[int] = None, 
                   input_id: Union[str, int] = 'Impedancia') -> float:
        """
        Read a value from the hardware sensor (ADC).
        
        For RFA applications, this typically reads impedance values from 
        tissue sensors to monitor treatment progress.
        
        Args:
            index_: Not used in hardware mode (compatibility with simulation)
            input_id: Sensor identifier ('Impedancia', 'Temperature', etc.)
            
        Returns:
            float: The sensor reading (e.g., impedance in Ohms)
        """
        if self.mock_mode:
            return self._read_mock_value(input_id)
        else:
            return self._read_adc_value()
    
    def _read_mock_value(self, input_id: Union[str, int]) -> float:
        """Read a simulated sensor value for testing."""
        current_time = time.time()
        time_delta = current_time - self._mock_timestamp
        
        if input_id == 'Impedancia' or input_id == 0:
            # Simulate impedance changing over time (typical RFA pattern)
            base_impedance = 500.0
            variation = 50.0 * (0.5 + 0.5 * math.sin(time_delta * 0.1))
            value = base_impedance + variation
            
        elif input_id == 'Temperature' or input_id == 1:
            # Simulate temperature reading
            base_temp = 37.0  # Body temperature
            heating = 30.0 * min(1.0, time_delta / 60.0)  # Heat up over 1 minute
            value = base_temp + heating
            
        else:
            log.warning(f"Unknown input_id: {input_id}, returning default value")
            value = 0.0
            
        log.debug(f"Mock reading {input_id}: {value}")
        return value
    
    def _read_adc_value(self) -> float:
        """Read actual ADC value from ADS1115 hardware."""
        try:
            # Read voltage directly from ADS1115
            voltage = self.adc_input.voltage
            
            # Read raw ADC value for debugging
            raw_value = self.adc_input.value
            
            # Convert voltage to impedance (assuming voltage divider circuit)
            # This conversion depends on your specific sensor circuit
            impedance = self._voltage_to_impedance(voltage)
            
            log.debug(f"ADS1115 reading - Raw: {raw_value}, Voltage: {voltage:.3f}V, Impedance: {impedance:.1f}Ω")
            return impedance
            
        except Exception as e:
            log.error(f"Failed to read ADS1115 value: {e}")
            # Fallback to mock value
            return self._read_mock_value('Impedancia')
    
    def _voltage_to_impedance(self, voltage: float) -> float:
        """
        Convert ADC voltage reading to impedance value.
        
        This function implements the specific conversion formula based on
        your sensor circuit design. Modify according to your hardware setup.
        
        Args:
            voltage: ADC voltage reading
            
        Returns:
            float: Impedance value in Ohms
        """
        # Example conversion (modify based on your circuit)
        # Assuming a voltage divider with known reference resistor
        if voltage < 0.1:  # Avoid division by zero
            return 9999.0  # High impedance
            
        # Example: R_tissue = R_ref * (V_ref - V_measured) / V_measured
        reference_resistor = 1000.0  # 1kΩ reference
        impedance = reference_resistor * (self.reference_voltage - voltage) / voltage
        
        return max(0.0, min(impedance, 9999.0))  # Clamp to reasonable range
    
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
        """Set RF power output via DAC or PWM."""
        # Clamp power to safe range
        power_percent = max(0.0, min(power_percent, 100.0))
        
        try:
            # Convert percentage to DAC value (0-4095 for 12-bit DAC)
            dac_value = int((power_percent / 100.0) * 4095)
            
            # Send to DAC via SPI (example for MCP4922)
            # Command format depends on your specific DAC
            dac_command = [0x70 | ((dac_value >> 8) & 0x0F), dac_value & 0xFF]
            self.spi.xfer2(dac_command)
            
            log.debug(f"RF power set to {power_percent}% (DAC value: {dac_value})")
            
        except Exception as e:
            log.error(f"Failed to set RF power: {e}")
    
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
        """Clean up GPIO, SPI, and I2C resources."""
        if not self.mock_mode:
            try:
                if hasattr(self, 'spi'):
                    self.spi.close()
                if hasattr(self, 'i2c'):
                    self.i2c.deinit()
                GPIO.cleanup()
                log.info("Hardware resources cleaned up")
            except Exception as e:
                log.error(f"Error during cleanup: {e}")
    
    def __del__(self) -> None:
        """Destructor to ensure cleanup."""
        self.cleanup()
