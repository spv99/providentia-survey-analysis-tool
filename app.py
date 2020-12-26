from flask import Flask, make_response, render_template
from flask_restplus import Api, Resource
from werkzeug.datastructures import FileStorage
import pickle

import extract_col
import univariate_analysis

flask_app = Flask(__name__)
app = Api(app = flask_app, 
          version="1.0", 
          title="Providentia", 
          description="Interface to manage results of survey data analysis")

survey_data = app.namespace('survey-data', description='Extract data from csv input')
univar_analysis = app.namespace('univar-analysis', description='Univariate analysis on survey data')

upload_parser = app.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)

@survey_data.route('/')
@survey_data.expect(upload_parser)
class Main(Resource):
    def post(self):
        csv = upload_parser.parse_args()
        uploaded_file = csv['file']
        extracted_cols = extract_col.extract_cols(uploaded_file)
        jsonParseCols = extract_col.jsonParseCols(extracted_cols)
        return jsonParseCols
    
@univar_analysis.route('/bargraph')
class UnivariateAnalysis(Resource):
    def get(self):
        bargraphHTML = univariate_analysis.bargraph()
        return {"fileLocation": bargraphHTML}
      
@univar_analysis.route('/piechart')
class UnivariateAnalysis(Resource):
    def get(self):
        piechartHTML = univariate_analysis.piechart()
        return {"fileLocation": piechartHTML}  
