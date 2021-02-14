import unittest
from tests.base_test import BaseTest
from avista_sensors.sensor_sweep import SensorSweep
from avista_sensors.sweep_state import SweepState
from avista_data.sensor import Sensor
from avista_data import db
from avista_data.unit import Unit
import time


class SensorSweepTest(BaseTest):

    def setUp(self):
        super().setUp()
        sensor = Sensor(name="Test", quantity="Quantity", module="avista_sensors.impl.random_processor",
                        cls="RandomProcessor", unit=Unit.F)
        db.session.add(sensor)
        db.session.commit()
        self.fixture = SensorSweep(self.app)

    def test_start(self):
        self.fixture.init()
        self.fixture.start()
        time.sleep(5)
        self.fixture.stop()
        self.fixture.join()
        self.assertEqual(SweepState.IDLE, self.fixture.state)

    def test_stop(self):
        self.assertEqual(SweepState.IDLE, self.fixture.state)
        self.fixture.init()
        self.fixture.start()
        time.sleep(2)
        self.assertEqual(SweepState.EXECUTING, self.fixture.state)
        self.fixture.stop()
        self.fixture.join()
        self.assertEqual(SweepState.IDLE, self.fixture.state)

    def test_init(self):
        self.fixture.init()
        self.assertEqual(1, len(self.fixture.processors))
        self.assertEqual(SweepState.INITIALIZING, self.fixture.state)


if __name__ == '__main__':
    unittest.main()
