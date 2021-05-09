import { Component, OnInit } from '@angular/core';
import {Profile} from "../../../models/profile";
import {User} from "../../../models/user";
import {AuthService} from "../../../services/auth.service";
import {Utils} from "../../../services/utils";

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  constructor(public authService: AuthService) { }

  profile: User = new User();

  validateEmail = Utils.validateEmail;

  ngOnInit() {
  }

  submitRegister(): void {
    this.authService.register(this.profile).subscribe((data) => {
      console.log(data);
    })
  }

  isValidPassword(): boolean {
    if(this.profile.password2) {
      return (this.profile.password1 === this.profile.password2)
    } else {
      return false;
    }
  }

}
