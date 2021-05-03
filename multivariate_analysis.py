import matplotlib
matplotlib.use('Agg')
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn import preprocessing
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from sklearn.cluster import KMeans
import plotly.express as px
from collections import Counter 
import random, pickle, math, os

def pca_options():
    # every qs-option
    if os.path.exists("tmp/pca_options.html"):
        os.remove("tmp/pca_options.html")
    df = pickle.load(open("raw_data_store.dat", "rb"))
    questions = pickle.load(open("data_store.dat", "rb"))

    for q in questions:
        if(q.dataType == 'QUALITATIVE' or q.questionType != 'MULTIPLE_CHOICE'):
            col_names = df[q.question].dropna().unique().tolist()
            df[col_names] = pd.get_dummies(df[q.question])
            del df[q.question]
        else:
            del df[q.question]

    cols = list(df)
    for q in questions:
        for op in q.options:
            for val in cols:
                if val == op:
                    df = df.rename(columns={val: str(q.question) + ': ' + str(val)})
            
    data = df

    scaled_data = preprocessing.scale(data.T)
    pca = PCA()
    pca.fit(scaled_data)
    pca_data = pca.transform(scaled_data)
    per_var = np.round(pca.explained_variance_ratio_*100, decimals=1)
    labels = ['PCA'+ str(x) for x in range(1, len(per_var)+1)]

    pca_df = pd.DataFrame(pca_data, index=df.columns.values, columns=labels)
    fig = go.Figure()
    fig = go.Figure(go.Scatter(x=pca_df.PCA1, y=pca_df.PCA2, mode='markers', marker_symbol='diamond', marker=dict(size=10, color='gold'), text=df.columns.values, name="options"))
    fig.update_layout(title="Correlating Questions and Responses")
    with open('tmp/pca_options.html', 'a') as f:
             f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    if os.path.exists("tmp/pca_options.html"):
        file = open("tmp/pca_options.html", 'r', encoding='utf-8')
        source_code = file.read() 
        return 'tmp/pca_options.html', source_code
    else:
        return None, None
    
def pca_respondents():
    # every respondent
    if os.path.exists("tmp/pca_respondents.html"):
        os.remove("tmp/pca_respondents.html")
    df = pickle.load(open("raw_data_store.dat", "rb"))
    questions = pickle.load(open("data_store.dat", "rb"))

    mc_questions = []
    for q in questions:
        if(q.questionType == 'MULTIPLE_CHOICE'):
           mc_questions.append(q) 
        else:
            del df[q.question]
            
    respondent_choices = {}
    selected_cols_encoded = []
    col_name = []
    for q in mc_questions:
        if(q.questionType == 'MULTIPLE_CHOICE'): 
            encoded = []
            col_options = []
            for d in df[q.question]:
                if(d != d):
                    encoded.append(999)
                    col_options.append(999)
                else:
                    index = q.options.index(d)
                    flattened_option = q.flattened_options[index] + 1
                    encoded.append(flattened_option)
                    col_options.append(d)
            col_name.append(q.question)
            selected_cols_encoded.append(encoded)
            respondent_choices[q.question] = col_options

    dataframe = {}
    for i in range(0, len(selected_cols_encoded)):
        dataframe[col_name[i]] = selected_cols_encoded[i]

    data = pd.DataFrame(dataframe)
    scaled_data = preprocessing.scale(data)
    pca = PCA()
    pca.fit(scaled_data)
    pca_data = pca.transform(scaled_data)
    per_var = np.round(pca.explained_variance_ratio_*100, decimals=1)
    labels = ['PCA'+ str(x) for x in range(1, len(per_var)+1)]

    pca_df = pd.DataFrame(pca_data, index=selected_cols_encoded, columns=labels)
    variance = pca.explained_variance_ratio_.cumsum()[1]

    distortions = []
    K_to_try = range(1, len(col_name))

    for i in K_to_try:
        model = KMeans(
                n_clusters=i,
                init='k-means++',
                random_state=1)
        model.fit(pca_data)
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
    print(k_num)
    #plt.show() - show elbow graph and optimal line

    model = KMeans(
        n_clusters=k_num,
        init='k-means++',
        random_state=1)

    model = model.fit(pca_data)
    y = model.predict(pca_data)
    
    clusters = model.labels_.tolist()
    respondent_choices['cluster'] = clusters
    frame = pd.DataFrame(respondent_choices, index = clusters , columns = list(respondent_choices.keys()))
    
    
    all_profiles = []
    count = 0
    for i in range(k_num):
        cluster_profile = []
        for q in mc_questions:
            grouped_frame = frame.loc[frame['cluster'] == i]
            profile_data = [{
                "question": q.question,
                "common_response": most_frequent(grouped_frame[q.question].values.tolist()),
                "common_response_count": most_frequent_count(grouped_frame[q.question].values.tolist())
            }]
            cluster_profile.append(profile_data)
        count += 1
        cluster_profile.append({"respondents": clusters.count(i)})
        all_profiles.append(cluster_profile)   
    fig = go.Figure()
    for i in range(k_num):
        fig.add_trace(go.Scatter(x=pca_data[y == i, 0], y=pca_data[y == i, 1], mode='markers', 
                                marker=dict(color=px.colors.qualitative.Plotly[i], size=12, line=dict(
                                width=2,
                                color=px.colors.qualitative.Plotly[i])), 
                                name="Profile " + str(i+1)))
    fig.update_layout(title="User Clusters")
    with open('tmp/pca_respondents.html', 'a') as f:
             f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    if os.path.exists("tmp/pca_respondents.html"):
        file = open("tmp/pca_respondents.html", 'r', encoding='utf-8')
        source_code = file.read() 
        return 'tmp/pca_respondents.html', source_code, all_profiles
    else:
        return None, None, None

