import sys
import fake_rpi

sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi
sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO # Fake GPIO
sys.modules['smbus'] = fake_rpi.smbus # Fake smbus (I2C)

import unittest
from avista_sensors.impl.simulated_processor import SimulatedProcessor
from datetime import datetime
from pathlib import Path
import os


class SimulatedProcessorTest(unittest.TestCase):

    def setUp(self):
        path = Path(os.getcwd()) / ".." / "testdata" / "simulated.csv"
        self.fixture = SimulatedProcessor()
        self.fixture._init(path)

    def test_read_sensor(self):
        result = self.fixture._read_sensor(int(datetime.timestamp(datetime.now())))
        print(f"Result: {result}")
        self.assertTrue(result['simulated'] > 0)
        self.assertTrue(isinstance(result, dict))


if __name__ == '__main__':
    unittest.main()
