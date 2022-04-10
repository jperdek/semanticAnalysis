import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ErrorSnackbarComponent } from 'src/app/components/snackbars/error-snackbar/error-snackbar.component';
import { FileModel } from 'src/app/models/fileModel';
import { SharedFilesForAnalysisService } from 'src/app/services/shared-files-for-analysis.service';

// USED RESOURCE: https://github.com/progtarek/angular-drag-n-drop-directive
@Component({
  selector: 'app-file-upload',
  templateUrl: './file-upload.component.html',
  styleUrls: ['./file-upload.component.css', './file-upload.component.scss']
})
export class FileUploadComponent implements OnInit {

  filesToUpload: FileList | null = null;
  uploadedFiles: any[] = [];

  constructor(private matSnackBar: MatSnackBar) { }

  public ngOnInit(): void {
    SharedFilesForAnalysisService.setReference(this.uploadedFiles);
  }

  public handleFileInput(files: FileList): void {
      this.filesToUpload = files;
      this.printContent();

      this.uploadFilesSimulator(0);
  }

  public printContent(): void{
    for (let i = 0; i < this.filesToUpload.length; i++){
      const processedFile: FileModel = this.filesToUpload.item(i) as FileModel;
      processedFile.progress = 0;
      processedFile.showed = false;
      this.uploadedFiles.push(processedFile);
    }
  }

  public onFileDropped($event: Array<any>): void {
    this.prepareFilesList($event);
  }

  public fileBrowseHandler(files: Array<any>): void {
    this.prepareFilesList(files);
  }

  public deleteFile(index: number): void {
    if (this.uploadedFiles[index].progress < 100) {
      ErrorSnackbarComponent.openSnackBar(this.matSnackBar, 'Error: Cannot delete file, because upload is in progress.');
      return;
    }
    this.uploadedFiles.splice(index, 1);
  }

  public uploadFilesSimulator(fileIndex: number): void {
    setTimeout(() => {
      if (fileIndex === this.uploadedFiles.length) {
        return;
      } else {
        const progressInterval = setInterval(() => {
          if (this.uploadedFiles[fileIndex] === undefined || this.uploadedFiles[fileIndex].progress === 100) {
            clearInterval(progressInterval);
            this.uploadFilesSimulator(fileIndex + 1);
          } else {
            this.uploadedFiles[fileIndex].progress += 5;
          }
        }, 200);
      }
    }, 1000);
  }

  /**
   * Convert Files list to normal array list
   * @param files (Files List)
   */
  public prepareFilesList(files: Array<any>): void {
    for (const processedFile of files) {
      processedFile.progress = 0;
      this.uploadedFiles.push(processedFile);
    }
    this.uploadFilesSimulator(0);
  }

  private formatBytes(bytes: number, decimals = 2): string {
    if (bytes === 0) { return '0 Bytes'; }

    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];

    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
  }
}
