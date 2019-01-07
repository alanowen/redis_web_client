import unittest

from flask import current_app

from app import create_app, db


class ClientTestClient(unittest.TestCase):

    def setUp(self):
        self.app = current_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app.app_context.pop()
