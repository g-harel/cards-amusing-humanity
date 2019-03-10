import unittest
from app import create_app


class TestQuestions(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config['TESTING'] = True
        self.app = app.test_client()


    def test_follow_a_question(self):
        # send the request and check the response status code
        response = self.app.get("/api/questions", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        isStringLogic = "I sleep at night?" in str(response.data)
        print(response.data)
        self.assertTrue(isStringLogic)

