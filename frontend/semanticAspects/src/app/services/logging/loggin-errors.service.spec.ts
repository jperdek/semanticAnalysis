import { TestBed } from '@angular/core/testing';

import { LogginErrorsService } from './loggin-errors.service';

describe('LogginErrorsService', () => {
  let service: LogginErrorsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(LogginErrorsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
