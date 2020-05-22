from pymongo import MongoClient
from classifier import is_news
from watchdog import conn
from rq import Queue
import performance
import requests
import crawler
import json
import time

MONGO_URL = 'mongodb+srv://watchdog:example@clef-uaic-svoxc.mongodb.net/test?retryWrites=true&w=majority'
client = MongoClient(MONGO_URL)
db = client.Tweets

all_collection = db.filteredTweets_v1
features_collection = db.tweetsFeatures_v1
verdict_collection = db.tweetsVerdict_v1

q = Queue(connection=conn)


def insert_tweets():
    # global CONTOR
    CONTOR = 0

    start_time = performance.update_start_time('crawler')
    start_v1 = performance.get_current_time()
    tweetlist = crawler.gatherTweets()

    if tweetlist is False:
        return "invalid number of retrieved tweets"
    end_v1 = performance.get_current_time()
    duration = end_v1 - start_v1
    performance.update_end_time_duration('crawler', start_time + duration)

    start_time = performance.update_start_time('filtering')
    start_v1 = performance.get_current_time()

    print("Filtering the tweets: ")
    tweetsToInsert = list()
    for tweet in tweetlist:
        tweet = json.loads(tweet)
        tweet2 = db.filteredTweets_v1.find_one({"id_str": tweet['id_str']})
        if not tweet2:
            # db.unfilteredTweets.insert_one(tweet)
            if is_news(tweet):
                CONTOR += 1
                print("Valid tweet #" + str(CONTOR))
                tweetsToInsert.append(tweet)
    print('Inserting ' + str(CONTOR) + ' tweets into the db.')
    db.filteredTweets_v1.insert_many(tweetsToInsert)

    end_v1 = performance.get_current_time()
    duration = end_v1 - start_v1
    performance.update_end_time_duration('filtering', start_time + duration)

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
    referencedID = tweet['_id']
    tweet['_id'] = referencedID
    verdict = verdict_collection.find_one({"reference": referencedID})
    del tweet['hashtags']
    del tweet['lang']
    if verdict is not None:
        del verdict['_id']
        del verdict['reference']
        tweet['cnn_verdict'] = verdict['cnn_verdict']
        tweet['svm_verdict'] = verdict['svm_verdict']
        tweet.update(verdict)
    tweet['_id'] = str(tweet['_id'])
    return tweet
