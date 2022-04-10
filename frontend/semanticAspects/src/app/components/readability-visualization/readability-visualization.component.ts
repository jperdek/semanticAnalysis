import { Component, Input } from '@angular/core';
import { ReadabilityIndexes } from 'src/app/models/readability';


@Component({
  selector: 'app-readability-visualization',
  templateUrl: './readability-visualization.component.html',
  styleUrls: ['./readability-visualization.component.scss']
})
export class ReadabilityVisualizationComponent {

  @Input()
  readabilityIndexes: ReadabilityIndexes;
}
