import { Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { CanActivate, ActivatedRouteSnapshot, Route, Router } from '@angular/router';
import { Observable } from 'rxjs';
import { ErrorSnackbarComponent } from 'src/app/components/snackbars/error-snackbar/error-snackbar.component';
import { Role } from 'src/app/models/role';
import { environment } from 'src/environments/environment';
import { AuthenticationService } from './authentication.service';


@Injectable({
  providedIn: 'root'
})
export class AuthGuardService implements CanActivate {

  constructor(private router: Router, private matSnackBar: MatSnackBar, private authenticationService: AuthenticationService) { }

  canActivate(route: ActivatedRouteSnapshot): Observable<boolean> | Promise<boolean> | boolean {
    if (!environment.useOcta){
      return true;
    }
    if (!this.authenticationService.isAuthorized()) {
      ErrorSnackbarComponent.openSnackBar(this.matSnackBar, 'Error: Not authorized! Please log in!');
      this.router.navigate(['login']);
      return false;
    }
    const roles = route.data.roles as Role[];
    if (roles && !roles.some(r => this.authenticationService.hasRole(r))) {
        // this.router.navigate(['error', 'not-found']);
        ErrorSnackbarComponent.openSnackBar(this.matSnackBar, 'Error: Not authorized! Please log in!');
        this.router.navigate(['login']);
        return false;
    }
    return true;
  }

  canLoad(route: Route): Observable<boolean> | Promise<boolean> | boolean {
      if (!environment.useOcta){
        return true;
      }
      if (!this.authenticationService.isAuthorized()) {
        ErrorSnackbarComponent.openSnackBar(this.matSnackBar, 'Error: Not authorized! Please log in!');
        return false;
      }
      const roles = route.data && route.data.roles as Role[];
      if (roles && !roles.some(r => this.authenticationService.hasRole(r))) {
          return false;
      }
      return true;
  }
}
