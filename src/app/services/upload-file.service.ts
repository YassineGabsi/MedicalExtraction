import { Injectable } from '@angular/core';
import {GenericService} from './generic.service';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UploadFileService extends GenericService {

  constructor(private http: HttpClient) {
    super();
    this.url = this.url + 'upload/';
  }

  public sendFile(file): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post(this.url, formData, {headers: this.getHeaders()}) as Observable<any>;
  }

}
