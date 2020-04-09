import unittest
import main
import json
import os


class TestMain(unittest.TestCase):
    def test_post(self):
        os.chdir("..")
        response = main.app.test_client().get('/post')
        self.assertEqual(response.status_code, 200,
                         "Invalid status code (expected 200)")
        self.assertEqual(response.data, b'done',
                         "Invalid data (expected \"data\")")

    def test_all(self):
        os.chdir("..")
        response = main.app.test_client().get('/all')
        self.assertEqual(response.status_code, 200, "The GET method was not successfully called.")
        self.assertIsNotNone(json.loads(response.data), "No response body!")

    def test_getCountTweets(self):
        response2 = main.app.test_client().get("/all/2")
        self.assertEqual(response2.status_code, 200, "The GET method was not successfully called.")
        self.assertRaises(ValueError, main.getCountTweets, 9223372036854775807)