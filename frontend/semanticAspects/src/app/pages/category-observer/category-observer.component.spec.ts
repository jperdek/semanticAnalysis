import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CategoryObserverComponent } from './category-observer.component';

describe('CategoryObserverComponent', () => {
  let component: CategoryObserverComponent;
  let fixture: ComponentFixture<CategoryObserverComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CategoryObserverComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CategoryObserverComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
