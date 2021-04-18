import { Component, OnInit } from '@angular/core';
import { AnalyticsService } from './details-page.service';
import { CloudData, CloudOptions } from 'angular-tag-cloud-module';
import { BivariateRelationship } from '../models/bivariate_relationship.model';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ProvidentiaService } from '../providentia/providentia.service';

@Component({
  selector: 'app-details-page',
  templateUrl: './details-page.component.html',
  styleUrls: ['./details-page.component.scss']
})

export class DetailsPageComponent implements OnInit  {
  public data: any;
  public wordCloudData: CloudData[];
  public dataMap = new Map();
  public bivariateRelationships: BivariateRelationship;
  public wordcloudImage: any;
  public form: FormGroup;
  public sentiment_text: string

  constructor(
    private analyticsService: AnalyticsService, 
    private formBuilder: FormBuilder,
    private router: Router,
    private localStorageService: ProvidentiaService) { }

  ngOnInit() {
    this.changeActiveTab();

    this.form = this.formBuilder.group({
      bargraph: [false],
      piechart: [false],
      boxplot: [false],
      sentimentAnalysis: [false],
      thematicAnalysis: [false],
      bivariateRelationship: [false],
      clusteredBargraph: [false],
      stackedBargraph: [false],
      scatterPlot: [false],
      sunburstChart: [false],
      treemapChart: [false]
    });

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
      // this.wordCloudData = data[1];    
      // console.log(this.wordCloudData)
      this.analyticsService.getUnivariateWordmaps().subscribe(data => {
        this.createImageFromBlob(data);
      });
    });

    this.analyticsService.getSentimentCharts().subscribe(data => {
      this.dataMap.set("sentiment-charts", data);
    });

    this.analyticsService.getThemesCharts().subscribe(data => {
      this.dataMap.set("themes-charts", data);
    });

    this.analyticsService.getBivariateRelationships().subscribe(data => {
      this.dataMap.set("bivariate-relationships", data);
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
        if (selectedPage.id != "Wordmaps" && selectedPage.id != "Insights Overview" && selectedPage.id != "Export Report") {
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

  public createImageFromBlob(image: Blob) {
    let reader = new FileReader();
    reader.addEventListener("load", () => {
       this.wordcloudImage = reader.result;
    }, false);
 
    if (image) {
       reader.readAsDataURL(image);
    }
 }

 public generatePreview(): void {
   this.localStorageService.clear();
    let serialisedForm = JSON.stringify(this.form.value);
    const formObject = JSON.parse(serialisedForm);
    const formControlNames = 
      [["bargraph", "bargraphs"],
      ["piechart", "piecharts"],
      ["boxplot", "boxplot"], 
      ["sentimentAnalysis", "sentiment-charts"],
      ["thematicAnalysis", "themes-charts"],
      ["bivariateRelationship", "bivariate-relationships"],
      ["clusteredBargraph", "clustered-bargraph"],
      ["stackedBargraph", "stacked-bargraph"], 
      ["scatterPlot", "scatter-plots"],
      ["sunburstChart", "sunburst"],
      ["treemapChart", "treemap"]];
    let selectedGraphs = []
    formControlNames.forEach(checkboxName => {
      if(formObject[checkboxName[0]] === true) {
        let element = <HTMLInputElement> document.querySelector("input[formControlName='" + checkboxName[0] + "']") as HTMLInputElement;
        selectedGraphs.push([element.value, checkboxName[1]]);
      }
    });
    selectedGraphs.forEach(selectedGraph => {
      let graph = document.getElementById(selectedGraph[0]);
      graph.className = graph.className.replace("hide", "view");
      this.localStorageService.set(selectedGraph[0], this.dataMap.get(selectedGraph[1]));
    });
    const link = 'providentia/results/preview';
    this.router.navigate([]).then(result => {  window.open(link, '_blank'); });
 }

}
