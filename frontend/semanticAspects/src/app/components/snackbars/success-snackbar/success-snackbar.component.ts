import { Component, Inject} from '@angular/core';
import { MatSnackBar, MAT_SNACK_BAR_DATA } from '@angular/material/snack-bar';


@Component({
  selector: 'app-success-snackbar',
  templateUrl: './success-snackbar.component.html',
  styleUrls: ['./success-snackbar.component.css']
})
export class SuccessSnackbarComponent {

  private static readonly displayTimeout = 3000;
  successMessage = 'Success!';
  successAction: string = null;

  constructor(@Inject(MAT_SNACK_BAR_DATA) public data: any) {
    this.successMessage = (data.successMessage) ? data.successMessage : 'Success';
    this.successAction = (data.successAction) ? data.successAction : null;
  }

  static openSnackBarAction(snackBar: MatSnackBar, message: string, action: string): void {
    snackBar.open(message, action, {
     duration: SuccessSnackbarComponent.displayTimeout,
    });
  }

  static openSnackBar(snackBar: MatSnackBar, message: string): void {
    snackBar.openFromComponent(SuccessSnackbarComponent,  {
      data: { successMessage: message },
      duration: SuccessSnackbarComponent.displayTimeout,
    });
  }
}
