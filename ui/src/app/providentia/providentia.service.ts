import {Injectable} from "@angular/core";
import {Observable, throwError} from "rxjs";
import {HttpClient} from "@angular/common/http";
import {environment} from "src/environments/environment";
import {map} from "rxjs/operators";

const SURVEY_DATA = '/survey-data';

@Injectable()
export class ProvidentiaService {
    baseUrl = environment.baseUrl;
    
    constructor(private httpClient: HttpClient) {}

    public uploadSurvey(file: File): Observable<any> {
        // Validate inputs
        let fileExtension = /(?:\.([^.]+))?$/;
        const fileName = file.name;
        if(!file || fileName.length == 0 || fileExtension.exec(fileName)[1] != 'csv') {
            let errMessage = 'Error uploading file: Provide a valid file';
            return throwError(errMessage)
        }
        console.log('here')
        let formData:FormData = new FormData();
        // name has to be 'file' to connect with what the backend expects (app.py: request.files['file'])
        formData.append('file', file, file.name); 
        
        const surveyDataUrl: string = this.baseUrl + `${SURVEY_DATA}/`;
        return this.httpClient.post<any>(surveyDataUrl, formData).pipe(map(res => {
            console.log(res)
        }))
    }
}

