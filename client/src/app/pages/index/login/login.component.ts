import { Component, OnInit } from '@angular/core';
import {AuthService} from "../../../services/auth.service";
import {User} from "../../../models/user";
import {Utils} from "../../../services/utils";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  constructor(public authService: AuthService) { }

  profile: User = new User();
  emailToSend = '';
  passwordToSend = '';

  validateEmail = Utils.validateEmail;

  ngOnInit() {
  }

  submitLogin(): void {
    this.authService.login({username: this.emailToSend, password: this.passwordToSend}).subscribe((data) => {
      console.log(data);
    })
  }

}
