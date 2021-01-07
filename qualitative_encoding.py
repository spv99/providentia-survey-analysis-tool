import pandas as pd
import nltk
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn import feature_extraction
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import re, string, random, os, pickle, mpld3, sys
from PIL import Image
from wordcloud import WordCloud
from collections import Counter 
import matplotlib.pyplot as plt
from nltk import FreqDist, classify, NaiveBayesClassifier
from nltk.corpus import twitter_samples, stopwords
stop_words = stopwords.words('english')

# tokenising, lemming, cleaning and checking term freq of data

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
    stop_words.append('n/a')
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
            
def token_to_dict_converter(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tokens)

def sentiment_analysis():
    df = pickle.load(open("raw_data_store.dat", "rb"))
    questions = pickle.load(open("data_store.dat", "rb"))
    df.dropna()
    sentiments = {}
    
    for q in questions:
        if(q.questionType != 'FREE_TEXT' or q.dataType != 'QUALITATIVE'):
            del df[q.question]
    
    for col in range(len(df.columns)):      
        totalvocab_tokenized = []
        totalvocab_lemmetized = []
        totalvocab_cleaned = []

        for x in range(len(df)):
            if(isinstance(df.iloc[x,col], str) == False):
                df.iloc[x,col] = "N/A" 
            allwords_tokenized = tokenize_only(df.iloc[x,col])
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
        for x in range(len(df)):
            token_sentiment = classifier.classify(dict([token, True] for token in totalvocab_cleaned[x]))
            sentiment_identifier = str(x) + ': ' + str(df.columns.values.tolist()[col])
            sentiments[sentiment_identifier] = [token_sentiment, totalvocab_cleaned[x]]
    return ({"sentiments": sentiments})

def wordmaps():
    path = 'tmp/'
    files = [i for i in os.listdir(path) if os.path.isfile(os.path.join(path,i)) and 'wordmap' in i]
    for f in files:
        os.remove(f)
    df = pickle.load(open("raw_data_store.dat", "rb"))
    questions = pickle.load(open("data_store.dat", "rb"))
    df.dropna()

    count = 0
    for q in questions:
        if(q.questionType == 'FREE_TEXT' and q.dataType == 'QUALITATIVE'):
            count += 1
            text = df[q.question].values.tolist()
            wordcloud = WordCloud(min_font_size=9, max_words=100, background_color="white").generate(str(text))
            plt.figure()
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.savefig('tmp/wordmap-' + str(count) + '.png')
    files = [i for i in os.listdir(path) if os.path.isfile(os.path.join(path,i)) and 'wordmap' in i]
    return files

def thematic_analysis():
    df = pickle.load(open("raw_data_store.dat", "rb"))
    questions = pickle.load(open("data_store.dat", "rb"))
    df.dropna()

    for q in questions:
        if(q.questionType != 'FREE_TEXT' or q.dataType != 'QUALITATIVE'):
            del df[q.question]
    
    themes = {}
    data = df
    columns = df.columns.values.tolist()
    stopwords = nltk.corpus.stopwords.words('english')
    stemmer = SnowballStemmer("english")
    
    def tokenize_and_stem(text):
        tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
        filtered_tokens = []
        for token in tokens:
            if re.search('[a-zA-Z]', token):
                filtered_tokens.append(token)
        stems = [stemmer.stem(t) for t in filtered_tokens]
        return stems


    def tokenize_only(text):
        tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
        filtered_tokens = []
        for token in tokens:
            if re.search('[a-zA-Z]', token) and len(token) > 1:
                filtered_tokens.append(token)
        return filtered_tokens
    
    for col in range(len(df.columns)):
        totalvocab_stemmed = [] 
        totalvocab_tokenized = []

        for x in range(len(df)):
            if(isinstance(df.iloc[x,col], str) == False):
                df.iloc[x,col] = "N/A" 
            allwords_stemmed = tokenize_and_stem(df.iloc[x,col])
            totalvocab_stemmed.extend(allwords_stemmed)
            
            allwords_tokenized = tokenize_only(df.iloc[x,col])
            totalvocab_tokenized.extend(allwords_tokenized)

        #define vectorizer parameters
        tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                        min_df=0.2, stop_words='english',
                                        use_idf=True, tokenizer=tokenize_and_stem)

        tfidf_matrix = tfidf_vectorizer.fit_transform(df[df.columns.values.tolist()[col]].values)

        terms = tfidf_vectorizer.get_feature_names()
        dist = 1 - cosine_similarity(tfidf_matrix)

        num_clusters = 4 #TODO: generate this via kmeans elbow ml algo
        km = KMeans(n_clusters=num_clusters, max_iter=10)
        km.fit(tfidf_matrix)
        clusters = km.labels_.tolist()

        cluster_values = [[] for _ in range(num_clusters)]
        for index, totalvocab_stemmed in enumerate(df[df.columns.values.tolist()[col]].values.tolist()):
            cluster_values[clusters[index]].append(str(totalvocab_stemmed))

        categories = []
        for i in range(len(cluster_values)):
            totalvocab_tokenized = []
            totalvocab_lemmetized = []
            totalvocab_cleaned = []
            allwords_tokenized = tokenize_only(str(cluster_values[i]))
            totalvocab_tokenized.extend([allwords_tokenized])
            totalvocab_lemmetized.extend([lemmatize_sentence(totalvocab_tokenized[x in cluster_values[i]])])
            totalvocab_cleaned.extend([remove_noise(totalvocab_lemmetized[x in cluster_values[i]], stop_words)])
            CounterVariable  = Counter(str(totalvocab_cleaned).split())
            most_occur = CounterVariable.most_common(1)
            categories.append(most_occur[0])

        themes[questions[col].question] = categories
    return ({"themes": themes})
#TODO - Scatter plot of clusters
#TODO - Append sentiment and thematic variables onto questions class to use in uni and bi analysis