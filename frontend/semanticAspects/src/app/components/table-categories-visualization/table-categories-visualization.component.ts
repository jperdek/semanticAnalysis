import { Component, Input, OnInit } from '@angular/core';
import { Sort } from '@angular/material/sort';
import { CategoryRating } from 'src/app/models/category';


@Component({
  selector: 'app-table-categories-visualization',
  templateUrl: './table-categories-visualization.component.html',
  styleUrls: ['./table-categories-visualization.component.scss']
})
export class TableCategoriesVisualizationComponent implements OnInit {

  @Input()
  categoryRating: CategoryRating[];

  constructor() { }

  ngOnInit(): void {
  }

  public sortData(sort: Sort, ratings: CategoryRating[]): CategoryRating[] {
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
