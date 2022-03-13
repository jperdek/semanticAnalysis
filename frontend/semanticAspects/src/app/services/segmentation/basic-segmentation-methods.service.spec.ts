import { TestBed } from '@angular/core/testing';

import { BasicSegmentationMethodsService } from './basic-segmentation-methods.service';

describe('BasicSegmentationMethodsService', () => {
  let service: BasicSegmentationMethodsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(BasicSegmentationMethodsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
