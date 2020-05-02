#!/usr/bin/env python
from flask import Flask, render_template, request, redirect, jsonify, abort
from bson.json_util import dumps
from bson.objectid import ObjectId
from pymongo import MongoClient
from classifier import is_news
from flask_cors import CORS
import threading
import crawler
import json
import os


MONGO_URL = 'mongodb+srv://watchdog:example@clef-uaic-svoxc.mongodb.net/test?retryWrites=true&w=majority'
client = MongoClient(MONGO_URL)
db = client.Tweets

all_collection = db.filteredTweets
features_collection = db.tweetsFeatures
verdict_collection = db.tweetsVerdict

app = Flask(__name__)
CORS(app)


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


@app.route("/", defaults={'u_path': ''})
@app.route("/<path:u_path>")
def catch_all(u_path):
    return "Hello! This is the catchall route. I guess you wanted to visit " + u_path


@app.route("/tweets")
def getTweets():
    documents = []
    for document in all_collection.find({}).limit(10):
        documents.append(gatherTweetData(document))
    return json.dumps(documents)


@app.route("/tweets/<path:id>")
def getTweet(id):
    document = all_collection.find_one({"_id": ObjectId(id)})
    if document is not None:
        return dumps(gatherTweetData(document))
    else:
        return abort(404, description="Resource not found")


@app.route("/all_unfiltered_tweets", methods=['GET'])
def unfiltered_tweets():
    tweetsList = list(db.unfilteredTweets.find())
    return jsonify(dumps(tweetsList))


@app.route("/all_unfiltered_tweets/<int:count>", methods=['GET'])
def getCountUnfilteredTweets(count):
    if count > db.unfilteredTweets.count_documents({}):
        raise ValueError("Count too big")
    tweetsList = list(db.unfilteredTweets.find().sort('_id', -1).limit(count))
    return jsonify(dumps(tweetsList))


def insert_tweets():
    # global CONTOR
    CONTOR = 0
    tweetlist = crawler.main()

    if tweetlist is False:
        return "invalid number of retrieved tweets"
    for tweet in tweetlist:
        tweet = json.loads(tweet)
        tweet2 = db.filteredTweets.find_one({"id_str": tweet['id_str']})
        if not tweet2:
            db.unfilteredTweets.insert_one(tweet)
            if is_news(tweet):
                CONTOR += 1
                db.filteredTweets.insert_one(tweet)


@app.route("/post", methods=['GET'])
def post():
    thread = threading.Thread(target=insert_tweets)
    thread.daemon = True
    thread.start()
    return jsonify({'thread_name': str(thread.name),
                    'started': True})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    t1 = threading.Thread(target=app.run, args=('0.0.0.0', port))
    t1.start()
    # app.run(host='0.0.0.0', port=port)
    t2 = threading.Thread(target=crawler.autoInsertTweets)
    t2.start()
    t1.join()
    t2.join()
