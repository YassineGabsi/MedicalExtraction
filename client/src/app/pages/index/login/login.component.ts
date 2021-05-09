import { Component, OnInit } from '@angular/core';
import {AuthService} from '../../../services/auth.service';
import {User} from '../../../models/user';
import {Utils} from '../../../services/utils';
import {NgxSpinnerService} from 'ngx-spinner';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  constructor(public authService: AuthService,
              private spinner: NgxSpinnerService,
  ) { }

  profile: User = new User();
  emailToSend = '';
  passwordToSend = '';
  isLoading = false;
  validateEmail = Utils.validateEmail;

  ngOnInit() {
  }

  submitLogin(): void {
    this.isLoading = true;
    this.spinner.show('spinner');
    this.authService.login({username: this.emailToSend, password: this.passwordToSend}).subscribe((data) => {
      console.log(data);
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

}
