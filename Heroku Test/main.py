#!/usr/bin/env python
from flask import Flask, render_template, request, redirect, jsonify
from bson.json_util import dumps
from pymongo import MongoClient
from filter import is_news
import unittest
import threading
import pymongo
import crawler
import json
import os

MONGO_URL = 'mongodb://heroku_pp4rkrx5:9919l2jg2bmm0jrvf50oj8m3f3@ds141613.mlab.com:41613/heroku_pp4rkrx5?retryWrites=false'
client = MongoClient(MONGO_URL)
db = client.heroku_pp4rkrx5
app = Flask(__name__)

CONTOR = 0


@app.route("/", methods=['GET'])
def index():
    global CONTOR
    if CONTOR == 0:
        return render_template('welcome.html')
    tweetsList = db.filteredTweets.find().sort('_id', -1).limit(CONTOR)
    tweetsList = list(tweetsList)
    CONTOR = 0
    return jsonify(dumps(tweetsList))


@app.route("/all", methods=['GET'])
def all():
    try:
        tweetsList = list(db.filteredTweets.find())
    except:
        raise MemoryError("Not enough memory")
    return jsonify(dumps(tweetsList))


@app.route("/all/<int:count>", methods=['GET'])
def getCountTweets(count):
    if count > db.filteredTweets.count_documents({}):
        raise ValueError("Count too big")
    tweetsList = list(db.filteredTweets.find().sort('_id', -1).limit(count))
    return jsonify(dumps(tweetsList))


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


@app.route("/secret", methods=['GET'])
def special():
    return render_template('special.html')


@app.route("/post", methods=['GET'])
def post():
    global CONTOR
    tweetlist = crawler.main()
    if tweetlist == False:
        return "invalid number of retrieved tweets"
    for tweet in tweetlist:
        tweet = json.loads(tweet)
        tweet2 = db.filteredTweets.find_one({"id_str": tweet['id_str']})
        if not tweet2:
            db.unfilteredTweets.insert_one(tweet)
            if is_news(tweet):
                CONTOR += 1
                db.filteredTweets.insert_one(tweet)
    return "done"


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    t1 = threading.Thread(target=app.run, args=('0.0.0.0', port))
    t1.start()
    # app.run(host='0.0.0.0', port=port)
    t2 = threading.Thread(target=crawler.autoInsertTweets)
    t2.start()
    t1.join()
    t2.join()
