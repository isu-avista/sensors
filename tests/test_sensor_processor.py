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
        self.fixture.add_pinout("test", 2)

    def test_name(self):
        self.fixture.set_name("Test2")
        self.assertEqual("Test2", self.fixture.get_name())

    def test_name_none(self):
        with self.assertRaises(Exception):
            self.fixture.set_name(None)

    def test_name_empty(self):
        with self.assertRaises(Exception):
            self.fixture.set_name("")

    def test_add_pinout(self):
        self.fixture.add_pinout("var", 1)
        self.assertTrue(self.fixture.has_pin_out("var", 1))

    def test_add_pinout_none_var(self):
        with self.assertRaises(Exception):
            self.fixture.add_pinout(None, 1)

    def test_add_pinout_empty_var(self):
        with self.assertRaises(Exception):
            self.fixture.add_pinout("", 1)

    def test_add_pinout_pin_range(self):
        with self.assertRaises(Exception):
            self.fixture.add_pinout("var", 0)

    def test_add_pinout_pin_range2(self):
        with self.assertRaises(Exception):
            self.fixture.add_pinout("var", 41)

    def test_remove_pinout(self):
        self.fixture.remove_pinout("test")
        self.assertFalse(self.fixture.has_pin_out("test", 2))

    def test_remove_pinout_none(self):
        with self.assertRaises(Exception):
            self.fixture.remove_pinout(None)

    def test_remove_pinout_empty(self):
        with self.assertRaises(Exception):
            self.fixture.remove_pinout("")

    def test_pin(self):
        self.assertEqual(2, self.fixture.get_pin("test"))

    def test_pin_none(self):
        with self.assertRaises(Exception):
            self.fixture.get_pin(None)

    def test_pin_empty(self):
        with self.assertRaises(Exception):
            self.fixture.get_pin("")

    def test_pin_unknown(self):
        with self.assertRaises(Exception):
            self.fixture.get_pin("foo")

    def test_has_pin_out(self):
        self.assertTrue(self.fixture.has_pin_out("test", 2))
        self.assertFalse(self.fixture.has_pin_out("test", 1))

    def test_has_pin_out_none_pin(self):
        with self.assertRaises(Exception):
            self.fixture.has_pin_out(None, 1)

    def test_has_pin_out_none_var(self):
        with self.assertRaises(Exception):
            self.fixture.has_pin_out("test", None)

    def test_has_pin_out_empty_var(self):
        with self.assertRaises(Exception):
            self.fixture.has_pin_out("", 1)

    def test_has_pin_out_pin_range(self):
        with self.assertRaises(Exception):
            self.fixture.has_pin_out("test", 0)

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
