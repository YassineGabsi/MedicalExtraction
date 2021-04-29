import {Icd10Item} from './icd10-item';

export class ResearchItem {
  id: number;
  icd10_item: Icd10Item;
  title: string;
  research_summary: string;
  inclusion_criteria: string;
  project: number;
}
