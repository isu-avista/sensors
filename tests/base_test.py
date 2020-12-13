#!/usr/bin/env python
import unittest
from flask import Flask
import avista_data.data_manager
import os


def create_app(config):
    app = Flask("Test")
    app.app_context().push()
    app.config.from_object(config)
    avista_data.data_manager.init()
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

        self.db = avista_data.data_manager.get_db()
        self.db.create_all()
        avista_data.populate_initial_data()

    def tearDown(self):
        avista_data.db.session.remove()
        avista_data.db.drop_all()
        self.app_context.pop()
