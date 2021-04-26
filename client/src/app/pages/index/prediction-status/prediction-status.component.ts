import { Component, OnInit } from '@angular/core';
import {StatisticsService} from '../../../services/statistics.service';
import {PredictedStats} from '../../../models/predicted-stats';
import {ValidatedStats} from '../../../models/validated-stats';

declare var $: any;

@Component({
  selector: 'app-prediction-status',
  templateUrl: './prediction-status.component.html',
  styleUrls: ['./prediction-status.component.css']
})
export class PredictionStatusComponent implements OnInit {

  constructor(private statsService: StatisticsService) { }

  predictedStatus: PredictedStats;
  validatedStatus: ValidatedStats;
  projectId = localStorage.getItem('project_id');

  ngOnInit() {
    this.getPredictedStatus();
    this.getValidatedStatus();
    const interval = setInterval(() => {
      this.getPredictedStatus();
      this.getValidatedStatus();
      if (parseInt(this.predictedStatus.percentage, 10) === 100 && parseInt(this.validatedStatus.percentage, 10) === 100 ) {
        clearInterval(interval);
      }
    }, 4000);
  }

  getPredictedStatus() {
    this.statsService.getPredicted(this.projectId).subscribe(data => {
      this.predictedStatus = data;
      this.setPercentagePredicted(parseInt(this.predictedStatus.percentage, 10));
      console.log(data);
    });
  }

  getValidatedStatus() {
    this.statsService.getValidated(this.projectId).subscribe(data => {
      this.validatedStatus = data;
      this.setPercentageValidated(parseInt(this.validatedStatus.percentage, 10));
      console.log(data);
    });
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
