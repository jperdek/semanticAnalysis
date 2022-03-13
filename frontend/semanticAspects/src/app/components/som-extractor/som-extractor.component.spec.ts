import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SomExtractorComponent } from './som-extractor.component';

describe('SomExtractorComponent', () => {
  let component: SomExtractorComponent;
  let fixture: ComponentFixture<SomExtractorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SomExtractorComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SomExtractorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
