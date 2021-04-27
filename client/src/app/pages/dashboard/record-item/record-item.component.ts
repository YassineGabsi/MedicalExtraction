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
  public suggestionsNumber;
  public acceptedPredictions = new Set<number>();
  public allAccepted = false;

  constructor() { }

  ngOnInit(): void {
    this.suggestionsNumber = Array(3).fill(5).map((x, i) => i + 1);
    this.medicalTags.push('complications');
    this.medicalTags.push('heart diseases');
    this.medicalTags.push('coronary artery diseases');
    this.medicalTags.push('lorem upsum lorem upsum lorem upsum');
  }

  addSlice(): void {
    for (let i = 0 ; i< 3 ; i++) {
      this.suggestionsNumber.push(this.suggestionsNumber[this.suggestionsNumber.length - 1 ] + 1)
    }
  }

  acceptOnePrediction(index) {
    this.acceptedPredictions.add(index);
  }

  acceptAll() {
    this.suggestionsNumber.forEach(this.acceptedPredictions.add, this.acceptedPredictions);
    this.acceptedPredictions.add(0);
    this.acceptedPredictions.delete(this.suggestionsNumber[this.suggestionsNumber.length - 1])
    this.allAccepted = true;
  }

  deleteAll() {
    this.suggestionsNumber.forEach(this.acceptedPredictions.delete, this.acceptedPredictions);
    this.acceptedPredictions.delete(0);
    this.allAccepted = false;
  }

  deleteOnePrediction(index) {
    this.acceptedPredictions.delete(index);
  }

  isSuggAccepted(index) {
    return this.acceptedPredictions.has(index);
  }

}
