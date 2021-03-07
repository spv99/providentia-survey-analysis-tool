import pandas as pd
import numpy as np
import json
import pickle

MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
FREE_TEXT = "FREE_TEXT"
QUANT = "QUANTITATIVE"
QUAL = "QUALITATIVE"

class Question:
    def __init__(self, question, questionType, dataType, options, flattened_options):
      self.question = question
      self.questionType = questionType
      self.dataType = dataType
      self.options = options.tolist()
      self.flattened_options = flattened_options.tolist()
      
    def to_dict(self):
        return {"question": self.question, 
                "questionType": self.questionType, 
                "dataType": self.dataType, 
                "options": self.options, 
                "flattened_options": self.flattened_options}

def extract_cols(csv):  
    df = pd.read_csv(csv, encoding= 'unicode_escape')
    with open('raw_data_store.dat', 'wb') as f:
        pickle.dump(df, f) 
    cols = list(df.columns.values)
    total_respondents = df.shape[0]
    index = 0
    questions = [[] for _ in range(len(cols))]
    for col in cols:
        unique_vals = df.iloc[:,index].dropna().unique()
        options = unique_vals
        unique_val_index = 0
        for unique_val in unique_vals:
            df.iloc[:,index] = np.where(df.iloc[:,index] == unique_val, unique_val_index, df.iloc[:,index])
            unique_val_index += 1
        unique_vals = df.iloc[:,index].dropna().unique()
        if(df.iloc[:,index].dtype == np.int64 or df.iloc[:,index].dtype == np.float64):
            dataType = QUANT
        else:
            dataType = QUAL
        if(len(unique_vals) > 10):
            questions[index] = Question(col, FREE_TEXT, dataType, options, unique_vals)
        else:
            questions[index] = Question(col, MULTIPLE_CHOICE, dataType, options, unique_vals)
        index +=1
    index = 0
    for q in questions:
        if (q.question.lower() == 'id' or q.question.lower() == 'kerberos'):
            questions.remove(questions[index])
        index += 1
    with open('data_store.dat', 'wb') as f:
        pickle.dump(questions, f)
    return questions

def jsonParseCols(questions):
    extracted_cols = []
    for q in questions:
        data = q.to_dict()
        extracted_cols.append(data)
    return({"extracted_cols": extracted_cols})