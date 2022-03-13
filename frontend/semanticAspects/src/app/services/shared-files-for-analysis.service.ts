import { Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ErrorSnackbarComponent } from '../components/snackbars/error-snackbar/error-snackbar.component';
import { FileModel } from '../models/fileModel';

@Injectable({
  providedIn: 'root'
})
export class SharedFilesForAnalysisService {

  constructor() { }

  private static uploadedFiles: FileModel[] = [];

  public static setReference(uploadedFiles: FileModel[]): void {
    SharedFilesForAnalysisService.uploadedFiles = uploadedFiles;
  }

  public static async getUploadedFilesAsync(matSnackBar: MatSnackBar): Promise<FileModel[]> {
     for (const uploadedFile of SharedFilesForAnalysisService.uploadedFiles) {
      if (uploadedFile.textResult === null || uploadedFile.textResult === undefined) {
        try {
          const result = await SharedFilesForAnalysisService.getFileContent(uploadedFile);
          if (result !== undefined && result !== null) {
            uploadedFile.textResult = result;
          }
        } catch (error) {
          ErrorSnackbarComponent.openSnackBar(matSnackBar, error);
        }
      }
    }
     return SharedFilesForAnalysisService.uploadedFiles;
  }

  public static getUploadedFiles(): FileModel[] {
    return SharedFilesForAnalysisService.uploadedFiles;
  }

  public static getFileContent(loadedFile: FileModel): Promise<string> {
    if (loadedFile.text === null){
      if (loadedFile.textResult === undefined) {
        console.log('Error: content of file is not available!');
      }
    } else {
        return loadedFile.text();
    }
  }
}
