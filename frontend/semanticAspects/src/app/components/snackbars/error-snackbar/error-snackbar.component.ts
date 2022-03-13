import {Component, Inject} from '@angular/core';
import {MatSnackBar, MAT_SNACK_BAR_DATA} from '@angular/material/snack-bar';


@Component({
  selector: 'app-error-snackbar',
  templateUrl: './error-snackbar.component.html',
  styleUrls: ['./error-snackbar.component.css']
})
export class ErrorSnackbarComponent {

  private static readonly displayTimeout = 3000;
  errorMessage = 'Fail!';
  errorAction: string = null;

  constructor(@Inject(MAT_SNACK_BAR_DATA) public data: any) {
    this.errorMessage = (data.errorMessage) ? data.errorMessage : 'Failed';
    this.errorAction = (data.errorAction) ? data.errorAction : null;
  }

  static openSnackBarAction(snackBar: MatSnackBar, message: string, action: string): void {
    snackBar.open(message, action, {
      duration: ErrorSnackbarComponent.displayTimeout,
    });
  }

  static openSnackBar(snackBar: MatSnackBar, message: string): void {
    snackBar.openFromComponent(ErrorSnackbarComponent,  {
      data: { errorMessage: message },
      duration: ErrorSnackbarComponent.displayTimeout,
    });
  }
}
