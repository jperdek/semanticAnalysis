import { Component, Input } from '@angular/core';
import { Sort } from '@angular/material/sort';
import { CategoryRating } from 'src/app/models/category';

@Component({
  selector: 'app-table-clusters-visualization',
  templateUrl: './table-clusters-visualization.component.html',
  styleUrls: ['./table-clusters-visualization.component.scss']
})
export class TableClustersVisualizationComponent {

  @Input()
  categoryRating: CategoryRating[];

  @Input()
  mappings: any;

  constructor() { }

  openArray: boolean[] = [];

  public showRepresentantsMapping(category: string): void {
    if (category in this.mappings){
      return this.mappings[category];
    }
    return null;
  }

  public switchMappingVisibility(index: number): void {
    if (this.openArray === undefined || this.openArray.length !== this.categoryRating.length) {
      this.openArray = new Array(this.categoryRating.length).fill(false);
    }
    this.openArray[index] = !this.openArray[index];
  }

  public checkOpenedMapping(index: number): boolean {
    if (this.openArray === undefined || this.openArray.length !== this.categoryRating.length) {
      return false;
    }
    return this.openArray[index];
  }

  public sortData(sort: Sort, ratings: CategoryRating[]): CategoryRating[] {
    this.openArray = new Array(this.categoryRating.length).fill(false);

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
