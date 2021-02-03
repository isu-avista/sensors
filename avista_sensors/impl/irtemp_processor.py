from avista_sensors.sensor_processor import SensorProcessor
from smbus2 import SMBus
from mlx90614 import MLX90614


class IRTempProcessor(SensorProcessor):
    """MLX90614 sensor implementation (Infrared Temperature)

    Attributes:
        **_address (int)**: I2C address

        **_bus_id (int)**: I2C bus number

        **_bus (:obj: `SMBus`)**: smbus object

        **_sensor (:obj: `MLX90614`)**: MLX90614 sensor object
    """

    def __init__(self):
        """Constructs a new IRTempProcessor instance"""
        super().__init__()
        self._address = None
        self._bus_id = None
        self._bus = None
        self._sensor = None

    def setup(self):
        """Sets up sensor configurations that should happen after loading from the database"""
        self._address = int(self._parameters['address'], 16)
        self._bus_id = int(self._parameters['bus_id'])
        self._bus = SMBus(self._bus_id)
        self._sensor = MLX90614(self._bus, address=self._address)

    def _read_sensor(self, ts):
        """Reads data from the sensor

        Args:
            **ts (int)**: timestamp of when the data was read
        """
        data = {
            "ambient": self._sensor.get_ambient(),
            "object": self._sensor.get_object_1()
        }

        self._bus.close()

        return data
