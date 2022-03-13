import { HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { FileModel } from 'src/app/models/fileModel';
import { AuthManagerService } from '../authentification/auth-manager.service';

@Injectable({
  providedIn: 'root'
})
export class SomSegmentationMethodService {

  private readonly somApiPart = '/segmentationAnalysis/SOM/';
  private readonly createSOM = 'createTree';
  private readonly updateSOM = 'updateTree';
  private readonly extractSOM = 'extractFromTree';

  constructor(private authManagerService: AuthManagerService) { }


  public createSOMTree(content: string): Promise<any> {
    const httpParameters = new HttpParams();

    return this.authManagerService.perform('post', this.somApiPart + this.createSOM, httpParameters, content);
  }

  public updateSOMTree(filesContent: string, templateContent: string): Promise<any> {
    const httpParameters = new HttpParams();
    const templateFileContent = this.mergeFilesWithTemplate(filesContent, templateContent);
    return this.authManagerService.perform('post', this.somApiPart + this.updateSOM, httpParameters, templateFileContent);
  }

  public extractFromSOMTree(templateContent: string, acceptPercentage: number): Promise<any> {
    const httpParameters = new HttpParams().set('accept_percentage', acceptPercentage.toString());
    return this.authManagerService.perform('post', this.somApiPart + this.extractSOM, httpParameters, templateContent);
  }

  public mergeFilesWithTemplate(filesContent: string, templateContent: string): string {
    return filesContent + '\n<----------DIVISION_OF_MANY_PAGES_AND_SOM_THREE----------->\n' + templateContent;
  }

  public mergeFileWithFileContent(filesContent: string, fileContent: string): string {
    return filesContent + '\n<----------DIVISION_OF_MANY_PAGES----------->\n' + fileContent;
  }

  public mergeContentFiles(files: FileModel[], contentType: string): string {
    let finalContent = null;
    files.forEach(file => {
      if (!file.disallowedMethods.includes('SOM')
      && (file.somSettings === undefined || file.somSettings.usageType === contentType)){
        if (finalContent === null) {
          finalContent = file.textResult;
        } else {
          finalContent = this.mergeFileWithFileContent(file.textResult, finalContent);
        }
      }
    });
    return finalContent;
  }
}
