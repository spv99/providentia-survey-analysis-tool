import numpy as np
import pandas as pd
from scipy import stats
import plotly.express as px
import pickle
import math
import os

class Bivariate_Relationship:
    def __init__(self, question1, question2, pvalue, cramersv):
      self.question1 = question1
      self.question2 = question2
      self.pvalue = pvalue
      self.cramersv = cramersv
      
    def to_dict(self):
        return {"question1": self.question1, 
                "question2": self.question2, 
                "pvalue": self.pvalue, 
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
    for i in range(0, len(selected_cols_encoded)):
        for j in range(0, len(selected_cols_encoded)):
            if (i!=j and i<j):  
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

                bi = Bivariate_Relationship(selected_cols[i].question, selected_cols[j].question, p_val, cramers_v)
                bi_relats.append(bi)
    return bi_relats

def jsonParseBivarRelationships(bi_relats):
    bi_relats.sort(key=byCramers)
    bi_relats_parsed = []
    for b in bi_relats:
        data = b.to_dict()
        bi_relats_parsed.append(data)
    return({"bivariate_relationships": bi_relats_parsed})

# sort by cramer's v ascending
def byCramers(elem):
    return elem.cramersv