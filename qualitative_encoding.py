import matplotlib
matplotlib.use('Agg')
from PIL import Image
from wordcloud import WordCloud
from collections import Counter 
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import nltk.classify.util
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
import math, csv, operator, re, os, pickle, string, json

def remove_noise(tokens, stop_words = ()):
    # stop_words.append('n/a')
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
        
def strip_non_ascii(string):
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

def sentiment_analysis():
    df = pickle.load(open("raw_data_store.dat", "rb"))
    questions = pickle.load(open("data_store.dat", "rb"))
    df = df.dropna()
    
    for q in questions:
        if(q.questionType != 'FREE_TEXT' or q.dataType != 'QUALITATIVE'):
            del df[q.question]
            
    df = df.dropna()
    
    for col in range(len(df.columns)):    
        lexicon = dict()
        with open('csv/subjectivity-lexicon.csv', 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                lexicon[row[0]] = int(row[1])
            
        text_body = []
        for x in range(len(df)):
            text_dict = dict()
            text_dict['original'] = df.iloc[x,col]
            text_dict['clean'] = strip_non_ascii(text_dict['original'])
            text_dict['clean'] = text_dict['clean'].lower()
            text_body.append(text_dict)

        for text in text_body:
            score = 0
            for word in text['clean'].split():
                if word in lexicon:
                    score = score + lexicon[word]

            text['score'] = score
            if (score > 0):
                text['sentiment'] = 'positive'
            elif (score < 0):
                text['sentiment'] = 'negative'
            else:
                text['sentiment'] = 'neutral'
                
        total = float(len(text_body))
        num_pos = sum([1 for t in text_body if t['sentiment'] == 'positive'])
        num_neg = sum([1 for t in text_body if t['sentiment'] == 'negative'])
        num_neu = sum([1 for t in text_body if t['sentiment'] == 'neutral'])
        positive_percentage = 100.0 * (num_pos/total)
        negative_percentage = 100.0 * (num_neg/total)
        neutral_percentage = 100.0 * (num_neu/total)
        
        text_body_sorted = sorted(text_body, key=lambda k: k['score'])
        negative_sentiments = []
        positive_sentiments = []
        neutral_sentiments = [] 

        negative_text = [d for d in text_body_sorted if d['sentiment'] == 'negative']
        for text_dict in negative_text:
            negative_sentiments.append(text_dict['original'])

        positive_text = [d for d in text_body_sorted if d['sentiment'] == 'positive']
        for text_dict in positive_text:
            positive_sentiments.append(text_dict['original'])

        neutral_text = [d for d in text_body_sorted if d['sentiment'] == 'neutral']
        for text_dict in neutral_text:
            neutral_sentiments.append(text_dict['original'])
    
    return negative_percentage, positive_percentage, neutral_percentage, negative_sentiments, positive_sentiments, neutral_sentiments, df.columns.values.tolist()

def sentiment_tokens():
    neg_percentage, pos_percentage, neu_percentage, neg_sentiments, pos_sentiments, neu_sentiments, questions = sentiment_analysis()
    categories = {}            
    lexicon = dict()
    with open('csv/subjectivity-lexicon.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            lexicon[row[0]] = int(row[1])
    for q in range(len(questions)):        
        if(len(pos_sentiments) > 5):
            pos_tokens = []
            scrubbed = []
            for pos in pos_sentiments:
                for word in pos.split():
                    if word in lexicon:
                        scrubbed.append(word)
            CounterVariable  = Counter(str(scrubbed).split())
            pos_tokens = [word for word, word_count in CounterVariable.most_common(10)]                
        else:
            pos_tokens = []
            
        if(len(neg_sentiments) > 5):
            neg_tokens = []
            scrubbed = []
            for neg in neg_sentiments:
                for word in neg.split():
                    if word in lexicon:
                        scrubbed.append(word)
            CounterVariable  = Counter(str(scrubbed).split())
            neg_tokens = [word for word, word_count in CounterVariable.most_common(10)] 
        else:
            neg_tokens = []
            
        if(len(neu_sentiments) > 5):
            neu_tokens = []
            scrubbed = []
            for neu in neu_sentiments:
                for word in neu.split():
                    if word in lexicon:
                        scrubbed.append(word)
            CounterVariable  = Counter(str(scrubbed).split())
            neu_tokens = [word for word, word_count in CounterVariable.most_common(10)] 
        else:
            neu_tokens = []
            
        categories[questions[q]] = {
            "pos_tokens": pos_tokens,
            "positive_statements": pos_sentiments, 
            "neg_tokens": neg_tokens,
            "negative_statements": neg_sentiments, 
            "neu_tokens": neu_tokens,
            "neutral_statements": neu_sentiments
        }
    return categories

def sentiment_piechart():
    if os.path.exists("tmp/sentiment_piechart.html"):
        os.remove("tmp/sentiment_piechart.html")
    neg_percentage, pos_percentage, neu_percentage, neg_sentiments, pos_sentiments, neu_sentiments, questions = sentiment_analysis()
    colors = ['mediumspringgreen', 'tomato', 'dodgerblue']
    for q in range(len(questions)):
        fig = go.Figure([go.Pie(labels=["Positive", "Negative", "Neutral"], values=[pos_percentage, neg_percentage, neu_percentage])])
        fig.update_traces(marker=dict(colors=colors))
        fig.update_layout(title=questions[q])
        with open('tmp/sentiment_piechart.html', 'a') as f:
            f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    if os.path.exists("tmp/sentiment_piechart.html"):
        file = open("tmp/sentiment_piechart.html", 'r', encoding='utf-8')
        source_code = file.read() 
        return 'tmp/sentiment_piechart.html', source_code
    else:
        return None, None
    
def sentiment_bargraph():
    if os.path.exists("tmp/sentiment_bargraph.html"):
        os.remove("tmp/sentiment_bargraph.html")
    neg_percentage, pos_percentage, neu_percentage, neg_sentiments, pos_sentiments, neu_sentiments, questions = sentiment_analysis()
    colors = ['mediumspringgreen', 'tomato', 'dodgerblue']
    for q in range(len(questions)):
        fig = go.Figure([go.Bar(x=["Positive", "Negative", "Neutral"], y=[pos_percentage, neg_percentage, neu_percentage],  marker_color=colors)])
        fig.update_layout(title=questions[q])
        with open('tmp/sentiment_bargraph.html', 'a') as f:
             f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    if os.path.exists("tmp/sentiment_bargraph.html"):
        file = open("tmp/sentiment_bargraph.html", 'r', encoding='utf-8')
        source_code = file.read() 
        return 'tmp/sentiment_bargraph.html', source_code
    else:
        return None, None
    
def tokenize_only(text):
        tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
        filtered_tokens = []
        for token in tokens:
            if re.search('[a-zA-Z]', token) and len(token) > 1:
                filtered_tokens.append(token)
        return filtered_tokens
    
def thematic_analysis():
    df = pickle.load(open("raw_data_store.dat", "rb"))
    questions = pickle.load(open("data_store.dat", "rb"))
    df = df.dropna()

    for q in questions:
        if(q.questionType != 'FREE_TEXT' or q.dataType != 'QUALITATIVE'):
            del df[q.question]
    
    themes = {}
    data = df
    columns = df.columns.values.tolist()
    stopwords = nltk.corpus.stopwords.words('english')
    stemmer = SnowballStemmer("english")

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
    
    def tokenize_and_stem(text):
        tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
        filtered_tokens = []
        for token in tokens:
            if re.search('[a-zA-Z]', token):
                filtered_tokens.append(token)
        stems = [stemmer.stem(t) for t in filtered_tokens]
        return stems

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
        
        distortions = []
        K_to_try = range(1, 10)

        for i in K_to_try:
            model = KMeans(
                n_clusters=i,
                init='k-means++',
                random_state=1)
            model.fit(tfidf_matrix)
            distortions.append(model.inertia_)
            
        x_values = [K_to_try[0], K_to_try[len(K_to_try)-1]]
        y_values = [distortions[0], distortions[len(distortions)-1]]
        line = plt.plot(x_values, y_values)
        elbow = plt.plot(K_to_try, distortions, marker='o')
        plt.xlabel('Number of Clusters (k)')
        plt.ylabel('Distortion')
    
        # getting coefficients of optimal line
        start = [x_values[0], y_values[0]]
        end = [x_values[1], y_values[1]]
        a=(start[1] - end[1])
        b=(end[0] - start[0])
        c=(start[0]*end[1]) - (end[0]*start[1])
        
        # diff between optimal line and elbow line (perpendicular/euclidian diff)
        k_num = 0
        max_k_val = 0
        for k in range(len(K_to_try)):
            max_k = abs((a * K_to_try[k] + b * distortions[k] + c)) / (math.sqrt(a * a + b * b)) 
            if(k_num == 0 or max_k > max_k_val):
                max_k_val = max_k
                k_num = K_to_try[k]
            else:
                break

        num_clusters = k_num - 1
        print(num_clusters)
        km = KMeans(n_clusters=num_clusters, max_iter=10)
        km.fit(tfidf_matrix)
        clusters = km.labels_.tolist()

        cluster_values = [[] for _ in range(num_clusters)]
        for index, totalvocab_stemmed in enumerate(df[df.columns.values.tolist()[col]].values.tolist()):
            cluster_values[clusters[index]].append(str(totalvocab_stemmed))

        categories = {}
        themes = {}
        for i in range(len(cluster_values)):
            totalvocab_tokenized = []
            totalvocab_lemmetized = []
            totalvocab_cleaned = []
            allwords_tokenized = tokenize_only(str(cluster_values[i]))
            totalvocab_tokenized.extend([allwords_tokenized])
            totalvocab_lemmetized.extend([lemmatize_sentence(totalvocab_tokenized[x in cluster_values[i]])])
            totalvocab_cleaned.extend([remove_noise(totalvocab_lemmetized[x in cluster_values[i]], stop_words)])
            CounterVariable  = Counter(str(totalvocab_cleaned).split())
            most_occur = [word for word, word_count in CounterVariable.most_common(10)]
            topic = most_occur[0].translate(str.maketrans('', '', string.punctuation))
            tokens = [word.translate(str.maketrans('', '', string.punctuation)) for word in most_occur]
            statements = cluster_values[i]
            themes[topic] = {
                "theme": topic,
                "tokens": tokens,
                "statements": statements
            }
        categories[df.columns[col]] = {
            "themes": themes
        }
    return categories, df.columns.values.tolist()

def themes_bargraph():
    if os.path.exists("tmp/themes_bargraph.html"):
        os.remove("tmp/themes_bargraph.html")
    categories, questions = thematic_analysis()
    for q in questions:
        themes = categories.get(q)
        x = []
        y = []
        for v in themes.get("themes"):
            x.append(themes.get("themes").get(v).get("theme"))
            y.append(len(themes.get("themes").get(v).get("statements")))
        fig = go.Figure([go.Bar(x=x, y=y)])
        fig.update_layout(title=q)
        with open('tmp/themes_bargraph.html', 'a') as f:
             f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    if os.path.exists("tmp/themes_bargraph.html"):
        file = open("tmp/themes_bargraph.html", 'r', encoding='utf-8')
        source_code = file.read() 
        return 'tmp/themes_bargraph.html', source_code
    else:
        return None, None
    
def themes_piechart():
    if os.path.exists("tmp/themes_piechart.html"):
        os.remove("tmp/themes_piechart.html")
    categories, questions = thematic_analysis()
    for q in questions:
        themes = categories.get(q)
        x = []
        y = []
        for v in themes.get("themes"):
            x.append(themes.get("themes").get(v).get("theme"))
            y.append(len(themes.get("themes").get(v).get("statements")))
        fig = go.Figure([go.Pie(labels=x, values=y)])
        fig.update_layout(title=q)
        with open('tmp/themes_piechart.html', 'a') as f:
             f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    if os.path.exists("tmp/themes_piechart.html"):
        file = open("tmp/themes_piechart.html", 'r', encoding='utf-8')
        source_code = file.read() 
        return 'tmp/themes_piechart.html', source_code
    else:
        return None, None
    
def wordmaps():
    df = pickle.load(open("raw_data_store.dat", "rb"))
    questions = pickle.load(open("data_store.dat", "rb"))
    df = df.dropna()
    
    for q in questions:
        if(q.questionType != 'FREE_TEXT' or q.dataType != 'QUALITATIVE'):
            del df[q.question]
            
    df = df.dropna()
    
    wordmap = {}
    for col in range(len(df.columns)):
        free_text = df[df.columns.values.tolist()[col]].values.tolist()
        free_text = str(free_text).replace("'", "")
        totalvocab_tokenized = []
        totalvocab_lemmetized = []
        totalvocab_cleaned = []
        allwords_tokenized = tokenize_only(str(free_text))
        totalvocab_tokenized.extend([allwords_tokenized])
        totalvocab_cleaned = [w for w in totalvocab_tokenized[0] if not w in stop_words]
        CounterVariable  = Counter(str(totalvocab_cleaned).split())
        variable = [word for word, word_count in CounterVariable.most_common(30)]
        counter = [word_count for word, word_count in CounterVariable.most_common(30)]
        count = 0
        words = {}
        for i in range(0, len(counter)):
            words[count] = {
               "word": variable[i].translate(str.maketrans('', '', string.punctuation)),
               "count": counter[i] 
            }
            count += 1
        wordmap[df.columns[col]] = {
            "wordmap": words
        }
    return wordmap