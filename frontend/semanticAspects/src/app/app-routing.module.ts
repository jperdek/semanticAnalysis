import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CategoryObserverComponent } from './pages/category-observer/category-observer.component';
import { LoginComponent } from './pages/login/login.component';
import { Role } from './models/role';
import { RegisterComponent } from './pages/register/register.component';
import { OktaCallbackComponent } from '@okta/okta-angular';
import { SenseAnalysisComponent } from './pages/sense-analysis/sense-analysis.component';
import { SegmentationAnalysisComponent } from './pages/segmentation-analysis/segmentation-analysis.component';
import { AutomatizationComponent } from './pages/automatization/automatization.component';
import { AuthGuardService } from './services/authentification/auth-guard.service';


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
    canLoad: [AuthGuardService],  // OktaAuthGuard can be used => import { OktaAuthGuard } from '@okta/okta-angular';
    canActivate: [AuthGuardService],
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
    canLoad: [AuthGuardService],
    canActivate: [AuthGuardService],
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
