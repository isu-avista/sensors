import time
import logging
from avista_sensors.manager_state import ManagerState
from avista_sensors.processor_loader import ProcessorLoader


class ProcessorManager:
    """Manages the data collection from sensor processors

    Attributes:
        processors (list): sensor processors attached to this processor manager
        periodicity (int): periodicity of recording sensor data in milliseconds
        state (:obj: `ManagerState`): current state of the processor manager
        config (dict): Configuration file
    """

    def __init__(self, config):
        """Constructs a new ProcessorManager instance

        Args:
            config (dict): the base configuration for the process manager
        """
        self.processors = []
        self.periodicity = 5
        self.state = ManagerState.IDLE
        self.config = config

    def start(self):
        """Starts the processor manager"""
        self.state = ManagerState.STARTING

        logging.info("Processor Manager Starting")

        self.init()

        logging.info("Processor Manager Started")

        self.execute()

    def stop(self):
        """Stops the processor manager"""
        self.state = ManagerState.STOPPING

        logging.info("Processor Manager Stopping")

        self.state = ManagerState.IDLE

    def restart(self):
        """Restarts the processor manager"""
        logging.info("Processor Manager Restarting")
        self.stop()
        self.start()

    def init(self):
        """Initializes the processors using a processor loader"""
        self.state = ManagerState.INITIALIZING
        logging.info("Processor Manager Initializing")

        loader = ProcessorLoader()
        for item in self.config['sensors']:
            self.processors.append(load(item))

        logging.info("Processor Manager Initialized")

    def execute(self):
        """Starts the data collection process"""
        self.state = ManagerState.EXECUTING

        logging.info("Processor Manager Running")

        while self.state == ManagerState.EXECUTING:
            for p in self.processors:
                p.process()
            time.sleep(self.periodicity)
