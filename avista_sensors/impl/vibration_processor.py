import time
from avista_sensors.sensor_processor import SensorProcessor
from mpu6050 import mpu6050
import numpy.fft as nfft
import numpy as np


class VibrationProcessor(SensorProcessor):
    """MPU6050 sensor implementation (Accelerometer and Vibration)

    Attributes:
        **_address (int)**: I2C address

        **_sensor (:obj: `mpu6050`)**: mpu6050 sensor object

        **_time_step (float)**: short periodicity to capture movement
    """

    def __init__(self):
        """Constructs a new VibrationSensor instance"""
        super().__init__()
        self._address = None
        self._sensor = None
        self._time_step = 0.005

    def setup(self):
        """Sets up sensor configurations that should happen after loading from the database"""
        self._address = int(self._parameters['address'], 16)
        self._sensor = mpu6050(self._address)

    def _read_sensor(self, ts):
        """Reads data from the sensor

        Args:
            **ts (int)**: timestamp of when the data was read
        """
        x = np.empty([400])
        y = np.empty([400])
        z = np.empty([400])

        self._sample(x, y, z)

        data = {
            "x": self._find_freq(x),
            "y": self._find_freq(y),
            "z": self._find_freq(z)
        }

        return data

    def _find_freq(self, data):
        """Performs an fft on the data to extract the frequency

        Args:
            **data (:obj: `array`)**: a collected data sample
        """
        # execute the fft
        w = nfft.fft(data)
        freqs = nfft.fftfreq(len(data), d=self._time_step)

        # get the power
        pwr = np.abs(data)

        # remove negatives
        freqs = freqs[1:int(len(freqs) / 2)]
        pwr = pwr[1:int(len(pwr) / 2)]

        # find max power and its index
        pmax = np.max(pwr)
        condition = (pwr == pmax)
        index = np.where(condition)

        # return frequency
        return freqs[index][0]

    def _sample(self, x, y, z):
        """Samples acceleration data

        Args:
            **x (:obj: `array`)**: a numpy array to store x acceleration data

            **y (:obj: `array`)**: a numpy array to store y acceleration data

            **z (:obj: `array`)**: a numpy array to store z acceleration data
        """
        for i in range(400):
            data = self._sensor.get_accel_data()
            x[i] = data["x"]
            y[i] = data["y"]
            z[i] = data["z"]
            time.sleep(self._time_step)
