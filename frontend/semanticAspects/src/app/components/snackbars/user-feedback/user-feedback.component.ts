import { Component, Inject, OnInit} from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { MatSnackBar, MatSnackBarRef, MAT_SNACK_BAR_DATA } from '@angular/material/snack-bar';
import { FileModel } from 'src/app/models/fileModel';
import { LoggingService } from 'src/app/services/logging/logging.service';


@Component({
  selector: 'app-user-feedback',
  templateUrl: './user-feedback.component.html',
  styleUrls: ['./user-feedback.component.scss']
})
export class UserFeedbackComponent implements OnInit {

  constructor(private formBuilder: FormBuilder,
              public sbRef: MatSnackBarRef<UserFeedbackComponent>, @Inject(MAT_SNACK_BAR_DATA) public data: any) {
    this.feedbackMessage = (data.feedbackMessage) ? data.feedbackMessage : 'Feedback';
    this.feedbackAction = (data.feedbackAction) ? data.feedbackAction : null;
  }

  userFeedbackFormGroup: FormGroup;

  starRating = 3.5;
  feedbackMessage = 'Feedback!';
  feedbackAction: string = null;

  static openSnackBarAction(snackBar: MatSnackBar, message: string, action: string): void {
    snackBar.open(message, action, {
    });
  }

  static openSnackBar(snackBar: MatSnackBar, message: string, loggingService: LoggingService, fileModel: FileModel): void {
    snackBar.openFromComponent(UserFeedbackComponent, {
      data: { successMessage: message, loggingService, fileModel },
      horizontalPosition: 'left',
      verticalPosition: 'bottom',
    });
  }

  public ngOnInit(): void {
    this.userFeedbackFormGroup = this.formBuilder.group({
      starRatingFormControl: [3, ],
      userFeedbackFormControl: ['', ],
    });
  }

  sendResponse(loggingService: LoggingService, fileModel: FileModel): void {
    if (this.userFeedbackFormGroup.valid) {
       const responseData = {
         rating: this.starRating,
         content: this.userFeedbackFormGroup.controls.userFeedbackFormControl.value,
         fileNmae: fileModel.name,
         fileContentPart: fileModel.textResult.substring(0, 250)
       };
       loggingService.logJSONInfo(responseData);
    } else {
      console.log('Error: form for user feedback is invalid!');
    }
    this.sbRef.dismiss();
  }

  public onRate(rating: number): void {
    this.starRating = rating;
  }
}
