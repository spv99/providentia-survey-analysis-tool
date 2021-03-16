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
  public options: CloudOptions;

  constructor(private analyticsService: AnalyticsService) { }

  ngOnInit() {
    this.changeActiveTab();
    this.analyticsService.getUnivariateBargraph().subscribe(data => {
      this.injectHTML("bargraphs", data);
    });

    this.analyticsService.getUnivariatePiechart().subscribe(data => {
      this.injectHTML("piecharts", data);
    });

    this.analyticsService.getUnivariateBoxPlot().subscribe(data => {
      this.injectHTML("boxplots", data);
    });

    this.analyticsService.getUnivariateWordmaps().subscribe(data => {
      // console.log(data)
      // this.wordCloudData = data[0][1];
      // this.options = {
      //   width: 1000,
      //   height: 400,
      //   overflow: false,
      // };
    
    });

    this.analyticsService.getBivariateClusteredBargraph().subscribe(data => {
      this.injectHTML("clustered-bargraph", data);
    });

    this.analyticsService.getBivariateStackedBargraph().subscribe(data => {
      this.injectHTML("stacked-bargraph", data);
    });

    this.analyticsService.getBivariateScatterPlot().subscribe(data => {
      this.injectHTML("scatter-plots", data);
    });

    this.analyticsService.getMultivariateSunburst().subscribe(data => {
      this.injectHTML("sunburst", data);
    });

    this.analyticsService.getMultivariateTreemap().subscribe(data => {
      this.injectHTML("treemap", data);
    });

  }

  public changeActiveTab(): void {
    let tabs = document.getElementsByClassName("hover");
    let name;
    for (let i = 0; i < tabs.length; i++) {
        tabs[i].addEventListener("click", function() {
        let currentTab = document.getElementsByClassName("active");
        currentTab[0].className = currentTab[0].className.replace(" active", "");
        let currentPage = document.getElementsByClassName("view");
        currentPage[0].className = currentPage[0].className.replace("view", "hide");
        
        this.className += " active";
        let selected = <HTMLElement> document.getElementsByClassName(this.className)[0] as HTMLElement;
        selected.innerText.includes("-") ?  name = selected.innerText.replace(" - ", "") : name = selected.innerText;
        let selectedPage = document.getElementById(name);
        selectedPage.className = selectedPage.className.replace("hide", "view");
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
    }
  }

}
