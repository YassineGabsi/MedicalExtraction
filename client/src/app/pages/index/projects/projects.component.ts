import { Component, OnInit } from '@angular/core';
import {ProjectService} from '../../../services/project.service';
import {NgxSpinnerService} from "ngx-spinner";
import {ResearchProject} from "../../../models/research-project";
import {StatisticsService} from "../../../services/statistics.service";

@Component({
  selector: 'app-projects',
  templateUrl: './projects.component.html',
  styleUrls: ['./projects.component.css']
})
export class ProjectsComponent implements OnInit {

  isLoading = false;
  projects = new Array<ResearchProject>();
  projectsInfos = [];

  constructor(private projectService: ProjectService,
              private spinner: NgxSpinnerService,
              private statsService: StatisticsService,
  ) { }

  ngOnInit(): void {
    this.getProjects()
  }

  getProjects() {
    this.isLoading = true;
    // this.spinner.show('spinner1');
    // this.spinner.show('spinner2');
    this.projectService.getProjects().subscribe((data) => {
      console.log(data);
      this.projects = data;
      this.getProjectsStatus();
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
            predicted: predicted.percentage
          });
          console.log(this.projectsInfos);
        });
      })
    })
  }

}
