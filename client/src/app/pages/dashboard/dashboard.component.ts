import {Component, HostListener, OnInit, ViewChild} from '@angular/core';
import {ProjectService} from '../../services/project.service';
import {ResearchItem} from '../../models/research-item';
import {NgxSpinnerService} from 'ngx-spinner';
import {RecordItemComponent} from './record-item/record-item.component';
import {ExportFileService} from '../../services/export-file.service';
import Swal from 'sweetalert2';
import {ResearchProject} from "../../models/research-project";

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
  public filteredRecords: ResearchItem[];
  public recordSelected: ResearchItem;
  public project: ResearchProject;

  public isLoading = false;

  private projectId = localStorage.getItem('project_id');
  private searchString = '';
  private searchSelected = 'all';
  private windowsWidth = window.innerWidth;
  private mobileOpen = false;

  @ViewChild(RecordItemComponent) recordItemChild;

  constructor(private projectService: ProjectService,
              private spinner: NgxSpinnerService,
              private exportFileService: ExportFileService
  ) {
  }

  ngOnInit() {
    if (window.screen.width < 576) {
      this.mode = 'over';
      this.mobileOpen = true;
      this.opened = false;
      this.minimized = true;
    } else {
      this.mode = 'push';
      this.mobileOpen = false;
      this.opened = true;
      this.minimized = false;
    }
    if (window.screen.width >= 576 && window.screen.width < 769) {
      this.mode = 'over';
    }
    this.getProject();
  }

  getProject() {
    this.isLoading = true;
    this.spinner.show('spinner1');
    this.spinner.show('spinner2');
    this.projectService.getProjectById(this.projectId).subscribe((data) => {
      console.log(data);
      this.project = data;
      this.records = data.items;
      this.filteredRecords = this.records;
      this.recordSelected = this.records[0];
      this.isLoading = false;
      this.spinner.hide('spinner1');
      this.spinner.hide('spinner2');
    });
  }


  @HostListener('window:resize') windwosResize() {
    this.windowsWidth = window.innerWidth;
    if (this.windowsWidth < 576) {
      this.mode = 'over';
      this.mobileOpen = true;
      if (this.opened) {
        this._toggleSidebar()
      }

    } else if (this.windowsWidth >= 576) {
      this.mode = 'push';
      this.opened = true;
      this.minimized = false;
      this.mobileOpen = false;
    }
    if (window.screen.width >= 576 && window.screen.width < 769) {
      this.mode = 'over';
    }
  }

  selectRecord(i): void {
    this.recordSelected = this.filteredRecords[i];
    if (this.recordSelected.icd10_item) {
      this.recordItemChild.updateElements(this.recordSelected);
    }
  }

  public _toggleSidebar(): void {
    this.opened = !this.opened;
    this.minimized = !this.minimized;
  }

  filterRows(e) {
    if (this.searchSelected === 'all') {
      this.filteredRecords = this.records.filter((item) => item.title.toLowerCase().includes(e.toLowerCase()));
    } else if (this.searchSelected === 'validated') {
      const validated = this.records.filter(item => item.icd10_item.validated);
      this.filteredRecords = validated.filter((item) => item.title.toLowerCase().includes(e.toLowerCase()));
    } else if (this.searchSelected === 'non-validated') {
      const nonValidated = this.records.filter(item => !item.icd10_item.validated);
      this.filteredRecords = nonValidated.filter((item) => item.title.toLowerCase().includes(e.toLowerCase()));
    }
    console.log(e);
  }

  nextRecord() {
    this.selectRecord(this.filteredRecords.indexOf(this.recordSelected) + 1);
  }

  toggleSearch(search) {
    this.searchString = '';
    this.searchSelected = search;
    if (search === 'validated') {
      this.filteredRecords = this.records.filter(item => item.icd10_item.validated);
    } else if (search === 'non-validated') {
      this.filteredRecords = this.records.filter(item => !item.icd10_item.validated);
    } else {
      this.filteredRecords = this.records;
    }
  }

  exportOutput() {
    this.exportFileService.exportFile(this.projectId).subscribe((data) => {
      console.log(data);
      this.downloadData(data);
      Swal.fire({
        icon: 'success',
        title: 'Congratulation!',
        text: 'Your download should have been started. If not, you can click on \'Download again\' button.',
        showCancelButton: true,
        cancelButtonText: 'Close',
        confirmButtonText: 'Download Again'
      }).then((res) => {
        if (res.value) {
          this.downloadData(data);
        }
      });
    });
  }

  downloadData(data) {
    const link = document.createElement('a');
    link.setAttribute('target', '_blank');
    link.setAttribute('href', data.file_url);
    link.setAttribute('download', `result.csv`);
    document.body.appendChild(link);
    link.click();
    link.remove();
  }
}
