import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SemanticAspectOverviewComponent } from './semantic-aspect-overview.component';

describe('SemanticAspectOverviewComponent', () => {
  let component: SemanticAspectOverviewComponent;
  let fixture: ComponentFixture<SemanticAspectOverviewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SemanticAspectOverviewComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SemanticAspectOverviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
