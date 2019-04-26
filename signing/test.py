import unittest
import json

import jwt

from main import app as tested_app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = tested_app.test_client()


    def test_sign_400_payload_missing(self):
        data = {}

        response = self.app.post("/sign", data=json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 400, msg=response.data)


    def test_sign_400_payload_empty(self):
        data = {"payload": None}

        response = self.app.post("/sign", data=json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 400, msg=response.data)


    def test_sign_400_payload_wrong_type(self):
        data = {"payload": ""}

        response = self.app.post("/sign", data=json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 400, msg=response.data)


    def test_sign_200(self):
        data = {"payload": {"test_sign_200": ""}}

        response = self.app.post("/sign", data=json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 200, msg=response.data)
        self.assertTrue(type(json.loads(str(response.data, "utf8")).get("token")) is str)


    def test_verify_400_token_missing(self):
        data = {}

        response = self.app.post("/verify", data=json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 400, msg=response.data)


    def test_verify_400_token_wrong_type(self):
        data = {"token": 0}

        response = self.app.post("/verify", data=json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 400, msg=response.data)


    def test_verify_401_token_invalid(self):
        data = {"token": "test_verify_401_token_invalid"}

        response = self.app.post("/verify", data=json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 401, msg=response.data)


    def test_verify_200_success(self):
        data = {"payload": {"test_verify_200": ""}}

        sign_response = self.app.post("/sign", data=json.dumps(data), content_type="application/json")
        verify_response = self.app.post("/verify", data=str(sign_response.data, "utf8"), content_type="application/json")

        self.assertEqual(verify_response.status_code, 200, msg=verify_response.data)


    def test_verify_200_sign_contains_payload(self):
        data = {"payload": {"test_verify_200_sign_contains_payload": ""}}

        response = self.app.post("/sign", data=json.dumps(data), content_type="application/json")
        token = json.loads(response.data).get("token")
        payload = jwt.decode(token, verify=False, algorithms=["HS256"])

        self.assertEqual(response.status_code, 200, msg=response.data)
        self.assertDictContainsSubset(data["payload"], payload)
