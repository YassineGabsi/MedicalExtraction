import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardComponent } from './dashboard.component';
import {SidebarModule} from 'ng-sidebar';
import {DashboardRoutingModule} from './dashboard-routing.module';



@NgModule({
  declarations: [DashboardComponent],
  imports: [
    CommonModule,
    SidebarModule,
    DashboardRoutingModule
  ]
})
export class DashboardModule { }
