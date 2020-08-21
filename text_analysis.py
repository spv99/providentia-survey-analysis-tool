import pandas as pd
import nltk
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn import feature_extraction
import re, string, random
from nltk.corpus import stopwords
from nltk import FreqDist, classify, NaiveBayesClassifier
from nltk.corpus import twitter_samples
stop_words = stopwords.words('english')

# tokenising, lemming, cleaning and checking term freq of data

df = pd.read_csv("csv/youtube_comments_oscar_trailer.csv").dropna()

def tokenize_only(text):
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens

def lemmatize_sentence(tokens):
    lemmatizer = WordNetLemmatizer()
    lemmatized_sentence = []
    for word, tag in pos_tag(tokens):
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
    return lemmatized_sentence

def remove_noise(tokens, stop_words = ()):
    cleaned_tokens = []
    for token, tag in pos_tag(tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token

totalvocab_tokenized = []
totalvocab_lemmetized = []
totalvocab_cleaned = []

for x in range(df.size):
    allwords_tokenized = tokenize_only(df.iloc[x,0])
    totalvocab_tokenized.extend([allwords_tokenized])
    totalvocab_lemmetized.extend([lemmatize_sentence(totalvocab_tokenized[x])])
    totalvocab_cleaned.extend([remove_noise(totalvocab_lemmetized[x], stop_words)])

all_words = get_all_words(totalvocab_cleaned)
freq_dist = FreqDist(all_words)

# training dataset
positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

positive_cleaned_tokens_list = []
negative_cleaned_tokens_list = []

for tokens in positive_tweet_tokens:
    positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

for tokens in negative_tweet_tokens:
    negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

all_pos_words = get_all_words(positive_cleaned_tokens_list)

freq_dist_pos = FreqDist(all_pos_words)

def token_to_dict_converter(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tokens)

positive_tokens_for_model = token_to_dict_converter(positive_cleaned_tokens_list)
negative_tokens_for_model = token_to_dict_converter(negative_cleaned_tokens_list)

positive_dataset = [(tweet_dict, "Positive")
                        for tweet_dict in positive_tokens_for_model]

negative_dataset = [(tweet_dict, "Negative")
                        for tweet_dict in negative_tokens_for_model]

dataset = positive_dataset + negative_dataset
random.shuffle(dataset)
train_data = dataset[:7000]
test_data = dataset[7000:]

classifier = NaiveBayesClassifier.train(train_data)

print("Training data accuracy is: ", classify.accuracy(classifier, test_data))

# using survey data for sentiment analysis
# prints out pos/neg output and accuracy % for each response
for x in range(df.size):
    print(totalvocab_cleaned[x])
    token_sentiment = classifier.classify(dict([token, True] for token in totalvocab_cleaned[x]))
    print(token_sentiment)
    print('#############################')