"""This module is used to provide the capability to read data from sensors attached to the IoT device"""


def init(a):
    """Initializes the module with the provided Flask app

    Args:
        a (:obj: `Flask`): the flask app with which this sensor package is to be connected
    """
    global app
    app = a


app = None

import avista_sensors.impl
import avista_sensors.manager_state
import avista_sensors.processor_loader
import avista_sensors.processor_manager
import avista_sensors.sensor_processor
