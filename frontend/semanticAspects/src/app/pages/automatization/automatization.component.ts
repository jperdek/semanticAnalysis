import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AutomatizationService } from 'src/app/services/automatization/automatization.service';
import { SharedFilesForAnalysisService } from 'src/app/services/shared-files-for-analysis.service';
import { FileModel } from 'src/app/models/fileModel';
import { AutomatizationResult } from 'src/app/models/automatizationResult';
import { ReadabilityAnalysisService } from 'src/app/semanticAspects/readability/readability-analysis.service';
import { ReadabilityIndexes } from 'src/app/models/readability';
import { LoggingService } from 'src/app/services/logging/logging.service';
import { SuccessSnackbarComponent } from 'src/app/components/snackbars/success-snackbar/success-snackbar.component';
import { MatSnackBar } from '@angular/material/snack-bar';
import { InfoSnackbarComponent } from 'src/app/components/snackbars/info-snackbar/info-snackbar.component';
import { UserFeedbackComponent } from 'src/app/components/snackbars/user-feedback/user-feedback.component';


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
    console.log(automatizedResultIndex);
    console.log(this.automatizationResults[automatizedResultIndex]);

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
      readability_indexes: automatizationResultData.readability_indexes
    };
  }

  public applyAutomatization(): void {
    InfoSnackbarComponent.openSnackBar(this.matSnackBar, 'Started processing files. Please wait!');
    console.log(SharedFilesForAnalysisService.getUploadedFiles()[0]);
    if (SharedFilesForAnalysisService.getUploadedFiles()[0] !== undefined) {
        SharedFilesForAnalysisService.getUploadedFilesAsync(this.matSnackBar).then(uploadedFiles => {
          uploadedFiles.forEach((uploadedFile: FileModel, index: number) => {
            this.automatizationService.automatizationRequest(
              uploadedFile.textResult, uploadedFile.name).then((automatizationResultData: AutomatizationResult) => {
                const automatizationResult: AutomatizationResult = this.copyAutomatizationResultData(automatizationResultData);
                // automatizationResult.unprocessed_text = uploadedFile.textResult;
                automatizationResult.readability_indexes = this.analyzeReadabilityMetris(uploadedFile.textResult);
                console.log(automatizationResult);
                this.automatizationResults.push(automatizationResult);
                SuccessSnackbarComponent.openSnackBar(this.matSnackBar, 'File: ' + uploadedFile.name + ' has been loaded!');
                if (index === uploadedFiles.length - 1) {
                  setTimeout(() => this.getFeedback(uploadedFile), 1000);
                }
            });
          });
        });
      }
  }

  private getFeedback(fileModel: FileModel): void {
    UserFeedbackComponent.openSnackBar(this.feedbackBar, 'Provide your feedback', this.loggingeService, fileModel);
  }
  public formatScoreLabel(value: number): number {
    return AutomatizationComponent.roundNumberToPlaces(value, 2);
  }

  public getMinScore(text: string): number {
    let minScore = 10000000;
    const scores = text.match(/score=([\"\'][^\"\']+[\"\'])/g);
    if (scores !== null) {
      for (const scoreString of scores){
          const score = Number(scoreString.split('"')[1]);
          if (minScore > score) {
              minScore = score;
          }
      }
    }
    return minScore;
  }

  public getMaxScore(text: string): number {
    let maxScore = 0.0;
    const scores = text.match(/score=([\"\'][^\"\']+[\"\'])/g);

    if (scores !== null) {
      for (const scoreString of scores){
          const score = Number(scoreString.split('"')[1]);
          if (maxScore < score) {
              maxScore = score;
          }
      }
    }
    return maxScore;
  }

  public scoreOnSlideChange1(threshold: number, automatizationResult: AutomatizationResult): void {
    let finalString = '';
    const tagParts = automatizationResult.analyzed_text.match(
      /([^<])+<\s*p\s+score=[\"\'][^\"\']+[\"\']\s+class=[\"\'][^\"\']+[\"\']\s*>[^<]+<\s*\/p\s*>/g);
    console.log(tagParts);
    for (const tagPart of tagParts){
        const score = Number(tagPart.split('score="')[1].split('"')[0]);
        console.log(tagPart);
        if (score >= threshold) {
            finalString = finalString + tagPart.replace(/class=[\"\'][^\"\']+[\"\']/, 'class="relevant-word chosen-relevant-word"');
        } else {
          finalString = finalString + tagPart.replace(/class=[\"\'][^\"\']+[\"\']/, 'class="relevant-word deny-relevant-word"');
        }
    }
    automatizationResult.analyzed_text = finalString;
  }

  public scoreOnSlideChange(threshold: number, automatizationResult: AutomatizationResult): void {
    const domParser = new DOMParser();
    const htmlElement = domParser.parseFromString('<div id="DOMWRAP">' + automatizationResult.analyzed_text + '</div>', 'text/html');
    const relevantElements = htmlElement.getElementsByClassName('relevant-word');

    Array.from(relevantElements).forEach((relevantElement: Element) => {
        const score = Number(relevantElement.getAttribute('score'));
        if (score >= threshold) {
          relevantElement.classList.add('chosen-relevant-word');
          relevantElement.classList.remove('deny-relevant-word');
        } else {
          relevantElement.classList.add('deny-relevant-word');
          relevantElement.classList.remove('chosen-relevant-word');
        }
    });
    automatizationResult.analyzed_text = htmlElement.getElementById('DOMWRAP').innerHTML;
  }
}
