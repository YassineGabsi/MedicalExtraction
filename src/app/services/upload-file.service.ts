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
    this.url = this.url + 'upload-file';
  }

  public sendFile(file: string): Observable<any> {
    return this.http.post(this.url, file, {headers: this.getHeaders()}) as Observable<any>;
  }

}
