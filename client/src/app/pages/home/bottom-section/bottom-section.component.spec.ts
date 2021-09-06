import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BottomSectionComponent } from './bottom-section.component';

describe('BottomSectionComponent', () => {
  let component: BottomSectionComponent;
  let fixture: ComponentFixture<BottomSectionComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BottomSectionComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BottomSectionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
