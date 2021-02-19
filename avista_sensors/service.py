from avista_sensors import config
from avista_sensors.sensor_sweep import SensorSweep
from avista_data.device import Device
from pathlib import Path
import avista_data
import logging
import os
import socket


class Service:
    """Represents the base service class

    Attributes:
        _config (dict): The app configuration
        _name (str): The service name
    """

    _instance = None

    @classmethod
    def get_instance(cls):
        """ Static access method

        Returns:
            The singleton instance of IoTServer
        """
        if Service._instance is None:
            cls()
        return Service._instance

    def __init__(self):
        """Constructs a new service the current app with the given name """
        if Service._instance is not None:
            raise Exception("This class is a singletion!")
        else:
            Service._instance = self
        self._config = None
        self._config_path = Path(os.environ.get("CONFIG_PATH"))
        self._config_file = 'conf.yml'
        self._log_path = Path(os.environ.get("LOG_PATH"))
        self._log_file = 'server.log'
        self.hostname = '0.0.0.0'
        self._name = __name__
        self.sweep = None
        self.db = None

    def initialize(self):
        """Initializes the service"""
        self._setup_logging()
        logging.info("Initializing")
        self._load_config()
        self._setup_database()
        self._setup_sweep()

    def _setup_sweep(self):
        periodicity = self.db.query(Device).first().get_periodicity()
        self.sweep = SensorSweep(self.db, periodicity, 3)
        self.sweep.init()

    def _setup_logging(self):
        logging.basicConfig(filename=self._log_path / self._log_file, level=logging.DEBUG)

    def _load_config(self):
        """Loads the flask configuration"""
        logging.info("Loading Service Configuration")

        self._config = config.load(self._config_path / self._config_file)

    def __generate_db_uri(self):
        typ = ip = port = user = passwd = db = None
        for key in self._config:
            if key == "DBMS Type":
                typ = self._config[key]
            elif key == "DBMS IP":
                ip = self._config[key]
            elif key == "DBMS Port":
                port = self._config[key]
            elif key == "DBMS User":
                user = self._config[key]
            elif key == "DBMS Pass":
                passwd = self._config[key]
            elif key == "DBMS DB Name":
                db = self._config[key]

        user_pass = ''
        if user and passwd:
            user_pass = f'{user}:{passwd}@'

        ip_port = ''
        if ip and port:
            ip_port = f'{ip}:{port}'
        elif ip and not port:
            ip_port = ip
        return f'{typ}://{user_pass}{ip_port}/{db}'

    def _setup_database(self):
        uri = self.__generate_db_uri()
        avista_data.database.init(uri)
        self.db = avista_data.database.db

    def run(self):
        self.sweep.run()

    def get_hostname(self):
        return self.hostname

    def get_ipaddress(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(10)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except socket.error:
            return "0.0.0.0"
