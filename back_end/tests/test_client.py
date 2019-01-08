import json
import unittest

from flask import current_app

from app import create_app, db


class ClientTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def _post_auth_login(self, **kwargs):
        response = self.client.post('/auth/login', **kwargs)
        return response.status, json.loads(response.data)

    # def test_user_register_with_no_used_mail(self):
    #     pass
    #
    # def test_user_register_with_used_mail(self):
    #     pass
    #

    def test_user_register(self):
        response = self.client.post('/user/singup')

    def test_existing_user_login(self):
        response = self.client.post('/auth/login',
                                    data=dict(email='user@domain.com',
                                              password='password'))

        status, data = response.status, response.data

        self.assertEqual(status, '200 OK')

        data = json.loads(data)

        self.assertEqual(data['code'], 1)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['text'], 'Email or password is incorrect.')

    def test_none_existing_user_login(self):

        status, data = self._post_auth_login(data=dict(email='user@domain.com',
                                                       password='password'))
        self.assertEqual(status, '200 OK')
        self.assertEqual(data['code'], 1)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['text'], 'Email or password is incorrect.')
