import unittest
from unittest.mock import patch, ANY
import json

import jwt

from main import app as tested_app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = tested_app.test_client()


    def test_submit_400_token_missing(self):
        data = {"choice": ""}

        response = self.app.post("/submit", data=json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 400, msg=response.data)


    def test_submit_400_token_wrong_type(self):
        data = {"token": 0, "choice": ""}

        response = self.app.post("/submit", data=json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 400, msg=response.data)


    def test_submit_400_choice_missing(self):
        data = {"token": "choice_missing"}

        response = self.app.post("/submit", data=json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 400, msg=response.data)


    def test_submit_400_choice_wrong_type(self):
        data = {"token": "choice_wrong_type", "choice": 0}

        response = self.app.post("/submit", data=json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 400, msg=response.data)


    @patch("requests.post", return_value={"status_code": 401})
    def test_submit_401_token_invalid(self, mock_post):
        data = {"token": "token_invalid", "choice": "token_invalid"}

        response = self.app.post("/submit", data=json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 401, msg=response.data)
        mock_post.assert_called_with(ANY, json={"token": data["token"]})


    @patch("requests.post", return_value={"status_code": 500})
    def test_submit_500_downstream_error(self, mock_post):
        data = {"token": "downstream_error", "choice": "downstream_error"}

        response = self.app.post("/submit", data=json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 500, msg=response.data)
        mock_post.assert_called_with(ANY, json={"token": data["token"]})


    @patch("requests.post", return_value={"status_code": 200})
    @patch("persistence.tokens.TokenStore.get", return_value=True)
    def test_submit_403_duplicate_submission(self, mock_get, mock_post):
        data = {"token": "duplicate_submission", "choice": "duplicate_submission"}

        response = self.app.post("/submit", data=json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 403, msg=response.data)
        mock_get.assert_called_with(data["token"])


    @patch("requests.post", return_value={"status_code": 200})
    @patch("persistence.tokens.TokenStore.get", return_value=False)
    def test_submit_400_token_question_missing(self, mock_get, mock_post):
        payload = {"answers": []}
        data = {"token": str(jwt.encode(payload, "", algorithm="HS256"), "utf8"), "choice": "token_question_missing"}

        response = self.app.post("/submit", data=json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 400, msg=response.data)


    @patch("requests.post", return_value={"status_code": 200})
    @patch("persistence.tokens.TokenStore.get", return_value=False)
    def test_submit_400_token_question_wrong_type(self, mock_get, mock_post):
        payload = {"question": 0, "answers": []}
        data = {"token": str(jwt.encode(payload, "", algorithm="HS256"), "utf8"), "choice": "token_question_wrong_type"}

        response = self.app.post("/submit", data=json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 400, msg=response.data)


    @patch("requests.post", return_value={"status_code": 200})
    @patch("persistence.tokens.TokenStore.get", return_value=False)
    def test_submit_400_token_question_id_missing(self, mock_get, mock_post):
        payload = {"question": {}, "answers": []}
        data = {"token": str(jwt.encode(payload, "", algorithm="HS256"), "utf8"), "choice": "token_question_id_missing"}

        response = self.app.post("/submit", data=json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 400, msg=response.data)


    @patch("requests.post", return_value={"status_code": 200})
    @patch("persistence.tokens.TokenStore.get", return_value=False)
    def test_submit_400_token_answers_missing(self, mock_get, mock_post):
        payload = {"question": {"id": "token_answers_missing"}}
        data = {"token": str(jwt.encode(payload, "", algorithm="HS256"), "utf8"), "choice": "token_answers_missing"}

        response = self.app.post("/submit", data=json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 400, msg=response.data)


    @patch("requests.post", return_value={"status_code": 200})
    @patch("persistence.tokens.TokenStore.get", return_value=False)
    def test_submit_400_token_answers_wrong_type(self, mock_get, mock_post):
        payload = {"question": {"id": "token_answers_wrong_type"}, "answers": 0}
        data = {"token": str(jwt.encode(payload, "", algorithm="HS256"), "utf8"), "choice": "token_answers_wrong_type"}

        response = self.app.post("/submit", data=json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 400, msg=response.data)


    @patch("requests.post", return_value={"status_code": 200})
    @patch("persistence.tokens.TokenStore.get", return_value=False)
    def test_submit_400_token_answers_id_missing(self, mock_get, mock_post):
        payload = {"question": {"id": "token_answers_id_missing"}, "answers": [{}]}
        data = {"token": str(jwt.encode(payload, "", algorithm="HS256"), "utf8"), "choice": "token_answers_id_missing"}

        response = self.app.post("/submit", data=json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 400, msg=response.data)


    @patch("persistence.records.RecordStore")
    @patch("requests.post", return_value={"status_code": 200})
    @patch("persistence.tokens.TokenStore.get", return_value=False)
    @patch("persistence.tokens.TokenStore.set")
    @patch("persistence.records.RecordStore.add")
    @patch("persistence.records.RecordStore.count_agree", return_value=1)
    @patch("persistence.records.RecordStore.count_disagree", return_value=1)
    def test_submit_200_success(self, mock_disagree, mock_agree, mock_add, mock_set, mock_get, mock_post, _):
        payload = {"question": {"id": "submit_success_question_id"}, "answers": [{"id": "submit_success_answer_id"}]}
        data = {"token": str(jwt.encode(payload, "", algorithm="HS256"), "utf8"), "choice": "submit_success_choice_id"}

        response = self.app.post("/submit", data=json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 200, msg=response.data)
        mock_get.assert_called_with(data["token"])
        mock_set.assert_called_with(data["token"], ANY, ANY)
        mock_add.assert_called_with(payload["question"]["id"], data["choice"], payload["answers"][0]["id"])
        mock_agree.assert_called_with(payload["question"]["id"], data["choice"], payload["answers"])
        mock_disagree.assert_called_with(payload["question"]["id"], data["choice"], payload["answers"])


    @patch("persistence.records.RecordStore")
    @patch("requests.post", return_value={"status_code": 200})
    @patch("persistence.tokens.TokenStore.get", return_value=False)
    @patch("persistence.tokens.TokenStore.set")
    @patch("persistence.records.RecordStore.add")
    @patch("persistence.records.RecordStore.count_agree", return_value=8)
    @patch("persistence.records.RecordStore.count_disagree", return_value=32)
    def test_submit_200_similarity_correct(self, mock_disagree, mock_agree, mock_add, mock_set, mock_get, mock_post, _):
        payload = {"question": {"id": "similarity_correct_question_id"}, "answers": [{"id": "similarity_correct_answer_id"}]}
        data = {"token": str(jwt.encode(payload, "", algorithm="HS256"), "utf8"), "choice": "similarity_correct_choice_id"}

        response = self.app.post("/submit", data=json.dumps(data), content_type="application/json")
        print(response.json["similarity"])

        self.assertEqual(response.status_code, 200, msg=response.data)
        self.assertEqual(response.json["similarity"], mock_agree() / (mock_agree() + mock_disagree()))
