import csv
import pickle
import operator

from nltk import word_tokenize
from nltk.corpus import stopwords

TWEET_LANGUAGE_FIELD = 'lang'
TWEET_TEXT_FIELD = 'full_text'
TWEET_TAGS_FIELD = 'hashtags'
TWEET_TAG_TEXT_FIELD = 'text'

CSV_TWEET_ID_FIELD = "tweet_id"
CSV_TWEET_TEXT_FIELD = "tweet_text"
CSV_TWEET_TAGS_FIELD = "tweet_tags"
CSV_TWEET_LABEL_FIELD = "label"

TRAINING_DATASET_FILE = "data/training_dataset.csv"
MODEL_FILE = "data/model.ser"

DEFAULT_LABELS = ['news', 'ad', 'job', 'other']


def get_text_from_tweet(tweet):
    return tweet[TWEET_TEXT_FIELD]


def get_tags_from_tweet(tweet):
    tags_list = tweet[TWEET_TAGS_FIELD]
    tags = [tag[TWEET_TAG_TEXT_FIELD] for tag in tags_list]
    new_tags = [tag.lower() for tag in tags]
    return new_tags


def remove_stop_words(words):
    stop_words = set(stopwords.words('english'))
    filtered_words = []

    for word in words:
        if word not in stop_words:
            filtered_words.append(word)

    return filtered_words


def extract_tokens(text):
    tokens = word_tokenize(text)
    tokens = remove_stop_words(tokens)
    return tokens


def get_training_data():
    file_handler = open(MODEL_FILE, 'rb')
    training_data = pickle.load(file_handler)

    if not training_data:
        with open(TRAINING_DATASET_FILE, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                tokens = extract_tokens(row[CSV_TWEET_TEXT_FIELD])
                label = row[CSV_TWEET_LABEL_FIELD]
                tags = extract_tokens(row[CSV_TWEET_TAGS_FIELD])
                training_data.append([tokens, tags, label])

    return training_data


def get_words(training_data):
    words = []
    for data in training_data:
        words.extend(data[0])  # tokens
        words.extend(data[1])  # tags
    return list(set(words))


def get_words_probabilities_by_label(training_data, label):
    words = get_words(training_data)
    freq = {}

    for word in words:
        freq[word] = 1

    total_count = 0
    for data in training_data:
        if data[2] == label:
            total_count += len(data[0]) + len(data[1])
            for word in data[0]:
                freq[word] += 1
            for word in data[1]:
                freq[word] += 1

    probabilities = {}
    for word in freq.keys():
        probabilities[word] = freq[word] * 1.0 / total_count

    return probabilities


def get_tweet_label_probability(training_data, label):
    count = 0
    total_count = 0
    for data in training_data:
        total_count += 1
        if data[2] == label:
            count += 1

    return count * 1.0 / total_count


def label_tweet(tokens, training_data):
    labels_words_probabilities = {}
    for label in DEFAULT_LABELS:
        labels_words_probabilities[label] = get_words_probabilities_by_label(training_data, label)

    tweet_label_probability = {}
    for label in DEFAULT_LABELS:
        tweet_label_probability[label] = get_tweet_label_probability(training_data, label)

    for word in tokens:
        for current_label in labels_words_probabilities.keys():
            if word in labels_words_probabilities[current_label].keys():
                for label in DEFAULT_LABELS:
                    tweet_label_probability[label] *= labels_words_probabilities[label][word]
                break

    # return the label with maximum probability
    label = max(tweet_label_probability.items(), key=operator.itemgetter(1))[0]
    return label


def is_news(tweet):
    # written in english
    if tweet[TWEET_LANGUAGE_FIELD] != 'en':
        return False

    tweet_text = get_text_from_tweet(tweet)
    tokens = extract_tokens(tweet_text.lower())

    tags = get_tags_from_tweet(tweet)
    tokens.extend(tags)

    training_data = get_training_data()

    return label_tweet(tokens, training_data) == 'news'
