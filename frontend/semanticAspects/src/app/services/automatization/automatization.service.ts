import { HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { AuthManagerService } from '../authentification/auth-manager.service';


@Injectable({
  providedIn: 'root'
})
export class AutomatizationService {

  private readonly automatizationApiPart = '/automatization';

  constructor(private authManagerService: AuthManagerService) { }

  public automatizationRequest(content: string, fileName: string): Promise<any> {
    const additionalHeaders = { use_html_tags: 'true'};
    const httpParameters = new HttpParams().set('fileName', fileName);

    return this.authManagerService.perform(
      'post', this.automatizationApiPart, httpParameters, content, additionalHeaders, true);
  }
}
