import unittest
import json

import jwt

from main import app as tested_app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = tested_app.test_client()


    def test(self):
        print("test")
