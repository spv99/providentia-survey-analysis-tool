import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn import preprocessing
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from sklearn.cluster import KMeans
import plotly.express as px
import random
import pickle
import math
import os

def pca():
    # every qs-option
    if os.path.exists("tmp/pca.html"):
        os.remove("tmp/pca.html")
    df = pickle.load(open("raw_data_store.dat", "rb"))
    questions = pickle.load(open("data_store.dat", "rb"))

    for q in questions:
        # TODO: make free text col mutliple choice
        if(q.questionType == 'MULTIPLE_CHOICE'):
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
                    df = df.rename(columns={val: str(q.question + ': ' + val)})
            
    data = df

    scaled_data = preprocessing.scale(data.T)
    pca = PCA()
    pca.fit(scaled_data)
    pca_data = pca.transform(scaled_data)
    per_var = np.round(pca.explained_variance_ratio_*100, decimals=1)
    labels = ['PCA'+ str(x) for x in range(1, len(per_var)+1)]

    pca_df = pd.DataFrame(pca_data, index=df.columns.values, columns=labels)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=pca_df.PCA1, y=pca_df.PCA2, mode='markers', marker_symbol='diamond', marker=dict(size=10, color='gold'), text=df.columns.values, name="options"))

    # every respondent
    df = pickle.load(open("raw_data_store.dat", "rb"))
    questions = pickle.load(open("data_store.dat", "rb"))

    selected_cols_encoded = []
    col_name = []
    for q in questions:   
        encoded = []
        for d in df[q.question]:
            if(d != d):
                encoded.append(999)
            else:
                index = q.options.index(d)
                flattened_option = q.flattened_options[index] + 1
                encoded.append(flattened_option)
        col_name.append(q.question)
        selected_cols_encoded.append(encoded)
        
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
    print(variance)

    distortions = []
    K_to_try = range(1, len(col_name))

    for i in K_to_try:
        model = KMeans(
                n_clusters=i,
                init='k-means++',
                n_jobs=-1,
                random_state=1)
        model.fit(pca_data)
        distortions.append(model.inertia_)
    plt.plot(K_to_try, distortions, marker='o')
    plt.xlabel('Number of Clusters (k)')
    plt.ylabel('Distortion')
    plt.show()

    # TODO: use silhoutte score instead of elbow 
    # https://gitlab.com/blazetamareborn/StudentSurveyClustering/-/blob/master/training/TrainKMeans.py
    model = KMeans(
        n_clusters=2,
        init='k-means++',
        n_jobs=-1,
        random_state=1)

    model = model.fit(pca_data)
    y = model.predict(pca_data)
    fig.add_trace(go.Scatter(x=pca_data[y == 0, 0], y=pca_data[y == 0, 1], mode='markers', 
                            marker=dict(color='cornflowerblue', size=12, line=dict(width=2,color='cornflowerblue')), 
                            name="Profile 1"))
    fig.add_trace(go.Scatter(x=pca_data[y == 1, 0], y=pca_data[y == 1, 1], mode='markers',
                            marker=dict(color='darkblue', size=12, line=dict(width=2,color='darkblue')), 
                            name="Profile 2"))
    with open('tmp/pca.html', 'a') as f:
        f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    if os.path.exists("tmp/pca.html"):
        return 'tmp/pca.html'

def treemap():
    if os.path.exists("tmp/treemap.html"):
        os.remove("tmp/treemap.html")
    df = pickle.load(open("raw_data_store.dat", "rb"))
    questions = pickle.load(open("data_store.dat", "rb"))
    for q in questions:
        # TODO: make free text col mutliple choice
        if(q.questionType != 'MULTIPLE_CHOICE'):
            del df[q.question]
    col_names = df.columns.values.tolist()
    #TODO: Make sure there is no col named 'count' else rename inserted col to count_x
    df["count"] = 1
    df = df.groupby(col_names)["count"].count().reset_index()
    df = df.sort_values(by=["count"], ascending=False)
    df["treemap"] = "treemap"
    fig = px.treemap(df, path=col_names, values='count', color ='count', color_continuous_scale='dense')
    with open('tmp/treemap.html', 'a') as f:
        f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    if os.path.exists("tmp/treemap.html"):
        return 'tmp/treemap.html'

def sunburst():
    if os.path.exists("tmp/sunburst.html"):
        os.remove("tmp/sunburst.html")
    df = pickle.load(open("raw_data_store.dat", "rb"))
    questions = pickle.load(open("data_store.dat", "rb"))
    for q in questions:
        # TODO: make free text col mutliple choice
        if(q.questionType != 'MULTIPLE_CHOICE'):
            del df[q.question]
    col_names = df.columns.values.tolist()
    #TODO: Make sure there is no col named 'count' else rename inserted col to count_x
    df["count"] = 1
    df = df.groupby(col_names)["count"].count().reset_index()
    df = df.sort_values(by=["count"], ascending=False)
    fig = px.sunburst(df, path=col_names, values='count', color ='count', color_continuous_scale='dense')
    with open('tmp/sunburst.html', 'a') as f:
        f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    if os.path.exists("tmp/sunburst.html"):
        return 'tmp/sunburst.html'