import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
@Component({
  selector: 'app-upload-file',
  templateUrl: './upload-file.component.html',
  styleUrls: ['./upload-file.component.css']
})
export class UploadFileComponent implements OnInit {

  loadedImg = true;
  fileToSend: any;

  constructor(private httpClient: HttpClient) { }

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
        const formData = new FormData();
        formData.append('file', this.fileToSend);
    
        this.httpClient.post<any>("http://127.0.0.1:8000/api/upload/", formData).subscribe(
          (res) => console.log(res),
          (err) => console.log(err)
        );
    }
  }
}
