#!/usr/bin/env python
from flask import Flask, jsonify, abort
from bson.objectid import ObjectId
from bson.json_util import dumps
from pymongo import MongoClient
from flask_cors import CORS
from watchdog import conn
from rq import Queue
import threading
import utils
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

q = Queue(connection=conn)


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


# @app.route("/all_unfiltered_tweets", methods=['GET'])
# def unfiltered_tweets():
#     tweetsList = list(db.unfilteredTweets.find())
#     return jsonify(dumps(tweetsList))


# @app.route("/all_unfiltered_tweets/<int:count>", methods=['GET'])
# def getCountUnfilteredTweets(count):
#     if count > db.unfilteredTweets.count_documents({}):
#         raise ValueError("Count too big")
#     tweetsList = list(db.unfilteredTweets.find().sort('_id', -1).limit(count))
#     return jsonify(dumps(tweetsList))


@app.route("/post", methods=['GET'])
def post():
    result = q.enqueue_call(utils.insert_tweets, timeout=15 * 60)
    print(result)
    return jsonify({"Insert status": "started"})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    # app.run('0.0.0.0', port)
    t1 = threading.Thread(target=app.run, args=('0.0.0.0', port))
    t1.start()
    # app.run(host='0.0.0.0', port=port)
    t2 = threading.Thread(target=utils.auto_insert_tweets)
    t2.start()
    t1.join()
    t2.join()
