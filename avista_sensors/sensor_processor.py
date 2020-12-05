from abc import ABC, abstractmethod
from avista_data.data_point import DataPoint
from avista_data import db
from avista_data.sensor import Sensor


class SensorProcessor(ABC):
    """Abstract base class for all sensor processors.

    Attributes:
        _pinout (dict): mapping of variable names to pins on the IoT device
        _sensor_name (str): name of the sensor to which this processor belongs
    """

    def __init__(self):
        """Constructs a new sensor processor"""
        self._pinout = {}
        self._sensor_name = ""

    def set_name(self, name):
        """Assigns the sensor name to which this processor belongs

        Args:
            name (str): The new name of the sensor to which this processor belongs

        Raises:
            Exception if the provided name is None or the Empty String
        """
        if name is None or name == "":
            raise Exception("name cannot be none or empty")
        self._sensor_name = name

    def get_name(self):
        """Retrieves the name of the sensor to which the processor belongs

        Returns:
            Name of the sensor this processor collects data for
        """
        return self._sensor_name

    def add_pinout(self, var, pin):
        """Adds a pin and var mapping to this processor

        Args:
            var (str): The string name of the pin
            pin (int): The value of the pin

        Raises:
            Exception if the provided var name is None or empty or if the pin is less than 1 or greater than 40
        """
        if var is None or var == "":
            raise Exception("var cannot be None or empty")
        if pin <= 0 or pin > 40:
            raise Exception("pin must be between 1 and 40, inclusive")
        self._pinout[var] = pin

    def remove_pinout(self, var):
        """Removes the pin mapping associated with the provided var

        Args:
            var (str): name of the pin mapping to be removed

        Raises:
            Exception if the provided var name is None or empty
        """
        if var is None or var == "":
            raise Exception("var cannot be None or empty")
        self._pinout.pop(var, None)

    def get_pin(self, var):
        """Returns the pin associated with the provided variable name

        Args:
            var (str): name of the variable

        Raises:
            Exception, if the provided var is None or not in the pinout
        """
        if var is None or var == "" or var not in self._pinout.keys():
            raise Exception("Unknown var")
        return self._pinout[var]

    def has_pin_out(self, var, pin):
        """Tests whether a the pinout provided (var, pin) is associated with this sensor processor

        Args:
            var (str): the name of the pin
            pin (int): the pin number

        Return:
            True if the pinout (var, pin) is associated with this processor, False otherwise.

        Raises:
             Exception if the var is None or empty or if the pin is None, less than 1 or greater than 40.
        """
        if var is None or var == "":
            raise Exception("var cannot be None or Empty")
        if pin is None or pin < 1 or pin > 40:
            raise Exception("pin cannot be None, < 1 or > 40")
        return var in self._pinout.keys() and self._pinout[var] == pin

    def _create_data_point(self, value, ts):
        """Constructs a data point with the given value and timestamp and commit the changes to the database

        Args:
            value (float): the measured value
            ts (int): the timestamp

        Returns:
            the newly created DataPoint
        """
        dp = DataPoint(value=value, timestamp=ts)
        db.session.add(dp)
        sensor = Sensor.query.filter_by(name=self._sensor_name).first()
        sensor.add_data_point(dp)
        db.session.commit()
        return dp

    def process(self, ts):
        """Template method which collects data from the sensor and creates then creates the data point

        Args:
            ts (int): the timestamp at which this reading is associated with

        Return:
            The created data point
        """
        value = self._read_sensor(ts)
        return self._create_data_point(value, ts)

    @abstractmethod
    def _read_sensor(self, ts):
        """Abstract method in which the reading of data from a sensor should be executed

        Args:
            ts (int): timestamp of the data to be collected

        Returns:
            float: value of the associated sensor
        """
        pass
