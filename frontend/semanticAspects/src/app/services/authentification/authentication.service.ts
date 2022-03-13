import { Injectable } from '@angular/core';
import { Role } from 'src/app/models/role';
import { UserRole } from 'src/app/models/user';


@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {

  constructor() { }

  private user: UserRole = new UserRole();

  public isAuthorized(): boolean {
      return this.user.role !== Role.Guest;
  }

  public hasRole(role: Role): boolean {
      return this.isAuthorized() && this.user.role === role;
  }

  public login(role: Role): void {
    this.user = { role };
  }

  public logout(): void {
    this.user =  { role: Role.Guest };
  }
}
