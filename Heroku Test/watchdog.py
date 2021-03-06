from rq import Worker, Queue, Connection
from bson.objectid import ObjectId
import threading
import pymongo
import pusher
import redis
import os

BEFORE_CHANNEL = 'DEFAULT'
CHANGED_EVENT = "CHANGED"
INSERTED_EVENT = "INSERTED"

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

pusher_client = pusher.Pusher(
    app_id='992704',
    key='576452672b8655ff2e01',
    secret='24af546a041262912214',
    cluster='eu',
    ssl=True
)

db = pymongo.MongoClient(
    "mongodb+srv://watchdog:example@clef-uaic-svoxc.mongodb.net/test?retryWrites=true&w=majority").Tweets

def exists(_id):
    cursor = db.filteredTweets_v1.find({'_id': ObjectId(_id)})
    found = False
    id = ""
    for i in cursor:
        found = True
        id = _id
        break
    return found, str(id)

def isFinal(_id):
    cursor = db.tweetsVerdict_v1.find({'_id': ObjectId(_id)})
    found = False
    id = ""
    for i in cursor:
        found = True
        id = i['reference']
        break
    return found, str(id)

def getStatus(_id):
    status, id = isFinal(_id)
    if status:
        return 3, id
    status, id = exists(_id)
    if status:
        return 1, id
    return 0, ""

class MongoWatchdog:
    def __init__(self, channel):
        self.channel = channel
        self.__attachCollection()

    def __attachCollection(self):
        self.tweets_change_stream = db.watch()

    def serve(self):
        for change in self.tweets_change_stream:
            _id = str(change['documentKey']['_id'])
            collection = change['ns']['coll']

            if change['operationType'] == "insert" and (collection == "filteredTweets_v1"):
                status, id = getStatus(_id)
                if status == 3:
                    self.handleChange(id)
                else:
                    self.handleNew(id)
            elif (change['operationType'] == "replace" or change['operationType'] == 'update') and collection == "tweetsVerdict_v1":
                status, id = getStatus(_id)
                if status == 3:
                    self.handleChange(id)

    def handleNew(self, id):
        print("NEW TWEET")
        self.sendTrigger(self.channel, INSERTED_EVENT, str(id))

    def handleChange(self, id):
        print("CHANGED TWEET STATUS")
        self.sendTrigger(self.channel, CHANGED_EVENT, str(id))
        
    def sendTrigger(self, channel, event, id):
        pusher_client.trigger(channel, event, {'id': id})

def watchdog_serve():
    watchdog = MongoWatchdog(BEFORE_CHANNEL)
    watchdog.serve()

if __name__ == '__main__':
    t1 = threading.Thread(target=watchdog_serve)
    t1.start()
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
    t1.join()
