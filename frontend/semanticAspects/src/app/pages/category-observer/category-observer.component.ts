import { Component } from '@angular/core';
import { ReadabilityAnalysisService } from '../../semanticAspects/readability/readability-analysis.service';

@Component({
  selector: 'app-category-observer',
  templateUrl: './category-observer.component.html',
  styleUrls: ['./category-observer.component.css']
})
export class CategoryObserverComponent {

  constructor(private readabilityAnalysisService: ReadabilityAnalysisService) { }
}
