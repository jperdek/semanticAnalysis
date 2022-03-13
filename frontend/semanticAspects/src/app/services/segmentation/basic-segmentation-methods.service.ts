import { HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { AuthManagerService } from '../authentification/auth-manager.service';

@Injectable({
  providedIn: 'root'
})
export class BasicSegmentationMethodsService {

  private readonly cetdApiPart = '/segmentationAnalysis/CETD/';
  private readonly textApiPart = '/segmentationAnalysis/text';

  constructor(private authManagerService: AuthManagerService) { }

  public cetdExtractor(content: string, methods: string[]): Promise<any> {
    const httpParameters = new HttpParams();

    if (methods.length === 0) {
      return this.authManagerService.perform('post', this.cetdApiPart + 'all', httpParameters, content);
    } else {
      return this.authManagerService.perform('post', this.cetdApiPart + methods.toString(), httpParameters, content);
    }
  }

  public textExtractor(content: string): Promise<any> {
    const httpParameters = new HttpParams();

    return this.authManagerService.perform('post', this.textApiPart, httpParameters, content);
  }
}
