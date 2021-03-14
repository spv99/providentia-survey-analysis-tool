import { Component, OnInit } from '@angular/core';
import { NgbModal, ModalDismissReasons } from '@ng-bootstrap/ng-bootstrap';
import { AnalyticsService } from './details-page.service';
import $ from "jquery";

@Component({
  selector: 'app-details-page',
  templateUrl: './details-page.component.html',
  styleUrls: ['./details-page.component.scss']
})

export class DetailsPageComponent implements OnInit {
  public data: any;
  public selectedBivarBargraph: string = '';
  public closeResult: string;
  public title: string;
  public modalIFrame: Document;

  constructor(private analyticsService: AnalyticsService, private modalService: NgbModal) { }

  ngOnInit() {
    // this.analyticsService.getUnivariateBargraph().subscribe(data => {
    //   this.injectHTML("bargraphs", data);
    // });

    // this.analyticsService.getUnivariatePiechart().subscribe(data => {
    //   this.injectHTML("piecharts", data);
    // });

    // this.analyticsService.getUnivariateBoxPlot().subscribe(data => {
    //   this.injectHTML("boxplots", data);
    // });

    // this.analyticsService.getBivariateClusteredBargraph().subscribe(data => {
    //   this.injectHTML("clustered-bargraph", data);
    // });

    // this.analyticsService.getBivariateStackedBargraph().subscribe(data => {
    //   this.injectHTML("stacked-bargraph", data);
    //   let iFrameContainer = <HTMLDivElement>document.getElementById("stacked-bargraph-box") as HTMLDivElement;
    //   iFrameContainer.setAttribute("style", "display: none");
    // });

    // this.analyticsService.getMultivariateSunburst().subscribe(data => {
    //   this.injectHTML("sunburst", data);
    // });

    // this.analyticsService.getMultivariateTreemap().subscribe(data => {
    //   this.injectHTML("treemap", data);
    // });
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
      this.resizeIFrameToFitContent(iframe);
    }
  }

  public resizeIFrameToFitContent(iFrame: any): void {
    iFrame.width = iFrame.contentWindow.document.body.scrollWidth;
    iFrame.height = iFrame.contentWindow.document.body.scrollHeight;
  }

  public selectChangeHandler(event: any): void {
    let hiddenBargraph = "";
    this.selectedBivarBargraph = event.target.value;

    // deselect other checkbox if another checkbox is selected
    if (this.selectedBivarBargraph === 'stacked-bargraph') {
      hiddenBargraph = 'clustered';
    } else if (this.selectedBivarBargraph === 'clustered-bargraph') {
      hiddenBargraph = 'stacked';
    }
    let checkbox = <HTMLInputElement>document.getElementById(hiddenBargraph) as HTMLInputElement;
    checkbox.checked = false;

    // if no checkboxes are selected check the last selected
    const clustered = <HTMLInputElement>document.getElementById('clustered') as HTMLInputElement;
    const stacked = <HTMLInputElement>document.getElementById('stacked') as HTMLInputElement;
    if (clustered.checked == false && stacked.checked == false) {
      if (this.selectedBivarBargraph.includes('clustered')) {
        clustered.checked = true;
      } else if (this.selectedBivarBargraph.includes('stacked')) {
        stacked.checked = true;
      }
    }

    // hide unselected bi_var bargraph
    const hiddenIFrameContainerId = hiddenBargraph + '-bargraph-box';
    let hiddenIFrameContainer = <HTMLDivElement>document.getElementById(hiddenIFrameContainerId) as HTMLDivElement;
    hiddenIFrameContainer.setAttribute("style", "display: none");

    // display selected bivar_bargraph
    const visibleIFrameContainerId = this.selectedBivarBargraph + '-box';
    let visibleIFrameContainer = <HTMLDivElement>document.getElementById(visibleIFrameContainerId) as HTMLDivElement;
    visibleIFrameContainer.setAttribute("style", "display: block");
  }

}
