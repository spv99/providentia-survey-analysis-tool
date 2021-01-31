import { Component, OnInit } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})

export class AppComponent implements OnInit {
  public fileToUpload: File = null;

  public title1 = 'Decipher';
  public subtitle1 ="your data";
  public text1 = "Upload your survey responses and generate visual insights and analysis in minutes!"

  public title2 = 'Discover';
  public subtitle2 ="your reach";
  public text2 = "As well as classic analysis techniques we also use machine learning to find trends that you wouldn't usually find in Excel!"

  public title3 = 'Decide';
  public subtitle3 ="your next move";
  public text3 = "Our easy-to-read analytical insights can help determine your next steps by identifying correlations and patterns!"

  constructor() {}

  public ngOnInit() {}
  
  public uploadFile($event) {
    this.fileToUpload = $event.target.files[0];
  }

  // public postFile(fileToUpload: File): boolean {
  //   const endpoint = 'your-destination-url';
  //   const formData: FormData = new FormData();
  //   formData.append('fileKey', fileToUpload, fileToUpload.name);
  //   return true;
  // }

}

