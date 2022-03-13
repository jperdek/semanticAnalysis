import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AutomatizationResultVisualizationComponent } from './automatization-result-visualization.component';

describe('AutomatizationResultVisualizationComponent', () => {
  let component: AutomatizationResultVisualizationComponent;
  let fixture: ComponentFixture<AutomatizationResultVisualizationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AutomatizationResultVisualizationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AutomatizationResultVisualizationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
