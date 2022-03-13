import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { OktaAuthService } from '../../services/authentification/okta-auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  constructor(private oktaAuth: OktaAuthService, private router: Router) { }

  async ngOnInit(): Promise<any> {
    const isAuthenticated = await this.oktaAuth.isAuthenticated();
    if (isAuthenticated) {
      this.router.navigate(['/'], {replaceUrl: true});
    }
  }

  async login(event: Event): Promise<any> {
    event.preventDefault();
    const isAuthenticated = await this.oktaAuth.isAuthenticated();
    console.log(isAuthenticated);
    await this.oktaAuth.login('/');
  }

}
