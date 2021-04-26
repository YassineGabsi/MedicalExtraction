import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {HomeComponent} from '../home/home.component';
import {LoginComponent} from './login/login.component';
import {RegisterComponent} from './register/register.component';
import {UploadFileComponent} from './upload-file/upload-file.component';
import {IndexComponent} from './index.component';
import {PredictionStatusComponent} from './prediction-status/prediction-status.component';

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
    },
    {
      path: 'status',
      component: PredictionStatusComponent,
    },
  ]
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class IndexRoutingModule { }
