import {Icd10Prediction} from './icd10-prediction';

export class Icd10Item {
  id: number;
  icd10_prediction = new Array<Icd10Prediction>();
  icd10_validation = new Array<any>();
  medical_terms = new Array<string>();
  first_prediction_accepted: boolean;
  validated: boolean;
  item: number;
}
