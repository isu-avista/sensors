import time
from avista_sensors.sensor_processor import SensorProcessor
import RPi.GPIO as GPIO


class IRBeamProcessor(SensorProcessor):

    def __init__(self):
        super().__init__()
        self.channel = self._parameters['channel']
        self.blades = self._parameters['blades']
        self._sample = self._parameters['sample']
        self._count = 0
        self._start = 0
        self._end = 0
        self._finished = False
        self._rpm = 0
        self._setup()

    def _setup(self):
        GPIO.add_event_detect(self.channel, GPIO.RISING, callback=self.callback)

        while not self._finished:
            time.sleep(0.1)
        GPIO.remove_event_detect(self.channel)
        return self._rpm

    def set_start(self):
        self._start = time.time()

    def set_end(self):
        self._end = time.time()

    def callback(self):
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
        pass
