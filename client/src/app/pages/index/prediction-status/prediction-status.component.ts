import { Component, OnInit } from '@angular/core';

declare var $: any;

@Component({
  selector: 'app-prediction-status',
  templateUrl: './prediction-status.component.html',
  styleUrls: ['./prediction-status.component.css']
})
export class PredictionStatusComponent implements OnInit {

  constructor() { }

  ngOnInit() {
    this.setPercentagePredicted(15);
    this.setPercentageValidated(40);
  }

  setPercentagePredicted(val) {
      console.log(val);
      const $circle = $('#svg #bar');
      if (isNaN(val)) {
        val = 100;
      } else {
        const r = $circle.attr('r');
        const c = Math.PI * (r * 2);

        if (val < 0) { val = 0; }
        if (val > 100) { val = 100; }

        const pct = ((100 - val ) / 100) * c;

        $circle.css({ strokeDashoffset: pct});

        $('#cont').attr('data-pct', val);
      }
  }
  setPercentageValidated(val) {
    console.log(val);
    const $circle = $('#svg2 #bar2');
    if (isNaN(val)) {
      val = 100;
    } else {
      const r = $circle.attr('r');
      const c = Math.PI * (r * 2);

      if (val < 0) { val = 0; }
      if (val > 100) { val = 100; }

      const pct = ((100 - val ) / 100) * c;

      $circle.css({ strokeDashoffset: pct});

      $('#cont2').attr('data-pct', val);
    }
  }

}
