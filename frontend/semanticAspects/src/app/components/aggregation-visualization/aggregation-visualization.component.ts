import { Component, Input } from '@angular/core';
import { AggregationRepresentants } from 'src/app/models/aggregation';


@Component({
  selector: 'app-aggregation-visualization',
  templateUrl: './aggregation-visualization.component.html',
  styleUrls: ['./aggregation-visualization.component.scss']
})
export class AggregationVisualizationComponent {

  @Input()
  aggregationName: string;

  @Input()
  aggregationRepresentants: AggregationRepresentants[];

  constructor() { }
}
