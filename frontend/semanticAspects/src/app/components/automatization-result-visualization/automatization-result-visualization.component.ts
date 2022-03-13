import { Component, Input, OnInit } from '@angular/core';
import { AutomatizationResult } from 'src/app/models/automatizationResult';
import { Sort } from '@angular/material/sort';
import { SenseRating } from '../../models/senseRating';

@Component({
  selector: 'app-automatization-result-visualization',
  templateUrl: './automatization-result-visualization.component.html',
  styleUrls: ['./automatization-result-visualization.component.css']
})
export class AutomatizationResultVisualizationComponent implements OnInit {

  @Input()
  automatizationResult: AutomatizationResult;

  constructor() { }

  ngOnInit(): void {
  }

  public sortData(sort: Sort, ratings: SenseRating[]): SenseRating[] {
    console.log(ratings);
    const data = ratings.slice();
    if (!sort.active || sort.direction === '') {
      const newData1 = data;
      return newData1;
    }

    const newData2 = data.sort((a, b) => {
      const isAsc = sort.direction === 'asc';
      switch (sort.active) {
        case 'category': return this.compare(a.category, b.category, isAsc);
        case 'value': return this.compare(a.value, b.value, isAsc);
        default: return 0;
      }
    });
    return newData2;
  }

  public compare(a: number | string, b: number | string, isAsc: boolean): number {
    return (a < b ? -1 : 1) * (isAsc ? 1 : -1);
  }
}
