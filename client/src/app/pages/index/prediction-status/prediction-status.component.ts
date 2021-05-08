import {Component, OnDestroy, OnInit} from '@angular/core';
import {StatisticsService} from '../../../services/statistics.service';
import {PredictedStats} from '../../../models/predicted-stats';
import {ValidatedStats} from '../../../models/validated-stats';
import {NgxSpinnerService} from "ngx-spinner";

declare var $: any;

@Component({
  selector: 'app-prediction-status',
  templateUrl: './prediction-status.component.html',
  styleUrls: ['./prediction-status.component.css']
})
export class PredictionStatusComponent implements OnInit, OnDestroy {

  constructor(private statsService: StatisticsService,
              private spinner: NgxSpinnerService,
  ) { }

  predictedStatus: PredictedStats = new PredictedStats();
  validatedStatus: ValidatedStats = new ValidatedStats();
  projectId = localStorage.getItem('project_id');
  statusTracker;
  isLoading = true;

  ngOnInit() {
    this.predictedStatus.predicted_count = 0;
    this.predictedStatus.total_count = 0;
    this.validatedStatus.total_count = 0;
    this.validatedStatus.validated_count = 0;
    this.isLoading = true;
    this.spinner.show();
    this.getPredictedStatus();
    this.statusTracker = setInterval(() => {
      this.getPredictedStatus();
      if (parseInt(this.predictedStatus.percentage, 10) === 100 && parseInt(this.validatedStatus.percentage, 10) === 100 ) {
        clearInterval(this.statusTracker);
      }
    }, 4000);
  }

  getPredictedStatus() {
    this.statsService.getPredicted(this.projectId).subscribe(data => {
      this.predictedStatus = data;
      this.getValidatedStatus();
      console.log(data);
    });
  }

  getValidatedStatus() {
    this.statsService.getValidated(this.projectId).subscribe(data => {
      this.spinner.hide();
      this.isLoading = false;
      this.validatedStatus = data;
      this.setPercentageValidated(parseInt(this.validatedStatus.percentage, 10));
      this.setPercentagePredicted(parseInt(this.predictedStatus.percentage, 10));
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

  ngOnDestroy(): void {
    clearInterval(this.statusTracker);
  }

}
