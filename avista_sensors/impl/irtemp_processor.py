from avista_sensors.sensor_processor import SensorProcessor
from smbus2 import SMBus
from mlx90614 import MLX90614


class IRTempProcessor(SensorProcessor):

    def __init__(self):
        super().__init__()
        self._address = self._parameters['address']
        self._bus_id = self._parameters['bus_id']
        self._bus = SMBus(self._bus_id)
        self._sensor = MLX90614(self._bus, address=self._address)

    def _read_sensor(self, ts):
        data = {
            "ambient": self._sensor.get_ambient(),
            "object": self._sensor.get_object_1()
        }
        self._bus.close()
        return data