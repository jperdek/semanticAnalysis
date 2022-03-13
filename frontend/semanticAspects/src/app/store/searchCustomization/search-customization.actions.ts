import { createAction, props } from '@ngrx/store';
import { SearchCustomizationModel } from './searchCustomizationModel';

export const addSearchCustomizationEntity = createAction(
  '[SearchCustomizationModel] Add SearchCustomizationModel',
  props<{ searchCustomizationModel: SearchCustomizationModel }>()
);

export const loadSearchCustomizationEntities = createAction(
    '[SearchCustomizationModel] Load SearchCustomizationModel',
    props<{ searchCustomizationModel: SearchCustomizationModel[] }>()
  );

export const deleteSearchCustomizationEntity = createAction(
  '[SearchCustomizationModel] Delete SearchCustomizationModel',
  props<{ id: string }>()
);

