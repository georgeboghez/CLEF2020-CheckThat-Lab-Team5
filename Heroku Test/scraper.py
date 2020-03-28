import os
import json
import requests

if __name__ == '__main__':
    os.environ['NO_PROXY'] = '127.0.0.1'
    response = requests.get('http://127.0.0.1:5000/all/2')
    print(json.loads(response.json())[0]['_id'])