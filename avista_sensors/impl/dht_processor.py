from avista_sensors.sensor_processor import SensorProcessor
import board
import adafruit_dht


class DHTSensor(SensorProcessor):

    def __init__(self):
        super().__init__()
        self._channel = self._parameters['channel']
        self._sensor = adafruit_dht.DHT22(board.D15)

    def _read_sensor(self, ts):
        return {
            "temp": self._sensor.temperature,
            "humidity": self._sensor.humidity
        }
