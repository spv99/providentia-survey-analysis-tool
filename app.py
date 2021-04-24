from flask import Flask, make_response, render_template, request, abort, send_file
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
    def get(self):#
        try:
            bargraphHTML, bargraphContent, titles = univariate_analysis.bargraph()
            return {"fileLocation": bargraphHTML, "renderContent": bargraphContent, "titles": titles}
        except KeyError as e:
            abort(500, "Could not retrieve chart", statusCode = "500")
        except Exception as e:
            abort(400, "Could not save information", statusCode = "400")
            
@univar_analysis.route('/piechart')
class Piechart(Resource):
    def get(self):
        try:
            piechartHTML, piechartContent, titles = univariate_analysis.piechart()
            return {"fileLocation": piechartHTML, "renderContent": piechartContent, "titles": titles}  
        except KeyError as e:
            abort(500, "Could not retrieve chart", statusCode = "500")
        except Exception as e:
            abort(400, "Could not save information", statusCode = "400")
            
@univar_analysis.route('/boxplot')
class Boxplot(Resource):
    def get(self):
        try:
            boxplotHTML, boxplotContent, titles = univariate_analysis.boxplot()
            return {"fileLocation": boxplotHTML, "renderContent": boxplotContent, "titles": titles}
        except KeyError as e:
            abort(500, "Could not retrieve chart", statusCode = "500")
        except Exception as e:
            abort(400, "Could not save information", statusCode = "400")
            
@bivar_analysis.route('/bivariate-relationships')
class BivariateRelationships(Resource):
    def get(self):
        try:
            bi_relats = bivariate_analysis.relationshipStrength()
            birelationshipHTML, relationshipContent = bivariate_analysis.visualiseRelationship(bi_relats)
            return {"fileLocation": birelationshipHTML, "renderContent": relationshipContent}
        except KeyError as e:
            abort(500, "Could not retrieve chart", statusCode = "500")
        except Exception as e:
            abort(400, "Could not save information", statusCode = "400")
            
@bivar_analysis.route('/clustered-bargraph')
class ClusteredBargraph(Resource):
    def get(self):
        try:
            clusteredbargraphHTML, stackedContent, titles = bivariate_analysis.bivar_bargraph('group')
            return {"fileLocation": clusteredbargraphHTML, "renderContent": stackedContent, "titles": titles}
        except KeyError as e:
            abort(500, "Could not retrieve chart", statusCode = "500")
        except Exception as e:
            abort(400, "Could not save information", statusCode = "400")
            
@bivar_analysis.route('/stacked-bargraph')
class StackedBargraph(Resource):
    def get(self):
        try:
            stackedbargraphHTML, clusteredContent, titles = bivariate_analysis.bivar_bargraph('stack')
            return {"fileLocation": stackedbargraphHTML, "renderContent": clusteredContent, "titles": titles}
        except KeyError as e:
            abort(500, "Could not retrieve chart", statusCode = "500")
        except Exception as e:
            abort(400, "Could not save information", statusCode = "400")
            
@bivar_analysis.route('/scatter-plot')
class StackedBargraph(Resource):
    def get(self):
        try:
            stackedScatterHTML, scatterContent, titles = bivariate_analysis.scatter_plot()
            return {"fileLocation": stackedScatterHTML, "renderContent": scatterContent, "titles": titles}
        except KeyError as e:
            abort(500, "Could not retrieve chart", statusCode = "500")
        except Exception as e:
            abort(400, "Could not save information", statusCode = "400")
            
@multivar_analysis.route('/treemap')
class Treemap(Resource):
    def get(self):
        try:
            treemapHTML, questions, treemapContent = multivariate_analysis.treemap()
            return {"fileLocation": treemapHTML, "questions": questions, "renderContent": treemapContent}
        except KeyError as e:
            abort(500, "Could not retrieve chart", statusCode = "500")
        except Exception as e:
            abort(400, "Could not save information", statusCode = "400")
            
