import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Role } from 'src/app/models/role';
import { AuthenticationService } from 'src/app/services/authentification/authentication.service';
import { OktaAuthService } from '../../services/authentification/okta-auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  constructor(private oktaAuth: OktaAuthService,
              private router: Router,
              private authenticationService: AuthenticationService) { }

  async ngOnInit(): Promise<any> {
    const isAuthenticated = await this.oktaAuth.isAuthenticated();
    if (isAuthenticated) {
      this.authenticationService.setRole(Role.User);
      this.router.navigate(['/'], {replaceUrl: true});
    } else {
      this.authenticationService.setRole(Role.Guest);
    }
  }

  public login(event: Event) {
    event.preventDefault();
    this.oktaAuth.isAuthenticated().then(isAuthenticated => {
      if (isAuthenticated) {
        this.authenticationService.setRole(Role.User);
      } else {
        this.authenticationService.setRole(Role.Guest);
        this.oktaAuth.login('/').then(() => {
          this.authenticationService.setRole(Role.User);
        });
      }
    });
  }
}
