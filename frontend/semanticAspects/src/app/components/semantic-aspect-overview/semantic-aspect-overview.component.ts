import { Component, Input, OnInit } from '@angular/core';
import { Aggregation, AggregationStructure } from 'src/app/models/aggregation';
import { AutomatizationResult } from 'src/app/models/automatizationResult';
import { CategoryRating } from 'src/app/models/category';
import { AutomatizationComponent } from 'src/app/pages/automatization/automatization.component';

@Component({
  selector: 'app-semantic-aspect-overview',
  templateUrl: './semantic-aspect-overview.component.html',
  styleUrls: ['./semantic-aspect-overview.component.scss']
})
export class SemanticAspectOverviewComponent implements OnInit {

  @Input()
  automatizationResult: AutomatizationResult;
  panelOpenState = true;

  constructor() { }

  ngOnInit(): void {
  }

  public formatScoreLabel(value: number): number {
    return AutomatizationComponent.roundNumberToPlaces(value, 2);
  }

  public getMinScore(text: string): number {
    let minScore = 10000000;
    const scores = text.match(/score=([\"\'][^\"\']+[\"\'])/g);
    if (scores !== null) {
      for (const scoreString of scores){
          const score = Number(scoreString.split('"')[1]);
          if (minScore > score) {
              minScore = score;
          }
      }
    }
    return minScore;
  }

  public getMaxScore(text: string): number {
    let maxScore = 0.0;
    const scores = text.match(/score=([\"\'][^\"\']+[\"\'])/g);

    if (scores !== null) {
      for (const scoreString of scores){
          const score = Number(scoreString.split('"')[1]);
          if (maxScore < score) {
              maxScore = score;
          }
      }
    }
    return maxScore;
  }

  public scoreOnSlideChange1(threshold: number, automatizationResult: AutomatizationResult): void {
    let finalString = '';
    const tagParts = automatizationResult.analyzed_text.match(
      /([^<])+<\s*p\s+score=[\"\'][^\"\']+[\"\']\s+class=[\"\'][^\"\']+[\"\']\s*>[^<]+<\s*\/p\s*>/g);
    for (const tagPart of tagParts){
        const score = Number(tagPart.split('score="')[1].split('"')[0]);
        if (score >= threshold) {
            finalString = finalString + tagPart.replace(/class=[\"\'][^\"\']+[\"\']/, 'class="relevant-word chosen-relevant-word"');
        } else {
          finalString = finalString + tagPart.replace(/class=[\"\'][^\"\']+[\"\']/, 'class="relevant-word deny-relevant-word"');
        }
    }
    automatizationResult.analyzed_text = finalString;
  }

  public scoreOnSlideChange(threshold: number, automatizationResult: AutomatizationResult): void {
    const domParser = new DOMParser();
    const htmlElement = domParser.parseFromString('<div id="DOMWRAP">' + automatizationResult.analyzed_text + '</div>', 'text/html');
    const relevantElements = htmlElement.getElementsByClassName('relevant-word');

    Array.from(relevantElements).forEach((relevantElement: Element) => {
        const score = Number(relevantElement.getAttribute('score'));
        if (score >= threshold) {
          relevantElement.classList.add('chosen-relevant-word');
          relevantElement.classList.remove('deny-relevant-word');
        } else {
          relevantElement.classList.add('deny-relevant-word');
          relevantElement.classList.remove('chosen-relevant-word');
        }
    });
    automatizationResult.analyzed_text = htmlElement.getElementById('DOMWRAP').innerHTML;
  }

}
