import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { environment } from 'src/environments/environment';
import { AuthenticationService } from '../../services/authentification/authentication.service';
import { OktaAuthService } from '../../services/authentification/okta-auth.service';

@Component({
  selector: 'app-navigation',
  templateUrl: './navigation.component.html',
  styleUrls: ['./navigation.component.css']
})
export class NavigationComponent implements OnInit {

  constructor(
    private oktaAuth: OktaAuthService,
    private router: Router,
    private authenticationService: AuthenticationService) {
      router.events.subscribe((val) => {
        this.oktaAuth.isAuthenticated().then(isAuthenticated => {
          if (isAuthenticated) {
            this.logged = true;
          } else {
            this.logged = false;
          }
        });
      });
  }

  logged = false;
  useOcta = true;

  public ngOnInit(): void {
    this.useOcta = environment.useOcta;
    this.oktaAuth.isAuthenticated().then(isAuthenticated => {
      if (isAuthenticated) {
        this.logged = true;
      } else {
        this.logged = false;
      }
    });
  }

  public logout(): void {
    this.oktaAuth.logout();
    this.authenticationService.logout();
    this.router.navigate(['/']);
  }

  public isLogged(): boolean {
    return this.logged;
  }

  public hasAccessRights(pathParent: string): boolean{
      /*
      for(var dataPath of this.router.config){
          if(dataPath['path'] == pathParent){
            const routerData = dataPath as RouterData;
            const roles:Role[] = routerData.data.roles;
            if (roles && !roles.some(r => this.authenticationService.hasRole(r))) {
              //this.router.navigate(['error', 'not-found']);
              //this.router.navigate(['login']);
              return false;
            }
            return true;
          }
      }
      return true;
    }
  */
    return true;
  }
}
