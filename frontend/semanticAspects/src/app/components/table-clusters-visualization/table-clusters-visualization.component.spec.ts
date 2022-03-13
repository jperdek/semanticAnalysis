import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TableClustersVisualizationComponent } from './table-clusters-visualization.component';

describe('TableClustersVisualizationComponent', () => {
  let component: TableClustersVisualizationComponent;
  let fixture: ComponentFixture<TableClustersVisualizationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TableClustersVisualizationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TableClustersVisualizationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
