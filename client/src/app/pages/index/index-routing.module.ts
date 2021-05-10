import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {HomeComponent} from '../home/home.component';
import {LoginComponent} from './login/login.component';
import {RegisterComponent} from './register/register.component';
import {UploadFileComponent} from './upload-file/upload-file.component';
import {IndexComponent} from './index.component';
import {PredictionStatusComponent} from './prediction-status/prediction-status.component';
import {ProjectsComponent} from './projects/projects.component';
import {
  AuthGuardService as AuthGuard
} from './../../services/auth-guard.service';
import {ProfileComponent} from "./profile/profile.component";

const routes: Routes = [{
  path: '',
  component: IndexComponent,
  children: [
    {
      path: '',
      component: HomeComponent,
    },
    {
      path: 'login',
      component: LoginComponent,
    },
    {
      path: 'register',
      component: RegisterComponent,
    },
    {
      path: 'upload-file',
      component: UploadFileComponent,
      canActivate: [AuthGuard]
    },
    {
      path: 'status',
      component: PredictionStatusComponent,
      canActivate: [AuthGuard]
    },
    {
      path: 'projects',
      component: ProjectsComponent,
      canActivate: [AuthGuard]
    },
    {
      path: 'profile',
      component: ProfileComponent,
      canActivate: [AuthGuard]
    },
  ]
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class IndexRoutingModule { }
