from avista_sensors.sensor_processor import SensorProcessor
import numpy as np


class SimulatedProcessor(SensorProcessor):
    """An example sensor processor which utilizes empirical data to simulate sensor readings

    Attributes:
        **__data (np.Array)**: A numpy array of the data read in from a file

        **__probs (list)**: list of probabilities associated with values

        **__unique_elements (list)**: the list of unique values in the data
    """

    def setup(self):
        pass

    def __init__(self):
        """Constructs a new simulated processor"""
        super(SimulatedProcessor, self).__init__()
        self.__data = []
        self.__probs = []
        self.__unique_elements = []

    def _init(self, file):
        """Constructs a new simulated processor based on the data from the provided file

        Args:
            **file (str)**: path to the file to read the data from
        """
        self.__data = np.genfromtxt(file, delimiter=",")
        self.__unique_elements, counts_elements = np.unique(self.__data, return_counts=True)
        self.__probs = counts_elements / self.__data.size

    def _read_sensor(self, ts):
        """Implementation of read sensor which returns a simulated data point based on the underlying distribution

        Args:
            **ts (int)**: time stamp of the data to be collected

        Returns:
            float: Simulated data
        """
        return np.random.choice(self.__unique_elements, 1, replace=False, p=self.__probs)[0]
