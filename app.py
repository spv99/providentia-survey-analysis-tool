from flask import Flask
from flask_restplus import Api, Resource
from werkzeug.datastructures import FileStorage
import json
import extract_col

flask_app = Flask(__name__)
app = Api(app = flask_app, 
          version="1.0", 
          title="Providentia", 
          description="Interface to manage results of survey data analysis")

survey_data = app.namespace('survey_data', description='Extract survey analysis from csv input')

upload_parser = app.parser()
upload_parser.add_argument('file', location='files',
                       type=FileStorage, required=True)

@survey_data.route('/')
@survey_data.expect(upload_parser)
class Main(Resource):
    def post(self):
        csv = upload_parser.parse_args()
        uploaded_file = csv['file']
        extracted_cols = extract_col.extract_cols(uploaded_file)
        
        # jsonParseCols = json.dumps([ec.__dict__ for ec in extracted_cols.tolist()])
        # print(jsonParseCols)
        
        # data = pd.read_csv(uploaded_file)
        # print(data.head)
        
        return json.dumps([ec.__dict__ for ec in extracted_cols])
