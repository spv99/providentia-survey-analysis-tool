import { Injectable } from "@angular/core";
import { Observable, throwError } from "rxjs";
import { HttpClient } from "@angular/common/http";
import { environment } from "src/environments/environment";
import { map } from "rxjs/operators";

const SURVEY_DATA = '/survey-data';

@Injectable()
export class ProvidentiaService {
    baseUrl = environment.baseUrl;
    localStorage: Storage;

    constructor(private httpClient: HttpClient) {
        this.localStorage = window.localStorage;
    }

    public uploadSurvey(file: File): Observable<any> {
        // Validate inputs
        let fileExtension = /(?:\.([^.]+))?$/;
        const fileName = file.name;
        if (!file || fileName.length == 0 || fileExtension.exec(fileName)[1] != 'csv') {
            let errMessage = 'Error uploading file: Provide a valid .csv file';
            return throwError(errMessage)
        }
        let formData: FormData = new FormData();
        // name has to be 'file' to connect with what the backend expects (app.py: request.files['file'])
        formData.append('file', file, file.name);

        const surveyDataUrl: string = this.baseUrl + `${SURVEY_DATA}/`;
        return this.httpClient.post<any>(surveyDataUrl, formData).pipe(map(res => { }));
    }

    get(key: string): any {
        if (this.isLocalStorageSupported) {
            return JSON.parse(this.localStorage.getItem(key));
        }
        return null;
    }

    getAllKeys(): any {
        if (this.isLocalStorageSupported) {
            return Object.keys(this.localStorage);
        }
        return null;
    }

    set(key: string, value: any): boolean {
        if (this.isLocalStorageSupported) {
            this.localStorage.setItem(key, JSON.stringify(value));
            return true;
        }
        return false;
    }

    remove(key: string): boolean {
        if (this.isLocalStorageSupported) {
            this.localStorage.removeItem(key);
            return true;
        }
        return false;
    }

    clear(): boolean {
        if (this.isLocalStorageSupported) {
            this.localStorage.clear();
            return true;
        }
        return false;
    }
    
    get isLocalStorageSupported(): boolean {
        return !!this.localStorage
    }
}

