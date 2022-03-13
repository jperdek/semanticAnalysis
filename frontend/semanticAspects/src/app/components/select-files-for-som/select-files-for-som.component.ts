import { Component, Input } from '@angular/core';
import { MatCheckboxChange } from '@angular/material/checkbox';
import { MatRadioChange } from '@angular/material/radio';
import { SOMUsageType } from 'src/app/models/somSettings';
import { FileModel } from '../../models/fileModel';

@Component({
  selector: 'app-select-files-for-som',
  templateUrl: './select-files-for-som.component.html',
  styleUrls: ['./select-files-for-som.component.scss']
})
export class SelectFilesForSOMComponent {

  @Input()
  files: FileModel[];

  @Input()
  segmentation: boolean;

  @Input()
  segmentationMethodName: string;

  public updateApply($event: MatCheckboxChange, fileModel: FileModel): void {
      if ($event.checked === false && !fileModel.disallowedMethods.includes(this.segmentationMethodName)) {
        fileModel.disallowedMethods.push(this.segmentationMethodName);
      } else {
        fileModel.disallowedMethods = fileModel.disallowedMethods.filter(element => element !== this.segmentationMethodName);
      }
  }

  public updateSOMType($event: MatRadioChange, fileModel: FileModel): void {
    const domainOrSegmentationValue = $event.value;
    if (domainOrSegmentationValue === 'domainRepresentant') {
      fileModel.somSettings = {
        usageType: SOMUsageType.forDomain
      };
    } else if (domainOrSegmentationValue === 'segmentation') {
      fileModel.somSettings = {
        usageType: SOMUsageType.forTest
      };
    } else {
      console.log('Error: unknown som option!');
    }
  }

  public updateRecord($event: Event, fileModel: FileModel): void {
    if (fileModel.textResult === undefined) {
      console.log('Please load content of file before saving hiting eye button');
      return;
    }

    // this.updateApply($event, index, fileModel);
    // this.updateSOMType($event, fileModel);

    $event.preventDefault();
    $event.stopPropagation();
  }
}
