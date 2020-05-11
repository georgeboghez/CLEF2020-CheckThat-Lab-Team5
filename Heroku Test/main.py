#!/usr/bin/env python
from flask import Flask, jsonify, abort, request
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
import string

MONGO_URL = 'mongodb+srv://watchdog:example@clef-uaic-svoxc.mongodb.net/test?retryWrites=true&w=majority'
client = MongoClient(MONGO_URL)
db = client.Tweets


app = Flask(__name__)
CORS(app)

q = Queue(connection=conn)


@app.route("/", defaults={'u_path': ''})
@app.route("/<path:u_path>")
def catch_all(u_path):
    return "Hello! This is the catchall route. I guess you wanted to visit " + u_path


@app.route("/tweets")
def getTweets():
    skip_param = str(request.args.get('skip'))
    limit_param = str(request.args.get('limit'))

    if skip_param is None or limit_param is None:
        return abort(400)
    
    if skip_param.isnumeric() == False or limit_param.isnumeric() == False:
        return abort(400)

    skip_param = int(skip_param)
    limit_param = int(limit_param)

    documents = []
    for document in utils.all_collection.find({}).skip(skip_param).limit(limit_param):
        documents.append(utils.gatherTweetData(document))

    return json.dumps(documents)


@app.route("/tweets/<path:id>")
def getTweet(id):
    document = utils.all_collection.find_one({"_id": ObjectId(id)})
    return dumps(utils.gatherTweetData(document))


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
