
import { Injectable } from '@angular/core';
import { Actions, ROOT_EFFECTS_INIT, ofType, createEffect } from '@ngrx/effects';
import { loadSearchCustomizationEntities } from '../store/searchCustomization/search-customization.actions';
import { map } from 'rxjs/operators';


@Injectable()
export class AppEffects {

  constructor(private actions$: Actions) {}

  init$ = createEffect(() => this.actions$.pipe(
    ofType(ROOT_EFFECTS_INIT),
    map((searchCustomizationModel) => loadSearchCustomizationEntities({ searchCustomizationModel }))));
}
