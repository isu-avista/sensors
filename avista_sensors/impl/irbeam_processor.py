import time
from avista_sensors.sensor_processor import SensorProcessor
import RPi.GPIO as GPIO


class IRBeamProcessor(SensorProcessor):
    """IR Break Beam sensor implementation

    Attributes:
        **channel (int)**: GPIO Pin

        **blades (int)**: Number of times per revolution that the beam is broken

        **_count (int)**: Count of the number of times the beam is broken during the measurement period

        **_start (int)**: time, in seconds since the epoch, when the measurment started
        
        **max_time (int)**: the timespan of measurement, in seconds.
    """

    def __init__(self):
        """Constructs a new IRBeamProcessor instance"""
        super().__init__()
        self.channel = None
        self.blades = None
        self._count = 0
        self._start = 0
        self.max_time = 15 # seconds

    def setup(self):
        """Sets up sensor configurations that should happen after loading from the database"""
        self.channel = int(self._parameters['channel'])
        self.blades = int(self._parameters['blades'])
        self.max_time = int(self._parameters['max_time'])
        GPIO.setup(self.channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def set_start(self):
        """Sets the start time of the sensor"""
        self._start = time.time()

    def callback(self):
        """Event based callback method that is executed when the sensor is read from"""
        self._count += 1

    def _read_sensor(self, ts):
        """Reads data from the sensor

        Args:
            **ts (int)**: timestamp of when the data was read
        """
        self.set_start()
        self._count = 0
        
        GPIO.add_event_detect(self.channel, GPIO.RISING, callback=self.callback)

        for i in range(1, self.max_time * 10):
            time.sleep(0.1)

        GPIO.remove_event_detect(self.channel)
        
        minutes = (time.time() - self._start) / 60
        rpm = (self._count / minutes) / self.blades

        data = {
            "rpm": rpm
        }

        return data
