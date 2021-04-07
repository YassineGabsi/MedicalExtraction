import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  public opened = false;
  public minimized = false;
  public mode = 'push';

  public records = new Array(15);
  public recordSelected = this.records[0];

  constructor() { }

  ngOnInit() {
    for (let i = 0; i < 16; i++) {
      this.records[i] = i + 1;
    }
  }

  selectRecord(i): void {
    this.recordSelected = i;
  }

  public _toggleSidebar(): void {
    this.opened = !this.opened;
    this.minimized = !this.minimized;
  }
}
