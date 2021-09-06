import { Component, OnInit } from '@angular/core';
import {AuthService} from '../../../services/auth.service';
import {User} from '../../../models/user';
import {Utils} from '../../../services/utils';
import {NgxSpinnerService} from 'ngx-spinner';
import Swal from 'sweetalert2';
import {Router} from "@angular/router";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  constructor(public authService: AuthService,
              private spinner: NgxSpinnerService,
              public router: Router,
  ) { }

  profile: User = new User();
  emailToSend = '';
  passwordToSend = '';
  isLoading = false;

  ngOnInit() {
  }

  submitLogin(): void {
    this.isLoading = true;
    this.spinner.show('spinner');
    this.authService.login({username: this.emailToSend, password: this.passwordToSend}).subscribe((data) => {
      localStorage.setItem('token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
      this.router.navigateByUrl('/dashboard');
      this.isLoading = false;
      this.spinner.hide('spinner');
      }, (err) => {
      console.log(err);
      Swal.fire({
        icon: 'error',
        title: 'Oops...',
      });
      this.isLoading = false;
      this.spinner.hide('spinner');
    });
  }

}
