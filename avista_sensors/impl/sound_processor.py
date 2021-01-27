import time
import math
from avista_sensors.sensor_processor import SensorProcessor
import busio
import board
import digitalio
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn


class SoundProcessor(SensorProcessor):

    def __init__(self):
        super().__init__()
        self.channel = None
        self.pin = self._parameters['pin']
        self.window = 50
        self._setup()

    def _setup(self):
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        cs = digitalio.DigitalInOut(self.pin)
        mcp = MCP.MCP3008(spi, cs)
        # create analog input channel on pin 0
        self.channel = AnalogIn(mcp, MCP.P0)

    def _read_sensor(self, ts):
        # Need to read for 50 ms to create a sample window
        # from this create two values:
        #    signalMax (the max during that window)
        #    signalMin (the min during that window)
        values = []
        for i in range(self.window):
            values.append(self.channel.value)
            time.sleep(.001)

        signalMax = max(values)
        signalMin = min(values)

        # Next create a value peakToPeak (diff between min and max)
        peakToPeak = signalMax - signalMin

        # Using this we can conver the peakToPeak to RMS voltage
        volts = ((peakToPeak * 3.3) / 1024) * 0.707
        first = math.log10(volts / 0.00631) * 20
        second = first + 94 - 44 - 25

        return second

