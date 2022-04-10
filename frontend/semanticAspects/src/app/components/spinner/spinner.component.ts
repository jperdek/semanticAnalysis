import { Component, Input } from '@angular/core';
import { addNonEnumerableProperty } from '@sentry/utils';

@Component({
  selector: 'app-spinner',
  templateUrl: './spinner.component.html',
  styleUrls: ['./spinner.component.css']
})
export class SpinnerComponent {

  visibility = true;

  constructor() { }
}
