import { Component, OnInit } from '@angular/core';
import { AnalyticsService } from './details-page.service';
import { CloudData, CloudOptions } from 'angular-tag-cloud-module';

@Component({
  selector: 'app-details-page',
  templateUrl: './details-page.component.html',
  styleUrls: ['./details-page.component.scss']
})

export class DetailsPageComponent implements OnInit {
  public data: any;
  public wordCloudData: CloudData[];
  public dataMap = new Map();

  constructor(private analyticsService: AnalyticsService) { }

  ngOnInit() {
    this.changeActiveTab();

    this.analyticsService.getUnivariateBargraph().subscribe(data => {
      this.dataMap.set("bargraphs", data);
    });

    this.analyticsService.getUnivariatePiechart().subscribe(data => {
      this.dataMap.set("piecharts", data);
    });

    this.analyticsService.getUnivariateBoxPlot().subscribe(data => {
      this.dataMap.set("boxplots", data);
    });

    this.analyticsService.getUnivariateWordmaps().subscribe(data => {
      this.wordCloudData = data[1];    
      console.log(this.wordCloudData)
    });

    this.analyticsService.getUnivariateSentimentBargraph().subscribe(data => {
      this.dataMap.set("sentiment-bargraph", data);
    });

    this.analyticsService.getUnivariateSentimentPiechart().subscribe(data => {
      this.dataMap.set("sentiment-piechart", data);
    });

    this.analyticsService.getUnivariateThemesBargraph().subscribe(data => {
      this.dataMap.set("themes-bargraph", data);
    });

    this.analyticsService.getUnivariateThemesPiechart().subscribe(data => {
      this.dataMap.set("themes-piechart", data);
    });

    this.analyticsService.getBivariateClusteredBargraph().subscribe(data => {
      this.dataMap.set("clustered-bargraph", data);
    });

    this.analyticsService.getBivariateStackedBargraph().subscribe(data => {
      this.dataMap.set("stacked-bargraph", data);
    });

    this.analyticsService.getBivariateScatterPlot().subscribe(data => {
      this.dataMap.set("scatter-plots", data);
    });

    this.analyticsService.getMultivariateSunburst().subscribe(data => {
      this.dataMap.set("sunburst", data);
    });

    this.analyticsService.getMultivariateTreemap().subscribe(data => {
      this.dataMap.set("treemap", data);
    });
  }

  public changeActiveTab(): void {
    let tabs = document.getElementsByClassName("hover");
    let name;
    for (let i = 0; i < tabs.length; i++) {
      tabs[i].addEventListener("click", () => {
        // deselecting/hiding previously active tab
        let currentTab = document.getElementsByClassName("active");
        currentTab[0].className = currentTab[0].className.replace(" active", "");
        let currentPage = document.getElementsByClassName("view");
        currentPage[0].className = currentPage[0].className.replace("view", "hide");
        
        // selecting/showing new active tab
        tabs[i].className += " active";
        let selected = <HTMLElement> document.getElementsByClassName(tabs[i].className)[0] as HTMLElement;
        selected.innerText.includes("-") ?  name = selected.innerText.replace(" - ", "") : name = selected.innerText;
        let selectedPage = document.getElementById(name);
        selectedPage.className = selectedPage.className.replace("hide", "view");

        // injecting new active tab's iframe where appropriate
        if (selectedPage.id != "Free Text Analysis") {
          let iframe = selectedPage.getElementsByTagName("iframe")[0].id;
          let data = this.dataMap.get(iframe);
          this.injectHTML(iframe, data)
        }
      });
    }
  }

  public injectHTML(id: string, data: string): void {
    if (data == undefined) {
      const iFrameContainerId = id + '-box';
      let iFrameContainer = <HTMLDivElement>document.getElementById(iFrameContainerId) as HTMLDivElement;
      iFrameContainer.setAttribute("style", "display: none");
    } else {
      let iframe = <HTMLIFrameElement>document.getElementById(id) as HTMLIFrameElement;
      let injectHTML = iframe.contentWindow.document;
      injectHTML.open();
      injectHTML.write(data);
      injectHTML.close();   
      this.resizeIFrameToFitContent(iframe)
    }
  }

  public resizeIFrameToFitContent(iFrame: any): void {
    iFrame.width = iFrame.contentWindow.document.body.scrollWidth + "px";
    iFrame.height = iFrame.contentWindow.document.body.scrollHeight + "px";
  }

}
