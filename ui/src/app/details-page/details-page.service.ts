import {Injectable} from "@angular/core";
import {Observable, throwError} from "rxjs";
import {HttpClient} from "@angular/common/http";
import {environment} from "src/environments/environment";
import {map} from "rxjs/operators";
import { Chart } from "../models/chart.model";

const PLOTLYJS = '../../assets/plotly.js';
const regexFind = 'https://cdn.plot.ly/plotly-latest.min.js';
const UNIVARIATE_ANALYSIS = '/univariate-analysis';
const BIVARIATE_ANALYSIS = '/bivariate-analysis';
const MULTIVARIATE_ANALYSIS = '/multivariate-analysis';
const QUALITATIVE_ENCODING = '/qualitative-encoding';
const BARGRAPH = '/bargraph';
const BOXPLOT = '/boxplot';
const SENTIMENT_ANALYSIS = '/sentiment-analysis';
const SENTIMENT_CHARTS = '/sentiment-charts';
const THEMATIC_ANALYSIS = '/themes-analysis';
const THEMES_CHARTS = '/themes-charts';
const PIECHART = '/piechart';
const CLUSTERED_BARGRAPH = '/clustered-bargraph';
const STACKED_BARGRAPH = '/stacked-bargraph';
const SCATTER_PLOT = "/scatter-plot";
const TREEMAP = '/treemap';
const SUNBURST = '/sunburst';
const BIVAR_RELATIONSHIPS = '/bivariate-relationships';
const PCA_RESPONDENTS = '/pca-respondents';

const QUESTIONS_HEADER = '<div style="margin-left: 1rem;background-color: #fff;"><p style="font-family: Segoe UI; font-size: 25px; font-weight: 200; margin-top: 1rem; margin-bottom: 1rem;">Questions: </p>';
const LIST_STYLE = 'style="font-family: Bahnschrift; text-decoration-line: none; font-weight: 200; font-size: 19px; line-height: 26px; color: #013a83;"';
const COLLAPSIBLE_STYLE = '<style type="text/css">   input[type="checkbox"] {   display: none;   }   .lbl-toggle {   display: block;   font-weight: bold;   font-family: monospace;   font-family: "Segoe UI";   font-size: 1.2rem;   text-transform: uppercase;   text-align: center;   padding: 1rem;   color: #FFFFFF;   background: #2A7BE5;   cursor: pointer;   margin-right: 3rem;   margin-left: 3rem;   border-radius: 7px;   transition: all 0.25s ease-out;   margin-bottom: 0rem;   }   .lbl-toggle:hover {   color: #FFFFFF;   }   .lbl-toggle::before {   content: " "; display: inline-block;   border-top: 5px solid transparent;   border-bottom: 5px solid transparent;   border-left: 5px solid currentColor;   vertical-align: middle;   margin-right: .7rem;   transform: translateY(-2px);   transition: transform .2s ease-out;   }   .collapsible-content {   max-height: 0px;   overflow: hidden;   transition: max-height .25s ease-in-out;   }   .collapsible-content {   max-height: 0px;   overflow: hidden;   transition: max-height .25s ease-in-out;   }   .toggle:checked + .lbl-toggle + .collapsible-content {   max-height: 100vh;   }   .toggle:checked + .lbl-toggle::before {   transform: rotate(90deg) translateX(-3px);   }   .toggle:checked + .lbl-toggle {   border-bottom-right-radius: 0;   border-bottom-left-radius: 0;   }   .collapsible-content .content-inner {   height: 30rem;   overflow-y: auto;   margin-right: 3rem;   margin-left: 3rem;   font-family: Bahnschrift;   background-color: #f0f8ff ;   padding: 1.3rem;   border: 1px solid black;   }</style>';

@Injectable()
export class AnalyticsService {
    baseUrl = environment.baseUrl;
    
    constructor(private httpClient: HttpClient) {}

    private renderIframe(graph, renderContent, titles): any {
        let html = (renderContent.toString());
        html = html.replace(regexFind, PLOTLYJS);
        titles.forEach(title => {
            let anchor = '<a id="' + title + '"></a><div id';
            html = html.replace("   <div id", anchor)
        })
        let toc = '<h3 class="title" style="font-family: Segoe UI; margin-top: 3rem;line-height: 38px; font-size: 38px; font-weight: 100; text-align: left;" >' + graph + '</h3>' + QUESTIONS_HEADER;
        titles.forEach(title => {
            toc = toc + '<li><a '+ LIST_STYLE +' href="#'+title+'">'+ title +'</a></li>';
        })
        toc = toc + "</div>";
        html = toc + html;
        return html;
    }

