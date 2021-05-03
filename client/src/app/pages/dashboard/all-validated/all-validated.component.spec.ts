import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AllValidatedComponent } from './all-validated.component';

describe('AllValidatedComponent', () => {
  let component: AllValidatedComponent;
  let fixture: ComponentFixture<AllValidatedComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AllValidatedComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AllValidatedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
