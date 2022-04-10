import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Sort } from '@angular/material/sort';
import { from } from 'rxjs';
import { Observable } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { ErrorSnackbarComponent } from 'src/app/components/snackbars/error-snackbar/error-snackbar.component';
import { InfoSnackbarComponent } from 'src/app/components/snackbars/info-snackbar/info-snackbar.component';
import { SenseRating, SenseResult } from '../../models/senseRating';
import { SenseApiManagerService } from '../../services/senseAnalysis/sense-api-manager.service';


@Component({
  selector: 'app-sense-analysis',
  templateUrl: './sense-analysis.component.html',
  styleUrls: ['./sense-analysis.component.css']
})
export class SenseAnalysisComponent implements OnInit {

  senseFormGroup: FormGroup;
  private analyzedCategories: Observable<SenseResult>;
  sortedData: SenseRating[];

  constructor(private formBuilder: FormBuilder,
              private matSnackBar: MatSnackBar,
              private senseApiManagerService: SenseApiManagerService) { }

  public ngOnInit(): void {
    this.senseFormGroup = this.formBuilder.group({
      textAreaFormControl: ['', Validators.required],
      windowFormControl: [3, Validators.required],
    });
  }

  public formatLabel(value: number): string {
    return value + 'w';
  }

  public getAnalyzedCategories(): Observable<SenseResult> {
    return this.analyzedCategories;
  }

  public startSenseAnalysis(text: string, window: number): void {
   // this._senseApiManagerService.senseAnalysis(text, window).then(result => console.log(result)).catch(error => console.log(error));
   this.analyzedCategories = from(this.senseApiManagerService.senseAnalysis(text, window))
   .pipe(map(results => results as SenseResult), catchError(error => {
      ErrorSnackbarComponent.openSnackBar(this.matSnackBar, 'Error occurred during sense analysis!');
      throw error;
   } ));
  }

  public onSubmit($event: Event): void {
    if (this.senseFormGroup.valid){
      const text = this.senseFormGroup.controls.textAreaFormControl.value;
      const window = this.senseFormGroup.controls.windowFormControl.value;

      InfoSnackbarComponent.openSnackBar(this.matSnackBar, 'Text has been send to sense analysis!');
      this.startSenseAnalysis(text, window);
    } else {
      ErrorSnackbarComponent.openSnackBar(this.matSnackBar, 'Error: please fill form correctly!');
    }
  }

  public sortData(sort: Sort, ratings: SenseRating[]): void {
    const data = ratings.slice();
    if (!sort.active || sort.direction === '') {
      this.sortedData = data;
      return;
    }

    this.sortedData = data.sort((a, b) => {
      const isAsc = sort.direction === 'asc';
      switch (sort.active) {
        case 'category': return this.compare(a.category, b.category, isAsc);
        case 'value': return this.compare(a.value, b.value, isAsc);
        default: return 0;
      }
    });
  }

  public compare(a: number | string, b: number | string, isAsc: boolean): number {
    return (a < b ? -1 : 1) * (isAsc ? 1 : -1);
  }
}