@multivar_analysis.route('/sunburst')
class Sunburst(Resource):
    def get(self):
        try:
            sunburstHTML, questions, sunburstContent = multivariate_analysis.sunburst()
            return {"fileLocation": sunburstHTML, "questions": questions, "renderContent": sunburstContent}
        except KeyError as e:
            abort(500, "Could not retrieve chart", statusCode = "500")
        except Exception as e:
            abort(400, "Could not save information", statusCode = "400")
            
@multivar_analysis.route('/pca-options')
class PcaOptions(Resource):
    def get(self):
        try:
            pcaHTML, pcaContent = multivariate_analysis.pca_options()
            return {"fileLocation": pcaHTML, "renderContent": pcaContent}
        except KeyError as e:
            abort(500, "Could not retrieve chart", statusCode = "500")
        except Exception as e:
            abort(400, "Could not save information", statusCode = "400")
            
@multivar_analysis.route('/pca-respondents')
class PcaRespondents(Resource):
    def get(self):
        try:
            pcaHTML, pcaContent, cluster_profiles = multivariate_analysis.pca_respondents()
            return {"fileLocation": pcaHTML, "renderContent": pcaContent, "cluster_profiles": cluster_profiles}
        except KeyError as e:
            abort(500, "Could not retrieve chart", statusCode = "500")
        except Exception as e:
            abort(400, "Could not save information", statusCode = "400")
            
@qual_encoding.route('/sentiment-analysis')
class SentimentAnalysis(Resource):
    def get(self):
        try:
            categories = qualitative_encoding.sentiment_tokens()
            return {"categories": categories}
        except KeyError as e:
            abort(500, "Could not retrieve chart", statusCode = "500")
        except Exception as e:
            abort(400, "Could not save information", statusCode = "400")
            
@qual_encoding.route('/sentiment-charts')
class SentimentCharts(Resource):
    def get(self):
        try:
            sentimentHTML, sentimentContent, titles = qualitative_encoding.sentiment_charts()
            categories = qualitative_encoding.sentiment_tokens()
            return {"fileLocation": sentimentHTML, "renderContent": sentimentContent, "categories": categories, "titles": titles}
        except KeyError as e:
            abort(500, "Could not retrieve chart", statusCode = "500")
        except Exception as e:
            abort(400, "Could not save information", statusCode = "400")
            
@qual_encoding.route('/thematic-analysis')
class Themes(Resource):
    def get(self):
        try:
            categories = qualitative_encoding.thematic_analysis()
            return {"categories": categories}
        except KeyError as e:
            abort(500, "Could not retrieve chart", statusCode = "500")
        except Exception as e:
            abort(400, "Could not save information", statusCode = "400")
            
@qual_encoding.route('/themes-charts')
class ThemesCharts(Resource):
    def get(self):
        try:
            themesHTML, themesContent, titles = qualitative_encoding.themes_charts()
            return {"fileLocation": themesHTML, "renderContent": themesContent, "titles": titles}
        except KeyError as e:
            abort(500, "Could not retrieve chart", statusCode = "500")
        except Exception as e:
            abort(400, "Could not save information", statusCode = "400")
            
@qual_encoding.route('/wordmaps')
class Wordmaps(Resource):
    def get(self):
        categories = qualitative_encoding.wordmaps()
        return {"categories": categories}
        # img, title = qualitative_encoding.wordmaps()
        # return send_file(img, mimetype='image/png', attachment_filename='wordmap.png')
    
@qual_encoding.route('/questions')
class FreeTextQuestions(Resource):
    def get(self):
        try:
            questions =  qualitative_encoding.free_text_questions()
            print(questions)
            return {"questions": questions}
        except KeyError as e:
            abort(500, "Could not retrieve chart", statusCode = "500")
        except Exception as e:
            abort(400, "Could not save information", statusCode = "400")
            