import pandas as pd
import numpy as np

MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
FREE_TEXT = "FREE_TEXT"
QUANT = "QUANTITATIVE"
QUAL = "QUALITATIVE"

class Question:
    def __init__(self, question, questionType, dataType, options, flattened_options):
      self.question = question
      self.questionType = questionType
      self.dataType = dataType
      self.options = options
      self.flattened_options = flattened_options

def extract_cols(csv):   
    df = pd.read_csv(csv)
    cols = list(df.columns.values)
    total_respondents = df.shape[0]
    index = 0
    questions = [[] for _ in range(len(cols))]
    # getting question types
    # TODO: Remove id - determined by ui/business data layout (tes by adding id col back in) - do in validate()
    for col in cols:
        unique_vals = df.iloc[:,index].dropna().unique()
        options = unique_vals
        unique_val_index = 0
        for unique_val in unique_vals:
            df.iloc[:,index] = np.where(df.iloc[:,index] == unique_val, unique_val_index, df.iloc[:,index])
            unique_val_index += 1
        unique_vals = df.iloc[:,index].dropna().unique()
        if(df.iloc[:,index].dtype == np.int64):
            dataType = QUANT
        else:
            dataType = QUAL
        if(len(unique_vals) > 10):
            questions[index] = Question(col, FREE_TEXT, dataType, options, unique_vals)
        else:
            questions[index] = Question(col, MULTIPLE_CHOICE, dataType, options, unique_vals)
        print(questions[index].questionType)
        print(questions[index].dataType)
        print(questions[index].question)
        print(questions[index].flattened_options)
        index +=1
    return questions
