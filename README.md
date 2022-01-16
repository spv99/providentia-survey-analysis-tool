# providential-survey-analysis-tool

### About

Final year dissertation project that automates the analysis of surveys, using both quantiative and qualitative analysis tools.
On the upload of survey results, this tool will automatically generate the below interactive graphs and features:

  - Bargraphs	
  - Pie Charts
  - Box Plots
  - Sentiment Analaysis
  - Thematic Analysis
  - Bivariate Relationships (Correlations)
  - Clustered Bar Graphs
  - Stacked Bar Graphs
  - Scatter Plots
  - Sunburst Chart
  - Treemap Chart
  - User Profiles (Principle Component Analysis)

(WIP) Preview: 

![providentia](https://user-images.githubusercontent.com/39187328/149662007-01ee0308-c315-4d53-96eb-83a5f896c737.gif)


### Running in local:
Local set up of Python: https://timmyreilly.azurewebsites.net/python-pip-virtualenv-installation-on-windows/

Local set up of Angular: https://angular.io/guide/setup-local

### Running flask backend:
Within your your virtual environment:
`pip install -r requirements.txt` (on running the application for the first time to load libraries)
`set FLASK_APP=app.py`
`set FLASK_ENV=development`
`flask run`
You will be able to see the Swagger Definition at http://127.0.0.1:5000/api/

### Running UI:
`cd ui`
`npm i` (on running the application for the first time to generate node_modules)
`ng serve`
You will be able to see the interface at http://localhost:4200/providentia

### Running Backend Tests:
`python -m unittest -v test.py`

### Running Frontend Tests:
`ng test`
