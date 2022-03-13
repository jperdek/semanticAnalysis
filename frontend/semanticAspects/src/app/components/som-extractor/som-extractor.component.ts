import { Component, Input, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { FileModel } from '../../models/fileModel';

@Component({
  selector: 'app-som-extractor',
  templateUrl: './som-extractor.component.html',
  styleUrls: ['./som-extractor.component.scss']
})
export class SomExtractorComponent implements OnInit {

  @Input()
  somTemplateFile: FileModel;

  somTemplateFormGroup: FormGroup;

  constructor(private formBuilder: FormBuilder) { }

  public ngOnInit(): void {
    this.somTemplateFormGroup = this.formBuilder.group({
      somTemplateFormControl: ['', ],
    });
  }

  public updateSOMTemplateFile(): void {
    if (this.somTemplateFormGroup.valid) {
      if (this.somTemplateFile !== undefined) {
        this.somTemplateFile.textResult = this.somTemplateFormGroup.controls.somTemplateFormControl.value;
        if (this.somTemplateFile.textResult === '') {
          this.somTemplateFile.textResult = undefined;
        }
        console.log(this.somTemplateFile);
      } else {
        console.log('Error: som template is undefined!');
      }
    } else {
      console.log('Error: form for SOM template is invalid!');
    }
  }
}
