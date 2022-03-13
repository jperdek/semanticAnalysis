import { TestBed } from '@angular/core/testing';

import { ReadabilityAnalysisService } from './readability-analysis.service';

describe('ReadabilityAnalysisService', () => {
  let service: ReadabilityAnalysisService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ReadabilityAnalysisService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
