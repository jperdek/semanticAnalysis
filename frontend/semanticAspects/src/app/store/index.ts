import { ActionReducerMap } from '@ngrx/store';
import * as searchCustomizationState from './searchCustomization/search-customization.reducer';

export interface SearchState {
    [searchCustomizationState.canvasStateFeatureKey]: searchCustomizationState.SearchState;
}

export const reducers: ActionReducerMap<SearchState> = {
    [searchCustomizationState.canvasStateFeatureKey]: searchCustomizationState.reducer,
};

export const selectCanvasObjectsList = (state: SearchState):
searchCustomizationState.SearchState => state[searchCustomizationState.canvasStateFeatureKey];
