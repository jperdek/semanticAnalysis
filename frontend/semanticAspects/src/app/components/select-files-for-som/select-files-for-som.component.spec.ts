import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SelectFilesForSOMComponent } from './select-files-for-som.component';

describe('SelectFilesForSOMComponent', () => {
  let component: SelectFilesForSOMComponent;
  let fixture: ComponentFixture<SelectFilesForSOMComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SelectFilesForSOMComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SelectFilesForSOMComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
