import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AutomatizationService } from 'src/app/services/automatization/automatization.service';
import { SharedFilesForAnalysisService } from 'src/app/services/shared-files-for-analysis.service';
import { FileModel } from 'src/app/models/fileModel';
import { AutomatizationResult } from 'src/app/models/automatizationResult';
import { ReadabilityAnalysisService } from 'src/app/semanticAspects/readability/readability-analysis.service';
import { ReadabilityIndexes } from 'src/app/models/readability';
import { LoggingService } from 'src/app/services/logging/logging.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { InfoSnackbarComponent } from 'src/app/components/snackbars/info-snackbar/info-snackbar.component';
import { UserFeedbackComponent } from 'src/app/components/snackbars/user-feedback/user-feedback.component';
import { ErrorSnackbarComponent } from 'src/app/components/snackbars/error-snackbar/error-snackbar.component';
import { environment } from 'src/environments/environment';
import { SuccessSnackbarComponent } from 'src/app/components/snackbars/success-snackbar/success-snackbar.component';
import { CategoryRating } from 'src/app/models/category';
import { Aggregation, AggregationRepresentants } from 'src/app/models/aggregation';


@Component({
  selector: 'app-automatization',
  templateUrl: './automatization.component.html',
  styleUrls: ['./automatization.component.scss']
})
export class AutomatizationComponent implements OnInit {

  constructor(private formBuilder: FormBuilder,
              private automatizationService: AutomatizationService,
              private readabilityService: ReadabilityAnalysisService,
              private loggingeService: LoggingService,
              private feedbackBar: MatSnackBar,
              private matSnackBar: MatSnackBar) {}

  isLinear = false;
  spinnerVisibility = false;
  senseFormGroup: FormGroup;
  fileFormGroup: FormGroup;
  automatizationResults: AutomatizationResult[] = [];

  public static roundNumberToPlaces(numbertobeRound: number, decimalplaces: number): number {
    return Math.round(numbertobeRound * Math.pow(10, decimalplaces)) / Math.pow(10, decimalplaces);
  }

  public ngOnInit(): void {
    this.fileFormGroup = this.formBuilder.group({
      firstCtrl: ['', Validators.required]
    });
    this.senseFormGroup = this.formBuilder.group({
      secondCtrl: ['', Validators.required]
    });
  }

  public deleteAutomatizedResult(automatizedResultIndex: number): void {
    this.automatizationResults = this.automatizationResults.splice(automatizedResultIndex + 1, 1);
  }

  public analyzeReadabilityMetris(text: string): ReadabilityIndexes {
    return this.readabilityService.analyzeText(text, []);
  }

  getAutomatizationResults(): AutomatizationResult[] {
    return this.automatizationResults;
  }

  getUploadedFiles(): any[] {
    if (SharedFilesForAnalysisService.getUploadedFiles()[0] !== undefined) {
      if (SharedFilesForAnalysisService.getUploadedFiles()[0].progress === 100) {
       // SharedFilesForAnalysisService.getUploadedFiles()[0].text().then(content => console.log(content));
      }
    }
    return SharedFilesForAnalysisService.getUploadedFiles();
  }

  public formatLabel(value: number): string {
    return value.toString();
  }

  public copyAutomatizationResultData(automatizationResultData: AutomatizationResult): AutomatizationResult {
    return {
      fileName: automatizationResultData.fileName,
      category: automatizationResultData.category,
      categories: automatizationResultData.categories,
      categories_with_scores: automatizationResultData.categories_with_scores,
      concepts_with_scores: automatizationResultData.concepts_with_scores,
      analyzed_text: automatizationResultData.analyzed_text,
      unprocessed_text: automatizationResultData.unprocessed_text,
      interesting_parts: automatizationResultData.interesting_parts,
      links: automatizationResultData.links,
      mappings: automatizationResultData.mappings,
      readability_metrics: automatizationResultData.readability_metrics,
      readability_indexes: automatizationResultData.readability_indexes,
      co_occurrence_aggregations: automatizationResultData.co_occurrence_aggregations
    };
  }

  public applyAutomatization(): void {
    InfoSnackbarComponent.openSnackBar(this.matSnackBar, 'Started processing files. Please wait!');
    if (SharedFilesForAnalysisService.getUploadedFiles()[0] !== undefined) {
        this.spinnerVisibility = true;
        SharedFilesForAnalysisService.getUploadedFilesAsync(this.matSnackBar).then(uploadedFiles => {
          uploadedFiles.forEach((uploadedFile: FileModel, index: number) => {
            this.automatizationService.automatizationRequest(
              uploadedFile.textResult, uploadedFile.name).then((automatizationResultData: AutomatizationResult) => {
                const automatizationResult: AutomatizationResult = this.copyAutomatizationResultData(automatizationResultData);
                if (automatizationResult.co_occurrence_aggregations !== null && automatizationResult.co_occurrence_aggregations !== undefined) {
                  automatizationResult.co_occurrence_aggregations = this.getAggregationsStructure(
                    automatizationResult.co_occurrence_aggregations);
                }
                automatizationResult.readability_indexes = this.analyzeReadabilityMetris(uploadedFile.textResult);
                if (environment.debug){ console.log(automatizationResult); }
                this.automatizationResults.push(automatizationResult);
                SuccessSnackbarComponent.openSnackBar(this.matSnackBar, 'File: ' + uploadedFile.name + ' has been loaded!');
                this.spinnerVisibility = false;
                if (index === uploadedFiles.length - 1) {
                  setTimeout(() => this.getFeedback(uploadedFile), 1000);
                }
            }).catch(error => {
              this.spinnerVisibility = false;
              if (environment.debug){ console.log(error); }
              ErrorSnackbarComponent.openSnackBar(this.matSnackBar, 'Error occurred while loading file: ' + uploadedFile.name + '! Try again!');
            });
          });
        });
      }
  }

  private getFeedback(fileModel: FileModel): void {
    UserFeedbackComponent.openSnackBar(this.feedbackBar, 'Provide your feedback', this.loggingeService, fileModel);
  }

  private capitalize(word: string): string {
    return word[0].toUpperCase() + word.slice(1).toLowerCase();
  }

  public getAggregationsStructure(aggregationsDictionary: any): any[] {
    let key: string;
    let value: any;
    const aggregationsStructure: any[] = [];
    for ([key, value] of Object.entries(aggregationsDictionary)) {
      aggregationsStructure.push({name: this.capitalize(key.split('_').join(' ')), data: this.convertAggregation(value)});
    }
    return aggregationsStructure;
  }

  private convertAggregation(aggregations: Aggregation[]): AggregationRepresentants[] {
    let category: string;
    let value: any;
    const aggregationRepresentants: AggregationRepresentants[] = [];
    aggregations.forEach(aggregation => {
      const categoryRatings: CategoryRating[] = [];
      for ([category, value] of Object.entries(aggregation.matched)) {
        categoryRatings.push({category, value: Number(value)});
      }
      aggregationRepresentants.push({meaning: aggregation.meaning, representants: categoryRatings});
    });
    return aggregationRepresentants;
  }
}
