import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.offline as py
import plotly.graph_objects as go
import nltk
import math
from collections import Counter
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn import feature_extraction
import re, string, random
from nltk.corpus import stopwords
from nltk import FreqDist, classify, NaiveBayesClassifier
from nltk.corpus import twitter_samples
from scipy.stats import pearsonr
stop_words = stopwords.words('english')

MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
FREE_TEXT = "FREE_TEXT"
df = pd.read_csv("csv/grad-pays.csv")
df_clean = pd.read_csv("csv/grad-pays.csv")
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
# TODO: Remove id - determined by ui/business data layout (tes by adding id col back in)
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

# bivariate analysis

# pearson's correlation - every col with every col
for q1 in range(len(questions)):
    print('main qs:' , questions[q1].question)
    for q2 in range(len(questions)):
        if(q1 != q2):   
            print(questions[q2].question)
            corr = (df.iloc[:,q1].astype('float64')).corr(df.iloc[:,q2].astype('float64'))
            print(corr)

# this does same this as above but one line + in df.shape    
pearsons_corr = df.astype('float64').corr()        
print(pearsons_corr)

# Finding duplicated rows by selected cols
counter = Counter(list(zip(df_clean.iloc[:,0].dropna(), df_clean.iloc[:,2].dropna()))) # hard coded 0 and 2
values = list(counter.values())
x = []
y = []
for a, b in counter:
    x.append(a)
    y.append(b)

temp_df = pd.DataFrame({'Var1':x, 'Var2':y, 'Count': values})
print(temp_df)

# Bubble Chart - plot categorical scatter plot
temp_df["markersize"] = temp_df.Count + 10
ax = temp_df.plot.scatter(x='Var1', y='Var2', alpha=0.5, s=temp_df.markersize)
for i, txt in enumerate(values):
    ax.annotate(txt, (temp_df.Var1.iat[i],temp_df.Var2.iat[i]), fontsize=8)
plt.tight_layout()
plt.savefig('bubblechart.png',dpi=300, bbox_inches = "tight")