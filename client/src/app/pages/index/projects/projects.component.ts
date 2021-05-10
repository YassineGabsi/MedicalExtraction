import { Component, OnInit } from '@angular/core';
import {ProjectService} from '../../../services/project.service';
import {NgxSpinnerService} from "ngx-spinner";
import {ResearchProject} from "../../../models/research-project";

@Component({
  selector: 'app-projects',
  templateUrl: './projects.component.html',
  styleUrls: ['./projects.component.css']
})
export class ProjectsComponent implements OnInit {

  isLoading = false;
  projects = new Array<ResearchProject>();

  constructor(private projectService: ProjectService,
              private spinner: NgxSpinnerService,
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
    });
  }

}
