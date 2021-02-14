import time
import logging
from threading import Thread
import threading
from datetime import datetime
from avista_sensors.sweep_state import SweepState
import avista_sensors.processor_loader as pl
from avista_data.sensor import Sensor
from avista_sensors.data_transporter import DataTransporter
import RPi.GPIO as GPIO


class SensorSweep(Thread):
    """Manages the data collection from sensor processors

    After constructing a SensorSweep, you should call the init() method followed
    by the run() method.

    Attributes:
        **processors (list)**: sensor processors attached to this processor manager

        **periodicity (int)**: periodicity of recording sensor data in milliseconds

        **max_holding_period (int)**: number of sensor periods to pass through before sending data to portal

        **state (:obj: `ManagerState`)**: current state of the processor manager

        **config (dict)**: Configuration file
    """

    def __init__(self, app, periodicity, holding, config=None, *args, **kwargs):
        """Constructs a new SensorSweep instance

        Args:
            **app (:obj: `Flask`)**: The Flask app to which this is associated

            **config (dict)**: the base configuration for the process manager

            **periodicity (float)**: the number of seconds to wait between sensor recordings

            **holding (int)**: number of periods of data to store prior to sending to the server

            __*args__: variable args passed to super class

            __**kwargs__: keyword args passed to super class
        """
        super(SensorSweep, self).__init__(*args, **kwargs)
        self.processors = []
        self.periodicity = periodicity
        self.max_holding_period = holding
        self.state = SweepState.IDLE
        self.config = config
        self._kill = threading.Event()
        self._transporter = DataTransporter()
        self.app = app

    def set_periodicity(self, periodicity):
        """
        Sets the time to wait between sensor sweeps to the provided value.

        Args:
            **periodicity (float)**: the number of seconds to wait in between sensor data collection sweeps

        Raises:
             Exception: when the provided value is either not a float or is <= 0
        """
        if float(periodicity) and periodicity > 0:
            self.periodicity = periodicity
        else:
            raise Exception("periodicity must be a float greater than 0")

    def get_periodicity(self):
        """
        Returns the current value of the periodicity

        Returns:
            current periodicity
        """
        return self.periodicity

    def set_holding_period(self, holding):
        """
        Updates the number of periods to hold data to the given value

        Args:
            **holding (int)**: The number of periods for which collected data will be held in the database be for
                               sending it to the server. Each period is defined by the periodicity value.

        Raises:
            Exception: if the provided value is not an integer or has a value <= 0
        """

        if int(holding) and holding > 0:
            self.max_holding_period = holding
        else:
            raise Exception("holding period must be an integer greater than 0")

    def get_holding_period(self):
        """
        Returns the current number of periods to hold data in the database

        Returns:
            current holding period value
        """
        return self.max_holding_period

    def run(self):
        """Main execution body of the thread"""
        self._begin()
        self._execute()

    def _begin(self):
        """Starts the sensor sweep"""
        self.state = SweepState.STARTING

        logging.info("Sensor Sweep Starting")

    def stop(self):
        """Stops the sensor sweep by setting the _kill event"""
        self.state = SweepState.STOPPING

        logging.info("Sensor Sweep Stopping")

        GPIO.cleanup()

        self.state = SweepState.IDLE
        self._kill.set()

    def stopped(self):
        """Determines if the sensor sweep is stopped

        Returns:
            True if the _kill event has been set, False otherwise
        """
        return self._kill.isSet()

    def init(self):
        """Initializes the processors using a processor loader"""
        self.state = SweepState.INITIALIZING
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
        self.state = SweepState.EXECUTING

        logging.info("Sensor Sweep Running")

        periods = 0
        while True:
            with self.app.app_context():
                if self.stopped():
                    return
                for p in self.processors:
                    if p is not None:
                        p.process(int(datetime.timestamp(datetime.now())))
                time.sleep(self.periodicity)
                periods += 1
                if periods >= self.max_holding_period:
                    self._transporter.transfer()
