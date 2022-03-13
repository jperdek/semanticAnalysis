import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CategoryObserverComponent } from './pages/category-observer/category-observer.component';
import { LoginComponent } from './pages/login/login.component';
import { Role } from './models/role';
import { RegisterComponent } from './pages/register/register.component';
import { OktaCallbackComponent, OktaAuthGuard } from '@okta/okta-angular';
import { SenseAnalysisComponent } from './pages/sense-analysis/sense-analysis.component';
import { SegmentationAnalysisComponent } from './pages/segmentation-analysis/segmentation-analysis.component';
import { AutomatizationComponent } from './pages/automatization/automatization.component';

const oktaConfig = {
  issuer: 'https://dev-03853854.okta.com',
  clientId: '0oa19wfjhrBoVLqSw5d7',
  redirectUri: window.location.origin + '/lcallback',
  scope: 'openid profile email'
};

const routes: Routes = [
  {
    path: 'login',
    component: LoginComponent
  },
  {
    path: 'register',
    component: RegisterComponent
  },
  {
    path: 'analyser',
    canLoad: [OktaAuthGuard],
    canActivate: [OktaAuthGuard],
    data: {
      roles: [
        Role.Admin,
        Role.User,
        Role.Guest
      ]
    },
    children: [
      {
        path: 'category',
        component: CategoryObserverComponent
      },
      {
        path: 'senseAnalysis',
        component: SenseAnalysisComponent
      }
    ]
  },
  {
    path: 'automatization',
    //canLoad: [OktaAuthGuard],
    //canActivate: [OktaAuthGuard],
    data: {
      roles: [
        Role.Admin,
        Role.User,
        Role.Guest
      ]
    },
    children: [
      {
        path: '',
        component: AutomatizationComponent
      }
    ]
  },
  {
    path: 'segmentation',
    canLoad: [OktaAuthGuard],
    canActivate: [OktaAuthGuard],
    data: {
      roles: [
        Role.Admin,
        Role.User,
        Role.Guest
      ]
    },
    children: [
      {
        path: '',
        component: SegmentationAnalysisComponent
      },
    ]
  },
  { path: 'lcallback', component: OktaCallbackComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
