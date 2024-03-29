import { Component, OnInit } from '@angular/core';
import { ProvidentiaService } from './providentia.service';
import { Router } from '@angular/router';

@Component({
  selector: 'providentia',
  templateUrl: './providentia.component.html',
  styleUrls: ['./providentia.component.scss']
})

export class ProvidentiaComponent implements OnInit {
  public fileToUpload: File = null;
  public status: string;
  public errorMessage: string;

  public title1 = 'Decipher';
  public subtitle1 = "your data";
  public text1 = "Upload your survey responses and generate visual insights and analysis!"

  public title2 = 'Discover';
  public subtitle2 = "your reach";
  public text2 = "As well as classic analysis techniques, we also use machine learning to find trends that you wouldn't usually find in Excel!"

  public title3 = 'Decide';
  public subtitle3 = "your next move";
  public text3 = "Our easy-to-read analytical insights can help determine your next steps!"

  constructor(private appService: ProvidentiaService, private router: Router) { }

  public ngOnInit() { }

  public uploadFile($event) {
    try {
      this.fileToUpload = $event.target.files[0];
    } catch(error) {
      this.fileToUpload = $event;
    }
    this.appService.uploadSurvey(this.fileToUpload).subscribe(data => {
      this.status = 'success';
      this.router.navigate(['providentia/results']);
      this.fileToUpload = null;
    }, error => {
      this.status = 'error';
      this.errorMessage = error;
      this.fileToUpload = null;
    });
  }

  public downloadSampleSurvey(): void {
    this.router.navigate([]).then(result => { window.open('assets/sample-survey.csv', '_blank'); });
    
    var getFileBlob = function (url, cb) {
      var xhr = new XMLHttpRequest();
      xhr.open("GET", url);
      xhr.responseType = "blob";
      xhr.addEventListener('load', function() {
          cb(xhr.response);
      });
      xhr.send();
    };

    var blobToFile = function (blob, name) {
      blob.lastModifiedDate = new Date();
      blob.name = name;
      return blob;
    };

    var getFileObject = function(filePathOrUrl, cb) {
      getFileBlob(filePathOrUrl, function (blob) {
          cb(blobToFile(blob, 'sample-survey.csv'));
      });
    };

    getFileObject('assets/sample-survey.csv', (fileObject) => {
      this.uploadFile(fileObject);
    }); 
  }
}

