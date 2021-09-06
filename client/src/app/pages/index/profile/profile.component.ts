import { Component, OnInit } from '@angular/core';
import {Profile} from "../../../models/profile";
import {AuthService} from "../../../services/auth.service";
import {NgxSpinnerService} from "ngx-spinner";
import {Router} from "@angular/router";

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  isLoading = false;
  profile = new Profile();

  constructor(public userService: AuthService,
              public  spinner: NgxSpinnerService,
              public router: Router) { }

  ngOnInit(): void {
    this.getProfile();
  }

  getProfile(): void {
    this.isLoading = true;
    this.spinner.show('spinner');
    this.userService.getProfile().subscribe((data) => {
      this.profile = data;
      this.isLoading = false;
      this.spinner.hide('spinner');
    });
  }

  updateProfile(): void {
    this.isLoading = true;
    this.spinner.show('spinner');
    this.userService.updateProfile(this.profile).subscribe((data) => {
      this.profile = data;
      const currentUrl = this.router.url;
      this.router.routeReuseStrategy.shouldReuseRoute = () => false;
      this.router.onSameUrlNavigation = 'reload';
      this.router.navigate([currentUrl]);
      this.isLoading = false;
      this.spinner.hide('spinner');
    })
  }
}
