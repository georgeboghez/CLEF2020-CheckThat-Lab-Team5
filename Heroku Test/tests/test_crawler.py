import unittest
import crawler


class TestCrawler(unittest.TestCase):
    def test_getTweets(self):
        self.assertTrue(crawler.getTweets("news", "2020-03-20", 2), "N-au fost gasite 2 tweet-uri.")
        self.assertTrue(crawler.getTweets("news", "2020-03-20", 10), "N-au fost gasite 10 tweet-uri.")
        # self.assertFalse(getTweets("news","2020-03-20",-1),"S-au preluat -1 tweet-uri noi.")
        self.assertFalse(crawler.getTweets("jdgsfjdgdiushighdoihgdioghdiodgh", "2020-03-20", 2),
                         "A fost gasit un tweet care contine jdgsfjdgdiushighdoihgdioghdiodgh")

    def test_getTweetsByUsers(self):
        self.assertTrue(crawler.getTweetsByUsers(["NASA"], "2020-03-20", 2),
                        "N-au fost gasite 2 tweet-uri de la utilizatorii NASA, Samsung.")
        self.assertTrue(crawler.getTweetsByUsers(["elonmusk", "JoeBiden"], "2020-03-20", 2),
                        "N-au fost gasite 10 tweet-uri de la utilizatorii elonmusk, JoeBiden.")
        # self.assertFalse(crawler.getTweetsByUsers(["dfhid8787"], "2020-03-20", 10), "Au fost gasite tweet-uri de la dfhidfsuisdfhfuisfhui.")
        self.assertRaises(ValueError, crawler.getTweetsByUsers, "NASA", "2020-03-20", 2)
        self.assertRaises(ValueError, crawler.getTweetsByUsers, ["NASA"], "2020-03-20", -5)
        self.assertRaises(ValueError, crawler.getTweetsByUsers, ["NASA"], "2020-03-20", "5")

    def test_autoInsertTweets(self):
        self.assertTrue(crawler.autoInsertTweets(), "Infinite while error. Exited while.")

    def test_main(self):
        self.assertRaises(ValueError, crawler.main, "Invalid Tweets list")


if __name__ == '__main__':
    unittest.main()
