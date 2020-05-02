from flask import Flask, abort
import pymongo
import json
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)

db = pymongo.MongoClient("mongodb://watchdogUnprocessed:example@debian/Tweets").Tweets
all_collection = db.filteredTweets
features_collection = db.tweetsFeatures
verdict_collection = db.tweetsVerdict


def gatherTweetData(tweet):
    referencedID = str(tweet['_id'])
    tweet['_id'] = referencedID
    features = features_collection.find_one({"reference": referencedID})
    verdict = verdict_collection.find_one({"reference": referencedID})
    if features is not None:
        del features['_id']
        del features['reference']
        tweet.update(features)
    if verdict is not None:
        del verdict['_id']
        del verdict['reference']
        tweet.update(verdict)
    return tweet

@app.route("/", defaults={'u_path': ''})
@app.route("/<path:u_path>")
def catch_all(u_path):
    return "Hello! This is the catchall route. I guess you wanted to visit " + u_path

@app.route("/api/tweets")
def getTweets():
    documents = []
    for document in all_collection.find({}):
        documents.append(gatherTweetData(document))
    return json.dumps(documents)

@app.route("/api/tweets/<path:id>")
def getTweet(id):
    document = all_collection.find_one({"_id": ObjectId(id)})
    if document is not None:
        return dumps(gatherTweetData(document))
    else:
        return abort(404, description="Resource not found")


app.run(host='0.0.0.0')