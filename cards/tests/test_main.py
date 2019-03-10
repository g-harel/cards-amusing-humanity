import unittest
import json
from app import create_app


class TestApp(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config['TESTING'] = True
        self.app = app.test_client()


    def test_404_on_invalid_url(self):
        # send the request and check the response status code
        response = self.app.get("/something", follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_root(self):
        # send the request and check the response status code
        response = self.app.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)