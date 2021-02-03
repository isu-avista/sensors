from avista_sensors.sensor_processor import SensorProcessor
import board
import adafruit_dht


class DHTProcessor(SensorProcessor):
    """DHT22 sensor implementation (Temperature and Humidity)

    Attributes:
        **_sensor (:obj: `DHT22`)**: DHT22 sensor object
    """

    def __init__(self):
        """Constructs a new DHTProcessor instance"""
        super().__init__()
        self._sensor = None

    def setup(self):
        """Sets up sensor configurations that should happen after loading from the database"""
        self._sensor = adafruit_dht.DHT22(board.D15)

    def _read_sensor(self, ts):
        """Reads data from the sensor

        Args:
            **ts (int)**: timestamp of when the data was read
        """
        data = {
            "temperature": self._sensor.temperature,
            "humidity": self._sensor.humidity
        }

        return data
