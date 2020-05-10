from bson.json_util import dumps
import tweepy as tw
import unittest
import utils
import json
import main

class TestUtils(unittest.TestCase):
    def test_auto_insert_tweets(self):
        self.assertTrue(utils.auto_insert_tweets(WAIT_TIME_SECONDS=5, num=0), "Non-viable tweetlist")

    def test_insert_tweets(self):
        self.assertTrue(utils.insert_tweets(), "POST error")

    def test_post(self):
        resp = main.app.test_client().get("/post")
        self.assertIsNotNone(resp.data, "no data")

    def test_gatherTweetData(self):
        tweet  = main.all_collection.find_one()
        tweet2 = utils.gatherTweetData(tweet)
        self.assertEqual(str(tweet['_id']), str(tweet2['_id']), "Couldn't properly gather tweet data!")

