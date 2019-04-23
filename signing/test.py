import unittest
import json

from main import app as tested_app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = tested_app.test_client()


    def test_sign_success(self):
        data = {"payload": {"a": 0}}
        response = self.app.post("/sign", data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

        body = json.loads(str(response.data, "utf8"))
        self.assertTrue(type(body.get("token")) is str)


    def test_verify_success(self):
        data = {"payload": {"b": 0}}
        sign_response = self.app.post("/sign", data=json.dumps(data), content_type="application/json")
        verify_response = self.app.post("/verify", data=str(sign_response.data, "utf8"), content_type="application/json")
        self.assertEqual(verify_response.status_code, 200)
