import {Component, Input, OnInit} from '@angular/core';
import {ResearchItem} from '../../../models/research-item';
import {Icd10Prediction} from '../../../models/icd10-prediction';

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
  public customICD10 = '';
  public predictedICDs: Array<Icd10Prediction>;

  constructor() { }

  ngOnInit(): void {
    console.log('aaa');
    this.predictedICDs = Array.from(this.recordItem.icd10_item.icd10_prediction);
    this.suggestionsNumber = Array(3).fill(5).map((x, i) => i);
    this.configureCustomICDSelection();
    console.log(this.suggestionsNumber);
    this.medicalTags.push('complications');
    this.medicalTags.push('heart diseases');
    this.medicalTags.push('coronary artery diseases');
    this.medicalTags.push('lorem upsum lorem upsum lorem upsum');
  }

  addSlice(): void {
    this.allAccepted = false;
    for (let i = 0 ; i< 3 ; i++) {
      this.suggestionsNumber.push(this.recordItem.icd10_item.icd10_prediction.indexOf(this.predictedICDs[0]));
      this.removeCustomICDAfterAdd(this.predictedICDs[0]);
    }
  }

  acceptOnePrediction(index) {
    this.acceptedPredictions.add(index);
    this.allAccepted = true;
    this.suggestionsNumber.forEach((item) => {
      if (!this.acceptedPredictions.has(item)) {
        this.allAccepted = false;
      }
    });
  }

  acceptAll() {
    console.log(this.suggestionsNumber);
    this.suggestionsNumber.forEach(this.acceptedPredictions.add, this.acceptedPredictions);
    console.log(this.acceptedPredictions);
    this.allAccepted = true;
  }

  deleteAll() {
    this.suggestionsNumber.forEach(this.acceptedPredictions.delete, this.acceptedPredictions);
    this.allAccepted = false;
  }

  deleteOnePrediction(index) {
    this.acceptedPredictions.delete(index);
    this.allAccepted = false;
  }

  isSuggAccepted(index) {
    return this.acceptedPredictions.has(index);
  }

  addCustomICD10() {
    this.allAccepted = false;
    const icd10PredArray = this.recordItem.icd10_item.icd10_prediction;
    const custICD10 = icd10PredArray.filter(item => item.predicted_block_name === this.customICD10)[0];
    this.suggestionsNumber.push(icd10PredArray.indexOf(custICD10));
    this.removeCustomICDAfterAdd(custICD10);
  }

  removeCustomICDAfterAdd(item) {
    console.log(item);
    this.predictedICDs.splice(this.predictedICDs.indexOf(item), 1);
    this.customICD10 = this.predictedICDs[0].predicted_block_name;
  }

  configureCustomICDSelection() {
    this.suggestionsNumber.forEach(item => {
      this.predictedICDs.splice(this.predictedICDs.indexOf(this.recordItem.icd10_item.icd10_prediction[item]), 1);
    });
    this.customICD10 = this.predictedICDs[0].predicted_block_name;
  }

  updateElements(record) {
    this.recordItem = record;
    this.acceptedPredictions = new Set<number>();
    this.predictedICDs = Array.from(this.recordItem.icd10_item.icd10_prediction);
    this.suggestionsNumber = Array(3).fill(5).map((x, i) => i);
    this.configureCustomICDSelection();
  }
}
