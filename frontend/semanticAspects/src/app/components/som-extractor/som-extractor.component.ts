import { Component, Input, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { FileModel } from '../../models/fileModel';
import { ErrorSnackbarComponent } from '../snackbars/error-snackbar/error-snackbar.component';

@Component({
  selector: 'app-som-extractor',
  templateUrl: './som-extractor.component.html',
  styleUrls: ['./som-extractor.component.scss']
})
export class SomExtractorComponent implements OnInit {

  @Input()
  somTemplateFile: FileModel;

  somTemplateFormGroup: FormGroup;

  constructor(private matSnackBar: MatSnackBar, private formBuilder: FormBuilder) { }

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
      } else {
        ErrorSnackbarComponent.openSnackBar(this.matSnackBar, 'Error: som template is undefined!');
      }
    } else {
      ErrorSnackbarComponent.openSnackBar(this.matSnackBar, 'Error: please fill SOM template form correctly!');
    }
  }
}
