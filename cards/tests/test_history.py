import unittest
from app import create_app


class TestHistory(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config['TESTING'] = True
        self.app = app.test_client()


    def test_get_history(self):
        # send the request and check the response status code
        response = self.app.get("/api/history", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        isStringLogic = "card_id" in str(response.data)
        self.assertTrue(isStringLogic)

