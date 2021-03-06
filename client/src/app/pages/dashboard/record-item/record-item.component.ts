import {Component, Input, OnInit, Output, EventEmitter, OnChanges} from '@angular/core';
import {ResearchItem} from '../../../models/research-item';
import {Icd10Prediction} from '../../../models/icd10-prediction';
import {Icd10ItemService} from '../../../services/icd10-item.service';
import Swal from 'sweetalert2';

declare var $: any;

@Component({
  selector: 'app-record-item',
  templateUrl: './record-item.component.html',
  styleUrls: ['./record-item.component.css']
})
export class RecordItemComponent implements OnInit, OnChanges {

  @Input() recordItem: ResearchItem;
  @Input() windowsWidth: number;
  public medicalTags = [];
  public suggestionsNumber;
  public acceptedPredictions = new Set<number>();
  public allAccepted = false;
  public customICD10 = '';
  public predictedICDs: Array<Icd10Prediction>;

  public splittedInclusionCriteria = null;
  public splittedTitle = null;
  public splittedSummary = null;

  @Output() nextRecordEvent = new EventEmitter<any>();
  @Output() validateNumber = new EventEmitter<any>();

  constructor(private icd10ItemService: Icd10ItemService) {
  }

  ngOnInit(): void {
    if (this.recordItem.icd10_item) {
      this.splitToColorMedicalTerms();
      if (this.recordItem.icd10_item.icd10_validation === null) {
        this.recordItem.icd10_item.icd10_validation = [];
      }
      this.predictedICDs = Array.from(this.recordItem.icd10_item.icd10_prediction);
      this.suggestionsNumber = Array(3).fill(5).map((x, i) => i);
      this.configureCustomICDSelection();
      if (this.recordItem.icd10_item.icd10_validation === null) {
        this.getValidatedPredictions();
      }
      console.log(this.suggestionsNumber);
      this.updateMedicalTags()
    }
  }

  updateMedicalTags() {
    this.medicalTags = [];
    this.recordItem.icd10_item.medical_terms.forEach(
      term => this.medicalTags.push(term.toLowerCase())
    )
  }

  ngOnChanges(changes) {
    if (this.recordItem.icd10_item) {
      this.updateMedicalTags();
      this.splitToColorMedicalTerms();
    }
  }

  addSlice(): void {
    this.allAccepted = false;
    for (let i = 0; i < 3; i++) {
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
    console.log(this.suggestionsNumber);
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

  testIfAllAccepted() {
    let test = true;
    this.suggestionsNumber.forEach(item => {
      if (!this.acceptedPredictions.has(item)) {
        test = false
      }
    });
    if (test) this.allAccepted = true;
    return test;
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
    console.log(this.recordItem)
    if (this.recordItem.icd10_item && this.recordItem.icd10_item.icd10_validation === null) {
      this.recordItem.icd10_item.icd10_validation = [];
    }
    this.recordItem = record;
    if (this.suggestionsNumber) this.deleteAll();
    this.predictedICDs = Array.from(this.recordItem.icd10_item.icd10_prediction);
    this.suggestionsNumber = Array(3).fill(5).map((x, i) => i);
    this.configureCustomICDSelection();
    if (this.recordItem.icd10_item.icd10_validation !== null) {
      this.getValidatedPredictions();
    }
  }

  scoreCalc(score) {
    return (score * 100).toFixed(2);
  }

  nextRecord(scrolled) {
    this.nextRecordEvent.emit();
    if (!scrolled) {
      $('.ng-sidebar__content').animate({
        scrollTop: 0
      });
    }
  }

  validateNum() {
    this.validateNumber.emit();
  }

  validatePrediction() {
    if (this.acceptedPredictions.size) {
      const validation = [];
      this.acceptedPredictions.forEach(item => {
        validation.push(this.recordItem.icd10_item.icd10_prediction[item]);
      });
      this.recordItem.icd10_item.icd10_validation = validation;
      this.recordItem.icd10_item.validated = false;
      const dataToSend = {
        icd10_validation: validation,
        validated: true,
        first_prediction_accepted: this.acceptedPredictions.has(0),
      };
      this.icd10ItemService.patchICD10Item(this.recordItem.icd10_item.id, dataToSend).subscribe((data) => {
        let scrolled = false;
        Swal.fire({
          icon: 'success',
          title: 'Record Validated',
          text: 'Congratulation, your record has been validated succefully!',
        }).then(() => {
          $('.ng-sidebar__content').animate({
            scrollTop: 0
          });
          this.validateNum();
          this.nextRecord(true);
          scrolled = true;
        });
        this.recordItem.icd10_item = data;
        setTimeout(() => {
          Swal.close();
          if (!scrolled) {
            this.validateNum();
            this.nextRecord(true);
            $('.ng-sidebar__content').animate({
              scrollTop: 0
            });
          }
        }, 2000);
      }, (err) => {
        Swal.fire({
          icon: 'error',
          title: 'Oops...',
          text: err.error.message,
        });
        console.log(err);
      });
    } else {
      Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: 'You didn\'t choose any suggestion to validate this record. Please choose an ICD10 block name.',
      });
    }
  }

  getValidatedPredictions() {
    this.recordItem.icd10_item.icd10_validation.forEach(item => {
      const itemFiltered = this.recordItem.icd10_item.icd10_prediction.filter(filtered =>
        filtered.predicted_block_code === item.predicted_block_code)[0];
      const indexOfItem = this.recordItem.icd10_item.icd10_prediction.indexOf(itemFiltered);
      this.acceptedPredictions.add(indexOfItem);
      !this.suggestionsNumber.includes(indexOfItem) ? this.suggestionsNumber.push(indexOfItem) : null;
    });
    console.log(this.testIfAllAccepted());
    console.log(this.acceptedPredictions);
  }

  splitToColorMedicalTerms() {
    this.splittedInclusionCriteria = this.recordItem.inclusion_criteria.split(' ');
    this.splittedTitle = this.recordItem.title.split(' ');
    console.log(this.recordItem);
    this.splittedSummary = this.recordItem.research_summary.split(' ');
  }

  isMedicalTag(word: string): boolean {
    const lowerCase = word.split('.')[0].split(',')[0].split('-')[0].toLowerCase();
    return this.medicalTags.includes(lowerCase);
  }
}
