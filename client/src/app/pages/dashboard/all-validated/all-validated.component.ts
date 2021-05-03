import {Component, EventEmitter, OnInit, Output} from '@angular/core';

@Component({
  selector: 'app-all-validated',
  templateUrl: './all-validated.component.html',
  styleUrls: ['./all-validated.component.css']
})
export class AllValidatedComponent implements OnInit {
  @Output() downloadResults = new EventEmitter<any>();

  constructor() { }

  ngOnInit(): void {
  }

  downloadOutput() {
    this.downloadResults.emit();
  }

}
