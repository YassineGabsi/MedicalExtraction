import { Injectable } from '@angular/core';
import {GenericService} from './generic.service';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {PredictedStats} from '../models/predicted-stats';
import {ValidatedStats} from '../models/validated-stats';

@Injectable({
  providedIn: 'root'
})
export class StatisticsService extends GenericService {

  urlPredicted;
  urlValidated;

  constructor(private http: HttpClient) {
    super();
    this.urlPredicted = this.url + 'predicted/';
    this.urlValidated = this.url + 'validated/';
  }

  public getPredicted(id: any): Observable<PredictedStats> {
    return this.http.get(this.urlPredicted) as Observable<PredictedStats>;
  }

  public getValidated(id: any): Observable<ValidatedStats> {
    return this.http.get(this.urlValidated) as Observable<ValidatedStats>;
  }

}
