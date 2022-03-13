import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { OktaAuthService } from '@okta/okta-angular';


@Injectable({
  providedIn: 'root'
})
export class AuthManagerService {

  constructor(private oktaAuth: OktaAuthService, private http: HttpClient) { }

  async perform(method: string, apiPart: string, httpParameters: HttpParams, data = {}, additionalHeaders: any = {}): Promise<any> {
    // const accessToken = await this.oktaAuth.getAccessToken();
    const accessToken = 'debug';
    console.log(accessToken);
    const url = `http://localhost:5000${apiPart}?${httpParameters.toString()}`;
    console.log(url);
    console.log(httpParameters.toString());
    const headersData = Object.assign({}, {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${accessToken}`,
    }, additionalHeaders);

    const httpOptions = {
      headers: new HttpHeaders(headersData)
    };

    switch (method) {
      case 'delete':
        return this.http.delete(url, httpOptions).toPromise();
      case 'get':
        return this.http.get(url, httpOptions).toPromise();
      default:
        return this.http[method](url, data, httpOptions).toPromise();
    }
  }
}
