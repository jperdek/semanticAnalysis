import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BasicFlowComponent } from './basic-flow.component';

describe('BasicFlowComponent', () => {
  let component: BasicFlowComponent;
  let fixture: ComponentFixture<BasicFlowComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BasicFlowComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BasicFlowComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
