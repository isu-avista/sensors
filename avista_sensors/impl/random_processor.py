from avista_sensors.sensor_processor import SensorProcessor
import math
from datetime import datetime


class RandomProcessor(SensorProcessor):
    """Represents a simulated sensor providing a logarithmic data stream.

    The data provided represents the typical increase of temperature in the windings of an AC Motor

    Attributes:
        __base_ts (int): the base time stamp used in the calculation
    """

    def __init__(self):
        """Constructs a new SimulatedProcessor with a base timestamp of now"""
        super(RandomProcessor, self).__init__()
        self.__base_ts = int(datetime.timestamp(datetime.now()))

    def _read_sensor(self, ts):
        """Simulates the reading of data from a sensor

        Args:
            ts (int): timestamp of the data to be collected

        Returns:
            float: value of the simulated sensor
        """
        return 20 * math.log(ts - self.__base_ts + 1) + 71
