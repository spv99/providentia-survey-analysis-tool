import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn import preprocessing
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import random
import pickle
import math
import os

def pca():
    # weight per qs:
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
    print(data.head())
    scaled_data = preprocessing.scale(data.T)
    pca = PCA()
    pca.fit(scaled_data)
    pca_data = pca.transform(scaled_data)


    per_var = np.round(pca.explained_variance_ratio_*100, decimals=1)
    labels = ['PCA'+ str(x) for x in range(1, len(per_var)+1)]

    pca_df = pd.DataFrame(pca_data, index=col_name, columns=labels)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=pca_df.PCA1, y=pca_df.PCA2, mode='markers', text=df.columns.values, name="question"))

    # weight per option:
    for q in questions:
        # TODO: make free text col mutliple choice
        if(q.questionType == 'MULTIPLE_CHOICE'):
            col_names = df[q.question].dropna().unique().tolist()
            df[col_names] = pd.get_dummies(df[q.question])
            del df[q.question]
        else:
            del df[q.question]
    print(df.head())

    data = df

    scaled_data = preprocessing.scale(data.T)
    pca = PCA()
    pca.fit(scaled_data)
    pca_data = pca.transform(scaled_data)

    per_var = np.round(pca.explained_variance_ratio_*100, decimals=1)
    labels = ['PCA'+ str(x) for x in range(1, len(per_var)+1)]

    pca_df = pd.DataFrame(pca_data, index=df.columns.values, columns=labels)

    fig.add_trace(go.Scatter(x=pca_df.PCA1, y=pca_df.PCA2, mode='markers', text=df.columns.values, name="options"))
    fig.show()

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
    print(len(df))
    print(df.head())
    fig = px.treemap(df, path=col_names, values='count', color ='count', color_continuous_scale='PuBu')
    with open('tmp/treemap.html', 'a') as f:
        f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    if os.path.exists("tmp/piecharts.html"):
        return 'tmp/treemap.html'
