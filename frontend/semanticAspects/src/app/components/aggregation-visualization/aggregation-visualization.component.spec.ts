import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AggregationVisualizationComponent } from './aggregation-visualization.component';

describe('AggregationVisualizationComponent', () => {
  let component: AggregationVisualizationComponent;
  let fixture: ComponentFixture<AggregationVisualizationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AggregationVisualizationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AggregationVisualizationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
