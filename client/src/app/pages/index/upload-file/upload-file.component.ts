import {Component, OnInit} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Utils} from 'src/app/services/utils';
import {UploadFileService} from 'src/app/services/upload-file.service';
import Swal from 'sweetalert2';
import { NgxSpinnerService } from 'ngx-spinner';
import {ActivatedRoute, Router} from '@angular/router';

@Component({
  selector: 'app-upload-file',
  templateUrl: './upload-file.component.html',
  styleUrls: ['./upload-file.component.css']
})
export class UploadFileComponent implements OnInit {

  isLoading = false;
  fileToSend: any;

  constructor(
    private uploadFileService: UploadFileService,
    private spinner: NgxSpinnerService,
    private route: Router,
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
      this.isLoading = true;
      this.spinner.show();
      this.uploadFileService.sendFile(this.fileToSend).subscribe((res) => {
          console.log(res);
          localStorage.setItem('project_id', res.project_id);
          this.isLoading = false;
          this.spinner.hide();
          this.route.navigateByUrl('/status');
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
          this.isLoading = false;
          this.spinner.hide();
        }
      );
    }
  }
}
