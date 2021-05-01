import unittest
from io import BytesIO
from unittest.mock import Mock
from app import *
from univariate_analysis import bargraph, piechart, boxplot
from bivariate_analysis import Bivariate_Relationship, relationshipStrength, visualiseRelationship, bivar_bargraph, scatter_plot
from multivariate_analysis import pca_respondents, treemap, sunburst
from qualitative_encoding import wordmaps, sentiment_charts, themes_charts, sentiment_tokens
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
        self.assertEqual(len(result[1].options), 5)
        
        self.assertEqual(result[2].question, 'How do you feel about the area you live in?')
        self.assertEqual(result[2].questionType, 'FREE_TEXT')
        self.assertEqual(result[2].dataType, 'QUALITATIVE')
        self.assertEqual(len(result[2].options), 88)
        
        self.assertEqual(result[3].question, 'What is your level of education?')
        self.assertEqual(result[3].questionType, 'MULTIPLE_CHOICE')
        self.assertEqual(result[3].dataType, 'QUALITATIVE')
        self.assertEqual(len(result[3].options), 5)
        
        self.assertEqual(result[4].question, 'What is your income?')
        self.assertEqual(result[4].questionType, 'MULTIPLE_CHOICE')
        self.assertEqual(result[4].dataType, 'QUALITATIVE')
        self.assertEqual(len(result[4].options), 8)
        
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
        bargraphHTML, bargraphContent, titles = bargraph()
        
        # act
        rest_call = rest.get('/api/univariate-analysis/bargraph', headers={"Content-Type": "application/json"})
        response = Bargraph.get('/api/univariate-analysis/bargraph');
        
        # assert        
        self.assertEqual(bargraphHTML, "tmp/bargraphs.html")
        self.assertEqual(titles, ['What is your gender?',
                                  'What is your race?', 
                                  'What is your level of education?', 
                                  'What is your income?', 
                                  'How old are you?',
                                  'How many kids do you have?'])
        self.assertEqual(200, rest_call.status_code)
        
    def test_univariate_piechart(self):
        """
        Test Univariate Piechart
        """
        # arrange
        rest = flask_app.test_client()
        pieChartHTML, pieChartContent, titles = piechart()
        
        # act
        rest_call = rest.get('/api/univariate-analysis/piechart', headers={"Content-Type": "application/json"})
        response = Piechart.get('/api/univariate-analysis/piechart');
        
        # assert        
        self.assertEqual(pieChartHTML, "tmp/piecharts.html")
        self.assertEqual(titles, ['What is your gender?',
                                  'What is your race?', 
                                  'What is your level of education?', 
                                  'What is your income?', 
                                  'How old are you?',
                                  'How many kids do you have?'])
        self.assertEqual(200, rest_call.status_code)
        
    def test_univariate_boxplot(self):
        """
        Test Univariate Boxplot
        """
        # arrange
        rest = flask_app.test_client()
        boxplotHTML, boxplotContent, titles = boxplot()
        
        # act
        rest_call = rest.get('/api/univariate-analysis/boxplot', headers={"Content-Type": "application/json"})
        response = Boxplot.get('/api/univariate-analysis/boxplot');
        
        # assert        
        self.assertEqual(boxplotHTML, "tmp/boxplots.html")
        self.assertEqual(titles, ['How old are you?'])
        self.assertEqual(200, rest_call.status_code)

        
    def test_bivariate_relationships(self):
        """
        Test Bivariate Relationships
        """
        # arrange
        mockRelationship = [Bivariate_Relationship("Question 1?", "Question 2?", 0.543)]
        rest = flask_app.test_client()
        relationshipStrength = Mock(return_value = mockRelationship)
        birelationshipHTML, relationshipContent = visualiseRelationship(mockRelationship)
        
        # act
        rest_call = rest.get('/api/bivariate-analysis/bivariate-relationships', headers={"Content-Type": "application/json"})
        response = BivariateRelationships.get('/api/bivariate-analysis/bivariate-relationships');
        
        # assert        
        self.assertEqual(birelationshipHTML, "tmp/bivariate-relationships.html")
        self.assertEqual(200, rest_call.status_code)
        
    def test_bivariate_clustered_bargraph(self):
        """
        Test Bivariate Clustered Bargraph
        """
        # arrange
        rest = flask_app.test_client()
        clusteredbargraphHTML, stackedContent, titles = bivar_bargraph('group')
        
        # act
        rest_call = rest.get('/api/bivariate-analysis/clustered-bargraph', headers={"Content-Type": "application/json"})
        response = ClusteredBargraph.get('/api/bivariate-analysis/clustered-bargraph');
        
        # assert        
        self.assertEqual(clusteredbargraphHTML, "tmp/clusteredbargraph.html")
        self.assertEqual(titles, ['Comparing What is your gender? and What is your race?', 
                                  'Comparing What is your gender? and What is your level of education?', 
                                  'Comparing What is your gender? and What is your income?', 
                                  'Comparing What is your gender? and How many kids do you have?', 
                                  'Comparing What is your race? and What is your level of education?', 
                                  'Comparing What is your race? and What is your income?', 
                                  'Comparing What is your race? and How many kids do you have?', 
                                  'Comparing What is your level of education? and What is your income?', 
                                  'Comparing What is your level of education? and How many kids do you have?', 
                                  'Comparing What is your income? and How many kids do you have?'])
        self.assertEqual(200, rest_call.status_code)
    
    def test_bivariate_stacked_bargraph(self):
        """
        Test Bivariate Stacked Bargraph
        """
        # arrange
        rest = flask_app.test_client()
        stackedbargraphHTML, stackedContent, titles = bivar_bargraph('stack')
        
        # act
        rest_call = rest.get('/api/bivariate-analysis/stacked-bargraph', headers={"Content-Type": "application/json"})
        response = StackedBargraph.get('/api/bivariate-analysis/stacked-bargraph');
        
        # assert        
        self.assertEqual(stackedbargraphHTML, "tmp/stackedbargraph.html")
        self.assertEqual(200, rest_call.status_code)
        self.assertEqual(titles, ['Comparing What is your gender? and What is your race?', 
                                  'Comparing What is your gender? and What is your level of education?', 
                                  'Comparing What is your gender? and What is your income?', 
                                  'Comparing What is your gender? and How many kids do you have?', 
                                  'Comparing What is your race? and What is your level of education?', 
                                  'Comparing What is your race? and What is your income?', 
                                  'Comparing What is your race? and How many kids do you have?', 
                                  'Comparing What is your level of education? and What is your income?', 
                                  'Comparing What is your level of education? and How many kids do you have?', 
                                  'Comparing What is your income? and How many kids do you have?'])
      
    def test_bivariate_scatter_plot(self):
        """
        Test Bivariate ScatterPlots
        """
        # arrange
        rest = flask_app.test_client()
        scatterPlotHTML, scatterPlotContent, titles = scatter_plot()

        # act
        rest_call = rest.get('/api/bivariate-analysis/scatter-plot', headers={"Content-Type": "application/json"})
        response = ScatterPlots.get('/api/bivariate-analysis/scatter-plot');
        
        # assert        
        self.assertEqual(scatterPlotHTML, "tmp/scatterplots.html")
        self.assertEqual(titles, ['Comparing How old are you? and How many kids do you have?'])
        self.assertEqual(200, rest_call.status_code)  
        
    def test_multivariate_treemap(self):
        """
        Test Multivariate Treemap
        """
        # arrange
        rest = flask_app.test_client()
        treemapHTML, questions, treemapContent = treemap()
        
        # act
        rest_call = rest.get('/api/multivariate-analysis/treemap', headers={"Content-Type": "application/json"})
        response = Treemap.get('/api/multivariate-analysis/treemap');
        
        # assert        
        self.assertIn(treemapHTML, "tmp/treemap.html")
        self.assertEqual(200, rest_call.status_code)
        self.assertEqual(list, type(rest_call.json['questions']))
        self.assertEqual(questions, ['What is your gender?', 'What is your race?', 'What is your level of education?', 'What is your income?'])
        
    def test_multivariate_sunburst(self):
        """
        Test Multivariate Sunburst
        """
        # arrange
        rest = flask_app.test_client()
        sunburstHTML, questions, sunburstContent = sunburst()
        
        # act
        rest_call = rest.get('/api/multivariate-analysis/sunburst', headers={"Content-Type": "application/json"})
        response = Sunburst.get('/api/multivariate-analysis/sunburst');
        
        # assert        
        self.assertIn(sunburstHTML, "tmp/sunburst.html")
        self.assertEqual(200, rest_call.status_code)
        self.assertEqual(list, type(rest_call.json['questions']))
        self.assertEqual(questions, ['What is your gender?', 'What is your race?', 'What is your level of education?', 'What is your income?'])
        
    def test_pca(self):
        """
        Test PCA
        """
        # arrange
        rest = flask_app.test_client()
        pcaHTML, pcaContent, cluster_profiles = pca_respondents()
        
        # act
        rest_call = rest.get('/api/multivariate-analysis/pca-respondents', headers={"Content-Type": "application/json"})
        response = PcaRespondents.get('/api/multivariate-analysis/pca-respondents');
        
        # assert        
        self.assertIn(pcaHTML, "tmp/pca_respondents.html")
        self.assertEqual(200, rest_call.status_code)
        self.assertEqual(list, type(rest_call.json['cluster_profiles']))
        self.assertEqual(cluster_profiles, [[[{'question': 'What is your gender?', 
                                               'common_response': ['Female', 'Male'], 
                                               'common_response_count': [52, 41]}], 
                                             [{'question': 'What is your race?', 
                                               'common_response': ['White/Caucasian', 'Black/ African American/ Caribbean American', 'Asian'], 
                                               'common_response_count': [34, 27, 18]}], 
                                             [{'question': 'What is your level of education?', 
                                               'common_response': ['Some college but degree not received or in progress', 'High school graduate or equivalent (i.e., GED)', 'Associate degree (i.e., AA, AS)'], 
                                               'common_response_count': [38, 29, 17]}], 
                                             [{'question': 'What is your income?', 
                                               'common_response': ['$25,000 - $34,999', '$15,000 - $24,999', 'Less than $14,999'], 
                                               'common_response_count': [30, 17, 14]}], 
                                             [{'question': 'How many kids do you have?', 
                                               'common_response': ['0', 2.0, 1.0], 
                                               'common_response_count': [61, 16, 12]}], 
                                             {'respondents': 93}], 
                                            [[{'question': 'What is your gender?', 
                                               'common_response': ['Male', 'Female', 'Refused'], 
                                               'common_response_count': [4, 2, 1]}], 
                                             [{'question': 'What is your race?', 
                                               'common_response': ['White/Caucasian', 'Other', 'Refused'], 
                                               'common_response_count': [3, 3, 1]}], 
                                             [{'question': 'What is your level of education?', 
                                               'common_response': ['High school graduate or equivalent (i.e., GED)', 'Some college but degree not received or in progress', 'Associate degree (i.e., AA, AS)'], 
                                               'common_response_count': [3, 2, 1]}], 
                                             [{'question': 'What is your income?', 
                                               'common_response': ['N/A', 'Refused'], 
                                               'common_response_count': [4, 3]}], 
                                             [{'question': 'How many kids do you have?', 
                                               'common_response': ['N/A'], 
                                               'common_response_count': [7]}], 
                                             {'respondents': 7}]])

    def test_sentiment_piecharts(self):
            """
            Test Sentiment Piechart
            """
            # arrange
            rest = flask_app.test_client()
            categories = sentiment_tokens()
            sentimentHTML, sentimentContent, titles = sentiment_charts()
            
            # act
            rest_call = rest.get('/api/qualitative-encoding/sentiment-charts', headers={"Content-Type": "application/json"})
            response = SentimentCharts.get('/api/qualitative-encoding/sentiment-charts');
            
            # assert        
            self.assertIn(sentimentHTML, "tmp/sentiment_charts.html")
            self.assertEqual(200, rest_call.status_code),
            self.assertEqual(list, type(rest_call.json['categories']))
            self.assertEqual(titles, ['How do you feel about the area you live in?'])
            
    def test_thematic_analysis(self):
            """
            Test Thematic Analysis
            """
            # arrange
            rest = flask_app.test_client()
            themesHTML, themesContent, titles, categories = themes_charts()
            
            # act
            rest_call = rest.get('/api/qualitative-encoding/themes-charts', headers={"Content-Type": "application/json"})
            response = ThemesCharts.get('/api/qualitative-encoding/themes-charts');
            
            # assert     
            self.assertEqual(themesHTML, "tmp/themes_charts.html")     
            self.assertEqual(200, rest_call.status_code)
            self.assertEqual(list, type(rest_call.json['categories']))
            self.assertEqual(titles, ['How do you feel about the area you live in?'])
            

if __name__ == '__main__':
    unittest.main()