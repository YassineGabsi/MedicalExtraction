import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PredictionStatusComponent } from './prediction-status.component';

describe('PredictionStatusComponent', () => {
  let component: PredictionStatusComponent;
  let fixture: ComponentFixture<PredictionStatusComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PredictionStatusComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PredictionStatusComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
