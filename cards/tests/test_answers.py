import unittest
from app import create_app


class TestAnswers(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config['TESTING'] = True
        self.app = app.test_client()


    def test_follow_an_answer(self):
        # send the request and check the response status code
        response = self.app.get("/api/answers", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        isStringLogic = "Obama" in str(response.data)
        print(response.data)
        self.assertTrue(isStringLogic)

