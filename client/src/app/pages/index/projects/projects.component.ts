import { Component, OnInit } from '@angular/core';
import {ProjectService} from '../../../services/project.service';
import {NgxSpinnerService} from "ngx-spinner";
import {ResearchProject} from "../../../models/research-project";
import {StatisticsService} from "../../../services/statistics.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-projects',
  templateUrl: './projects.component.html',
  styleUrls: ['./projects.component.css']
})
export class ProjectsComponent implements OnInit {

  isLoading = false;
  projects = new Array<ResearchProject>();
  projectsInfos = [];

  constructor(public projectService: ProjectService,
              public spinner: NgxSpinnerService,
              public statsService: StatisticsService,
              public router: Router,
  ) { }

  ngOnInit(): void {
    this.getProjects()
  }

  getProjects() {
    this.isLoading = true;
    this.spinner.show('spinner');
    this.projectService.getProjects().subscribe((data) => {
      this.projects = data;
      if (data.length) {
        this.getProjectsStatus();
      } else {
        this.spinner.hide('spinner');
        this.isLoading = false;
      }
    });
  }

  getProjectsStatus() {
    this.projects.forEach((project) => {
      this.statsService.getValidated(project.id).subscribe((validated) => {
        this.statsService.getPredicted(project.id).subscribe((predicted) => {
          this.projectsInfos.push({
            id: project.id,
            status: project.status,
            validated: validated.percentage,
            predicted: predicted.percentage,
            file: project.project_file_url,
          });
          if (this.projectsInfos.length === this.projects.length) {
            this.spinner.hide('spinner');
            this.isLoading = false;
          }
          console.log(this.projectsInfos);
        });
      })
    })
  }

  visitProject(id) {
    localStorage.setItem('project_id', id);
    this.router.navigateByUrl('/dashboard')
  }

  openFileInput(file) {
    window.open(file, '_blank');
  }

}
