import { TestBed } from '@angular/core/testing';

import { OktaRegisterService } from './okta-register.service';

describe('OktaRegisterService', () => {
  let service: OktaRegisterService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(OktaRegisterService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
