import { Injectable } from '@angular/core';
import * as Raven from 'raven-js';
import { environment } from 'src/environments/environment';
// import * as Sentry from "@sentry/browser";  // newest  packages, but more monitoring


@Injectable({
  providedIn: 'root'
})
export class LogginErrorsService {

  private readonly disabled = false;
  private readonly enableInAllEnvironments = false;
  constructor() { }

  private basicCheck(): boolean {
    return (environment.production || this.enableInAllEnvironments) && !this.disabled;
  }

  public captureError(error: any): void {
    if (this.basicCheck()){
      Raven.captureException(error.originalError || error);
    }
  }
}
