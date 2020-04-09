import tweepy as tw
import requests
import json
import time
import os

CONSUMER_KEY = 'CmQS1BFO5D38aYu38isgYfQSM'
CONSUMER_SECRET = '0BT4Pvkox9y4USuKmzsh6IzzfymdMcPrCKANnYVc82qXZMRn7D'
ACCESS_TOKEN = '1242346386756112384-rBnQ65dlWwgbVQp6Me6op8AEqogEgn'
ACCESS_TOKEN_SECRET = 'P6kfsxgeTkL7e6vifWf5VJmDQVKIKMehPyJLPJ16RcglK'


auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tw.API(auth, wait_on_rate_limit=True)

tweetList = list()


def getTweets(search_word, date_since, count):
    if count < 0:
        raise ValueError("Count negativ!")
    if type(count) != int:
        raise ValueError("Count nu este de tip int!")
    if type(search_word) != str:
        raise ValueError("Search word nu este string!")

    global tweetList
    length = len(tweetList)
    tweetList += [json.dumps(tweet._json, indent=4, sort_keys=True)
                  for tweet in (tw.Cursor(api.search,
                                          q=search_word,
                                          lang="en",
                                          tweet_mode='extended',
                                          since=date_since).items(count))]
    if len(tweetList) - length == count:
        return True
    return False
        #raise ValueError("Nu s-au adaugat tweets")


def getTweetsByUsers(user_ids, date_since, count):
    if type(count) != int:
        raise ValueError("Count nu este de tip int!")
    if count < 0:
        raise ValueError("Count negativ!")
    if type(user_ids) != list:
        raise ValueError("Lista de users invalida!")

    global tweetList
    length = len(tweetList)
    for user in user_ids:
        tweetList += [json.dumps(tweet._json, indent=4, sort_keys=True)
                      for tweet in (tw.Cursor(api.user_timeline,
                                              id=user,
                                              tweet_mode='extended',
                                              since=date_since).items(count))]
    if len(tweetList) - length == count*len(user_ids):
        return True
    return False


def autoInsertTweets():
    WAIT_TIME_SECONDS = 3 * 3600  # 3 ore

    while True:
        time.sleep(WAIT_TIME_SECONDS)
        response = requests.get('http://ip2020.herokuapp.com/post')
        print(response.text, type(response.text))
        if response.status_code != 200:
            print("eroare")
    return False


def main():
    user_list = ["EU_Comission", "realDonaldTrump", "BernieSanders",
                 "JoeBiden", "elonmusk", "tconnellyRTE",
                 "BarackObama", "Samsung", "NASA"]
    global tweetList
    getTweetsByUsers(user_list, "2020-03-20", 4)
    getTweets("coronavirus", "2020-03-20", 10)
    getTweets("#ad", "2020-03-20", 10)
    getTweets("economy", "2020-03-20", 4)
    getTweets("olympic games", "2020-03-20", 4)
    getTweets("russia", "2020-03-20", 6)
    getTweets("#europe", "2020-03-10", 4)
    getTweets("#breaking-news", "2020-03-20", 30)
    getTweets("news", "2020-03-20", 20)
    getTweets("pope", "2020-03-20", 6)
    getTweets("china", "2020-03-20", 15)
    getTweets("#newjob", "2020-03-20", 15)
    getTweets("#jobs", "2020-03-20", 15)
    getTweets("#selling", "2020-03-20", 20)
    getTweets("#weather", "2020-03-20", 15)

    if len(tweetList) != 14:
        return false
    return tweetList


if __name__ == '__main__':
    main()
