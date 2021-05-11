import {Injectable} from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor, HttpResponse, HttpErrorResponse
} from '@angular/common/http';
import {BehaviorSubject, Observable, throwError} from 'rxjs';
import {AuthService} from './auth.service';
import {JwtHelperService} from '@auth0/angular-jwt';
import {catchError, filter, finalize, switchMap, take, tap} from 'rxjs/operators';

@Injectable()
export class TokenInterceptor implements HttpInterceptor {

  private isRefreshing = false;
  tokenSubject: BehaviorSubject<string> = new BehaviorSubject<string>(null);

  constructor(private userService: AuthService, private jwtHelper: JwtHelperService) {
  }

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    console.log('aaa');
    // const token = localStorage.getItem('token');
    // if (token) {
    //   const timeout = this.jwtHelper.getTokenExpirationDate(token).getTime() - Date.now() - 1000;
    //   console.log(timeout);
    //   if (timeout <= 280000) {
    //     this.isRefreshing = true;
    //     this.userService.refreshToken().subscribe(data => {
    //       localStorage.setItem('token', data.refresh);
    //       this.isRefreshing = false;
    //       return next.handle(request);
    //     });
    //   } else {
    //     setTimeout(() => {
    //       this.userService.refreshToken().subscribe(data => {
    //         console.log(data);
    //         localStorage.setItem('token', data.refresh);
    //         return next.handle(request);
    //       });
    //     }, timeout);
    //   }
    // }
    return next.handle(this.attachTokenToRequest(request)).pipe(
      tap((event: HttpEvent<any>) => {
        if (event instanceof HttpResponse) {
          console.log('succ');
        }
      }),
      catchError((err): Observable<any> => {
        if (err instanceof HttpErrorResponse) {
          switch ((err as HttpErrorResponse).status) {
            case 401:
              console.log('Token expired');
              return this.handeHttpErrorResponse(request, next);
            case 400:
              return this.userService.logout() as any;
          }
        }
      })
    );
  }

  private handeHttpErrorResponse(request: HttpRequest<any>, next: HttpHandler) {
    if (!this.isRefreshing) {
      this.isRefreshing = true;
      this.tokenSubject.next(null);
      return this.userService.refreshToken().pipe(
        switchMap((tokenResponse: any) => {
          if (tokenResponse) {
            localStorage.setItem('token', tokenResponse.access);
            return next.handle(this.attachTokenToRequest(request));
          }
          return this.userService.logout() as any;
        }),
        catchError(err => {
          this.userService.logout();
          return this.handleError(err);
        }),
        finalize(() => {
          this.isRefreshing = false;
        })
      );
    } else {
      this.isRefreshing = false;
      return this.tokenSubject.pipe(
        filter(token => token != null),
        take(1),
        switchMap(token => {
          return next.handle(this.attachTokenToRequest(request));
        })
      )
    }
  }

  private attachTokenToRequest(request: HttpRequest<any>) {
    const token = localStorage.getItem('token');
    return request.clone({setHeaders: {Authorization: `Bearer ${token}`}})
  }

  private handleError(errorResponse: HttpErrorResponse) {
    return throwError('error');
  }
}
