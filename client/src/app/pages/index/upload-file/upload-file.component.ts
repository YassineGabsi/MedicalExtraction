import {Component, OnInit} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Utils} from 'src/app/services/utils';
import {UploadFileService} from 'src/app/services/upload-file.service';
import Swal from 'sweetalert2';
import {ProjectService} from '../../../services/project.service';

@Component({
  selector: 'app-upload-file',
  templateUrl: './upload-file.component.html',
  styleUrls: ['./upload-file.component.css']
})
export class UploadFileComponent implements OnInit {

  loadedImg = true;
  fileToSend: any;

  constructor(
    private uploadFileService: UploadFileService,
    private projectService: ProjectService
  ) {
  }

  ngOnInit() {
  }

  onDropFile(event) {
    this.fileToSend = event[0];
    console.log(this.fileToSend);
  }


  onChangeFile(event) {
    if (event.target.files.length > 0) {
      this.fileToSend = event.target.files[0];
      console.log(this.fileToSend);
    }
  }

  uploadFile() {
    document.getElementById('upload-file').click();
  }

  upload() {
    if (this.fileToSend) {
      this.uploadFileService.sendFile(this.fileToSend).subscribe((res) => {
          console.log(res);
          localStorage.setItem('project_id', res.project_id);
        },
        (err) => {
          Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: err.error.message,
          });
          const errorMessage = err.error.message;
          console.log(errorMessage);
          console.log(err);
        }
      );
    }
  }
}
