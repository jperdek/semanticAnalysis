import { TestBed } from '@angular/core/testing';

import { SenseApiManagerService } from './sense-api-manager.service';

describe('SenseApiManagerService', () => {
  let service: SenseApiManagerService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SenseApiManagerService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
