import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {LoginComponent} from './login/login.component';
import {HomeComponent} from '../home/home.component';
import {TopSectionComponent} from '../home/top-section/top-section.component';
import {BottomSectionComponent} from '../home/bottom-section/bottom-section.component';
import {UploadFileComponent} from './upload-file/upload-file.component';
import {RegisterComponent} from './register/register.component';
import { IndexComponent } from './index.component';
import {HeaderComponent} from '../../components/header/header.component';
import {FooterComponent} from '../../components/footer/footer.component';
import {RouterModule} from '@angular/router';
import {IndexRoutingModule} from './index-routing.module';
import { DndDirective } from '../../directives/dnd.directive';
import { PredictionStatusComponent } from './prediction-status/prediction-status.component';
import { NgxSpinnerModule } from 'ngx-spinner';
import {FormsModule} from "@angular/forms";



@NgModule({
  declarations: [
    HeaderComponent,
    FooterComponent,
    LoginComponent,
    HomeComponent,
    TopSectionComponent,
    BottomSectionComponent,
    UploadFileComponent,
    RegisterComponent,
    IndexComponent,
    DndDirective,
    PredictionStatusComponent
  ],
  exports: [
    HeaderComponent
  ],
  imports: [
    CommonModule,
    RouterModule,
    IndexRoutingModule,
    NgxSpinnerModule,
    FormsModule,
  ]
})
export class IndexModule { }
