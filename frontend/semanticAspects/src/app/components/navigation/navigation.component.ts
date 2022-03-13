import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthenticationService } from '../../services/authentification/authentication.service';
import { Role } from '../../models/role';
import { RouterData } from '../../models/router';
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
    console.log(this.router.config);
  }

  public ngOnInit(): void {
  }

  public logout(): void {
    this.authenticationService.logout();
    this.oktaAuth.logout();
    this.router.navigate(['/']);
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
