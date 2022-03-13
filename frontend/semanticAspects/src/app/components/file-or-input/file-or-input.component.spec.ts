import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FileOrInputComponent } from './file-or-input.component';

describe('FileOrInputComponent', () => {
  let component: FileOrInputComponent;
  let fixture: ComponentFixture<FileOrInputComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FileOrInputComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FileOrInputComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
