# simple-sentiment-analysis

## steps
1) extract values from csv
2) select qs. to do analysis on
3) run cluster algo on them
4) get basic data from them (bar charts, percentages etc.)
5) determine what open ended qs are / what free text responses are
6) run sentiment analysis on free text
#### 7) make each response a variable and plot pca --> look into pca, plotting, what the graph will show, scree plots 
8) determine euclidian distance to find similar variables


### Running in local:
Local set up: https://timmyreilly.azurewebsites.net/python-pip-virtualenv-installation-on-windows/

### local variables to run flask
set FLASK_APP=app.py
set FLASK_ENV=development

`workon surveys` in directory to start venv
deactivate to exit venv
`py` to run python shell
`flask run` to run swagger
`python extract_col.py extract_cols "csv/grad-pays.csv"` to run specific file with args