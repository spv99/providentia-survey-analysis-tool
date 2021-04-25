import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'no-graph-view',
  templateUrl: './no-graph-view.component.html',
  styleUrls: ['./no-graph-view.component.scss']
})

export class NoGraphViewComponent implements OnInit{
  @Input() chart: string;

  ngOnInit() {
    if ((this.chart).includes("-")) {
      this.chart = this.chart.replace("-", " ");
    }
  }
}
