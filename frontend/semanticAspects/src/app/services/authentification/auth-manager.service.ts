import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { OktaAuthService } from '@okta/okta-angular';
import { ErrorSnackbarComponent } from 'src/app/components/snackbars/error-snackbar/error-snackbar.component';
import { environment } from 'src/environments/environment';


@Injectable({
  providedIn: 'root'
})
export class AuthManagerService {

  constructor(private oktaAuth: OktaAuthService, private matSnackBar: MatSnackBar, private http: HttpClient) { }

  private get baseUrl(): string {
    return environment.apiBaseUrl || 'http://localhost:5000';
  }

  async perform(method: string, apiPart: string,
                httpParameters: HttpParams, data = {},
                additionalHeaders: any = {},
                notUseOkta: boolean = false): Promise<any> {
    let accessToken;
    if (environment.useOcta && !notUseOkta){
      accessToken = await this.oktaAuth.getAccessToken();
    } else {
      accessToken = 'debug';
    }
    const url = `${this.baseUrl}${apiPart}?${httpParameters.toString()}`;
    if (environment.debug){
      console.log(url);
      console.log(httpParameters.toString());
    }

    const headersData = Object.assign({}, {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${accessToken}`,
    }, additionalHeaders);

    const httpOptions = {
      headers: new HttpHeaders(headersData)
    };
    try {
      switch (method) {
        case 'delete':
          return this.http.delete(url, httpOptions).toPromise();
        case 'get':
          return this.http.get(url, httpOptions).toPromise();
        default:
          return this.http[method](url, data, httpOptions).toPromise();
      }
    } catch (error) {
      ErrorSnackbarComponent.openSnackBar(this.matSnackBar, 'Error occurred while sending request!');
      if (environment.debug){ console.log(error); }
    }
  }
}
