import unittest
from datetime import datetime
from avista_sensors.impl.random_processor import RandomProcessor


class RandomProcessorTest(unittest.TestCase):

    def setUp(self):
        self.fixture = RandomProcessor()

    def test_read_sensor(self):
        result = self.fixture._read_sensor(int(datetime.timestamp(datetime.now())))
        self.assertTrue(result['random'] > 0)
        self.assertTrue(isinstance(result['random'], float))

    def test_read_sensor_none(self):
        with self.assertRaises(Exception):
            self.fixture._read_sensor(None)

    def test_read_sensor_range(self):
        with self.assertRaises(Exception):
            self.fixture._read_sensor(1)


if __name__ == '__main__':
    unittest.main()
