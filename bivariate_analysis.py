import numpy as np
import pandas as pd
from scipy import stats
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter, OrderedDict
import pickle
import math
import os

class Bivariate_Relationship:
    def __init__(self, question1, question2, cramersv):
      self.question1 = question1
      self.question2 = question2
      self.cramersv = cramersv
      
    def to_dict(self):
        return {"question1": self.question1, 
                "question2": self.question2, 
                "cramersv": self.cramersv}
        
def encode_cols():
    df = pickle.load(open("raw_data_store.dat", "rb"))
    questions = pickle.load(open("data_store.dat", "rb"))
    selected_cols = []
    for q in questions:
        if(q.questionType == 'MULTIPLE_CHOICE'):
            selected_cols.append(q)

    selected_cols_encoded = []
    for sc in selected_cols:   
        encoded = []
        for d in df[sc.question]:
            if(d != d):
                encoded.append(999)
            else:
                index = sc.options.index(d)
                flattened_option = sc.flattened_options[index] + 1
                encoded.append(flattened_option)
        selected_cols_encoded.append(encoded)
    return df, selected_cols, selected_cols_encoded

def bivar_bargraph(bar_type):
    if(bar_type == 'stack'):
        bar_path = 'tmp/stackedbargraph.html'
    if (bar_type == 'group'):
        bar_path = 'tmp/clusteredbargraph.html'
    if os.path.exists(bar_path):
        os.remove(bar_path)
        
    df, selected_cols, selected_cols_encoded = encode_cols()
    df = df.astype(str)
    df = df.replace(to_replace = "\.0+$",value = "", regex = True)
    df = df.replace(to_replace = "nan",value = "N/A", regex = False)
    for i in range(0, len(selected_cols_encoded)):
        for j in range(0, len(selected_cols_encoded)):
            if (i!=j and i<j):              
                group_by_cols = df.groupby([selected_cols[i].question, selected_cols[j].question])[selected_cols[i].question].count().reset_index(name='frequency')
                group_by_df = pd.DataFrame(group_by_cols)
                
                fig = px.bar(group_by_df, x=selected_cols[i].question, color=selected_cols[j].question, y='frequency',
                            title=selected_cols[i].question + ' ' + selected_cols[j].question,
                            barmode=bar_type,
                            height=600)

                with open(bar_path, 'a') as f:
                    f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    if os.path.exists(bar_path):
        file = open(bar_path, 'r', encoding='utf-8')
        source_code = file.read()
        return bar_path, source_code
    else:
        return None, None

            
def relationshipStrength():
    df, selected_cols, selected_cols_encoded = encode_cols()
    bi_relats = []
    for i in range(0, len(selected_cols_encoded)):
        for j in range(0, len(selected_cols_encoded)):
            if (i!=j and i<j): 
                 
                # chi squared test
                np_array = np.array([selected_cols_encoded[i], selected_cols_encoded[j]])
                chi_stat, p_val, dof, ex = stats.chi2_contingency(np_array)
                
                # cramers v test
                n = np.sum(np_array)
                minDim = min(np_array.shape)-1
                cramers_v = np.sqrt((chi_stat/n) / minDim)

                bi = Bivariate_Relationship(selected_cols[i].question, selected_cols[j].question, cramers_v)
                bi_relats.append(bi)
    return bi_relats

