import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-upload-file',
  templateUrl: './upload-file.component.html',
  styleUrls: ['./upload-file.component.css']
})
export class UploadFileComponent implements OnInit {

  loadedImg = true;
  fileToSend: any;

  constructor() { }

  ngOnInit() {
  }

  onChangeFile(fileInput) {
    const reader2 = new FileReader();
    let src;
    reader2.onload = (e) => {
      this.loadedImg = true;
      src = reader2.result;
      setTimeout(() => {
        const image = document.getElementById('image_500');
        const image1 = document.getElementById('image_500_1');
        if (image) { image.setAttribute('src', src); }
        if (image1) { image1.setAttribute('src', src); }
      });
      this.fileToSend = src;
      console.log(this.fileToSend);
    };
    reader2.readAsDataURL(fileInput.target.files[0]);
  }

  uploadFile() {
    document.getElementById('upload-file').click();
  }

}
