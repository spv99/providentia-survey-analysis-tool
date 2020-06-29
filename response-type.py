import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn import preprocessing
import matplotlib.pyplot as plt
import plotly.offline as py
import plotly.graph_objects as go
import math

class Question:
    def __init__(self, questionType, options):
      self.questionType = questionType
      self.options = options


MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
FREE_TEXT = "FREE_TEXT"
df = pd.read_csv("new-york-simplified.csv")
cols = list(df.columns.values)
total_respondents = df.shape[0]-1
index = 0
questions = [[] for _ in range(len(cols))]

# getting question types
for col in cols:
    options = df.iloc[:,index].dropna().unique()
    col_value = df.iloc[:,index].value_counts()
    # if 90% or more of respondents answers are different then assume it is free text based answer 
    # (note: same would be if they all answered "no" which would mean options = 1)
    if((total_respondents*0.90) <= len(options)):
        questions[index] = Question(FREE_TEXT, options)
    else:
        option_index = 0
        for option in options:
            df.iloc[:,index] = np.where(df.iloc[:,index] == option, option_index, df.iloc[:,index])
            option_index += 1
        options = df.iloc[:,index].dropna().unique()
        questions[index] = Question(MULTIPLE_CHOICE, options)
    index +=1

# PCA Execution 
# - note: group qs with same words in them and show correlation

# expects points to be in rows not cols, so transposing
# centering and scaling the data so that the means for each row = 0 and standard deviation = 1
df = df.dropna()
scaled_data = preprocessing.scale(df.T) 
pca = PCA()
# generates coordinates for a PCA graph based on loading scores and scaled data
pca.fit(scaled_data)
pca_data = pca.transform(scaled_data)

# Scree Plots
# calculating % of variation that each principle component accounts for 
per_var = np.round(pca.explained_variance_ratio_* 100, decimals=1)
labels = ['PC' + str(x) for x in range(1, len(per_var)+1)]
plt.bar(x=range(1, len(per_var)+1), height=per_var, tick_label=labels)
plt.ylabel('% of Explained Variance')
plt.xlabel('Principle Component')
plt.title('Scree Plot')
plt.show()


# PCA Clusters
pca_df = pd.DataFrame(pca_data, index=cols, columns = labels)

plt.scatter(pca_df.PC1, pca_df.PC2)
plt.title('My PCA Graph')
plt.xlabel('PC1 - {0}%'.format(per_var[0]))
plt.ylabel('PC2 - {0}%'.format(per_var[1])) # TODO: only use if pc1 scree plot > 70%
plt.show()

# Find closest point to each point on scatter
# index_point = 0
# smallest = 1000
# coordinates = [[] for _ in range(len(pca_df.index))]
# for point in pca_df.index:
#     plt.annotate(point, (pca_df.PC1.loc[point], pca_df.PC2.loc[point]))
#     coordinates[index_point] = [point, str(pca_df.PC1.loc[point]), str(pca_df.PC2.loc[point]), smallest]
#     index_point+=1

# index_co = 0
# for co in coordinates:
#     for _ in coordinates:
#         dist = math.sqrt((float(co[1]) - float(co[2]))**2 + (float(coordinates[index_co][1]) - float(coordinates[index_co][2]))**2)
#         print(dist)
#         if((dist != 0) & (dist < smallest)):
#             smallest = dist
#             co[3] = coordinates[index_co][0]
#         index_co +=1

# print(coordinates)



# mapping two cols
# row = 0
# label_1 = 0
# label_2 = 0
# label_3 = 0
# label_4 = 0
# for _ in (df.iloc[:,13]):
#     if ((df.iloc[row,13] == 0) & (df.iloc[row,14] == 0)):
#         label_1 +=1
#     if((df.iloc[row,13] == 0) & (df.iloc[row,14] == 1)):
#         label_2 +=1
#     if((df.iloc[row,13] == 1) & (df.iloc[row,14] == 0)):
#         label_3 +=1
#     if((df.iloc[row,13] == 1) & (df.iloc[row,14] == 1)):
#         label_4 +=1
#     row+=1


# trace0 = go.Pie(labels=["0 & 0", "0 & 1", "1 & 0", "1 & 1"], values = [(label_1), (label_2), (label_3), (label_4)] , title="test")
# data = [trace0]
# fig = go.Figure(data = data)
# py.plot(fig, 'init-scatter.html')

