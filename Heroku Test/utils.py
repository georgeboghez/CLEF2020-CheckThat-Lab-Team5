from pymongo import MongoClient
from classifier import is_news
from watchdog import conn
from rq import Queue
import requests
import crawler
import json
import time


MONGO_URL = 'mongodb+srv://watchdog:example@clef-uaic-svoxc.mongodb.net/test?retryWrites=true&w=majority'
client = MongoClient(MONGO_URL)
db = client.Tweets

all_collection = db.filteredTweets
features_collection = db.tweetsFeatures
verdict_collection = db.tweetsVerdict

q = Queue(connection=conn)


def insert_tweets():
    # global CONTOR
    CONTOR = 0
    tweetlist = crawler.gatherTweets()

    if tweetlist is False:
        return "invalid number of retrieved tweets"
    for tweet in tweetlist:
        tweet = json.loads(tweet)
        tweet2 = db.filteredTweets.find_one({"id_str": tweet['id_str']})
        if not tweet2:
            # db.unfilteredTweets.insert_one(tweet)
            if is_news(tweet):
                CONTOR += 1
                print(CONTOR)
                db.filteredTweets.insert_one(tweet)
    response = requests.post(
        'https://nlp-module.herokuapp.com/process', json={"count": CONTOR})
    print(response.status_code, response.text)
    if response.json()["response"] == "ok":
        return True
    return False


def auto_insert_tweets(WAIT_TIME_SECONDS=20 * 60, num=-1):
    if num == -1:
        while True:
            time.sleep(WAIT_TIME_SECONDS)
            result = q.enqueue_call(insert_tweets, timeout=15 * 60)
            print(result)
    else:
        while num > 0:
            time.sleep(WAIT_TIME_SECONDS)
            result = q.enqueue_call(insert_tweets, timeout=15 * 60)
            num -= 1
    return True


def gatherTweetData(tweet):
    referencedID = str(tweet['_id'])
    tweet['_id'] = referencedID
    features = features_collection.find_one({"reference": referencedID})
    verdict = verdict_collection.find_one({"reference": referencedID})
    if features is not None:
        del features['_id']
        del features['reference']
        tweet['features'] = features
    if verdict is not None:
        del verdict['_id']
        del verdict['reference']
        tweet.update(verdict)
    return tweet
