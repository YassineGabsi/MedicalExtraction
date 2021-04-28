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



@NgModule({
  declarations: [DashboardComponent, NavbarDashboardComponent, RecordItemComponent],
  imports: [
    CommonModule,
    SidebarModule,
    DashboardRoutingModule,
    IndexModule,
    NgxSpinnerModule,
    FormsModule
  ]
})
export class DashboardModule { }