def treemap():
    if os.path.exists("tmp/treemap.html"):
        os.remove("tmp/treemap.html")
    df = pickle.load(open("raw_data_store.dat", "rb"))
    questions = pickle.load(open("data_store.dat", "rb"))
    for q in questions:
        if(q.dataType != 'QUALITATIVE' or q.questionType != 'MULTIPLE_CHOICE'):
            del df[q.question]
    col_names = df.columns.values.tolist()
    df["count"] = 1
    df = df.groupby(col_names)["count"].count().reset_index()
    df = df.sort_values(by=["count"], ascending=False)
    df["treemap"] = "treemap"
    fig = px.treemap(df, path=col_names, values='count', color ='count', color_continuous_scale='dense')
    with open('tmp/treemap.html', 'a') as f:
        f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    if os.path.exists("tmp/treemap.html"):
        file = open('tmp/treemap.html', 'r', encoding='utf-8')
        source_code = file.read()
        return 'tmp/treemap.html', col_names, source_code
    else:
        return None, None, None

def sunburst():
    if os.path.exists("tmp/sunburst.html"):
        os.remove("tmp/sunburst.html")
    df = pickle.load(open("raw_data_store.dat", "rb"))
    questions = pickle.load(open("data_store.dat", "rb"))
    for q in questions:
        if(q.dataType != 'QUALITATIVE' or q.questionType != 'MULTIPLE_CHOICE'):
            del df[q.question]
    col_names = df.columns.values.tolist()
    df["count"] = 1
    df = df.groupby(col_names)["count"].count().reset_index()
    df = df.sort_values(by=["count"], ascending=False)
    fig = px.sunburst(df, path=col_names, values='count', color ='count', color_continuous_scale='dense')
    # fig.update_layout(uniformtext_minsize=8, uniformtext_mode='show')
    with open('tmp/sunburst.html', 'a') as f:
        f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    if os.path.exists("tmp/sunburst.html"):
        file = open('tmp/sunburst.html', 'r', encoding='utf-8')
        source_code = file.read()
        return 'tmp/sunburst.html', col_names, source_code
    else:
        return None, None, None
    
def most_frequent(profiles): 
    CounterVariable  = Counter(profiles)
    characteristics = [word for word, word_count in CounterVariable.most_common(3)]
    characteristics = ['N/A' if x==999 else x for x in characteristics]
    characteristics = ['0' if x==0 else x for x in characteristics]
    return characteristics

def most_frequent_count(profiles): 
    CounterVariable  = Counter(profiles)
    characteristics = [word_count for word, word_count in CounterVariable.most_common(3)]
    return characteristics
