import plotly.graph_objects as go
import pickle
import os

def bargraph():
    if os.path.exists("tmp/bargraphs.html"):
        os.remove("tmp/bargraphs.html")
    df = pickle.load(open("raw_data_store.dat", "rb"))
    questions = pickle.load(open("data_store.dat", "rb"))
    selected_cols = []
    for q in questions:
        if(q.questionType == 'MULTIPLE_CHOICE'):
            selected_cols.append(q)
    for sc in selected_cols:
        options = df[sc.question].dropna().unique()
        value_counts = df[sc.question].value_counts()
        fig = go.Figure([go.Bar(x=options, y=value_counts)])
        fig.update_layout(title=sc.question)
        with open('tmp/bargraphs.html', 'a') as f:
             f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    if os.path.exists("tmp/bargraphs.html"):
        return 'tmp/bargraphs.html'
        
def piechart():
    if os.path.exists("tmp/piecharts.html"):
        os.remove("tmp/piecharts.html")
    df = pickle.load(open("raw_data_store.dat", "rb"))
    questions = pickle.load(open("data_store.dat", "rb"))
    selected_cols = []
    for q in questions:
        if(q.questionType == 'MULTIPLE_CHOICE'):
            selected_cols.append(q)
    for sc in selected_cols:
        options = df[sc.question].dropna().unique()
        value_counts = df[sc.question].value_counts()
        fig = go.Figure([go.Pie(labels=options, values=value_counts)])
        fig.update_layout(title=sc.question)
        with open('tmp/piecharts.html', 'a') as f:
            f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    if os.path.exists("tmp/piecharts.html"):
        return 'tmp/piecharts.html'

def boxplot():
    if os.path.exists("tmp/boxplots.html"):
        os.remove("tmp/boxplots.html")
    df = pickle.load(open("raw_data_store.dat", "rb"))
    questions = pickle.load(open("data_store.dat", "rb"))
    selected_cols = []
    for q in questions:
        if(q.dataType == "QUANTITATIVE"):
            selected_cols.append(q)
    for sc in selected_cols:
        options = df[sc.question].dropna().unique()
        value_counts = df[sc.question].value_counts()
        fig = go.Figure([go.Box(quartilemethod="inclusive", y=value_counts, boxpoints='all', name=sc.question)])
        fig.update_layout(title=sc.question)
        with open('tmp/boxplots.html', 'a') as f:
            f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    if os.path.exists("tmp/boxplots.html"):
        return 'tmp/boxplots.html'