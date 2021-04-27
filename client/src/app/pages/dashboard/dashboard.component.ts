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
  public medicalTags = [];

  public isLoading = false;

  private projectId = localStorage.getItem('project_id');

  constructor(private projectService: ProjectService,
              private spinner: NgxSpinnerService,
  ) { }

  ngOnInit() {
    this.getProject();
    this.medicalTags.push('complications');
    this.medicalTags.push('heart diseases');
    this.medicalTags.push('coronary artery diseases');
    this.medicalTags.push('lorem upsum lorem upsum lorem upsum');
  }

  getProject() {
    this.isLoading = true;
    this.spinner.show();
    this.projectService.getProjectById(this.projectId).subscribe((data) => {
      console.log(data);
      this.records = data.items;
      this.recordSelected = this.records[0];
      this.isLoading = false;
      this.spinner.hide();
    })
  }
  selectRecord(i): void {
    this.recordSelected = i;
  }

  public _toggleSidebar(): void {
    this.opened = !this.opened;
    this.minimized = !this.minimized;
  }
}
