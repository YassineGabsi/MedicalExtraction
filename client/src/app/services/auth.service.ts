import {Injectable} from '@angular/core';
import {GenericService} from './generic.service';
import {Observable} from 'rxjs';
import {HttpClient} from '@angular/common/http';
import {Profile} from '../models/profile';
import {User} from '../models/user';

@Injectable({
  providedIn: 'root'
})
export class AuthService extends GenericService {

  constructor(private http: HttpClient) {
    super();
  }

  public login(user: string): Observable<any> {
    return this.http.post(this.url + 'api/login/', user) as Observable<Profile>;
  }

  public register(user: string): Observable<User> {
    return this.http.post(this.url + 'api/signup/', user) as Observable<User>;
  }

  public refreshToken(): Observable<{ refresh: string }> {
    return this.http.post(this.url + 'api/token/refresh/',
      {refresh: localStorage.getItem('refresh_token')}) as Observable<{ refresh: string }>;
  }

  public logout() {
    localStorage.removeItem('token');
  }

  public isLoggedIn() {
    return localStorage.getItem('token') !== null;
  }

  public getProfile(id: string): Observable<Profile> {
    return this.http.get(this.url + 'api/profile/') as Observable<Profile>;
  }

  public updateProfile(profile: Profile): Observable<Profile> {
    return this.http.put(this.url + 'api/profile/', profile) as Observable<Profile>;
  }
}
