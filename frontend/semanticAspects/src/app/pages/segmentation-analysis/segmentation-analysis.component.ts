import { Component, Input } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { SOMUsageType } from 'src/app/models/somSettings';
import { SomSegmentationMethodService } from 'src/app/services/segmentation/som-segmentation-method.service';
import { FileModel } from '../../models/fileModel';
import { BasicSegmentationMethodsService } from '../../services/segmentation/basic-segmentation-methods.service';

@Component({
  selector: 'app-segmentation-analysis',
  templateUrl: './segmentation-analysis.component.html',
  styleUrls: ['./segmentation-analysis.component.scss']
})
export class SegmentationAnalysisComponent {

  @Input()
  files: FileModel[];

  somTemplateFileReference: FileModel = {
    progress: 100,
    showed: true,
    textResult: undefined,
    appliedSegmentation: true,
    segmentationMethod: 'None',
    disallowedMethods: [],
    name: 'somTemplate',
    size: 1,
    type: 'text/plain',
    lastModified: Date.now().valueOf(),
    stream: null,
    arrayBuffer: null,
    slice: null,
    text: null,
    somSettings: undefined,
    webkitRelativePath: ''
  };

  cetdFormGroup: FormGroup;
  analyzeTemplateFormGroup: FormGroup;

  constructor(
    private formBuilder: FormBuilder,
    private basicSegmentationMethodsService: BasicSegmentationMethodsService,
    private somSegmentationMethod: SomSegmentationMethodService) {
    this.cetdFormGroup = this.formBuilder.group({
      cetdNormalMethod: ['', ],
      cetdEdgareMethod: ['', ],
      cetdVariantMethod: ['', ],
    });
    this.analyzeTemplateFormGroup = this.formBuilder.group({
      sliderPercentageFormControl: [0.5, {value: 0.5, disabled: false}],
    });
  }

  public useCETDSegmentation(): void {
    if (this.cetdFormGroup.valid){
      const methods = [];
      if (this.cetdFormGroup.controls.cetdNormalMethod.value){ methods.push('normal'); }
      if (this.cetdFormGroup.controls.cetdEdgareMethod.value){ methods.push('edgare'); }
      if (this.cetdFormGroup.controls.cetdVariantMethod.value){ methods.push('variant'); }
      for (const file of this.files){
        if (!file.disallowedMethods.includes('CETD')){
          this.basicSegmentationMethodsService.cetdExtractor(file.textResult, methods).then(result => {
            file.segmentationMethod = 'cetd';
            file.appliedSegmentation = true;
            file.textResult = JSON.stringify(result);
            console.log(result);
          }).catch(error => console.log('Error occured during cetd analysis: ' + error));
        }
      }
    } else {
      console.log('Error: cetd form group is invalid!');
    }
  }

  public useTextSegmentation(): void {
    for (const file of this.files){
      if (!file.disallowedMethods.includes('all_text')){
        this.basicSegmentationMethodsService.textExtractor(file.textResult).then(result => {
          file.segmentationMethod = 'all_text';
          file.appliedSegmentation = true;
          file.textResult = JSON.stringify(result);
          console.log(result);
        }).catch(error => console.log('Error occured during text analysis: ' + error));
      }
    }
  }

  public useSOMSegmentation(): void {
    const mergedFiles = this.somSegmentationMethod.mergeContentFiles(this.files, SOMUsageType.forDomain);
    if (this.somTemplateFileReference.textResult === undefined) {
      this.somSegmentationMethod.createSOMTree(mergedFiles).then(result => {
        console.log(result);
      }).catch(error => console.log('Error occured during SOM segmentation analysis: ' + error));
    } else {
      this.somSegmentationMethod.updateSOMTree(mergedFiles, this.somTemplateFileReference.textResult).then(result => {
        console.log(result);
      }).catch(error => console.log('Error occured during SOM segmentation analysis: ' + error));
    }
  }

  public somTemplateResults(): void {
    const mergedFiles = this.somSegmentationMethod.mergeContentFiles(this.files, SOMUsageType.forDomain);
    if (this.somTemplateFileReference.textResult === undefined) {
      this.somSegmentationMethod.createSOMTree(mergedFiles).then(result => {
        console.log(result);
      }).catch(error => console.log('Error occured during SOM segmentation analysis: ' + error));
    } else {
      this.somSegmentationMethod.updateSOMTree(mergedFiles, this.somTemplateFileReference.textResult).then(result => {
        console.log(result);
      }).catch(error => console.log('Error occured during SOM segmentation analysis: ' + error));
    }
  }

  public analyzeTemplate(): void {
    if (this.analyzeTemplateFormGroup.valid) {
      const acceptPercentage = this.analyzeTemplateFormGroup.controls.sliderPercentageFormControl.value;
      if (this.somTemplateFileReference.textResult !== undefined) {
        this.somSegmentationMethod.extractFromSOMTree(this.somTemplateFileReference.textResult, acceptPercentage).then(result => {
          console.log(result);
        }).catch(error => console.log('Error occured during SOM template analysis: ' + error));
      } else {
        console.log('Error: cant analyzed empty template')
      }
    } else {
      console.log('Error: form for template analysis is invalid');
    }
  }

  public formatPercentageLabel(value: number): string {
    return value.toString();
  }
}
