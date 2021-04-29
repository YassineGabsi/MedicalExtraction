import {ResearchItem} from './research-item';

export class ResearchProject {
  id: number;
  items = new Array<ResearchItem>();
  start_date: string;
  end_date: string;
  status: string;
  project_file_url: string;
}
