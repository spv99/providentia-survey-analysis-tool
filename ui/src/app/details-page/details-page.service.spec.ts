import { TestBed } from '@angular/core/testing';
import {HttpClientTestingModule, HttpTestingController} from '@angular/common/http/testing';
import { AnalyticsService } from './details-page.service';
import { environment } from 'src/environments/environment';

describe('AnalyticsService', () => {
    const base = environment.baseUrl;
    let service;
    let httpMock: HttpTestingController
    beforeEach(() => {
      TestBed.configureTestingModule({
            imports: [HttpClientTestingModule],
            providers: [AnalyticsService]
        });
        httpMock = TestBed.get(HttpTestingController);
        service = TestBed.get(AnalyticsService);
    });

  afterEach(() => {
    httpMock.verify();
  });

  it('should return data from get bargraphs', () => {
    // arrange
    const url = `${base}/univariate-analysis/bargraph`;

    // act
    service.getUnivariateBargraph().subscribe(response => {
      expect(response).toBeTruthy();
    });
    
    const req = httpMock.expectOne(request => {
      url: request.url
      return true;
    });

    // assert
    expect(req.request.url).toEqual(url);
    expect(req.request.method).toEqual('GET');
  });

  it('should return data from get piecharts', () => {
    // arrange
    const url = `${base}/univariate-analysis/piechart`;

    // act
    service.getUnivariatePiechart().subscribe(response => {
      expect(response).toBeTruthy();
    });
    
    const req = httpMock.expectOne(request => {
      url: request.url
      return true;
    });

    // assert
    expect(req.request.url).toEqual(url);
    expect(req.request.method).toEqual('GET');
  });

  it('should return data from get boxplots', () => {
    // arrange
    const url = `${base}/univariate-analysis/boxplot`;

    // act
    service.getUnivariateBoxPlot().subscribe(response => {
      expect(response).toBeTruthy();
    });
    
    const req = httpMock.expectOne(request => {
      url: request.url
      return true;
    });

    // assert
    expect(req.request.url).toEqual(url);
    expect(req.request.method).toEqual('GET');
  });

  it('should return data from get sentiment charts', () => {
    // arrange
    const url = `${base}/qualitative-encoding/sentiment-charts`;

    // act
    service.getSentimentCharts().subscribe(response => {
      expect(response).toBeTruthy();
    });
    
    const req = httpMock.expectOne(request => {
      url: request.url
      return true;
    });


    // assert
    expect(req.request.url).toEqual(url);
    expect(req.request.method).toEqual('GET');
  });

  it('should return data from get themes charts', () => {
    // arrange
    const url = `${base}/qualitative-encoding/themes-charts`;

    // act
    service.getThemesCharts().subscribe(response => {
      expect(response).toBeTruthy();
    });
    
    const req = httpMock.expectOne(request => {
      url: request.url
      return true;
    });


    // assert
    expect(req.request.url).toEqual(url);
    expect(req.request.method).toEqual('GET');
  });

  it('should return data from get bivariate relationships', () => {
    // arrange
    const url = `${base}/bivariate-analysis/bivariate-relationships`;

    // act
    service.getBivariateRelationships().subscribe(response => {
      expect(response).toBeTruthy();
    });
    
    const req = httpMock.expectOne(request => {
      url: request.url
      return true;
    });

   

    // assert
    expect(req.request.url).toEqual(url);
    expect(req.request.method).toEqual('GET');
  });

  it('should return data from get clustered bargraphs', () => {
    // arrange
    const url = `${base}/bivariate-analysis/clustered-bargraph`;

    // act
    service.getBivariateClusteredBargraph().subscribe(response => {
      expect(response).toBeTruthy();
    });
    
    const req = httpMock.expectOne(request => {
      url: request.url
      return true;
    });

    // assert
    expect(req.request.url).toEqual(url);
    expect(req.request.method).toEqual('GET');
  });

  it('should return data from get stacked bargraphs', () => {
    // arrange
    const url = `${base}/bivariate-analysis/stacked-bargraph`;

    // act
    service.getBivariateStackedBargraph().subscribe(response => {
      expect(response).toBeTruthy();
    });
    
    const req = httpMock.expectOne(request => {
      url: request.url
      return true;
    });

    // assert
    expect(req.request.url).toEqual(url);
    expect(req.request.method).toEqual('GET');
  });

  it('should return data from get scatter plots', () => {
    // arrange
    const url = `${base}/bivariate-analysis/scatter-plot`;

    // act
    service.getBivariateScatterPlot().subscribe(response => {
      expect(response).toBeTruthy();
    });
    
    const req = httpMock.expectOne(request => {
      url: request.url
      return true;
    });

    // assert
    expect(req.request.url).toEqual(url);
    expect(req.request.method).toEqual('GET');
  });

  it('should return data from get treemap chart', () => {
    // arrange
    const url = `${base}/multivariate-analysis/treemap`;

    // act
    service.getMultivariateTreemap().subscribe(response => {
      expect(response).toBeTruthy();
    });
    
    const req = httpMock.expectOne(request => {
      url: request.url
      return true;
    });

    // assert
    expect(req.request.url).toEqual(url);
    expect(req.request.method).toEqual('GET');
  });

  it('should return data from get sunburst chart', () => {
    // arrange
    const url = `${base}/multivariate-analysis/sunburst`;

    // act
    service.getMultivariateSunburst().subscribe(response => {
      expect(response).toBeTruthy();
    });
    
    const req = httpMock.expectOne(request => {
      url: request.url
      return true;
    });

    // assert
    expect(req.request.url).toEqual(url);
    expect(req.request.method).toEqual('GET');
  });

  it('should return data from get user profiles', () => {
    // arrange
    const url = `${base}/multivariate-analysis/pca-respondents`;

    // act
    service.getUserProfiles().subscribe(response => {
      expect(response).toBeTruthy();
    });
    
    const req = httpMock.expectOne(request => {
      url: request.url
      return true;
    });

    // assert
    expect(req.request.url).toEqual(url);
    expect(req.request.method).toEqual('GET');
  });

});