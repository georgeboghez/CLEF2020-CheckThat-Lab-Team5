#!/usr/bin/env python
import os
import pymongo
import json
import crawler
import requests
from flask import Flask, render_template, request, redirect, jsonify
from pymongo import MongoClient
from bson.json_util import dumps


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
    tweetsList = db.tweetsTable.find().sort('_id', -1).limit(CONTOR)
    tweetsList = list(tweetsList)
    CONTOR = 0
    return jsonify(dumps(tweetsList))


@app.route("/all", methods=['GET'])
def all():
    tweetsList = list(db.tweetsTable.find())
    return jsonify(dumps(tweetsList))


@app.route("/all/<int:count>", methods=['GET'])
def getCountTweets(count):
    tweetsList = list(db.tweetsTable.find().sort('_id', -1).limit(count))
    return jsonify(dumps(tweetsList))


@app.route("/secret", methods=['GET'])
def special():
    return render_template('special.html')


@app.route("/post", methods=['POST'])
def post():
    global CONTOR
    for tweet in crawler.main():
        tweet = json.loads(tweet)
        tweet2 = db.tweetsTable.find_one({"id_str": tweet['id_str']})
        if not tweet2:
            CONTOR += 1
            tweets_id = db.tweetsTable.insert_one(tweet)
    return redirect('/secret')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
