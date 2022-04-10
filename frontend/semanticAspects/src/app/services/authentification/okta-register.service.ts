import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { User } from 'src/app/models/user';
import { environment } from 'src/environments/environment';
import * as bcrypt from 'bcryptjs';

@Injectable({
  providedIn: 'root'
})
export class OktaRegisterService {

  constructor(private http: HttpClient) { }

  private constructRegisterBody(user: User, openedPassword: string): any {
    const workFactor = 10;
    const salt = bcrypt.genSaltSync(workFactor);
    const onlySalt = salt.split('$')[3].substring(0, 22);
    user.password = bcrypt.hashSync(openedPassword, salt);
    user.password = user.password.substring(user.password.indexOf(onlySalt) + 22, user.password.length);

    const nameParts = user.name.split(' ');
    let firstName: string;
    let lastName: string;
    if (nameParts.length > 1){
      firstName = user.name;
      lastName = '';
    } else {
      firstName = nameParts[0];
      lastName = nameParts[1];
    }

    return {
      profile: {
        firstName: user.name,
        lastName: user.name.split(' ')[1],
        email: user.email,
        login: user.email,
        mobilePhone: '555-415-1337'
      },
      credentials: {
        password : {
          hash: {
            algorithm: 'BCRYPT',
            workFactor,
            salt: onlySalt,
            value: user.password
          }
        }
      }
    };
  }

  private getHeadersData(): any {
    return {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      Authorization: 'SSWS ' + environment.octa_data.ssws_api_token
    };
  }
  public registerUser(user: User, openedPassword: string): void {
    const registerBody = this.constructRegisterBody(user, openedPassword);
    const httpOptions = {
      headers: new HttpHeaders(this.getHeadersData())
    };
    this.http.post(environment.octa_data.register_address, registerBody, httpOptions).toPromise().then((result: any) => {
    });
  }
}
