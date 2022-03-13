import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SenseAnalysisComponent } from './sense-analysis.component';

describe('SenseAnalysisComponent', () => {
  let component: SenseAnalysisComponent;
  let fixture: ComponentFixture<SenseAnalysisComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SenseAnalysisComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SenseAnalysisComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
