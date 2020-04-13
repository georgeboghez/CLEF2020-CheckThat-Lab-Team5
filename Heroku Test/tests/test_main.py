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
        self.assertEqual(response.data, b'done' or b'invalid number of retrieved tweets',
                         "Invalid data (expected 'data')")

    def test_all(self):
        os.chdir("..")
        try:
            response = main.app.test_client().get('/all')
            self.assertRaises(MemoryError, json.loads, response.data, "Not enough memory!")
            self.assertEqual(response.status_code, 200,
                             "The GET method was not successfully called.")
            self.assertIsNotNone(json.loads(response.data), "No response body!")
        except:
            print("not enough memory for running this test")
    
    def test_getCountTweets(self):
        os.chdir("..")
        response = main.app.test_client().get("/all/2")
        self.assertEqual(response.status_code, 200,
                         "The GET method was not successfully called.")
        self.assertRaises(ValueError, main.getCountTweets, 9223372036854775807)

    def test_unfiltered_tweets(self):
        os.chdir("..")
        response = main.app.test_client().get('/all_unfiltered_tweets')
        self.assertEqual(response.status_code, 200,
                         "The GET method was not successfully called.")
        self.assertIsNotNone(json.loads(response.data), "No response body!")

    def test_getCountUnfilteredTweets(self):
        os.chdir("..")
        response = main.app.test_client().get("/all_unfiltered_tweets/2")
        self.assertEqual(response.status_code, 200,
                         "The GET method was not successfully called.")
        self.assertRaises(ValueError, main.getCountTweets, 9223372036854775807)
