import numpy as np
from scipy import stats
from sklearn import preprocessing
import plotly.graph_objects as go
import pickle
import math

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
            
            x_axis = selected_cols[i].options
            # fig = go.Figure()
            # fig.add_trace(go.Bar(
            #     x=x_axis,
            #     y=[20, 14, 25, 16, 18, 22, 19, 15, 12, 16, 14, 17],
            #     name='Primary Product',
            #     marker_color='indianred'
            # ))
            
            