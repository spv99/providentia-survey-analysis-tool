import plotly.offline as py
import plotly.graph_objects as go
import pandas as pd

# univariate analysis

df = pd.read_csv("csv/intraday_5min_IBM.csv")
cols = list(df.columns.values)
index = 0
trace_list = [[] for _ in range(len(cols))]

for col in cols:
    options = df.iloc[:,index].dropna().unique()
    col_value_count = df.iloc[:,index].value_counts()
    trace = go.Pie(labels = options, values = col_value_count, title=col_value_count.name)
    trace_list[index] = trace
    index += 1

trace_count = 0
for trace in trace_list:
    data = [trace_list[trace_count]]
    fig = go.Figure(data=data)
    py.plot(fig, filename=str(trace_count) + '-simple-pie-subplot.html')
    trace_count += 1
