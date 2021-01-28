import unittest
from avista_data.data_point import DataPoint
from avista_data.sensor import Sensor
from avista_data.unit import Unit
from tests.base_test import BaseTest
from datetime import datetime
from avista_data import db
from avista_sensors.impl.random_processor import RandomProcessor


class SensorProcessorTest(BaseTest):

    def setUp(self):
        super().setUp()
        self.sensor = Sensor()
        self.sensor.set_name("Test")
        self.sensor.set_quantity("Test")
        self.sensor.set_class("Test")
        self.sensor.set_module('test.test')
        self.sensor.set_unit(Unit.kWh)
        db.session.add(self.sensor)
        db.session.commit()

        self.fixture = RandomProcessor()
        self.fixture.set_name("Test")
        self.fixture.add_parameter("TestKey", "TestValue")

    def test_name(self):
        self.fixture.set_name("Test2")
        self.assertEqual("Test2", self.fixture.get_name())

    def test_name_none(self):
        with self.assertRaises(Exception):
            self.fixture.set_name(None)

    def test_name_empty(self):
        with self.assertRaises(Exception):
            self.fixture.set_name("")

    def test_add_parameter(self):
        self.fixture.add_parameter("TestKey2", "TestValue2")
        self.assertTrue(self.fixture.has_parameter("TestKey2", "TestValue2"))

    def test_add_parameter_none_key(self):
        with self.assertRaises(Exception):
            self.fixture.add_parameter(None, "TestValue2")

    def test_add_parameter_empty_key(self):
        with self.assertRaises(Exception):
            self.fixture.add_parameter("", "TestValue2")

    def test_add_parameter_none_value(self):
        with self.assertRaises(Exception):
            self.fixture.add_parameter("TestKey2", None)

    def test_add_parameter_empty_value(self):
        with self.assertRaises(Exception):
            self.fixture.add_parameter("TestKey2", "")

    def test_remove_parameter(self):
        self.fixture.remove_parameter("TestKey")
        self.assertFalse(self.fixture.has_parameter("TestKey", "TestValue"))

    def test_remove_parameter_none(self):
        with self.assertRaises(Exception):
            self.fixture.remove_parameter(None)

    def test_remove_parameter_empty(self):
        with self.assertRaises(Exception):
            self.fixture.remove_parameter("")

    def test_value(self):
        self.assertEqual("TestValue", self.fixture.get_parameter_value("TestKey"))

    def test_parameter_none(self):
        with self.assertRaises(Exception):
            self.fixture.get_parameter_value(None)

    def test_parameter_empty(self):
        with self.assertRaises(Exception):
            self.fixture.get_parameter_value("")

    def test_parameter_unknown(self):
        with self.assertRaises(Exception):
            self.fixture.get_parameter_value("foo")

    def test_has_parameter(self):
        self.assertTrue(self.fixture.has_parameter("TestKey", "TestValue"))
        self.assertFalse(self.fixture.has_parameter("TestKey2", "TestValue2"))

    def test_has_parameter_none_key(self):
        with self.assertRaises(Exception):
            self.fixture.has_parameter(None, "TestValue")

    def test_has_parameter_none_value(self):
        with self.assertRaises(Exception):
            self.fixture.has_parameter("TestKey", None)

    def test_has_parameter_empty_key(self):
        with self.assertRaises(Exception):
            self.fixture.has_parameter("", "TestValue")

    def test_process(self):
        ts = int(datetime.timestamp(datetime.now()))
        result = self.fixture.process(ts)
        self.assertTrue(isinstance(result, DataPoint))
        self.assertEqual(ts, result.get_timestamp())
        self.assertTrue(result.get_value() > 0)

    def test_process_none(self):
        with self.assertRaises(Exception):
            self.fixture.process(None)

    def test_process_range(self):
        with self.assertRaises(Exception):
            self.fixture.process(1)


if __name__ == '__main__':
    unittest.main()
