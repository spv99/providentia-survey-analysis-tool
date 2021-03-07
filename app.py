from flask import Flask, make_response, render_template, request, abort
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
          threaded=True,
          title="API Providentia", 
          doc='/api/',
          description="Interface to manage results of survey data analysis")

survey_data = app.namespace('api/survey-data', description='Extract data from csv input')
univar_analysis = app.namespace('api/univariate-analysis', description='Univariate analysis on survey data')
bivar_analysis = app.namespace('api/bivariate-analysis', description='Bivariate analysis on survey data')
multivar_analysis = app.namespace('api/multivariate-analysis', description='Multivariate analysis on survey data')
qual_encoding = app.namespace('api/qualitative-encoding', description='Sentiment and thematic analysis on qualititative data')

upload_parser = app.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)

@flask_app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

@survey_data.route('/')
@survey_data.expect(upload_parser)
class Main(Resource):
    def post(self):
        try:
            if upload_parser:
                csv = upload_parser.parse_args()
                uploaded_file = csv['file']
            else:
                uploaded_file = request.files['file']
            extracted_cols = extract_col.extract_cols(uploaded_file)
            jsonParseCols = extract_col.jsonParseCols(extracted_cols)
            return jsonParseCols
        except:
            abort(400, 'ERROR: Please upload a file')
    
@univar_analysis.route('/bargraph')
class Bargraph(Resource):
    def get(self):
        bargraphHTML, bargraphContent = univariate_analysis.bargraph()
        return {"fileLocation": bargraphHTML, "renderContent": bargraphContent}
      
@univar_analysis.route('/piechart')
class Piechart(Resource):
    def get(self):
        piechartHTML, piechartContent = univariate_analysis.piechart()
        return {"fileLocation": piechartHTML, "renderContent": piechartContent}  

@univar_analysis.route('/boxplot')
class Boxplot(Resource):
    def get(self):
        boxplotHTML, boxplotContent = univariate_analysis.boxplot()
        return {"fileLocation": boxplotHTML, "renderContent": boxplotContent}
    
@bivar_analysis.route('/bivariate-relationships')
class BivariateRelationships(Resource):
    def get(self):
        bi_relats = bivariate_analysis.relationshipStrength()
        json_bi_relats = bivariate_analysis.jsonParseBivarRelationships(bi_relats)
        return json_bi_relats
    
@bivar_analysis.route('/clustered-bargraph')
class ClusteredBargraph(Resource):
    def get(self):
        clusteredbargraphHTML, stackedContent = bivariate_analysis.bivar_bargraph('group')
        return {"fileLocation": clusteredbargraphHTML, "renderContent": stackedContent}
    
@bivar_analysis.route('/stacked-bargraph')
class StackedBargraph(Resource):
    def get(self):
        stackedbargraphHTML, clusteredContent = bivariate_analysis.bivar_bargraph('stack')
        return {"fileLocation": stackedbargraphHTML, "renderContent": clusteredContent}
    
@bivar_analysis.route('/scatter-plot')
class StackedBargraph(Resource):
    def get(self):
        stackedScatterHTML, scatterContent = bivariate_analysis.scatter_plot()
        return {"fileLocation": stackedScatterHTML, "renderContent": scatterContent}
    
@multivar_analysis.route('/treemap')
class Treemap(Resource):
    def get(self):
        treemapHTML, questions, treemapContent = multivariate_analysis.treemap()
        return {"fileLocation": treemapHTML, "questions": questions, "renderContent": treemapContent}

@multivar_analysis.route('/sunburst')
class Sunburst(Resource):
    def get(self):
        sunburstHTML, questions, sunburstContent = multivariate_analysis.sunburst()
        return {"fileLocation": sunburstHTML, "questions": questions, "renderContent": sunburstContent}
    
@multivar_analysis.route('/pca')
class Pca(Resource):
    def get(self):
        pcaHTML, cluster_profiles,wordmap_files = multivariate_analysis.pca()
        return {"fileLocation": pcaHTML, "cluster_profiles": cluster_profiles, "wordmap_files": wordmap_files}
    
@qual_encoding.route('/sentiment-piechart')
class SentimentPiechart(Resource):
    def get(self):
        sentimentHTML, sentimentContent = qualitative_encoding.sentiment_piechart()
        return {"fileLocation": sentimentHTML, "renderContent": sentimentContent}
    
@qual_encoding.route('/sentiment-barchart')
class SentimentBargraph(Resource):
    def get(self):
        sentimentHTML, sentimentContent = qualitative_encoding.sentiment_bargraph()
        return {"fileLocation": sentimentHTML, "renderContent": sentimentContent}
    
@qual_encoding.route('/sentiment-analysis')
class SentimentAnalysis(Resource):
    def get(self):
        categories = qualitative_encoding.sentiment_tokens()
        return {"categories": categories}
    
@qual_encoding.route('/wordmaps')
class Wordmaps(Resource):
    def get(self):
        files, questions = qualitative_encoding.wordmaps()
        return {"files": files, "questions": questions}
    
@qual_encoding.route('/themes')
class Themes(Resource):
    def get(self):
        categories = qualitative_encoding.thematic_analysis()
        return {"categories": categories}
    
@qual_encoding.route('/themes-bargraph')
class ThemesBargraph(Resource):
    def get(self):
        themesHTML, themesContent = qualitative_encoding.themes_bargraph()
        return {"fileLocation": themesHTML, "renderContent": themesContent}
    
@qual_encoding.route('/themes-piechart')
class ThemesBargraph(Resource):
    def get(self):
        themesHTML, themesContent = qualitative_encoding.themes_piechart()
        return {"fileLocation": themesHTML, "renderContent": themesContent}
    