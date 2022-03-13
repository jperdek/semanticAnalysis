import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SelectFilesForGivenOperationComponent } from './select-files-for-given-operation.component';

describe('SelectFilesForGivenOperationComponent', () => {
  let component: SelectFilesForGivenOperationComponent;
  let fixture: ComponentFixture<SelectFilesForGivenOperationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SelectFilesForGivenOperationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SelectFilesForGivenOperationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
