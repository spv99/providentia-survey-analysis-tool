import csv
import numpy as np
import pandas as pd
import nltk
import re
import os
from sklearn import feature_extraction
import mpld3
from nltk.stem.snowball import SnowballStemmer

global data

f = open("new-york-survey.csv", "r")
col = (f.readline()).split(',')
data = ''
with open('new-york-survey.csv') as f:
    next(f)
    for line in f:
        data = data + line
 
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
vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)
