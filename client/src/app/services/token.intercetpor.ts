import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor
} from '@angular/common/http';
import { Observable } from 'rxjs';
import {AuthService} from './auth.service';
import {JwtHelperService} from '@auth0/angular-jwt';

@Injectable()
export class TokenInterceptor implements HttpInterceptor {

  constructor(private userService: AuthService, private jwtHelper: JwtHelperService) {
  }


  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const token = localStorage.getItem('token');
    if (token) {
      const timeout = this.jwtHelper.getTokenExpirationDate(token).getTime() - Date.now() - 1000;
      console.log(timeout);
      if (timeout <= 0) {
        this.userService.refreshToken().subscribe(data => {
          localStorage.setItem('token', data.refresh);
          return next.handle(request);
          console.log(data.refresh);
        });
      } else {
        setTimeout(() => {
          this.userService.refreshToken().subscribe(data => {
            localStorage.setItem('token', data.refresh);
            return next.handle(request);
          });
        }, timeout);
      }
    }
    return next.handle(request);
  }
}
