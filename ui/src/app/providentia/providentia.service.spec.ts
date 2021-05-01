import { TestBed } from '@angular/core/testing';
import {HttpClientTestingModule, HttpTestingController} from '@angular/common/http/testing';
import { environment } from 'src/environments/environment';
import { ProvidentiaService } from './providentia.service';

function MockFile() { };

MockFile.prototype.create = function (name, size, mimeType) {
    name = name || "mock.csv";
    size = size || 1024;
    mimeType = mimeType || 'plain/txt';

    function range(count) {
        var output = "";
        for (var i = 0; i < count; i++) {
            output += "a";
        }
        return output;
    }

    let blob = new Blob([range(size)], { type: mimeType });
    return blob;
};

function MockEmptyFile() { };

MockEmptyFile.prototype.create = function (name, size, mimeType) {
    name = name || "empty.csv";
    size = size || 0;
    mimeType = mimeType || 'plain/txt';

    function range(count) {
        var output = "";
        for (var i = 0; i < count; i++) {
            output += "a";
        }
        return output;
    }

    let blob = new Blob([range(size)], { type: mimeType });
    return blob;
};

describe('ProvidentiaService', () => {
    const base = environment.baseUrl;
    let service;
    let httpMock: HttpTestingController
    beforeEach(() => {
      TestBed.configureTestingModule({
            imports: [HttpClientTestingModule],
            providers: [ProvidentiaService]
        });
        httpMock = TestBed.get(HttpTestingController);
        service = TestBed.get(ProvidentiaService);
    });

  afterEach(() => {
    httpMock.verify();
  });

  it('should return data when valid csv sent to service', () => {
    // arrange
    const url = `${base}/survey-data/`;
    let mockFile = new MockFile();
    const file = new File([mockFile], "mock.csv", {type: "form"});

    // act
    service.uploadSurvey(file).subscribe(response => {
      expect(response).toBeTruthy();
    });
    
    const req = httpMock.expectOne(request => {
      url: request.url
      return true;
    });

    // assert
    expect(req.request.url).toEqual(url);
    expect(req.request.method).toEqual('POST');
  });
});