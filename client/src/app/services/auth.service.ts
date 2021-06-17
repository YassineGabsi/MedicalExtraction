import {Injectable} from '@angular/core';
import {GenericService} from './generic.service';
import {Observable} from 'rxjs';
import {HttpBackend, HttpClient} from '@angular/common/http';
import {Profile} from '../models/profile';
import {User} from '../models/user';
import {Router} from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AuthService extends GenericService {

  constructor(private http: HttpClient, private router: Router, handler: HttpBackend) {
    super();
    this.http = new HttpClient(handler);
  }

  public login(user: any): Observable<any> {
    return this.http.post(this.url + 'login/', user) as Observable<Profile>;
  }

  public register(user: User): Observable<User> {
    return this.http.post(this.url + 'signup/', user) as Observable<User>;
  }

  public refreshToken(): Observable<{ refresh: string }> {
    return this.http.post(this.url + 'token/refresh/',
      {refresh: localStorage.getItem('refresh_token')}) as Observable<{ refresh: string }>;
  }

  public logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('project_id');
    const currentUrl = this.router.url;
    this.router.routeReuseStrategy.shouldReuseRoute = () => false;
    this.router.onSameUrlNavigation = 'reload';
    this.router.navigate([currentUrl]);
  }

  public isLoggedIn() {
    return localStorage.getItem('token') !== null;
  }

  public getProfile(): Observable<Profile> {
    return this.http.get(this.url + 'profile/', {headers: this.getHeaders()}) as Observable<Profile>;
  }

  public updateProfile(profile: Profile): Observable<Profile> {
    return this.http.put(this.url + 'profile/', profile, {headers: this.getHeaders()}) as Observable<Profile>;
  }
}
