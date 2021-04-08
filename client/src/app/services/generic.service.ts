import { Injectable } from '@angular/core';
import {Utils} from './utils';
import {HttpHeaders} from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class GenericService {
  protected url;

  constructor() {
    this.url = Utils.url;
  }
  protected getHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    const toReturn = new HttpHeaders();
    if (token) {
      return toReturn.append('Authorization', 'Bearer ' + token);
    }
    return toReturn;
  }

}
