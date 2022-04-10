import { Injectable, Optional, SkipSelf } from '@angular/core';
import { OktaAuthService } from '@okta/okta-angular';
import { Role } from 'src/app/models/role';
import { UserRole } from 'src/app/models/user';


@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {

  user: UserRole;

  constructor(private oktaAuth: OktaAuthService, @Optional() @SkipSelf() sharedService?: AuthenticationService) {
    this.user = new UserRole(this.oktaAuth);
    if (sharedService) {
          throw new Error('Auth service already loaded!');
    }
  }

  public setRole(role: Role): void {
    this.user.role = role;
  }

  public isAuthorized(): boolean {
      return this.user.role !== Role.Guest;
  }

  public hasRole(role: Role): boolean {
      return this.isAuthorized() && this.user.role === role;
  }

  public login(role: Role): void {
    this.user.role = role;
  }

  public logout(): void {
    this.user.role = Role.Guest;
  }

  public isLogged(): boolean {
    return this.user !== undefined && this.user.role !== Role.Guest;
  }
}
