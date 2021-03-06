from abc import ABC, abstractmethod
from avista_data.data_point import DataPoint
from avista_data.sensor import Sensor
import avista_data.database


class SensorProcessor(ABC):
    """Abstract base class for all sensor processors.

    Attributes:
        **_parameters (dict)**: mapping of parameter keys and values for Processors

        **_sensor_name (str)**: name of the sensor to which this processor belongs
    """

    def __init__(self):
        """Constructs a new sensor processor"""
        self._parameters = {}
        self._sensor_name = ""
        self.db = avista_data.database.db

    @abstractmethod
    def setup(self):
        """Abstract method for setting up parameters or sensor specific classes, especially
           if something needs to be setup after a sensor is loaded from the database"""
        pass

    def set_name(self, name):
        """Assigns the sensor name to which this processor belongs

        Args:
            **name (str)**: The new name of the sensor to which this processor belongs

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

    def add_parameter(self, key, value):
        """Adds a key/value parameter to the current sensor

        Args:
            **key (str)**: The key of the parameter to be added

            **value (str)**: The value of the parameter to be added

        Raises:
            Exception if the provided key or value are None or Empty

        """
        if key is None or key == "":
            raise Exception("key cannot be None or empty")
        if value is None or value == "":
            raise Exception("value cannot be None or empty")
        self._parameters[key] = value

    def remove_parameter(self, key):
        """Removes the parameter with the matching key

        Args:
            **key (str)**: The key of the parameter to be removed

        Raises:
            Exception if the provided key name is None or empty

        """
        if key is None or key == "":
            raise Exception("key cannot be None or empty")
        self._parameters.pop(key, None)

    def get_parameter_value(self, key):
        """Returns the value associated with the key provided

        Args:
            **key (str)**: The key to the desired value

        Raises:
            Exception, if the provided key is None or not in the parameters

        """
        if key is None or key == "" or key not in self._parameters.keys():
            raise Exception("Unknown key")
        return self._parameters[key]

    def has_parameter(self, key, value):
        """Tests whether the parameter provided (key, value) is associated with this sensor processor

        Args:
            **key (str)**: The parameter key

            **value (str)**: The parameter value

        Return:
            True if the parameter (key, value) is associated with this processor, False otherwise.

        Raises:
             Exception if the key or value are None or empty

        """
        if key is None or key == "":
            raise Exception("key cannot be None or Empty")
        if value is None or value == "":
            raise Exception("value cannot be None or Empty")
        return key in self._parameters.keys() and self._parameters[key] == value

    def _create_data_point(self, name, value, ts):
        """Constructs a data point with the given value and timestamp and commit the changes to the database

        Args:
            **name (str)**: the name of the data point

            **value (float)**: the measured value

            **ts (int)**: the timestamp

        Returns:
            the newly created DataPoint
        """
        dp = DataPoint(name=name, value=value, timestamp=ts)
        self.db.add(dp)
        sensor = self.db.query(Sensor).filter_by(name=self._sensor_name).first()
        sensor.add_data_point(dp)
        self.db.commit()
        return dp

    def process(self, ts):
        """Template method which collects data from the sensor and creates then creates the data points

        Args:
            **ts (int)**: the timestamp at which this reading is associated with

        Return:
            list: a list of created datapoints
        """
        data = self._read_sensor(ts)

        datapoints = []

        for item in data.items():
            # dict.items() is a list of tuples name first, then value
            datapoints.append(self._create_data_point(item[0], item[1], ts))

        return datapoints

    @abstractmethod
    def _read_sensor(self, ts):
        """Abstract method in which the reading of data from a sensor should be executed

        Args:
            **ts (int)**: timestamp of the data to be collected

        Returns:
            float: value of the associated sensor
        """
        pass