    private renderSingleChartIframe(graph, renderContent): any {
        let html = (renderContent.toString());
        html = html.replace(regexFind, PLOTLYJS);
        let toc = '<h3 class="title" style="font-family: Segoe UI; margin-top: 3rem;line-height: 38px; font-size: 38px; font-weight: 100; text-align: left;" >' + graph + '</h3>';
        html = toc + html;
        return html;
    }

    private renderSentimentIframe(graph, renderContent, titles, categories): any {
        let html = (renderContent.toString());
        html = html.replace(regexFind, PLOTLYJS);
        let endGraph = '      </script>\n';
        titles.forEach((title, index) => {
            let collapsible = COLLAPSIBLE_STYLE + '<div class="wrap-collabsible"><input id="collapsible'+'-' +index+'" class="toggle" type="checkbox"> <label for="collapsible'+'-' +index+'" class="lbl-toggle">View Full Text Responses</label> <div class="collapsible-content"> <div class="content-inner"><div ';
            let sentiment = categories[index]
            collapsible = collapsible + '><p class="senti-subheader" style="font-size: 22px; margin-top: 1rem;">Positive Statements</p>';
            sentiment.positive_statements.forEach(pos => {
                collapsible = collapsible + '<div><li class="senti-details" style="font-size: 17px; font-weight: 200;"> ' + pos + ' </li></div>';
            })
            collapsible = collapsible + '<p class="senti-subheader" style="font-size: 22px; margin-top: 1rem;">Neutral Statements</p>';
            sentiment.neutral_statements.forEach(neu => {
                collapsible = collapsible + '<div><li class="senti-details" style="font-size: 17px; font-weight: 200;"> ' + neu + ' </li></div>';
            })
            collapsible = collapsible + '<p class="senti-subheader" style="font-size: 22px; margin-top: 1rem;">Negative Statements</p>';
            sentiment.negative_statements.forEach(neg => {
                collapsible = collapsible + '<div><li class="senti-details" style="font-size: 17px; font-weight: 200;"> ' + neg + ' </li></div>';
            })
            collapsible = collapsible + '</div></div></div></div>';
            let anchor = '<a id="' + title + '"></a><div id';
            html = html.replace("   <div id", anchor)
            html = html.replace(endGraph, '      </script> '+ collapsible)
        })
        let toc = '<h3 class="title" style="font-family: Segoe UI; margin-top: 3rem;line-height: 38px; font-size: 38px; font-weight: 100; text-align: left;" >' + graph + '</h3>' + QUESTIONS_HEADER;
        titles.forEach(title => {
            toc = toc + '<li><a '+ LIST_STYLE +' href="#'+title+'">'+ title +'</a></li>';
        })
        toc = toc + "</div>";
        html = toc + html;
        return html;
    }

    public renderThematicIframe(graph, renderContent, titles, categories): any {
        let html = (renderContent.toString());
        html = html.replace(regexFind, PLOTLYJS);
        let endGraph = '      </script>\n';
        titles.forEach((title, index) => {
            let collapsible = COLLAPSIBLE_STYLE + '<div class="wrap-collabsible"><input id="collapsible'+'-' +index+'" class="toggle" type="checkbox"> <label for="collapsible'+'-' +index+'" class="lbl-toggle">View Full Text Responses</label> <div class="collapsible-content"> <div class="content-inner"><div ';
            let thematic = categories[index]
            thematic.themes.forEach(theme => {
                collapsible = collapsible + '><p class="senti-subheader" style="font-size: 22px; margin-top: 1rem;">'+ theme.theme +'</p>';
                theme.statements.forEach(statements => {
                    collapsible = collapsible + '<div><li class="senti-details" style="font-size: 17px; font-weight: 200;"> ' + statements + ' </li></div>';
                })
            })
            collapsible = collapsible + '</div></div></div></div>';
            let anchor = '<a id="' + title + '"></a><div id';
            html = html.replace("   <div id", anchor)
            html = html.replace(endGraph, '      </script> '+ collapsible)
        })
        let toc = '<h3 class="title" style="font-family: Segoe UI; margin-top: 3rem; line-height: 38px; font-size: 38px; font-weight: 100; text-align: left;" >' + graph + '</h3>' + QUESTIONS_HEADER;
        titles.forEach(title => {
            toc = toc + '<li><a '+ LIST_STYLE +' href="#'+title+'">'+ title +'</a></li>';
        })
        toc = toc + "</div>";
        html = toc + html;
        return html;
    }

    public getUnivariateBargraph(): Observable<any> {
        const univariateBargraphUrl: string = this.baseUrl + `${UNIVARIATE_ANALYSIS}${BARGRAPH}`;
        return this.httpClient.get<Chart>(univariateBargraphUrl).pipe(map(res => {
            if(res.renderContent != null) {
                return this.renderIframe("Bar Graphs",  res.renderContent, res.titles)
            }
        }));
    }

