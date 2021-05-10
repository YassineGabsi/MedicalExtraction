import { Component, OnInit } from '@angular/core';
import {Profile} from "../../../models/profile";
import {User} from "../../../models/user";
import {AuthService} from "../../../services/auth.service";
import {Utils} from "../../../services/utils";
import {NgxSpinnerService} from "ngx-spinner";
import Swal from "sweetalert2";
import {Router} from "@angular/router";

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  constructor(public authService: AuthService,
              private spinner: NgxSpinnerService,
              public router: Router,
  ) { }

  profile: User = new User();
  isLoading = false;
  validateEmail = Utils.validateEmail;

  ngOnInit() {
  }

  submitRegister(): void {
    this.isLoading = true;
    this.spinner.show('spinner');
    this.authService.register(this.profile).subscribe((data) => {
      localStorage.setItem('user_id', data.id.toString());
      this.router.navigateByUrl('/login');
      this.isLoading = false;
      this.spinner.hide('spinner');
    }, (err) => {
      Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: err.error.message,
      });
      this.isLoading = false;
      this.spinner.hide('spinner');
    });
  }

  isValidPassword(): boolean {
    if(this.profile.password2) {
      return (this.profile.password1 === this.profile.password2)
    } else {
      return false;
    }
  }

}