def visualiseRelationship(bi_relats):
    if os.path.exists("tmp/bivariate-relationships.html"):
        os.remove("tmp/bivariate-relationships.html")
    cramersv=[]
    questions=[]
    for b in bi_relats:
        cramersv.append(b.cramersv)
        questions.append(b.question1 + " and " + b.question2 + "\n")
    xaxis = [1 for _ in range(len(cramersv))]
    cramersv.sort(reverse=True)
    right_pos_cv = [cramersv[i] for i in range(0, len(cramersv), 2)]
    right_pos_qs = [questions[i] for i in range(0, len(questions), 2)]
    left_pos_cv = [cramersv[i] for i in range(1, len(cramersv), 2)]
    left_pos_qs = [questions[i] for i in range(1, len(questions), 2)]
    right_trace=go.Scatter(
        x=xaxis,
        y=right_pos_cv,
        mode='markers+text',
        marker_color=right_pos_cv,
        marker_colorscale=px.colors.sequential.dense,
        text=right_pos_qs,
        textposition="middle right",
        marker=dict(
            line=dict(width=1, color='DodgerBlue'), size=25,
        ),
        hoverinfo="text+y"
    )
    left_trace=go.Scatter(
        x=xaxis,
        y=left_pos_cv,
        mode='markers+text',
        marker_color=left_pos_cv,
        marker_colorscale=px.colors.sequential.dense,
        text=left_pos_qs,
        textposition="middle left",
        marker=dict(
            line=dict(width=1, color='DodgerBlue'), size=25,
        ),
        hoverinfo="text+y"
    )

    layout = dict(xaxis=dict(visible=False), showlegend=False)
    fig = go.Figure([right_trace, left_trace], layout)
    with open('tmp/bivariate-relationships.html', 'a') as f:
        f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    if os.path.exists("tmp/bivariate-relationships.html"):
        file = open("tmp/bivariate-relationships.html", 'r', encoding='utf-8')
        source_code = file.read()
        return 'tmp/bivariate-relationships.html', source_code
    else:
        return None, None

def scatter_plot():
    if os.path.exists("tmp/scatterplots.html"):
        os.remove("tmp/scatterplots.html")
    df = pickle.load(open("raw_data_store.dat", "rb"))
    questions = pickle.load(open("data_store.dat", "rb"))
    selected_cols = []
    for q in questions:
        if(q.dataType == 'QUANTITATIVE'):
            selected_cols.append(q)
            
    for i in range(0, len(selected_cols)):
        for j in range(0, len(selected_cols)):
            if (i!=j and i<j):   
                joined_cols = []
                for k in range(0, len(df[selected_cols[i].question].dropna().tolist())):
                    a = df[selected_cols[i].question].dropna().tolist()[k] 
                    b = df[selected_cols[j].question].dropna().tolist()[k] 
                    c = str(a) + '&' + str(b)
                    joined_cols.append(c)
                count = Counter(joined_cols)
                sizes = [0] * len(joined_cols)
                for value in count: 
                    for m in range(0, len(joined_cols)):
                        a, b = joined_cols[m].split('&')
                        if a in value and b in value:
                            sizes[m] = count[value]
                normalised_sizes = []
                for size in sizes:
                    normalised_sizes.append((size-min(sizes))/(max(sizes)-min(sizes)) * (80 - 20) + 20)
                update_layout = go.Layout({"showlegend": False})
                fig = go.Figure(layout= update_layout)
                fig.add_trace(go.Scatter(
                    x=df[selected_cols[i].question].dropna().tolist(),
                    y=df[selected_cols[j].question].dropna().tolist(),
                    mode='markers',
                    text=["count:" + str(size) for size in sizes],
                    marker=dict(size=normalised_sizes, sizemode = 'diameter',
                                line=dict(width=1, color='DarkSlateGrey'),
                                color=normalised_sizes, colorscale= "dense", showscale=False)
                ))
                trendline_fig = px.scatter(x=df[selected_cols[i].question].dropna().tolist(), y=df[selected_cols[j].question].dropna().tolist(), trendline="ols")
                trendline = trendline_fig.data[1]
                fig.add_trace(trendline)
                fig.update_layout(plot_bgcolor='#fafafa', title=selected_cols[i].question + ' ' + selected_cols[j].question)
                with open('tmp/scatterplots.html', 'a') as f:
                    f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    if os.path.exists("tmp/scatterplots.html"):
        file = open("tmp/scatterplots.html", 'r', encoding='utf-8')
        source_code = file.read()
        return 'tmp/scatterplots.html', source_code
    else:
        return None, None