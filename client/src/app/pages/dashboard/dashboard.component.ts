import { Component, OnInit } from '@angular/core';
import {ProjectService} from '../../services/project.service';
import {ResearchItem} from '../../models/research-item';
import {NgxSpinnerService} from 'ngx-spinner';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  public opened = true;
  public minimized = false;
  public mode = 'push';

  public records: ResearchItem[];
  public recordSelected;

  public isLoading = false;

  private projectId = localStorage.getItem('project_id');

  constructor(private projectService: ProjectService,
              private spinner: NgxSpinnerService,
  ) { }

  ngOnInit() {
    this.getProject();
  }

  getProject() {
    this.isLoading = true;
    this.spinner.show('spinner1');
    this.spinner.show('spinner2');
    this.projectService.getProjectById(this.projectId).subscribe((data) => {
      console.log(data);
      this.records = data.items;
      this.recordSelected = this.records[0];
      this.isLoading = false;
      this.spinner.hide('spinner1');
      this.spinner.hide('spinner2');
    })
  }
  selectRecord(i): void {
    this.recordSelected = this.records[i];
  }

  public _toggleSidebar(): void {
    this.opened = !this.opened;
    this.minimized = !this.minimized;
  }
}
