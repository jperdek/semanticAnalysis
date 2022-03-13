import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, Route, Router } from '@angular/router';
import { Observable } from 'rxjs';
import { Role } from 'src/app/models/role';
import { AuthenticationService } from './authentication.service';


@Injectable({
  providedIn: 'root'
})
export class AuthGuardService implements CanActivate {

  constructor(private router: Router, private authenticationService: AuthenticationService) { }

  canActivate(route: ActivatedRouteSnapshot): Observable<boolean> | Promise<boolean> | boolean {
    if (!this.authenticationService.isAuthorized()) {
      console.log('NOT AUTHORIZED');
      this.router.navigate(['login']);
      return false;
    }
    const roles = route.data.roles as Role[];
    if (roles && !roles.some(r => this.authenticationService.hasRole(r))) {
        // this.router.navigate(['error', 'not-found']);
        this.router.navigate(['login']);
        return false;
    }
    return true;
  }

  canLoad(route: Route): Observable<boolean> | Promise<boolean> | boolean {
      if (!this.authenticationService.isAuthorized()) {
        console.log('NOT AUTHORIZED');
        return false;
      }
      const roles = route.data && route.data.roles as Role[];
      if (roles && !roles.some(r => this.authenticationService.hasRole(r))) {
          return false;
      }
      return true;
  }
}
