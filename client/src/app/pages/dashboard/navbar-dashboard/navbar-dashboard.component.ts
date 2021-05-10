import { Component, OnInit } from '@angular/core';
import {Profile} from "../../../models/profile";
import {AuthService} from "../../../services/auth.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-navbar-dashboard',
  templateUrl: './navbar-dashboard.component.html',
  styleUrls: ['./navbar-dashboard.component.css']
})
export class NavbarDashboardComponent implements OnInit {

  profile = new Profile();
  projectId = localStorage.getItem('project_id');

  constructor(public userService: AuthService,
              public router: Router) { }

  ngOnInit() {
    this.getProfile();
  }


  getProfile(): void {
    this.userService.getProfile().subscribe((data) => {
      this.profile = data;
    })
  }

  logout(): void {
    this.userService.logout();
    this.router.navigateByUrl('/')
  }


}
