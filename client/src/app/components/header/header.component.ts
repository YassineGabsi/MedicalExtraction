import { Component, OnInit } from '@angular/core';
import {AuthService} from '../../services/auth.service';
import {Profile} from '../../models/profile';
import {Router} from '@angular/router';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

  constructor(public userService: AuthService,
              public router: Router) { }

  isLoggedIn = null;
  profile = new Profile();
  projectId = localStorage.getItem('project_id');

  ngOnInit() {
    this.isLoggedIn = this.userService.isLoggedIn();
    if (this.isLoggedIn) {
      this.getProfile();
    }
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
