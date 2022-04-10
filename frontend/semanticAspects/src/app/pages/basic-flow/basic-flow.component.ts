import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ErrorSnackbarComponent } from 'src/app/components/snackbars/error-snackbar/error-snackbar.component';
import { InfoSnackbarComponent } from 'src/app/components/snackbars/info-snackbar/info-snackbar.component';
import { SuccessSnackbarComponent } from 'src/app/components/snackbars/success-snackbar/success-snackbar.component';
import { AutomatizationResult } from 'src/app/models/automatizationResult';
import { FileModel } from 'src/app/models/fileModel';
import { SenseApiManagerService } from 'src/app/services/senseAnalysis/sense-api-manager.service';
import { SharedFilesForAnalysisService } from 'src/app/services/shared-files-for-analysis.service';
import { AutomatizationComponent } from '../automatization/automatization.component';

@Component({
  selector: 'app-basic-flow',
  templateUrl: './basic-flow.component.html',
  styleUrls: ['./basic-flow.component.scss']
})
export class BasicFlowComponent implements OnInit {

  isLinear = false;
  automatizationResultSenseAnalysis: AutomatizationResult = null;
  senseBasedMethodFromGroup: FormGroup;
  senseFormGroup: FormGroup;
  fileFormGroup: FormGroup;
  processFiles = true;
  spinnerVisibility = false;
  numberAnalyzedWords = 8;

  constructor(private formBuilder: FormBuilder,
              private matSnackbar: MatSnackBar,
              private senseApiManagerService: SenseApiManagerService) {}

  public formatScoreLabel(value: number): number {
    return AutomatizationComponent.roundNumberToPlaces(value, 2);
  }

  public ngOnInit(): void {
    this.fileFormGroup = this.formBuilder.group({
      firstCtrl: ['', Validators.required]
    });
    this.senseFormGroup = this.formBuilder.group({
      secondCtrl: ['', Validators.required]
    });
    this.senseBasedMethodFromGroup = this.formBuilder.group({
      numberAnalyzedWords: [8, Validators.required],
      chosenFile: ['', Validators.required]
    });
  }

  getUploadedFiles(): any[] {
    if (this.processFiles && SharedFilesForAnalysisService.getUploadedFiles()[0] !== undefined) {
      if (SharedFilesForAnalysisService.getUploadedFiles()[0].progress === 100) {
       // SharedFilesForAnalysisService.getUploadedFiles()[0].text().then(content => console.log(content));
        this.processFiles = false;
      }
    }
    return SharedFilesForAnalysisService.getUploadedFiles();
  }

  public formatLabel(value: number): string {
    if (value >= 100) {
      return Math.round(value / 100) + ' words';
    }

    return value.toString();
  }

  public updateApply($event, loadedFile: FileModel): void {

  }

  public applyConfigurationAndStartAnalysis(): void {
    if (this.senseBasedMethodFromGroup.valid) {
      InfoSnackbarComponent.openSnackBar(this.matSnackbar, 'Methods execution according configuration started!');
      this.spinnerVisibility = true;
      const file = this.getUploadedFiles()[this.senseBasedMethodFromGroup.controls.chosenFile.value];
      const numberAnalyzedWords = this.senseBasedMethodFromGroup.controls.numberAnalyzedWords.value;
      this.senseApiManagerService.senseAnalysis(file.textResult, numberAnalyzedWords).then(
        result => {
          SuccessSnackbarComponent.openSnackBar(this.matSnackbar, 'Configured sense analysis has been performed!');
          this.automatizationResultSenseAnalysis = {
            fileName: file.name,
            category: null,
            categories: null,
            categories_with_scores: result.results,
            analyzed_text: file.textResult,
            concepts_with_scores: null,
            unprocessed_text: null,
            interesting_parts: null,
            links: null,
            mappings: null,
            readability_metrics: null,
            readability_indexes: null,
            co_occurrence_aggregations: null
          };
          this.spinnerVisibility = false;
        }).catch(error => console.log('Error: ' + error));
    } else {
      ErrorSnackbarComponent.openSnackBar(this.matSnackbar, 'Error: form is not valid!');
    }
  }
}
