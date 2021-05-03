# simple-sentiment-analysis

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