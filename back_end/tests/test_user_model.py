import unittest

from flask import current_app

from app import create_app, db
from app.models import User


class UserModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password='test_user_password')
        self.assertTrue(u.password_hash is not None)

    def test_password_getter(self):
        u = User(password='test_user_password')
        with self.assertRaises(AttributeError):
            password = u.password

    def test_password_verification(self):
        u = User(password='test_user_password')
        self.assertTrue(u.verify_password('test_user_password'))
        self.assertFalse(u.verify_password('fake_password'))

    def test_password_salts_are_random(self):
        u1 = User(password='test_user_password')
        u2 = User(password='test_user_password')
        self.assertNotEqual(u1.password_hash, u2.password_hash)

