import { TestBed } from '@angular/core/testing';

import { ExportFileService } from './export-file.service';

describe('ExportFileService', () => {
  let service: ExportFileService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ExportFileService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
