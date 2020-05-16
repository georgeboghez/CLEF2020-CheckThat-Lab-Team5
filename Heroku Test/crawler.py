import tweepy as tw
import json
import pprint

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

keyWords = {"news": 5,
            "coronavirus": 2,
            "news": 5,
            "pope": 15,
            # "china": 15,
            # "#newjob": 15,
            # "#jobs": 2,
            # "hiring": 2,
            # "applynow": 2,
            # "jobs": 2,
            # "job": 2,
            # "career": 2,
            # "jobsearch": 2,
            # "Vacancies": 2,
            # "recruitment": 2,
            # "NewJob": 2,
            # "nowhiring": 2,
            # "LookingForWork": 2,
            # "Fulltime": 2,
            # "wearehiring": 2,
            # "findjob": 2,
            # "vacancy": 2,
            # "breakingnews": 2,
            # "latestnews": 2,
            # "newsupdate": 2,
            # "newsdesk": 2,
            # "trendingnews": 2,
            # "weatherforcast": 2,
            # "forcast": 2,
            # "nsweather": 2,
            # "cunt": 2,
            # "fuck": 2,
            # "hell": 2,
            # "fag": 2,
            # "customer": 2,
            # "delivery": 2,
            # "deals": 2
            }


def getTweets(search_word, date_since, count):
    global tweetList

    if count < 0:
        raise ValueError("Count negativ!")
    if type(count) != int:
        raise TypeError("Count nu este de tip int!")
    if type(search_word) != str:
        raise TypeError("Search word nu este string!")

    length = len(tweetList)
    for tweet in (tw.Cursor(api.search,
                            q=search_word,
                            lang="en",
                            tweet_mode='extended',
                            since=date_since).items(count)):
        if 'retweeted_status' in tweet._json:
            tweetList.append(json.dumps({'full_text': tweet._json['retweeted_status']['full_text'],
                                         'lang': tweet._json['lang'],
                                         'screen_name': tweet._json['retweeted_status']['user']['screen_name'],
                                         'name': tweet._json['retweeted_status']['user']['name'],
                                         'profile_image_url_https': tweet._json['retweeted_status']['user']['profile_image_url_https'],
                                         'retweet_count': tweet._json['retweeted_status']['retweet_count'],
                                         'created_at': tweet._json['retweeted_status']['created_at'],
                                         'id_str': tweet._json['retweeted_status']['id_str'],
                                         'favorite_count': tweet._json['retweeted_status']['favorite_count'],
                                         'hashtags': tweet._json['retweeted_status']['entities']['hashtags']}, 
                                         indent=4, sort_keys=True))
        else:
            tweetList.append(json.dumps({'full_text': tweet._json['full_text'], 
                                         'lang': tweet._json['lang'], 
                                         'screen_name': tweet._json['user']['screen_name'], 
                                         'name': tweet._json['user']['name'], 
                                         'profile_image_url_https': tweet._json['user']['profile_image_url_https'],
                                         'retweet_count': tweet._json['retweet_count'], 
                                         'created_at': tweet._json['created_at'], 
                                         'id_str': tweet._json['id_str'], 
                                         'favorite_count': tweet._json['favorite_count'], 
                                         'hashtags': tweet._json['entities']['hashtags']}, 
                                         indent=4, sort_keys=True))
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
            if 'retweeted_status' in tweet._json:
                tweetList.append(json.dumps({'full_text': tweet._json['retweeted_status']['full_text'],
                                             'lang': tweet._json['lang'],
                                             'screen_name': tweet._json['retweeted_status']['user']['screen_name'],
                                             'name': tweet._json['retweeted_status']['user']['name'],
                                             'profile_image_url_https': tweet._json['retweeted_status']['user']['profile_image_url_https'],
                                             'retweet_count': tweet._json['retweeted_status']['retweet_count'],
                                             'created_at': tweet._json['retweeted_status']['created_at'],
                                             'id_str': tweet._json['retweeted_status']['id_str'],
                                             'favorite_count': tweet._json['retweeted_status']['favorite_count'],
                                             'hashtags': tweet._json['retweeted_status']['entities']['hashtags']}, 
                                             indent=4, sort_keys=True))
            else:
                tweetList.append(json.dumps({'full_text': tweet._json['full_text'], 
                                             'lang': tweet._json['lang'],
                                             'screen_name': tweet._json['user']['screen_name'], 
                                             'name': tweet._json['user']['name'], 
                                             'profile_image_url_https': tweet._json['user']['profile_image_url_https'],
                                             'retweet_count': tweet._json['retweet_count'], 
                                             'created_at': tweet._json['created_at'], 
                                             'id_str': tweet._json['id_str'], 
                                             'favorite_count': tweet._json['favorite_count'], 
                                             'hashtags': tweet._json['entities']['hashtags']}, 
                                             indent=4, sort_keys=True))
    if len(tweetList) - length == count * len(user_ids):
        return True
    return False


def gatherTweets(dummyNumber=0):
    global tweetList, userList, keyWords

    # getTweetsByUsers(userList, "2020-03-20", 4)
    sum = len(tweetList)
    for key in keyWords:
        sum += keyWords[key]
        getTweets(key, "2020-03-20", keyWords[key])

    sum += dummyNumber
    # if len(tweetList) != sum:
    #     return False
    return tweetList


if __name__ == '__main__':
    gatherTweets()
