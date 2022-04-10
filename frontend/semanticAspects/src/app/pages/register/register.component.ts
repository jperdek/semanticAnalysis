import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { ErrorSnackbarComponent } from 'src/app/components/snackbars/error-snackbar/error-snackbar.component';
import { InfoSnackbarComponent } from 'src/app/components/snackbars/info-snackbar/info-snackbar.component';
import { Role } from 'src/app/models/role';
import { User } from 'src/app/models/user';
import { OktaRegisterService } from 'src/app/services/authentification/okta-register.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {


  form: FormGroup;

  constructor(private matSnackBar: MatSnackBar,
              private oktaRegisterService: OktaRegisterService,
              private router: Router) { }

  ngOnInit(): void {
    this.form = new FormGroup({
      name: new FormControl('', [Validators.required]),
      password: new FormControl('', [Validators.required]),
      email: new FormControl('', [Validators.required]),
      confirmPassword: new FormControl('', [Validators.required]),
    });
  }

  public registerUser(): void {
    console.log(this.form.status);
    if (this.form.status !== 'INVALID') {
      const password = this.form.controls.password.value;
      if (password !== this.form.controls.confirmPassword.value){
        ErrorSnackbarComponent.openSnackBar(this.matSnackBar, 'Error: passwords not match!');
        return;
      }
      const user: User = {
        id: '',
        name: this.form.controls.name.value,
        password,
        email: this.form.controls.email.value,
        role: Role.User,
     };
      InfoSnackbarComponent.openSnackBar(this.matSnackBar, 'Registering...');
      this.oktaRegisterService.registerUser(user, password);
      this.router.navigate(['/login']);
    }
    else {
      ErrorSnackbarComponent.openSnackBar(this.matSnackBar, 'Error: form is not valid!');
    }
  }
}
