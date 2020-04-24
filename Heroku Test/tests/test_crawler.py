import unittest
import crawler


class TestCrawler(unittest.TestCase):
    def test_getTweets(self):
        self.assertTrue(crawler.getTweets("news", "2020-03-20", 2), "N-au fost gasite 2 tweet-uri.")
        self.assertFalse(crawler.getTweets("jdgsfjdgdiushighdoihgdioghdiodgh", "2020-03-20", 2),
                         "Received tweet with text: jdgsfjdgdiushighdoihgdioghdiodgh")
        self.assertRaises(ValueError, crawler.getTweets, "news", "2020-03-20", -1)
        self.assertRaises(TypeError, crawler.getTweets, "news", "2020-03-20", "10")
        self.assertRaises(TypeError, crawler.getTweets, 20, "2020-03-20", "5")

    def test_getTweetsByUsers(self):
        self.assertTrue(crawler.getTweetsByUsers(["NASA"], "2020-03-20", 2),
                        "Couldn't receive 2 tweets from users NASA, Samsung.")
        self.assertTrue(crawler.getTweetsByUsers(["elonmusk", "JoeBiden"], "2020-03-20", 2),
                        "Couldn't receive 10 tweets from users elonmusk, JoeBiden.")
        # self.assertFalse(crawler.getTweetsByUsers(["dfhid8787"], "2020-03-20", 10), "Au fost gasite tweet-uri de la dfhidfsuisdfhfuisfhui.")
        self.assertRaises(TypeError, crawler.getTweetsByUsers, "NASA", "2020-03-20", 2)
        self.assertRaises(ValueError, crawler.getTweetsByUsers, ["NASA"], "2020-03-20", -5)
        self.assertRaises(TypeError, crawler.getTweetsByUsers, ["NASA"], "2020-03-20", "5")

    def test_autoInsertTweets(self):
        self.assertTrue(crawler.autoInsertTweets(5, 2, "http://localhost:5000/post"), "Tweetlist neviabil")
        self.assertRaises(ValueError, crawler.autoInsertTweets, 5, 2, "http://localhost:5000/nothing")

    def test_main(self):
        self.assertFalse(crawler.main(1), "Numar insufient de tweet-uri")


if __name__ == '__main__':
    unittest.main()