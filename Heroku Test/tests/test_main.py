import unittest
import main


class TestMain(unittest.TestCase):
    def testIndex(self):
        # Basic GET
        resp = main.app.test_client().get("/")
        self.assertEqual(resp.status_code, 200,
                         "The GET method was not successfully called.")

    def testCatchall(self):
        # Basic GET
        resp = main.app.test_client().get("/<path:u_path>")
        self.assertEqual(resp.status_code, 200, "The GET method was not successfully called.")
        self.assertEqual(resp.data, b"Hello! This is the catchall route. I guess you wanted to visit <path:u_path>", "No response body")

    def testPost(self):
        # os.chdir("..")
        response = main.app.test_client().get('/post')
        self.assertEqual(response.status_code, 200,
                         "Invalid status code (expected 200)")
        self.assertEqual(response.data, b'{"Insert status":"started"}\n', "No response body")

    def testTweets(self):
        response = main.app.test_client().get('/tweets')
        self.assertEqual(response.status_code, 200, "Invalid status code (expected 200)")
        self.assertIsNotNone(response.data, "No response body!")

    def testTweet(self):
        response = main.app.test_client().get('/tweets/5ead6cd04d774f4f35deea70')
        self.assertEqual(response.status_code, 200, "Invalid status code (expected 200)")
        self.assertIsNotNone(response.data, "No response body!")