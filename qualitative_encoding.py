import matplotlib
matplotlib.use('Agg')
from PIL import Image
from collections import Counter 
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import nltk.classify.util
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
import math, csv, operator, re, os, pickle, string

def free_text_questions():
    df = pickle.load(open("raw_data_store.dat", "rb"))
    questions = pickle.load(open("data_store.dat", "rb"))
    df = df.dropna()
    cols = []
    
    for q in questions:
        if(q.questionType == 'FREE_TEXT' and q.dataType == 'QUALITATIVE'):
            cols.append(q.question)
            
    return cols      

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
    sentiment_data = []
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
    
        sentiment_data.append([negative_percentage, positive_percentage, neutral_percentage, negative_sentiments, positive_sentiments, neutral_sentiments, df.columns[col]])
    return sentiment_data

def sentiment_data_tokens(neg_sentiments, pos_sentiments, neu_sentiments):
    lexicon = dict()
    with open('csv/subjectivity-lexicon.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            lexicon[row[0]] = int(row[1])
    if(len(pos_sentiments) > 0):
        pos_tokens = []
        scrubbed = []
        for pos in pos_sentiments:
            for word in pos.split():
                if word in lexicon:
                    scrubbed.append(word)
        CounterVariable  = Counter(str(scrubbed).split())
        pos_tokens = [word.translate(str.maketrans('', '', string.punctuation)) for word, word_count in CounterVariable.most_common(10)]                
    else:
        pos_tokens = []
        
    if(len(neg_sentiments) > 0):
        neg_tokens = []
        scrubbed = []
        for neg in neg_sentiments:
            for word in neg.split():
                if word in lexicon:
                    scrubbed.append(word)
        CounterVariable  = Counter(str(scrubbed).split())
        neg_tokens = [word.translate(str.maketrans('', '', string.punctuation)) for word, word_count in CounterVariable.most_common(10)] 
    else:
        neg_tokens = []
        
    if(len(neu_sentiments) > 0):
        neu_tokens = []
        scrubbed = []
        for neu in neu_sentiments:
            for word in neu.split():
                if word in lexicon:
                    scrubbed.append(word)
        CounterVariable  = Counter(str(scrubbed).split())
        neu_tokens = [word.translate(str.maketrans('', '', string.punctuation)) for word, word_count in CounterVariable.most_common(10)] 
    else:
        neu_tokens = []
    return pos_tokens, neg_tokens, neu_tokens

def sentiment_tokens():
    sentiment_data = sentiment_analysis()
    categories = []            
    for neg_percentage, pos_percentage, neu_percentage, neg_sentiments, pos_sentiments, neu_sentiments, question in sentiment_data:        
       pos_tokens, neg_tokens, neu_tokens = sentiment_data_tokens(neg_sentiments, pos_sentiments, neu_sentiments)
       categories.append({
        "question": question,
        "pos_tokens": pos_tokens,
        "positive_statements": pos_sentiments, 
        "neg_tokens": neg_tokens,
        "negative_statements": neg_sentiments, 
        "neu_tokens": neu_tokens,
        "neutral_statements": neu_sentiments
       })
    return categories

def sentiment_charts():
    if os.path.exists("tmp/sentiment_charts.html"):
        os.remove("tmp/sentiment_charts.html")
    sentiment_data = sentiment_analysis()
    colors = ['mediumspringgreen', 'tomato', 'dodgerblue']
    titles = []
    for neg_percentage, pos_percentage, neu_percentage, neg_sentiments, pos_sentiments, neu_sentiments, question in sentiment_data:
        pos_tokens, neg_tokens, neu_tokens = sentiment_data_tokens(neg_sentiments, pos_sentiments, neu_sentiments)
        fig = make_subplots(rows=1, cols=2, specs=[[{"type": "bar"}, {"type": "pie"}]])
        fig.add_trace(go.Bar(x=["Positive", "Negative", "Neutral"], 
                             y=[pos_percentage, neg_percentage, neu_percentage],   
                             text = [pos_tokens, neg_tokens, neu_tokens],
                            #  hovertemplate = "<br>Tokens: %{text} </br>",
                             marker_color=colors, 
                             showlegend=False), 
                             row=1, col=1)
        fig.add_trace(go.Pie(text=["Positive", "Negative", "Neutral"], 
                             values=[pos_percentage, neg_percentage, neu_percentage],
                             labels = [pos_tokens, neg_tokens, neu_tokens],
                            #  hovertemplate ="<br>Tokens: %{label} </br>",
                             marker=dict(colors=colors)), 
                             row=1, col=2)
        fig.update_layout(title=question, xaxis_title="Sentiments", yaxis_title="Frequency")
        titles.append(question)
        with open('tmp/sentiment_charts.html', 'a') as f:
            f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    if os.path.exists("tmp/sentiment_charts.html"):
        file = open("tmp/sentiment_charts.html", 'r', encoding='utf-8')
        source_code = file.read() 
        return 'tmp/sentiment_charts.html', source_code, titles
    else:
        return None, None, None
    
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
    categories = []
    thematic_details = []

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

        num_clusters = k_num
        print(num_clusters)
        km = KMeans(n_clusters=num_clusters, max_iter=10)
        km.fit(tfidf_matrix)
        clusters = km.labels_.tolist()

        cluster_values = [[] for _ in range(num_clusters)]
        for index, totalvocab_stemmed in enumerate(df[df.columns.values.tolist()[col]].values.tolist()):
            cluster_values[clusters[index]].append(str(totalvocab_stemmed))

        themes = []
        topics = []
        keywords = []
        statements_count = []
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
            topics.append(topic)
            tokens = [word.translate(str.maketrans('', '', string.punctuation)) for word in most_occur]
            keywords.append(tokens)
            statements = cluster_values[i]
            statements_count.append(len(statements))
            themes.append({
                "theme": topic,
                "tokens": tokens,
                "statements": statements
            })
        thematic_details.append([df.columns.values.tolist()[col], topics, keywords, statements_count])
        categories.append({
            "question": df.columns.values.tolist()[col],
            "themes": themes
        })    
    return categories, df.columns.values.tolist(), thematic_details

def themes_charts():
    if os.path.exists("tmp/themes_charts.html"):
        os.remove("tmp/themes_charts.html")
    categories, questions, thematic_details = thematic_analysis()
    titles = []
    for theme in thematic_details:
        question = theme[0]
        x = theme[1]
        y = theme[3]
        tokens = theme[2]
        fig = make_subplots(rows=1, cols=2, specs=[[{"type": "bar"}, {"type": "pie"}]])
        fig.add_trace(go.Bar(x=x, y=y, text = tokens, marker_color=px.colors.qualitative.Plotly, showlegend=False), row=1, col=1)
        fig.add_trace(go.Pie(text=x, values=y, labels = tokens), row=1, col=2)
        fig.update_layout(title=question, xaxis_title="Themes", yaxis_title="Frequency")
        titles.append(question)
        with open('tmp/themes_charts.html', 'a') as f:
             f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    if os.path.exists("tmp/themes_charts.html"):
        file = open("tmp/themes_charts.html", 'r', encoding='utf-8')
        source_code = file.read() 
        return 'tmp/themes_charts.html', source_code, titles, categories
    else:
        return None, None, None, None
    