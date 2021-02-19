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
const MUTLIVARIATE_ANALYSIS = '/multivariate-analysis';
const QUALITATIVE_ENCODING = '/qualitative-encoding';
const BARGRAPH = '/bargraph';
const BOXPLOT = '/boxplot';
const PIECHART = '/piechart';

@Injectable()
export class AnalyticsService {
    baseUrl = environment.baseUrl;
    
    constructor(private httpClient: HttpClient) {}

    public getUnivariateBargraph(): Observable<any> {
        const univariateBargraphUrl: string = this.baseUrl + `${UNIVARIATE_ANALYSIS}${BARGRAPH}`;
        return this.httpClient.get<Chart>(univariateBargraphUrl).pipe(map(res => {
            if(res.renderContent != null) {
                let html = (res.renderContent.toString());
                html = html.replace(regexFind, PLOTLYJS);
                return html;
            }
        }));
    }

    public getUnivariatePiechart(): Observable<any> {
        const univariatePieChartUrl: string = this.baseUrl + `${UNIVARIATE_ANALYSIS}${PIECHART}`;
        return this.httpClient.get<Chart>(univariatePieChartUrl).pipe(map(res => {
            if(res.renderContent != null) {
                let html = (res.renderContent.toString());
                html = html.replace(regexFind, PLOTLYJS);
                return html;
            }
        }));
    }

    public getUnivariateBoxPlot(): Observable<any> {
        const univariateBoxplotUrl: string = this.baseUrl + `${UNIVARIATE_ANALYSIS}${BOXPLOT}`;
        return this.httpClient.get<Chart>(univariateBoxplotUrl).pipe(map(res => {
            if(res.renderContent != null) {
                let html = (res.renderContent.toString());
                html = html.replace(regexFind, PLOTLYJS);
                return html;
            }
        }));
    }
}

