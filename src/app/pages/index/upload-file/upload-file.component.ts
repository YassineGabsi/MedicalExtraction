import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Utils } from 'src/app/services/utils';
import { UploadFileService } from 'src/app/services/upload-file.service';
@Component({
  selector: 'app-upload-file',
  templateUrl: './upload-file.component.html',
  styleUrls: ['./upload-file.component.css']
})
export class UploadFileComponent implements OnInit {

  loadedImg = true;
  fileToSend: any;

  constructor(
    private uploadFileService: UploadFileService
  ) { }

  ngOnInit() {
  }

  onChangeFile(event) {
    if (event.target.files.length > 0) {
      this.fileToSend = event.target.files[0];
    }
  }

  uploadFile() {
    document.getElementById('upload-file').click();
  }

  upload(){
    if(this.fileToSend){
      const observable = this.uploadFileService.sendFile(this.fileToSend)
      observable.subscribe(
        (res) =>{
          console.log(res)
        },
        (err) => {
          const errorMessage = err.error.message

          console.log(errorMessage)
          console.log(err)
        }
      )
    }
  }
}
