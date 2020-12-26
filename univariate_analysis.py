import plotly.graph_objects as go
import pandas as pd
import pickle

def bargraph():
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
        with open('tmp/bargraphs.html', 'a') as f:
             f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    return 'tmp/bargraphs.html'
        
def piechart():
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
        with open('tmp/piecharts.html', 'a') as f:
            f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    return 'tmp/piecharts.html'

# to run this file directly with args
if __name__ == '__main__':
    import sys
    function = getattr(sys.modules[__name__], sys.argv[1])
    filename = sys.argv[2]
    function(filename)