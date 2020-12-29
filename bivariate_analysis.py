import numpy as np
import pandas as pd
from scipy import stats
from sklearn import preprocessing
import plotly.graph_objects as go
import plotly.express as px
import pickle
import math
import os

def bivar_bargraph(bar_type):
    if(bar_type == 'stack'):
        bar_path = 'tmp/stackedbargraph.html'
    if (bar_type == 'group'):
        bar_path = 'tmp/clusteredbargraph.html'
    if os.path.exists(bar_path):
        os.remove(bar_path)
    df = pickle.load(open("raw_data_store.dat", "rb"))
    questions = pickle.load(open("data_store.dat", "rb"))
    selected_cols = []
    for q in questions:
        if(q.questionType == 'MULTIPLE_CHOICE'):
            selected_cols.append(q)

    # encode cols
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

    for i in range(0, len(selected_cols_encoded)):
        for j in range(0, len(selected_cols_encoded)):
            if (i!=j and i<j):  
                print(selected_cols[i].question)    
                print(selected_cols[j].question)   
        
                # chi squared test
                np_array = np.array([selected_cols_encoded[i], selected_cols_encoded[j]])
                chi_stat, p_val, dof, ex = stats.chi2_contingency(np_array)
                print("p-value: " + str(p_val))

                # cramers v test
                rows = len(selected_cols_encoded[0])-1
                cols = len(selected_cols_encoded)

                smallest_res = 0
                if(rows<cols):
                    smallest_res = rows
                else:
                    smallest_res = cols
                    
                a = sum(selected_cols_encoded[0]) 
                b = sum(selected_cols_encoded[1]) 
                c = a+b

                denominator = c*smallest_res
                cramers_sq = chi_stat/denominator
                cramers_v = math.sqrt(cramers_sq)
                print("cramer's v: " + str(cramers_v))
                
                # clustered bar graph
                x_axis = selected_cols[i].options
                group_by_cols = df.groupby([selected_cols[i].question, selected_cols[j].question])[selected_cols[i].question].count().reset_index(name='frequency')
                group_by_df = pd.DataFrame(group_by_cols)
                
                fig = px.bar(group_by_df, x=selected_cols[i].question, color=selected_cols[j].question, y='frequency',
                            title=selected_cols[i].question + ' ' + selected_cols[j].question,
                            barmode=bar_type,
                            height=600)

                with open(bar_path, 'a') as f:
                    f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    if os.path.exists(bar_path):
        return bar_path

            
            