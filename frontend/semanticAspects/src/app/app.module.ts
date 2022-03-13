import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AppRoutingModule } from './app-routing.module';
import { MenuComponent } from './menu/menu.component';
import { NavigationComponent } from './components/navigation/navigation.component';
import { FooterComponent } from './components/footer/footer.component';
import { LoginComponent } from './pages/login/login.component';
import { RegisterComponent } from './pages/register/register.component';
import { MaterialModule } from './material/material.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { HttpClientModule } from '@angular/common/http';
import { environment } from 'src/environments/environment';

import { StoreModule } from '@ngrx/store';
import { EffectsModule } from '@ngrx/effects';
import { reducers } from './store';
import { AppEffects } from './effects/app.effects';
import { StoreDevtoolsModule } from '@ngrx/store-devtools';
import { StoreRouterConnectingModule } from '@ngrx/router-store';
import { FileUploadComponent } from './fileUploader/file-upload/file-upload.component';
import { CategoryObserverComponent } from './pages/category-observer/category-observer.component';
import { ProgressComponent } from './components/progress/progress.component';
import { BasicFlowComponent } from './pages/basic-flow/basic-flow.component';
import { OktaAuthModule, OKTA_CONFIG } from '@okta/okta-angular';
import { SenseAnalysisComponent } from './pages/sense-analysis/sense-analysis.component';
import { SegmentationAnalysisComponent } from './pages/segmentation-analysis/segmentation-analysis.component';
import { FileOrInputComponent } from './components/file-or-input/file-or-input.component';
import { SelectFilesForGivenOperationComponent } from './components/select-files-for-given-operation/select-files-for-given-operation.component';
import { SomExtractorComponent } from './components/som-extractor/som-extractor.component';
import { SelectFilesForSOMComponent } from './components/select-files-for-som/select-files-for-som.component';
import { DragAndDropDirective } from './directives/drag-and-drop.directive';
import { AutomatizationComponent } from './pages/automatization/automatization.component';
import { CapturedResultComponent } from './captured-result/captured-result.component';
import { AutomatizationResultVisualizationComponent } from './components/automatization-result-visualization/automatization-result-visualization.component';
import { SafeHtmlPipe } from './pipes/domSanitize';
// tslint:disable-next-line: max-line-length
import { TableCategoriesVisualizationComponent } from './components/table-categories-visualization/table-categories-visualization.component';
import { TableClustersVisualizationComponent } from './components/table-clusters-visualization/table-clusters-visualization.component';
import { ReadabilityVisualizationComponent } from './components/readability-visualization/readability-visualization.component';

import { ErrorSnackbarComponent } from './components/snackbars/error-snackbar/error-snackbar.component';
import { SuccessSnackbarComponent } from './components/snackbars/success-snackbar/success-snackbar.component';
import { UserFeedbackComponent } from './components/snackbars/user-feedback/user-feedback.component';
import { InfoSnackbarComponent } from './components/snackbars/info-snackbar/info-snackbar.component';
import { StarRatingModule } from '@sreyaj/ng-star-rating';


const oktaConfig = {
  issuer: 'https://dev-03853854.okta.com',
  clientId: '0oa19wfjhrBoVLqSw5d7',
  redirectUri: window.location.origin + '/lcallback',
  scope: 'openid profile email'
};

// FOR LOGGING USING SENTRY
import * as Raven from 'raven-js';
Raven.config('https://f7c7c35bac3a4cffa8676c1839c7b15d@o517887.ingest.sentry.io/6256077').install();
/*
import * as Sentry from "@sentry/browser";
import { Integrations } from "@sentry/tracing";
Sentry.init({
  dsn: "https://f7c7c35bac3a4cffa8676c1839c7b15d@o517887.ingest.sentry.io/6256077",
  // Alternatively, use `process.env.npm_package_version` for a dynamic release version
  // if your build tool supports it.
  release: "my-project-name@2.3.12",
  integrations: [new Integrations.BrowserTracing()],
  s
  // Set tracesSampleRate to 1.0 to capture 100%
  // of transactions for performance monitoring.
  // We recommend adjusting this value in production
  tracesSampleRate: 1.0,
});
*/


@NgModule({
  declarations: [
    AppComponent,
    MenuComponent,
    NavigationComponent,
    FooterComponent,
    LoginComponent,
    RegisterComponent,
    FileUploadComponent,
    CategoryObserverComponent,
    DragAndDropDirective,
    ProgressComponent,
    BasicFlowComponent,
    SenseAnalysisComponent,
    SegmentationAnalysisComponent,
    FileOrInputComponent,
    SelectFilesForGivenOperationComponent,
    SomExtractorComponent,
    SelectFilesForSOMComponent,
    AutomatizationComponent,
    CapturedResultComponent,
    AutomatizationResultVisualizationComponent,
    SafeHtmlPipe,
    TableCategoriesVisualizationComponent,
    TableClustersVisualizationComponent,
    ReadabilityVisualizationComponent,
    UserFeedbackComponent,
    ErrorSnackbarComponent,
    SuccessSnackbarComponent,
    InfoSnackbarComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    HttpClientModule,
    MaterialModule,
    FormsModule,
    ReactiveFormsModule,
    StoreModule.forRoot(reducers),
    EffectsModule.forRoot([AppEffects]),
    !environment.production ? StoreDevtoolsModule.instrument() : [],
    StoreRouterConnectingModule.forRoot(),
    OktaAuthModule,
    StarRatingModule
  ],
  providers: [{ provide: OKTA_CONFIG, useValue: oktaConfig }],
  bootstrap: [AppComponent]
})
export class AppModule { }
