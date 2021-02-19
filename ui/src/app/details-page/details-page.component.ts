import { Component, OnInit } from '@angular/core';
import { AnalyticsService } from './details-page.service';

@Component({
  selector: 'app-details-page',
  templateUrl: './details-page.component.html',
  styleUrls: ['./details-page.component.scss']
})

export class DetailsPageComponent implements OnInit {
  public data: any;

  constructor(private analyticsService: AnalyticsService) { }

  ngOnInit() {
    this.analyticsService.getUnivariateBargraph().subscribe(data => {
      this.injectHTML("Bargraphs", data)
    });

    this.analyticsService.getUnivariatePiechart().subscribe(data => {
      this.injectHTML("Piecharts", data)
    });

    this.analyticsService.getUnivariateBoxPlot().subscribe(data => {
      this.injectHTML("Boxplots", data)
    });
  }

  public injectHTML(id: string, data: string): void {
    if (data == undefined) {
      const iFrameContainerId = id + '-box';
      let iFrameContainer = <HTMLDivElement>document.getElementById(iFrameContainerId) as HTMLDivElement;
      iFrameContainer.setAttribute("style", "display: none");
    } else {
      let iframe = <HTMLIFrameElement>document.getElementById(id) as HTMLIFrameElement
      let injectHTML = iframe.contentWindow.document;
      injectHTML.open();
      injectHTML.write(data);
      injectHTML.close();
      this.resizeIFrameToFitContent(iframe);
    }
  }

  public resizeIFrameToFitContent(iFrame: any): void {
    iFrame.width  = iFrame.contentWindow.document.body.scrollWidth;
    iFrame.height = iFrame.contentWindow.document.body.scrollHeight;
  }

}
