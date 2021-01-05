from flask import Flask, make_response, render_template
from flask_restplus import Api, Resource
from werkzeug.datastructures import FileStorage
import pickle

import extract_col
import univariate_analysis
import bivariate_analysis
import multivariate_analysis
import qualitative_encoding

flask_app = Flask(__name__)
app = Api(app = flask_app, 
          version="1.0", 
          title="Providentia", 
          description="Interface to manage results of survey data analysis")

survey_data = app.namespace('survey-data', description='Extract data from csv input')
univar_analysis = app.namespace('univariate-analysis', description='Univariate analysis on survey data')
bivar_analysis = app.namespace('bivariate-analysis', description='Bivariate analysis on survey data')
multivar_analysis = app.namespace('multivariate-analysis', description='Multivariate analysis on survey data')
qual_encoding = app.namespace('qualitative-encoding', description='Sentiment and thematic analysis on qualititative data')

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

@univar_analysis.route('/boxplots')
class UnivariateAnalysis(Resource):
    def get(self):
        boxplotHTML = univariate_analysis.boxplot()
        return {"fileLocation": boxplotHTML}
    
@bivar_analysis.route('/bivariate-relationships')
class UnivariateAnalysis(Resource):
    def get(self):
        bi_relats = bivariate_analysis.relationshipStrength()
        json_bi_relats = bivariate_analysis.jsonParseBivarRelationships(bi_relats)
        return json_bi_relats
    
@bivar_analysis.route('/clustered-bargraph')
class UnivariateAnalysis(Resource):
    def get(self):
        clusteredbargraphHTML = bivariate_analysis.bivar_bargraph('group')
        return {"fileLocation": clusteredbargraphHTML}
    
@bivar_analysis.route('/stacked-bargraph')
class UnivariateAnalysis(Resource):
    def get(self):
        stackedbargraphHTML = bivariate_analysis.bivar_bargraph('stack')
        return {"fileLocation": stackedbargraphHTML}
    
@multivar_analysis.route('/treemap')
class MultivariateAnalysis(Resource):
    def get(self):
        treemapHTML = multivariate_analysis.treemap()
        return {"fileLocation": treemapHTML}

@multivar_analysis.route('/sunburst')
class MultivariateAnalysis(Resource):
    def get(self):
        sunburstHTML = multivariate_analysis.sunburst()
        return {"fileLocation": sunburstHTML}
    
@qual_encoding.route('/sentiment')
class QualitiativeEncoding(Resource):
    def get(self):
        return qualitative_encoding.sentiment_analysis();
    
@qual_encoding.route('/wordmaps')
class QualitiativeEncoding(Resource):
    def get(self):
        return qualitative_encoding.wordmaps();