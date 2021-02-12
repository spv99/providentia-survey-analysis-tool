import unittest
from io import BytesIO
from unittest.mock import Mock
from app import *
from univariate_analysis import bargraph, piechart, boxplot
from bivariate_analysis import Bivariate_Relationship, relationshipStrength, jsonParseBivarRelationships, bivar_bargraph
from multivariate_analysis import pca, treemap, sunburst
from qualitative_encoding import wordmaps, sentiment_piechart, thematic_analysis
from extract_col import extract_cols, jsonParseCols, Question

class TestMethods(unittest.TestCase):
    
    def setUp(self):
        extract_cols("csv/sample-survey.csv")
    
    def test_post_survey_data(self):
        """
        Test Post Survey Data
        """
        # arrange
        rest = flask_app.test_client()
        result = extract_cols("csv/sample-survey.csv")
        
        # act
        rest_call = rest.post('/api/survey-data/', headers={"Content-Type": "application/json"}, 
                              data={ 'file': (BytesIO(b'my file contents'), 'csv/sample-survey.csv')},
                              content_type='multipart/form-data' )
        
        # assert        
        self.assertEqual(result[0].to_dict(), {'question': 'What is your gender?', 
                                               'questionType': 'MULTIPLE_CHOICE', 
                                               'dataType': 'QUALITATIVE', 
                                               'options': ['Female', 'Male', 'Refused'], 
                                               'flattened_options': [0, 1, 2]})
        
        self.assertEqual(result[1].question, 'What is your race?')
        self.assertEqual(result[1].questionType, 'MULTIPLE_CHOICE')
        self.assertEqual(result[1].dataType, 'QUALITATIVE')
        self.assertEqual(len(result[1].options), 6)
        
        self.assertEqual(result[2].question, 'How do you feel about the area you live in?')
        self.assertEqual(result[2].questionType, 'FREE_TEXT')
        self.assertEqual(result[2].dataType, 'QUALITATIVE')
        self.assertEqual(len(result[2].options), 88)
        
        self.assertEqual(result[3].question, 'What is your level of education?')
        self.assertEqual(result[3].questionType, 'MULTIPLE_CHOICE')
        self.assertEqual(result[3].dataType, 'QUALITATIVE')
        self.assertEqual(len(result[3].options), 6)
        
        self.assertEqual(result[4].question, 'What is your income?')
        self.assertEqual(result[4].questionType, 'MULTIPLE_CHOICE')
        self.assertEqual(result[4].dataType, 'QUALITATIVE')
        self.assertEqual(len(result[4].options), 9)
        
        self.assertEqual(result[5].question, 'How old are you?')
        self.assertEqual(result[5].questionType, 'FREE_TEXT')
        self.assertEqual(result[5].dataType, 'QUANTITATIVE')
        self.assertEqual(len(result[5].options), 34)
        
        self.assertEqual(200, rest_call.status_code)
        self.assertEqual(list, type(rest_call.json['extracted_cols']))
        
    def test_post_survey_data_should_fail_if_no_file_given(self):
        """
        Test Post Survey Data
        """
        # arrange
        rest = flask_app.test_client()
        
        # act
        rest_call = rest.post('/api/survey-data/', headers={"Content-Type": "application/json"})
        
        # assert        
        self.assertEqual(400, rest_call.status_code)
    
    def test_univariate_bargraph(self):
        """
        Test Univariate Bargraph
        """
        # arrange
        rest = flask_app.test_client()
        result = bargraph()
        
        # act
        rest_call = rest.get('/api/univariate-analysis/bargraph', headers={"Content-Type": "application/json"})
        response = Bargraph.get('/api/univariate-analysis/bargraph');
        
        # assert        
        self.assertEqual(result, "tmp/bargraphs.html")
        self.assertEqual(200, rest_call.status_code)
        self.assertEqual(response, {"fileLocation": result})
        
    def test_univariate_piechart(self):
        """
        Test Univariate Piechart
        """
        # arrange
        rest = flask_app.test_client()
        result = piechart()
        
        # act
        rest_call = rest.get('/api/univariate-analysis/piechart', headers={"Content-Type": "application/json"})
        response = Piechart.get('/api/univariate-analysis/piechart');
        
        # assert        
        self.assertEqual(result, "tmp/piecharts.html")
        self.assertEqual(200, rest_call.status_code)
        self.assertEqual(response, {"fileLocation": result})
        
    def test_univariate_boxplot(self):
        """
        Test Univariate Boxplot
        """
        # arrange
        rest = flask_app.test_client()
        result = boxplot()
        
        # act
        rest_call = rest.get('/api/univariate-analysis/boxplot', headers={"Content-Type": "application/json"})
        response = Boxplot.get('/api/univariate-analysis/boxplot');
        
        # assert        
        self.assertEqual(result, "tmp/boxplots.html")
        self.assertEqual(200, rest_call.status_code)
        self.assertEqual(response, {"fileLocation": result})
        
    def test_bivariate_relationships(self):
        """
        Test Bivariate Relationships
        """
        # arrange
        mockRelationship = [Bivariate_Relationship("Question 1?", "Question 2?", 2.1, 0.543)]
        rest = flask_app.test_client()
        relationshipStrength = Mock(return_value = mockRelationship)
        result = jsonParseBivarRelationships(mockRelationship)
        
        # act
        rest_call = rest.get('/api/bivariate-analysis/bivariate-relationships', headers={"Content-Type": "application/json"})
        response = BivariateRelationships.get('/api/bivariate-analysis/bivariate-relationships');
        
        # assert        
        self.assertEqual(result, {'bivariate_relationships': 
                                    [{'cramersv': 0.543,
                                      'pvalue': 2.1,
                                      'question1': 'Question 1?',
                                      'question2': 'Question 2?'}]
                                  })
        self.assertEqual(200, rest_call.status_code)
        self.assertEqual(list, type(rest_call.json['bivariate_relationships']))
        
    def test_bivariate_clustered_bargraph(self):
        """
        Test Bivariate Clustered Bargraph
        """
        # arrange
        rest = flask_app.test_client()
        result = bivar_bargraph('group')
        
        # act
        rest_call = rest.get('/api/bivariate-analysis/clustered-bargraph', headers={"Content-Type": "application/json"})
        response = ClusteredBargraph.get('/api/bivariate-analysis/clustered-bargraph');
        
        # assert        
        self.assertEqual(result, "tmp/clusteredbargraph.html")
        self.assertEqual(200, rest_call.status_code)
        self.assertEqual(response, {"fileLocation": result}) 
    
    def test_bivariate_stacked_bargraph(self):
        """
        Test Bivariate Stacked Bargraph
        """
        # arrange
        rest = flask_app.test_client()
        result = bivar_bargraph('stack')
        
        # act
        rest_call = rest.get('/api/bivariate-analysis/stacked-bargraph', headers={"Content-Type": "application/json"})
        response = StackedBargraph.get('/api/bivariate-analysis/stacked-bargraph');
        
        # assert        
        self.assertEqual(result, "tmp/stackedbargraph.html")
        self.assertEqual(200, rest_call.status_code)
        self.assertEqual(response, {"fileLocation": result}) 
        
    def test_multivariate_treemap(self):
        """
        Test Multivariate Treemap
        """
        # arrange
        rest = flask_app.test_client()
        result = treemap()
        
        # act
        rest_call = rest.get('/api/multivariate-analysis/treemap', headers={"Content-Type": "application/json"})
        response = Treemap.get('/api/multivariate-analysis/treemap');
        
        # assert        
        self.assertIn("tmp/treemap.html", result)
        self.assertEqual(200, rest_call.status_code)
        self.assertEqual(list, type(rest_call.json['questions']))
        self.assertEqual(str, type(rest_call.json['fileLocation']))
        
    def test_multivariate_sunburst(self):
        """
        Test Multivariate Sunburst
        """
        # arrange
        rest = flask_app.test_client()
        result = sunburst()
        
        # act
        rest_call = rest.get('/api/multivariate-analysis/sunburst', headers={"Content-Type": "application/json"})
        response = Sunburst.get('/api/multivariate-analysis/sunburst');
        
        # assert        
        self.assertIn("tmp/sunburst.html", result)
        self.assertEqual(200, rest_call.status_code)
        self.assertEqual(list, type(rest_call.json['questions']))
        self.assertEqual(str, type(rest_call.json['fileLocation']))

    def test_pca(self):
        """
        Test PCA
        """
        # arrange
        rest = flask_app.test_client()
        result = pca()
        
        # act
        rest_call = rest.get('/api/multivariate-analysis/pca', headers={"Content-Type": "application/json"})
        response = Pca.get('/api/multivariate-analysis/pca');
        
        # assert        
        self.assertIn("tmp/pca.html", result)
        self.assertEqual(200, rest_call.status_code)
        self.assertEqual(list, type(rest_call.json['cluster_profiles']))
        self.assertEqual(str, type(rest_call.json['fileLocation']))

    def test_sentiment_piecharts(self):
            """
            Test Sentiment Piechart
            """
            # arrange
            rest = flask_app.test_client()
            result = sentiment_piechart()
            
            # act
            rest_call = rest.get('/api/qualitative-encoding/sentiment', headers={"Content-Type": "application/json"})
            response = Sentiment.get('/api/qualitative-encoding/sentiment');
            
            # assert        
            self.assertIn("tmp/senti_piechart.html", result)
            self.assertEqual(200, rest_call.status_code)
            self.assertEqual(dict, type(rest_call.json['categories']))
            self.assertEqual(str, type(rest_call.json['fileLocation']))
            
    def test_wordmaps(self):
            """
            Test Wordmaps
            """
            # arrange
            rest = flask_app.test_client()
            result = wordmaps()
            
            # act
            rest_call = rest.get('/api/qualitative-encoding/wordmaps', headers={"Content-Type": "application/json"})
            response = Wordmaps.get('/api/qualitative-encoding/wordmaps');
            
            # assert        
            # self.assertIn("tmp/wordmap.html", result) - use when wordmap is one file
            self.assertEqual(200, rest_call.status_code)
            self.assertEqual(list, type(rest_call.json['files']))
            self.assertEqual(list, type(rest_call.json['questions']))
            
    def test_thematic_analysis(self):
            """
            Test Thematic Analysis
            """
            # arrange
            rest = flask_app.test_client()
            result = thematic_analysis()
            
            # act
            rest_call = rest.get('/api/qualitative-encoding/themes', headers={"Content-Type": "application/json"})
            response = Themes.get('/api/qualitative-encoding/themes');
            
            # assert        
            self.assertEqual(200, rest_call.status_code)
            self.assertEqual(dict, type(rest_call.json['themes']))

if __name__ == '__main__':
    unittest.main()