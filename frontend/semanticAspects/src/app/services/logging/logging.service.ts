import { Injectable } from '@angular/core';
import * as Raven from 'raven-js';
import { environment } from 'src/environments/environment';
// import * as Sentry from '@sentry/browser';

@Injectable({
  providedIn: 'root'
})
export class LoggingService {

  private readonly disabled = false;
  private readonly enableInAllEnvironments = true; // turn in with value true
  constructor() {}

  private basicCheck(): boolean {
    return (environment.production || this.enableInAllEnvironments) && !this.disabled;
  }

  public logInfo(informationToLog: string): void {
    if (this.basicCheck()){
      Raven.captureMessage(informationToLog, { level: 'warning' });
    }
  }

  public logJSONInfo(informationJSONToLog: any): void {
    this.logInfo(JSON.stringify(informationJSONToLog));
  }
}
