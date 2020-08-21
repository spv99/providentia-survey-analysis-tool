import csv
import numpy as np
import pandas as pd
import nltk
import re
import os
from sklearn import feature_extraction
import mpld3
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans

global data

f = open("csv/new-york-survey.csv", "r")
col = (f.readline()).split(',')
data = ''
with open('csv/new-york-survey.csv') as f:
    next(f)
    count = 0
    for line in f:
        if count != 1000:
            data = data + line
            count +=1 
        else:
            break
 
stopwords = nltk.corpus.stopwords.words('english')
stemmer = SnowballStemmer("english")

def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems


def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters
    for token in tokens:
        if re.search('[a-zA-Z]', token) and len(token) > 1:
            filtered_tokens.append(token)
    return filtered_tokens

totalvocab_stemmed = [] # instead of stemmed try synonyms
totalvocab_tokenized = []
row = data.splitlines()

for response in row:
    allwords_stemmed = tokenize_and_stem(response)
    totalvocab_stemmed.extend(allwords_stemmed)
    
    allwords_tokenized = tokenize_only(response)
    totalvocab_tokenized.extend(allwords_tokenized)

print(len(totalvocab_stemmed))
print(len(totalvocab_tokenized))
vocab_frame = pd.DataFrame({'words': [totalvocab_tokenized]}, index = [totalvocab_stemmed])
print ('there are ' + str(vocab_frame.shape[0]) + ' items in vocab_frame')
print (vocab_frame.head())

#define vectorizer parameters
tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                 min_df=0.2, stop_words='english',
                                 use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1,3))

tfidf_matrix = tfidf_vectorizer.fit_transform(row)

print(tfidf_matrix.shape)
terms = tfidf_vectorizer.get_feature_names()
print(terms)
dist = 1 - cosine_similarity(tfidf_matrix)

# K-Means Clustering

num_clusters = 5
km = KMeans(n_clusters=num_clusters)
km.fit(tfidf_matrix)
clusters = km.labels_.tolist()
responses = {'col': col, 'row': row, 'cluster': clusters}
frame = pd.DataFrame(responses, index = [clusters] , columns = [clusters])
#frame.value_counts()
print(frame)
print("Top terms per cluster:")
print()
#sort cluster centers by proximity to centroid
order_centroids = km.cluster_centers_.argsort()[:, ::-1] 
#print(order_centroids)
local_terms = []

for i in range(num_clusters):
    print("Cluster %d words:" % i, end='')
    for ind in order_centroids[i, :6]: #replace 6 with n words per cluster
        #print(' %s' % vocab_frame.iloc[terms[ind].split(' ')].values.tolist()[0].encode('utf-8', 'ignore'), end=',')
        #local_terms.append((vocab_frame.loc[[terms[ind]]].values.tolist()[0]))
        print((' %s' % vocab_frame.loc[terms[ind].split(' ')].values.tolist()[0][0]).encode('utf-8', 'ignore'), end=',')
    print(local_terms)
