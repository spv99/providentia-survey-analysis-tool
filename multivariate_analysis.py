import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn import preprocessing
import matplotlib.pyplot as plt
import pickle
import math
import os

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
data = data.T
print(data.head())

scaled_data = preprocessing.scale(data.T)
pca = PCA()
pca.fit(scaled_data)
pca_data = pca.transform(scaled_data)

print(pca_data)

per_var = np.round(pca.explained_variance_ratio_*100, decimals=1)
labels = ['PCA'+ str(x) for x in range(1, len(per_var)+1)]

pca_df = pd.DataFrame(pca_data, index=selected_cols_encoded[2], columns=labels)
print(pca_df.head())

plt.scatter(pca_df.PCA1, pca_df.PCA2, c=selected_cols_encoded[2])
plt.title('PCA Graph')
plt.xlabel('PCA1 - {0}%'.format(per_var[0]))
plt.ylabel('PCA2 - {0}%'.format(per_var[1]))

print(pca_df.index)
print(len(labels))

# for sample in pca_df.index:
#     plt.annotate(sample, (pca_df.PCA1.loc[sample].tolist()[0], pca_df.PCA2.loc[sample].tolist()[0]))
    
plt.show()
