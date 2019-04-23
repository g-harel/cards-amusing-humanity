import unittest
import json

import jwt

from main import app as tested_app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = tested_app.test_client()


    def test_sign_success(self):
        data = {"payload": {"test_sign_success": ""}}
        response = self.app.post("/sign", data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

        body = json.loads(str(response.data, "utf8"))
        self.assertTrue(type(body.get("token")) is str)


    def test_verify_success(self):
        data = {"payload": {"test_verify_success": ""}}
        sign_response = self.app.post("/sign", data=json.dumps(data), content_type="application/json")

        verify_response = self.app.post("/verify", data=str(sign_response.data, "utf8"), content_type="application/json")

        self.assertEqual(verify_response.status_code, 200)


    def test_verify_sign_contains_payload(self):
        data = {"payload": {"test_verify_sign_contains_payload": ""}}
        response = self.app.post("/sign", data=json.dumps(data), content_type="application/json")

        token = json.loads(response.data).get("token")
        payload = jwt.decode(token, verify=False, algorithms=["HS256"])

        self.assertDictContainsSubset(data["payload"], payload)
