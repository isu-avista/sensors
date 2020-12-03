import unittest
import os
import avista_sensors.processor_loader as pl
from avista_sensors.impl.random_processor import RandomProcessor
import json


class ProcessorLoaderTest(unittest.TestCase):

    def test_dynamic_import(self):
        module = "avista_sensors.impl.random_processor"
        klass = "RandomProcessor"
        result = pl.dynamic_import(module, klass)
        self.assertTrue(isinstance(result, RandomProcessor), "not expected type")

    def test_dynamic_import_none_module(self):
        module = None
        klass = "RandomProcessor"
        result = pl.dynamic_import(module, klass)
        self.assertIsNone(result, "not none")

    def test_dynamic_import_empty_module(self):
        module = ""
        klass = "RandomProcessor"
        result = pl.dynamic_import(module, klass)
        self.assertIsNone(result, "not none")

    def test_dynamic_import_none_class(self):
        module = "avista_sensors.impl.random_processor"
        klass = None
        result = pl.dynamic_import(module, klass)
        self.assertIsNone(result, "not none")

    def test_dynamic_import_empty_class(self):
        module = "avista_sensors.impl.random_processor"
        klass = None
        result = pl.dynamic_import(module, klass)
        self.assertIsNone(result, "not none")

    def test_load_from_config(self):
        os.chdir("..")
        os.chdir("config")
        path = os.getcwd()
        sensors = pl.load_from_config(path)
        self.assertEqual(2, len(sensors), "not same length")

    def test_load_from_json(self):
        dct = {
            'module': 'avista_sensors.impl.random_processor',
            'cls': 'RandomProcessor',
            'name': 'Test',
            'pinout': [
                {'var': 'x', 'pin': 1},
                {'var': 'y', 'pin': 2}
            ]
        }
        result = pl.load_from_json(json.dumps(dct))
        self.assertTrue(isinstance(result, RandomProcessor), "not expected type")

    def test_load_from_json_none(self):
        data = None
        result = pl.load_from_json(data)
        self.assertIsNone(result)

    def test_import_from(self):
        module = 'avista_sensors.impl.random_processor.RandomProcessor'
        result = pl.import_from(module)
        self.assertTrue(isinstance(result, RandomProcessor.__class__), "not expected type")

    def test_import_from_none(self):
        module = None
        with self.assertRaises(Exception):
            pl.import_from(module)

    def test_import_from_empty(self):
        module = ''
        with self.assertRaises(Exception):
            pl.import_from(module)

    def test_load_sensor_from_dict(self):
        dct = {
            'module': 'avista_sensors.impl.random_processor',
            'cls': 'RandomProcessor',
            'name': 'Test',
            'pinout': [
                {'var': 'x', 'pin': 1},
                {'var': 'y', 'pin': 2}
            ]
        }
        result = pl.load_sensor_from_dict(dct)
        self.assertTrue(isinstance(result, RandomProcessor), "not expected type")
        self.assertEqual("Test", result.get_name())
        self.assertTrue(result.has_pin_out("x", 1))
        self.assertTrue(result.has_pin_out("y", 2))

    def test_load_sensor_from_dict_no_module(self):
        dct = {
            'cls': 'RandomProcessor',
            'name': 'Test',
            'pinout': [
                {'var': 'x', 'pin': 1},
                {'var': 'y', 'pin': 2}
            ]
        }
        result = pl.load_sensor_from_dict(dct)
        self.assertIsNone(result)

    def test_load_sensor_from_dict_empty_module(self):
        dct = {
            'module': '',
            'cls': 'RandomProcessor',
            'name': 'Test',
            'pinout': [
                {'var': 'x', 'pin': 1},
                {'var': 'y', 'pin': 2}
            ]
        }
        result = pl.load_sensor_from_dict(dct)
        self.assertIsNone(result)

    def test_load_sensor_from_dict_empty_cls(self):
        dct = {
            'module': 'avista_sensors.impl.random_processor',
            'cls': '',
            'name': 'Test',
            'pinout': [
                {'var': 'x', 'pin': 1},
                {'var': 'y', 'pin': 2}
            ]
        }
        result = pl.load_sensor_from_dict(dct)
        self.assertIsNone(result)

    def test_load_sensor_from_dict_no_cls(self):
        dct = {
            'module': 'avista_sensors.impl.random_processor',
            'name': 'Test',
            'pinout': [
                {'var': 'x', 'pin': 1},
                {'var': 'y', 'pin': 2}
            ]
        }
        result = pl.load_sensor_from_dict(dct)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
