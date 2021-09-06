import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardComponent } from './dashboard.component';
import {SidebarModule} from 'ng-sidebar';
import {DashboardRoutingModule} from './dashboard-routing.module';
import {IndexModule} from '../index/index.module';
import { NavbarDashboardComponent } from './navbar-dashboard/navbar-dashboard.component';
import {NgxSpinnerModule} from 'ngx-spinner';
import { RecordItemComponent } from './record-item/record-item.component';
import {FormsModule} from '@angular/forms';
import { NgSelectModule } from '@ng-select/ng-select';
import { AllValidatedComponent } from './all-validated/all-validated.component';



@NgModule({
  declarations: [DashboardComponent, NavbarDashboardComponent, RecordItemComponent, AllValidatedComponent],
  imports: [
    CommonModule,
    SidebarModule,
    DashboardRoutingModule,
    IndexModule,
    NgxSpinnerModule,
    FormsModule,
    NgSelectModule
  ]
})
export class DashboardModule { }
