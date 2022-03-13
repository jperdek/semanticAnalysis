import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CapturedResultComponent } from './captured-result.component';

describe('CapturedResultComponent', () => {
  let component: CapturedResultComponent;
  let fixture: ComponentFixture<CapturedResultComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CapturedResultComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CapturedResultComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
