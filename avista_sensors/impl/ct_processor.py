import time
import math
from avista_sensors.sensor_processor import SensorProcessor
import busio
import board
import digitalio

class CTProcessor(SensorProcessor):
    """Current Transformer Sensor. This sensor transforms a hight current to a low current readable for microcontrollers

    Attributes:
        **channel (:obj: `AnalogIn`)**: adc converter channel

        **pin (:obj: `pin`)**: physical pin of the sensor

        **window (int)**: window over which to sample data
    """

    def __init__(self):
        """Constructs a new CTProcessor instance"""
        super().__init__()
        self.channel = None
        self.pin = None
        self.burden_resistor = 23 # ohm
        self.outlet_voltage = 240 # volt - we assume fix value for voltage from outlet
        self.outlet_freq = 50 # Hz - 
        self.CTRatio = 2000
        self.sample_number = 20 # number of samples per outlet_freq
        self.sample_freq = self.sample_number * self.outlet_freq  # Hz - the frequency of sampling

    def setup(self):
        """Sets up sensor configurations that should happen after loading from the database"""
        self.pin = board.D22 # ???
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        cs = digitalio.DigitalInOut(self.pin)
        mcp = MCP.MCP3008(spi, cs)
        # create analog input channel on pin 0
        self.channel = AnalogIn(mcp, MCP.P0)
        

    def _read_sensor(self, ts):
        """Reads data from the sensor

        Args:
            **ts (int)**: timestamp of when the data was read
        """

        values = []
        sample_period = 1/self.sample_freq
        for i in range(self.sample_freq):
            values.append(self.channel.value)
            time.sleep(sample_period) 

        signalMax = max(values)
        signalMin = min(values)

        # Next create a value peakToPeak (diff between min and max)
        Vsecondary_peaktopeak = signalMax - signalMin

        # based on the calculation at https://learn.openenergymonitor.org/electricity-monitoring/ct-sensors/interface-with-arduino
        Isecondary_peaktopeak = Vsecondary_peaktopeak / self.burden_resistor
        Isecondary_peak = Isecondary_peaktopeak / 2
        Isecondary_rms = Isecondary_peak / math.sqrt(2)
        Iprimary_rms = Isecondary_rms * CTRatio
        current_power = Iprimary_rms * self.outlet_voltage # Watt - electrical power

        data = {
            "power": current_power
        }

        return data

