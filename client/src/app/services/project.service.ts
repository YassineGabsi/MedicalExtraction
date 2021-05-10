import { Injectable } from '@angular/core';
import {GenericService} from './generic.service';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {ResearchProject} from '../models/research-project';

@Injectable({
  providedIn: 'root'
})
export class ProjectService extends GenericService {

  urlInfo;
  urlProject;

  constructor(private http: HttpClient) {
    super();
    this.urlInfo = this.url + 'project-info/';
    this.urlProject = this.url + 'project/';
  }

  public getProjectById(id): Observable<ResearchProject> {
    return this.http.get(this.urlInfo + id, {headers: this.getHeaders()}) as Observable<ResearchProject>;
  }

  public getProjects(): Observable<Array<ResearchProject>> {
    return this.http.get(this.url + 'project', {headers: this.getHeaders()}) as Observable<Array<ResearchProject>>;
  }
}
