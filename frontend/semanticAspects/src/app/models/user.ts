import { OktaAuthService } from '@okta/okta-angular';
import { Role } from './role';

export class UserRole {
  role: Role;

  constructor(private oktaAuth: OktaAuthService) {
    this.oktaAuth.isAuthenticated().then(isAuthenticated => {
      if (isAuthenticated) {
        this.role = Role.User;
      } else {
        this.role = Role.Guest;
      }
    });
  }
}

export interface User {
  id: string | undefined;
  name: string;
  email: string;
  password: string;
  role: Role;
}
