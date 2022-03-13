import { Component, Inject} from '@angular/core';
import { MatSnackBar, MAT_SNACK_BAR_DATA } from '@angular/material/snack-bar';


@Component({
  selector: 'app-info-snackbar',
  templateUrl: './info-snackbar.component.html',
  styleUrls: ['./info-snackbar.component.css']
})
export class InfoSnackbarComponent {

  private static readonly displayTimeout = 1500;
  infoMessage = 'Information...';
  infoAction: string = null;

  constructor(@Inject(MAT_SNACK_BAR_DATA) public data: any) {
    this.infoMessage = (data.infoMessage) ? data.infoMessage : 'Information';
    this.infoAction = (data.infoAction) ? data.infoAction : null;
  }

  static openSnackBarAction(snackBar: MatSnackBar, message: string, action: string): void {
    snackBar.open(message, action, {
     duration: InfoSnackbarComponent.displayTimeout,
    });
  }

  static openSnackBar(snackBar: MatSnackBar, message: string): void {
    snackBar.openFromComponent(InfoSnackbarComponent,  {
      data: { infoMessage: message },
      duration: InfoSnackbarComponent.displayTimeout,
    });
  }

}
