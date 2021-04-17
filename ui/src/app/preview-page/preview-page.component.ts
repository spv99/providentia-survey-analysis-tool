import { Component, OnInit } from '@angular/core';
import { ProvidentiaService } from '../providentia/providentia.service';

@Component({
  selector: 'app-preview-page',
  templateUrl: './preview-page.component.html',
  styleUrls: ['./preview-page.component.scss']
})

export class PreviewPageComponent implements OnInit  {
  public graphs = [];

  constructor(private localStorageService: ProvidentiaService) {}

  ngOnInit() {
    let keys = this.localStorageService.getAllKeys();
    keys.forEach(key => {
      this.graphs.push(key);
      let iframe = <HTMLIFrameElement>document.getElementById(key) as HTMLIFrameElement;
      let injectHTML = iframe.contentWindow.document;
      injectHTML.open();
      injectHTML.write(this.localStorageService.get(key));
      injectHTML.close();   
      this.resizeIFrameToFitContent(iframe)
    });
  }

  public resizeIFrameToFitContent(iFrame: any): void {
    iFrame.width = iFrame.contentWindow.document.body.scrollWidth + "px";
    iFrame.height = iFrame.contentWindow.document.body.scrollHeight + "px";
  }

}
