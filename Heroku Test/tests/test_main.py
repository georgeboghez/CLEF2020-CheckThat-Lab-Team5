import os
import unittest
import main


class TestMain(unittest.TestCase):
    def test_index(self):
        os.chdir("..")

        # Basic GET
        resp = main.app.test_client().get("/")
        #print(resp.data)
        self.assertEqual(resp.status_code, 200, "The GET method was not successfully called.")
        self.assertIsNotNone(resp.data, "No response body!")

        # GET after a POST
        response = main.app.test_client().get('/post')
        resp = main.app.test_client().get("/")
        #print(resp.data)
        self.assertEqual(resp.status_code, 200, "The GET method was not successfully called.")
        self.assertIsNotNone(resp.data, "No response body!")

        # GET after a POST when COUNTER is 0
        response = main.app.test_client().get('/post')
        main.CONTOR = 0
        resp = main.app.test_client().get("/")
        #print(resp.data)
        self.assertEqual(resp.status_code, 200, "The GET method was not successfully called.")
        self.assertIsNotNone(resp.data, "No response body!")

    def test_special(self):
        resp = main.app.test_client().get("/secret")
        self.assertEqual(resp.status_code, 200, "The GET method was not successfully called.")
        self.assertIsNotNone(resp.data, "No response body!")