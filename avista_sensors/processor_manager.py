import time
import logging
from avista_sensors.manager_state import ManagerState
import avista_sensors.processor_loader as pl
from avista_data.sensor import Sensor
from threading import Thread
import threading
from datetime import datetime


class ProcessorManager(Thread):
    """Manages the data collection from sensor processors

    After constructing a ProcessorManager, you should call the init() method followed
    by the start() method.

    Attributes:
        processors (list): sensor processors attached to this processor manager
        periodicity (int): periodicity of recording sensor data in milliseconds
        state (:obj: `ManagerState`): current state of the processor manager
        config (dict): Configuration file
    """

    def __init__(self, app, config=None, *args, **kwargs):
        """Constructs a new ProcessorManager instance

        Args:
            app (:obj: `Flask`): The Flask app to which this is associated
            config (dict): the base configuration for the process manager
            *args: variable args passed to super class
            **kwargs: keyword args passed to super class
        """
        super(ProcessorManager, self).__init__(*args, **kwargs)
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
        """Starts the processor manager"""
        self.state = ManagerState.STARTING

        logging.info("Processor Manager Starting")

    def stop(self):
        """Stops the processor manager by setting the _kill event"""
        self.state = ManagerState.STOPPING
        print("STOPPING")

        logging.info("Processor Manager Stopping")

        self.state = ManagerState.IDLE
        self._kill.set()

    def stopped(self):
        """Determines if the processor manager is stopped

        Returns:
            True if the _kill event has been set, False otherwise
        """
        return self._kill.isSet()

    def init(self):
        """Initializes the processors using a processor loader"""
        self.state = ManagerState.INITIALIZING
        logging.info("Processor Manager Initializing")

        for sensor in Sensor.query.all():
            self.processors.append(pl.load_sensor_from_dict(sensor.to_dict()))

        logging.info("Processor Manager Initialized")

    def _execute(self):
        """Contains the main logic for the processor manager

        Here each attached sensor is polled, the process sleeps for the specified periodicity then continues.
        This process goes on until the processor manager is stopped.
        """
        self.state = ManagerState.EXECUTING

        logging.info("Processor Manager Running")

        while True:
            with self.app.app_context():
                if self.stopped():
                    return
                print(self.state)
                for p in self.processors:
                    p.process(int(datetime.timestamp(datetime.now())))
                time.sleep(self.periodicity)
