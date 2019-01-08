import unittest

from flask import current_app

from app import create_app, db
from app.models import User


class RedisServerModelTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
