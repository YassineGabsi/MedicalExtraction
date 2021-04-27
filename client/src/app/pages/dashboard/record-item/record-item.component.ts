import {Component, Input, OnInit} from '@angular/core';
import {ResearchItem} from '../../../models/research-item';

@Component({
  selector: 'app-record-item',
  templateUrl: './record-item.component.html',
  styleUrls: ['./record-item.component.css']
})
export class RecordItemComponent implements OnInit {

  @Input() recordItem: ResearchItem;
  public medicalTags = [];

  constructor() { }

  ngOnInit(): void {
    this.medicalTags.push('complications');
    this.medicalTags.push('heart diseases');
    this.medicalTags.push('coronary artery diseases');
    this.medicalTags.push('lorem upsum lorem upsum lorem upsum');
  }

}
