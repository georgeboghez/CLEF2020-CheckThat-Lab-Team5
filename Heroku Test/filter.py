from nltk.tokenize import word_tokenize

NEWS_KEYWORDS_FILE = "words/news.txt"
SWEAR_KEYWORDS_FILE = "words/swear.txt"
SALES_KEYWORDS_FILE = "words/sales.txt"
JOBS_KEYWORDS_FILE = "words/jobs.txt"
WEATHER_KEYWORDS_FILE = "words/weather.txt"

NEWS_TAGS_FILE = "tags/news-tags.txt"
SALES_TAGS_FILE = "tags/sales-tags.txt"
JOBS_TAGS_FILE = "tags/jobs-tags.txt"
WEATHER_TAGS_FILE = "tags/weather-tags.txt"

TWEET_TEXT_FIELD = 'full_text'
TWEET_RETWEETED_STATUS_FIELD = 'retweeted_status'
TWEET_ENTITIES_FIELD = 'entities'
TWEET_HASHTAGS_FIELD = 'hashtags'
TWEET_TAG_TEXT_FIELD = 'text'
TWEET_LANGUAGE_FIELD = 'lang'


def get_text_from_tweet(tweet):
    if TWEET_RETWEETED_STATUS_FIELD in tweet:
        return tweet[TWEET_RETWEETED_STATUS_FIELD][TWEET_TEXT_FIELD]

    return tweet[TWEET_TEXT_FIELD]


def tokenizer(text):
    tokens = word_tokenize(text)
    return tokens


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


def check_for_keywords(tokens):
    # check for news keywords
    if contains_keywords(tokens, NEWS_KEYWORDS_FILE) is True:
        return 0  # tweets is news

    array_of_keywords_files = (
        SWEAR_KEYWORDS_FILE,
        SALES_KEYWORDS_FILE,
        JOBS_KEYWORDS_FILE,
        WEATHER_KEYWORDS_FILE
    )

    for file in array_of_keywords_files:
        if contains_keywords(tokens, file) is True:
            return 1  # tweets is not news

    return 2  # vague


def check_for_tags(tags):
    if contains_tags(tags, NEWS_TAGS_FILE) is True:
        return 0  # tweet is news

    array_of_tags_files = (
        SALES_TAGS_FILE,
        JOBS_TAGS_FILE,
        WEATHER_TAGS_FILE
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

    # check for keywords
    keywords_checking_result = check_for_keywords(tokens)
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
