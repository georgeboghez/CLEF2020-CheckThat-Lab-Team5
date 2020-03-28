import tweepy as tw
from random import shuffle
import json

consumer_key = 'CmQS1BFO5D38aYu38isgYfQSM'
consumer_secret = '0BT4Pvkox9y4USuKmzsh6IzzfymdMcPrCKANnYVc82qXZMRn7D'
access_token = '1242346386756112384-rBnQ65dlWwgbVQp6Me6op8AEqogEgn'
access_token_secret = 'P6kfsxgeTkL7e6vifWf5VJmDQVKIKMehPyJLPJ16RcglK'


auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

tweetList = list()


def getTweets(search_word, date_since, count):
    tweets = tw.Cursor(api.search,
                       q=search_word,
                       lang="en",
                       tweet_mode='extended',
                       since=date_since).items(count)
    return tweets


def getTweetsByUsers(user_ids, date_since, count, query=""):
    tweets = list()
    for user in user_ids:
        tweets += tw.Cursor(api.user_timeline,
                            q=query,
                            id=user,
                            tweet_mode='extended',
                            since=date_since).items(count)
    return tweets


def displayTweets(tweets):
    for t in tweets:
        print(t.full_text + "\n")


def addTweetLists(*list):
    global tweetList
    for l in list:
        tweetList += [json.dumps(tweet._json, indent=4,
                                 sort_keys=True) for tweet in l]
    shuffle(tweetList)


def main():
    user_list = ["EU_Comission", "realDonaldTrump", "BernieSanders", "JoeBiden",
                 "elonmusk", "tconnellyRTE", "BarackObama", "Samsung", "NASA"]

    user_news = getTweetsByUsers(user_list, "2020-03-20", 4)
    news_tweets = getTweets("coronavirus", "2020-03-20", 10)
    ad_tweets = getTweets("#ad", "2020-03-20", 10)
    economy = getTweets("economy", "2020-03-20", 4)
    olympics = getTweets("olympic games", "2020-03-20", 4)
    russia = getTweets("russia", "2020-03-20", 6)
    europe = getTweets("#europe", "2020-03-10", 4)
    br_news_tweets = getTweets("#breaking-news", "2020-03-20", 30)
    general_news = getTweets("news", "2020-03-20", 20)

    addTweetLists(br_news_tweets, user_news, news_tweets,
                  ad_tweets, economy, olympics, russia, europe, general_news)

    return tweetList


if __name__ == '__main__':
    main()
