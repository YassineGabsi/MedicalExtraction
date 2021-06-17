import { Injectable } from '@angular/core';
import {GenericService} from './generic.service';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {ResearchItem} from '../models/research-item';

@Injectable({
  providedIn: 'root'
})
export class ExportFileService extends GenericService {

  constructor(private http: HttpClient) {
    super();
    this.url = this.url + 'generate-results/';
  }
  public exportFile(projectID: string): Observable<any>{
    return this.http.get(this.url + projectID, {headers: this.getHeaders()}) as Observable<any>;
  }
}
