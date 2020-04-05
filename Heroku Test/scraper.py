import requests
import json
import os

if __name__ == '__main__':
    # os.environ['NO_PROXY'] = '127.0.0.1'
    response = requests.get('http://ip2020.herokuapp.com/all/2')
    print(json.loads(response.json())[0]['full_text'])
