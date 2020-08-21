import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.offline as py
import plotly.graph_objects as go
import nltk
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn import feature_extraction
import re, string, random
from nltk.corpus import stopwords
from nltk import FreqDist, classify, NaiveBayesClassifier
from nltk.corpus import twitter_samples
stop_words = stopwords.words('english')

MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
FREE_TEXT = "FREE_TEXT"
df = pd.read_csv("csv/grad-pays.csv")
cols = list(df.columns.values)
total_respondents = df.shape[0]
index = 0
questions = [[] for _ in range(len(cols))]
x = np.array([])
y = np.array([])

class Question:
    def __init__(self, question, questionType, options, flattened_options):
      self.question = question
      self.questionType = questionType
      self.options = options
      self.flattened_options = flattened_options

# methods for text analysis
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
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token) # TODO: test regex 
        token = re.sub("(@[A-Za-z0-9_]+)","", token) # TODO: test regex 

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

def token_to_dict_converter(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tokens)


# training dataset for text analysis
def training_set():
    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []

    for tokens in positive_tweet_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    for tokens in negative_tweet_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    all_pos_words = get_all_words(positive_cleaned_tokens_list)

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

# getting question types
# TODO: Remove id if in first col
for col in cols:
    unique_vals = df.iloc[:,index].dropna().unique()
    options = unique_vals
    col_value = df.iloc[:,index].value_counts()
    # if 90% or more of respondents answers are different then assume it is free text based answer 
    # (note: same would be if they all answered "no" which would mean unique_vals = 1)
    if((total_respondents*0.90) <= len(unique_vals)):
        if(isinstance(unique_vals[0], str)):
            training_set()
            totalvocab_tokenized = []
            totalvocab_lemmetized = []
            totalvocab_cleaned = []
            unique_val_index = 0
            for unique_val in unique_vals:
                print(df.iloc[unique_val_index,index])
                allwords_tokenized = tokenize_only(df.iloc[unique_val_index,index])
                totalvocab_tokenized.extend([allwords_tokenized])
                totalvocab_lemmetized.extend([lemmatize_sentence(totalvocab_tokenized[unique_val_index])])
                totalvocab_cleaned.extend([remove_noise(totalvocab_lemmetized[unique_val_index], stop_words)])
                #print(totalvocab_cleaned[unique_val_index])
                token_sentiment = classifier.classify(dict([token, True] for token in totalvocab_cleaned[unique_val_index]))
                #print(token_sentiment)
                df.iloc[unique_val_index,index] = token_sentiment
                unique_val_index += 1
        unique_vals = df.iloc[:,index].dropna().unique()
        questions[index] = Question(col, FREE_TEXT, options, unique_vals)
    else:
        unique_val_index = 0
        for unique_val in unique_vals:
            df.iloc[:,index] = np.where(df.iloc[:,index] == unique_val, unique_val_index, df.iloc[:,index])
            unique_val_index += 1
        unique_vals = df.iloc[:,index].dropna().unique()
        questions[index] = Question(col, MULTIPLE_CHOICE, options, unique_vals)
        print(questions[index].question)
        print(questions[index].flattened_options)
    index +=1
    
# col_num = 0
# for d in df:
#     print(df.iloc[:,col_num])
#     col_num+=1
check_dupes_arr = []
dupe_count = []
x = []
y = []
hm_count = []
df['merge'] = df[df.columns[0:]].apply(lambda x: ','.join(x.dropna().astype(str)), axis=1)
for merge in (df['merge']):
    split_rows = merge.split(',')
    combo = split_rows[0] + ',' + split_rows[2] # 0 and 2 hardcoded
    check_dupes_arr.append(combo)
dupes_set = set([x for x in check_dupes_arr if check_dupes_arr.count(x)>1])
for elem in check_dupes_arr:
    split_combo = elem.split(',')
    x.append(split_combo[0])
    y.append(split_combo[1])
    for dupe in dupes_set:
        if dupe == elem:
            hm_count.append(check_dupes_arr.count(elem))
            check_dupes_arr.remove(elem)
    else:
        hm_count.append(1)

#print(x)
#print(y)
#print(hm_count)
n = 3 # max number of options for x (what is your gender?) 0 inclusive
reshaped_arr = [hm_count[i:i+n] for i in range(0, len(hm_count), n)]
print(reshaped_arr)

# for dupe in dupes_set:
#     # add column groupby count of two cols
#     check_dupes_arr.count(dupe)
#     print('dupe')
#     print(dupe)
#     print(check_dupes_arr.count(dupe))
#     dupe_count.append(check_dupes_arr.count(dupe))

#SCATTER
#fig = go.Figure(data=go.Scatter(x=(df.iloc[:,0]), y=(df.iloc[:,1]), mode='markers')) # bubble chart - count recurring

#HEATMAP
fig = go.Figure(data=go.Heatmap(z=reshaped_arr))
#fig.show()

py.plot(fig, filename='heatmap.html')

# pairing_df = pd.DataFrame(data, columns=['x', 'y'])11`1`1111111
# pairing_df.plot()
# pairing_df.plot(kind='scatter', x='x', y='y')
# plt.scatter(df.iloc[:,0], df.iloc[:,1])