import os
import pymongo
import pprint
import emoji
import json
import requests

class App(dict):
    def __str__(self):
        return json.dumps(self)


def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')


if __name__ == '__main__':
    os.environ['NO_PROXY'] = '127.0.0.1'
    response = requests.get('http://127.0.0.1:5000/all/2')
    print(json.loads(response.json())[0]['_id'])