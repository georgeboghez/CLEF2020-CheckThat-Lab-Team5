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

userList = ["EU_Comission", "realDonaldTrump", "BernieSanders",
            "JoeBiden", "elonmusk", "tconnellyRTE",
            "BarackObama", "Samsung", "NASA"]

countList = [10, 10, 4, 6, 4, 50, 20, 6, 15, 15, 15, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 2, 2, 2, 2, 2, 2, 2, 2]

keyWordsList = ["coronavirus", "#ad", "economy", "olympic games", "russia", "#europe", "#breaking-news", "news",
                "pope", "china", "#newjob", "#jobs", "hiring", "applynow", "jobs", "job", "career", "jobsearch",
                "Vacancies", "recruitment", "NewJob", "nowhiring", "LookingForWork", "Fulltime", "wearehiring",
                "findjob", "vacancy", "breakingnews", "latestnews", "newsupdate", "newsdesk", "trendingnews",
                "weatherforcast", "forcast", "nsweather", "cunt", "fuck", "hell", "fag", "customer", "delivery",
                "deals"]


def getTweets(search_word, date_since, count):
    if count < 0:
        raise ValueError("Count negativ!")
    if type(count) != int:
        raise TypeError("Count nu este de tip int!")
    if type(search_word) != str:
        raise TypeError("Search word nu este string!")

    global tweetList
    length = len(tweetList)
    for tweet in (tw.Cursor(api.search,
                            q=search_word,
                            lang="en",
                            tweet_mode='extended',
                            since=date_since).items(count)):
        tweetList.append(json.dumps(tweet._json, indent=4, sort_keys=True))
    if len(tweetList) - length == count:
        return True
    return False


def getTweetsByUsers(user_ids, date_since, count):
    if type(count) != int:
        raise TypeError("Count nu este de tip int!")
    if count < 0:
        raise ValueError("Count negativ!")
    if type(user_ids) != list:
        raise TypeError("Lista de users invalida!")

    global tweetList
    length = len(tweetList)
    for user in user_ids:
        for tweet in (tw.Cursor(api.user_timeline,
                                id=user,
                                tweet_mode='extended',
                                since=date_since).items(count)):
            tweetList.append(json.dumps(tweet._json, indent=4, sort_keys=True))
    if len(tweetList) - length == count * len(user_ids):
        return True
    return False


def autoInsertTweets(WAIT_TIME_SECONDS=3 * 3600, num=-1, route='http://ip2020.herokuapp.com/post'):
    if num == -1:
        while True:
            time.sleep(WAIT_TIME_SECONDS)
            response = requests.get(route)
            if response.status_code != 200:
                raise ValueError("Eroare la inserarea automata de tweet-uri")
    else:
        while num > 0:
            time.sleep(WAIT_TIME_SECONDS)
            response = requests.get(route)
            if response.status_code != 200:
                raise ValueError("Eroare la inserarea automata de tweet-uri")
            num -= 1
    return True


def main(dummyNumber=0):
    global tweetList, countList, userList, keyWordsList

    getTweetsByUsers(userList, "2020-03-20", 4)

    sum = len(tweetList)
    for i in range(len(countList)):
        sum += countList[i]
        getTweets(keyWordsList[i], "2020-03-20", countList[i])


    sum += dummyNumber
    if len(tweetList) != sum:
        return False
    return tweetList


if __name__ == '__main__':
    main()
