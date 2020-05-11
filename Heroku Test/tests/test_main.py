import os
import unittest
import main
import json


class TestMain(unittest.TestCase):
    def test_index(self):
        # os.chdir("..")
        resp = main.app.test_client().get("/")
        self.assertEqual(resp.status_code, 200, "The GET method was not successfully called.")
        self.assertIsNotNone(resp.data, "No response body!")

    def test_post(self):
        # os.chdir("..")
        response = main.app.test_client().get('/post')
        self.assertEqual(response.status_code, 200,
                         "Invalid status code (expected 200)")

    # def test_unfiltered_tweets(self):
    #     # os.chdir("..")
    #     response = main.app.test_client().get('/all_unfiltered_tweets')
    #     self.assertEqual(response.status_code, 200,
    #                      "The GET method was not successfully called.")
    #     self.assertIsNotNone(json.loads(response.data), "No response body!")

    # def test_getCountUnfilteredTweets(self):
    #     # os.chdir("..")
    #     response = main.app.test_client().get("/all_unfiltered_tweets/2")
    #     self.assertEqual(response.status_code, 200,
    #                      "The GET method was not successfully called.")
    #     self.assertRaises(ValueError, main.getCountTweets, 9223372036854775807)
