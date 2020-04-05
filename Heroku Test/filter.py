import json
import pprint
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from autocorrect import Speller

MINIMUM_NUMBER_OF_WORDS = 10

IRRELEVANT_KEYS_FILE = "resources/keys.txt"
NEWS_KEYWORDS_FILE = "words/news.txt"
SWEAR_KEYWORDS_FILE = "words/swear.txt"
SALES_KEYWORDS_FILE = "words/sales.txt"
JOBS_KEYWORDS_FILE = "words/jobs.txt"

NEWS_TAGS_FILE = "tags/news-tags.txt"
SALES_TAGS_FILE = "tags/sales-tags.txt"
JOBS_TAGS_FILE = "tags/jobs-tags.txt"

TWEET_TEXT_FIELD = 'full_text'
TWEET_RETWEETED_STATUS_FIELD = 'retweeted_status'
TWEET_ENTITIES_FIELD = 'entities'
TWEET_HASHTAGS_FIELD = 'hashtags'
TWEET_TAG_TEXT_FIELD = 'text'
TWEET_LANGUAGE_FIELD = 'lang'


# tweet - json object
# filename - name of the file which contains irrelevant keys
def remove_irrelevant_keys(tweet):
    with open(IRRELEVANT_KEYS_FILE) as keys_file:
        for line in keys_file:
            line = line.rstrip()
            tweet.pop(line, None)

    user = {'name': tweet['user']['name'], 'location': tweet['user']['location'],
            'verified': tweet['user']['verified'], 'id': tweet['user']['id']}

    tweet.pop("user", None)
    tweet['user'] = user

    return tweet


def get_text_from_tweet(tweet):
    if TWEET_RETWEETED_STATUS_FIELD in tweet:
        return tweet[TWEET_RETWEETED_STATUS_FIELD][TWEET_TEXT_FIELD]

    return tweet[TWEET_TEXT_FIELD]


def tokenizer(text):
    tokens = word_tokenize(text)
    return tokens


def remove_stop_words(tokens):
    stop_words = set(stopwords.words('english'))
    filtered_tokens = []

    for word in tokens:
        if word not in stop_words:
            filtered_tokens.append(word)

    return filtered_tokens


def has_spelling_errors(tokens):
    spell = Speller(lang='en')
    for word in tokens:
        if spell(word) != word:
            return True

    return False


def contains_keywords(tokens, filename):
    with open(filename) as keywords_file:
        for line in keywords_file:
            line = line.rstrip()
            for word in tokens:
                if line == word:
                    return True

    return False


def contains_tags(tags, filename):
    with open(filename) as tags_file:
        for line in tags_file:
            line = line.rstrip()
            for tag in tags:
                if tag[TWEET_TAG_TEXT_FIELD].lower() == line.lower():
                    return True

    return False


def check_for_keywords(filtered_tokens):
    # check for news keywords
    if contains_keywords(filtered_tokens, NEWS_KEYWORDS_FILE) is True:
        return 0  # tweets is news

    array_of_keywords_files = (
        SWEAR_KEYWORDS_FILE,
        SALES_KEYWORDS_FILE,
        JOBS_KEYWORDS_FILE
    )

    for file in array_of_keywords_files:
        if contains_keywords(filtered_tokens, file) is True:
            return 1  # tweets is not news

    return 2  # vague


def check_for_tags(tags):
    if contains_tags(tags, NEWS_TAGS_FILE) is True:
        return 0  # tweet is news

    array_of_tags_files = (
        SALES_TAGS_FILE,
        JOBS_TAGS_FILE
    )

    for file in array_of_tags_files:
        if contains_tags(tags, file) is True:
            return 1  # tweets is not news

    return 2  # vague


def is_news(tweet):
    # written in english
    if tweet[TWEET_LANGUAGE_FIELD] != 'en':
        return False

    tweet_text = get_text_from_tweet(tweet)
    tokens = tokenizer(tweet_text.lower())

    # has at least MINIMUM_NUMBER_OF_WORDS words
    if len(tokens) < MINIMUM_NUMBER_OF_WORDS:
        return False

    # optimisation
    filtered_tokens = remove_stop_words(tokens)

    # check for spelling errors
    # if has_spelling_errors(filtered_tokens):
    #     return False

    # check for keywords
    keywords_checking_result = check_for_keywords(filtered_tokens)
    if keywords_checking_result == 0:
        return True
    elif keywords_checking_result == 1:
        return False

    # check for tags
    tags = tweet[TWEET_ENTITIES_FIELD][TWEET_HASHTAGS_FIELD]
    tags_checking_result = check_for_tags(tags)
    if tags_checking_result == 0:
        return True
    elif tags_checking_result == 1:
        return False

    return True