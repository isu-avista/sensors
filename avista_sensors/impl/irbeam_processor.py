import time
from avista_sensors.sensor_processor import SensorProcessor
import RPi.GPIO as GPIO


class IRBeamProcessor(SensorProcessor):
    """IR Break Beam sensor implementation

    Attributes:
        **channel (int)**: adc converter channel

        **blades (int)**:

        **_sample (int)**:

        **_count (int)**:

        **_start (int)**: start time

        **_end (int)**: end time

        **_finished (bool)**:

        **_rpm (float)**:
    """

    def __init__(self):
        """Constructs a new IRBeamProcessor instance"""
        super().__init__()
        self.channel = None
        self.blades = None
        self._sample = None
        self._count = 0
        self._start = 0
        self._end = 0
        self._finished = False
        self._rpm = 0

    def setup(self):
        """Sets up sensor configurations that should happen after loading from the database"""
        self.channel = int(self._parameters['channel'])
        self.blades = int(self._parameters['blades'])
        self._sample = int(self._sample['sample'])
        GPIO.setup(self.channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def set_start(self):
        """Sets the start time of the sensor"""
        self._start = time.time()

    def set_end(self):
        """Sets the end time of the sensor"""
        self._end = time.time()

    def callback(self):
        """Event based callback method that is executed when the sensor is read from"""
        if not self._count:
            self.set_start()
            self._count += 1
        else:
            self._count += 1

        if self._count == self._sample:
            self.set_end()
            delta = self._end - self._start
            delta = delta / 60
            self._rpm = (self._sample / delta) / 7
            self._count = 0
            self._finished = True

    def _read_sensor(self, ts):
        """Reads data from the sensor

        Args:
            **ts (int)**: timestamp of when the data was read
        """
        GPIO.add_event_detect(self.channel, GPIO.RISING, callback=self.callback)

        while not self._finished:
            time.sleep(0.1)

        GPIO.remove_event_detect(self.channel)

        data = {
            "rpm": self._rpm
        }

        return data
