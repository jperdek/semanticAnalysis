import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ReadabilityVisualizationComponent } from './readability-visualization.component';

describe('ReadabilityVisualizationComponent', () => {
  let component: ReadabilityVisualizationComponent;
  let fixture: ComponentFixture<ReadabilityVisualizationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ReadabilityVisualizationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ReadabilityVisualizationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
