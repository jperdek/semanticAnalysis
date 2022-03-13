import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TableCategoriesVisualizationComponent } from './table-categories-visualization.component';

describe('TableCategoriesVisualizationComponent', () => {
  let component: TableCategoriesVisualizationComponent;
  let fixture: ComponentFixture<TableCategoriesVisualizationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TableCategoriesVisualizationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TableCategoriesVisualizationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
