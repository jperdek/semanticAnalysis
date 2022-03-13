import { TestBed } from '@angular/core/testing';

import { SomSegmentationMethodService } from './som-segmentation-method.service';

describe('SomSegmentationMethodService', () => {
  let service: SomSegmentationMethodService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SomSegmentationMethodService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
