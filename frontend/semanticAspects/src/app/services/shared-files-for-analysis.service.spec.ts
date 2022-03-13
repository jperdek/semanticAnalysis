import { TestBed } from '@angular/core/testing';

import { SharedFilesForAnalysisService } from './shared-files-for-analysis.service';

describe('SharedFilesForAnalysisService', () => {
  let service: SharedFilesForAnalysisService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SharedFilesForAnalysisService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
