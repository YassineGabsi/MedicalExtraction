import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardComponent } from './dashboard.component';
import {SidebarModule} from 'ng-sidebar';
import {DashboardRoutingModule} from './dashboard-routing.module';
import {IndexModule} from '../index/index.module';
import { NavbarDashboardComponent } from './navbar-dashboard/navbar-dashboard.component';



@NgModule({
  declarations: [DashboardComponent, NavbarDashboardComponent],
  imports: [
    CommonModule,
    SidebarModule,
    DashboardRoutingModule,
    IndexModule
  ]
})
export class DashboardModule { }
