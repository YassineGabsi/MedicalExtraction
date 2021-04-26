import { Injectable } from '@angular/core';
import {GenericService} from './generic.service';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {Icd10Item} from '../models/icd10-item';

@Injectable({
  providedIn: 'root'
})
export class Icd10ItemService extends GenericService {

  constructor(private http: HttpClient) {
    super();
    this.url = this.url + 'icd10-item/';
  }

  public getAllICD10(): Observable<Array<Icd10Item>> {
    return this.http.get(this.url) as Observable<Array<Icd10Item>>;
  }

  public addICD10Item(icd10: Icd10Item): Observable<any> {
    return this.http.post(this.url, icd10) as Observable<any>;
  }

  public getById(id: any): Observable<Icd10Item> {
    return this.http.get(this.url + id) as Observable<Icd10Item>;
  }

  public deleteICD10Item(id: any): Observable<Icd10Item> {
    return this.http.delete(this.url + id) as Observable<Icd10Item>;
  }

  public patchICD10Item(id: any, icd10: Icd10Item): Observable<Icd10Item> {
    return this.http.patch(this.url + id, icd10) as Observable<Icd10Item>;
  }

  public putICD10Item(id: any, icd10: Icd10Item): Observable<Icd10Item> {
    return this.http.put(this.url + id, icd10) as Observable<Icd10Item>;
  }
}
