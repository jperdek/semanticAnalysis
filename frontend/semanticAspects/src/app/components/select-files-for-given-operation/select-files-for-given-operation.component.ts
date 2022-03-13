import { Input } from '@angular/core';
import { Component } from '@angular/core';
import { MatCheckboxChange } from '@angular/material/checkbox';
import { FileModel } from '../../models/fileModel';

@Component({
  selector: 'app-select-files-for-given-operation',
  templateUrl: './select-files-for-given-operation.component.html',
  styleUrls: ['./select-files-for-given-operation.component.css']
})
export class SelectFilesForGivenOperationComponent {

  @Input()
  files: FileModel[];

  @Input()
  segmentation: boolean;

  @Input()
  segmentationMethodName: string;

  public updateApply($event: MatCheckboxChange, fileModel: FileModel): void {
    if ($event.checked === false && !fileModel.disallowedMethods.includes(this.segmentationMethodName)) {
      fileModel.disallowedMethods.push(this.segmentationMethodName);
    }
    else {
      fileModel.disallowedMethods = fileModel.disallowedMethods.filter(element => element !== this.segmentationMethodName);
    }
  }
}