    public getUnivariatePiechart(): Observable<any> {
        const univariatePieChartUrl: string = this.baseUrl + `${UNIVARIATE_ANALYSIS}${PIECHART}`;
        return this.httpClient.get<Chart>(univariatePieChartUrl).pipe(map(res => {
            if(res.renderContent != null) {
                return this.renderIframe("Pie Charts",res.renderContent, res.titles)
            }
        }));
    }

    public getUnivariateBoxPlot(): Observable<any> {
        const univariateBoxplotUrl: string = this.baseUrl + `${UNIVARIATE_ANALYSIS}${BOXPLOT}`;
        return this.httpClient.get<Chart>(univariateBoxplotUrl).pipe(map(res => {
            if(res.renderContent != null) {
                return this.renderIframe("Box Plots",res.renderContent, res.titles)
            }
        }));
    }

    public getSentimentCharts(): Observable<any> {
        const sentimentChartsUrl: string = this.baseUrl + `${QUALITATIVE_ENCODING}${SENTIMENT_CHARTS}`;
        return this.httpClient.get<Chart>(sentimentChartsUrl).pipe(map(res => {
            if(res.renderContent != null) {
                return this.renderSentimentIframe("Sentiment Analysis", res.renderContent, res.titles, res.categories)
            }
        }));
    }

    public getThemesCharts(): Observable<any> {
        const themesChartsUrl: string = this.baseUrl + `${QUALITATIVE_ENCODING}${THEMES_CHARTS}`;
        return this.httpClient.get<Chart>(themesChartsUrl).pipe(map(res => {
            if(res.renderContent != null) {
                return this.renderThematicIframe("Thematic Analysis", res.renderContent, res.titles, res.categories)
            }
        }));
    }

    public getBivariateRelationships(): Observable<any> {
        const bivariateRelationshipsUrl: string = this.baseUrl + `${BIVARIATE_ANALYSIS}${BIVAR_RELATIONSHIPS}`;
        return this.httpClient.get<Chart>(bivariateRelationshipsUrl).pipe(map(res => {
            if(res.renderContent != null) {
                return this.renderSingleChartIframe("Bivariate Relationships", res.renderContent);
            }
        }));
    }

    public getBivariateClusteredBargraph(): Observable<any> {
        const bivariateClusteredBargraph: string = this.baseUrl + `${BIVARIATE_ANALYSIS}${CLUSTERED_BARGRAPH}`;
        return this.httpClient.get<Chart>(bivariateClusteredBargraph).pipe(map(res => {
            if(res.renderContent != null) {
                return this.renderIframe("Clustered Bar Graphs", res.renderContent, res.titles)
            }
        }));
    }

    public getBivariateStackedBargraph(): Observable<any> {
        const bivariateStackedBargraph: string = this.baseUrl + `${BIVARIATE_ANALYSIS}${STACKED_BARGRAPH}`;
        return this.httpClient.get<Chart>(bivariateStackedBargraph).pipe(map(res => {
            if(res.renderContent != null) {
                return this.renderIframe("Stacked Bar Graphs",res.renderContent, res.titles)
            }
        }));
    }

    public getBivariateScatterPlot(): Observable<any> {
        const bivariateScatterPlot: string = this.baseUrl + `${BIVARIATE_ANALYSIS}${SCATTER_PLOT}`;
        return this.httpClient.get<Chart>(bivariateScatterPlot).pipe(map(res => {
            if(res.renderContent != null) {
                return this.renderIframe("Scatter Plots",res.renderContent, res.titles)
            }
        }));
    }

    public getMultivariateTreemap(): Observable<any> {
        const multivariateTreemap: string = this.baseUrl + `${MULTIVARIATE_ANALYSIS}${TREEMAP}`;
        return this.httpClient.get<Chart>(multivariateTreemap).pipe(map(res => {
            if(res.renderContent != null) {
                return this.renderSingleChartIframe("Treemap Chart", res.renderContent);
            }
        }));
    }

    public getMultivariateSunburst(): Observable<any> {
        const multivariateSunburst: string = this.baseUrl + `${MULTIVARIATE_ANALYSIS}${SUNBURST}`;
        return this.httpClient.get<Chart>(multivariateSunburst).pipe(map(res => {
            if(res.renderContent != null) {
                return this.renderSingleChartIframe("Sunburst Chart", res.renderContent);
            }
        }));
    }
    
    public getUserProfiles(): Observable<any> {
        const userProfiles: string = this.baseUrl + `${MULTIVARIATE_ANALYSIS}${PCA_RESPONDENTS}`;
        return this.httpClient.get<any>(userProfiles).pipe(map(res => {
            if(res.renderContent != null) {
                let html = (res.renderContent.toString());
                html = html.replace(regexFind, PLOTLYJS);
                let cluster_profiles = res.cluster_profiles
                return [html, cluster_profiles];
            }
        }));
    }
}

