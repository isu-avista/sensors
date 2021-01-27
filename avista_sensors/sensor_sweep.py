import time
import logging
from threading import Thread
import threading
from datetime import datetime
from avista_sensors.manager_state import ManagerState
import avista_sensors.processor_loader as pl
from avista_data.sensor import Sensor
import RPi.GPIO as GPIO


class SensorSweep(Thread):
    """Manages the data collection from sensor processors

    After constructing a SensorSweep, you should call the init() method followed
    by the run() method.

    Attributes:
        **processors (list)**: sensor processors attached to this processor manager

        **periodicity (int)**: periodicity of recording sensor data in milliseconds

        **state (:obj: `ManagerState`)**: current state of the processor manager

        **config (dict)**: Configuration file
    """

    def __init__(self, app, config=None, *args, **kwargs):
        """Constructs a new SensorSweep instance

        Args:
            **app (:obj: `Flask`)**: The Flask app to which this is associated

            **config (dict)**: the base configuration for the process manager

            __*args__: variable args passed to super class

            __**kwargs__: keyword args passed to super class
        """
        super(SensorSweep, self).__init__(*args, **kwargs)
        self.processors = []
        self.periodicity = 1
        self.state = ManagerState.IDLE
        self.config = config
        self._kill = threading.Event()
        self.app = app

    def run(self):
        """Main execution body of the thread"""
        self._begin()
        self._execute()

    def _begin(self):
        """Starts the sensor sweep"""
        self.state = ManagerState.STARTING

        logging.info("Sensor Sweep Starting")

    def stop(self):
        """Stops the sensor sweep by setting the _kill event"""
        self.state = ManagerState.STOPPING

        logging.info("Sensor Sweep Stopping")

        GPIO.cleanup()

        self.state = ManagerState.IDLE
        self._kill.set()

    def stopped(self):
        """Determines if the sensor sweep is stopped

        Returns:
            True if the _kill event has been set, False otherwise
        """
        return self._kill.isSet()

    def init(self):
        """Initializes the processors using a processor loader"""
        self.state = ManagerState.INITIALIZING
        logging.info("Sensor Sweep Initializing")

        GPIO.setmode(GPIO.BCM)

        for sensor in Sensor.query.all():
            self.processors.append(pl.load_sensor_from_dict(sensor.to_dict()))

        logging.info("Sensor Sweep Initialized")

    def _execute(self):
        """Contains the main logic for the sensor sweep

        Here each attached sensor is polled, the process sleeps for the specified periodicity then continues.
        This process goes on until the sensor sweep is stopped.
        """
        self.state = ManagerState.EXECUTING

        logging.info("Sensor Sweep Running")

        while True:
            with self.app.app_context():
                if self.stopped():
                    return
                for p in self.processors:
                    if p is not None:
                        p.process(int(datetime.timestamp(datetime.now())))
                time.sleep(self.periodicity)
