#!/usr/bin/env python
import unittest
from flask import Flask
import avista_data
import avista_sensors
import os


def create_app(config):
    app = Flask("Test")
    app.config.from_object(config)
    avista_data.init(app)
    avista_sensors.init(app)
    return app


class TestConfig(object):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

        avista_data.db.create_all()

    def tearDown(self):
        avista_data.db.session.remove()
        avista_data.db.drop_all()
        self.app_context.pop()
