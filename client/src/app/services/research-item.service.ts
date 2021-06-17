import { Injectable } from '@angular/core';
import {GenericService} from './generic.service';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {ResearchItem} from '../models/research-item';

@Injectable({
  providedIn: 'root'
})
export class ResearchItemService extends GenericService {

  constructor(private http: HttpClient) {
    super();
    this.url = this.url + 'research-item/';
  }

  public getAllResearchItems(): Observable<Array<ResearchItem>> {
    return this.http.get(this.url, {headers: this.getHeaders()}) as Observable<Array<ResearchItem>>;
  }

  public addResearchItem(resItem: ResearchItem): Observable<any> {
    return this.http.post(this.url, resItem, {headers: this.getHeaders()}) as Observable<any>;
  }

  public getById(id: any): Observable<ResearchItem> {
    return this.http.get(this.url + id, {headers: this.getHeaders()}) as Observable<ResearchItem>;
  }

  public deleteResearchItem(id: any): Observable<ResearchItem> {
    return this.http.delete(this.url + id, {headers: this.getHeaders()}) as Observable<ResearchItem>;
  }

  public patchResearchItem(id: any, resItem: ResearchItem): Observable<ResearchItem> {
    return this.http.patch(this.url + id, resItem, {headers: this.getHeaders()}) as Observable<ResearchItem>;
  }

  public putResearchItem(id: any, resItem: ResearchItem): Observable<ResearchItem> {
    return this.http.put(this.url + id, resItem, {headers: this.getHeaders()}) as Observable<ResearchItem>;
  }
}
