<template>
  <v-card class="mx-auto" width="360" max-height="400">
    <v-card-text>
      <div>총점</div>
      <p class="display-1 text--primary">
        {{scores.total_score}}
        <span style="font-size:20px">점</span>
      </p>
      <apexchart v-if="check" type="radar" height="350" :options="chartOptions" :series="series"></apexchart>
    </v-card-text>
  </v-card>
</template>
<script>
import http from "../../http-common";
import VueApexCharts from "vue-apexcharts";

export default {
  name: "Score",
  components: {
    apexchart: VueApexCharts
  },
  props: {
    guname: { type: String },
    dongname: { type: String }
  },
  data() {
    return {
      check: false,
      scores: {
        total_score: "", // 총점
        grade: "", // 등급
        grothIndex: "", // 성장성
        stability: "", // 안정성
        salePwr: "", // 영업력
        buyingPwr: "", // 구매력
        gathPwr: "" // 집객력
      },
      /////////5분야 점수/////
      series: [
        {
          name: "",
          data: []
        }
      ],
      chartOptions: {
        chart: {
          height: 350,
          type: "radar"
        },

        xaxis: {
          categories: ["성장성", "안정성", "영업력", "구매력", "집객력"]
        }
      }
    };
  },
  watch: {
    guname: "getAnalyzeReport",
    dongname: "getAnalyzeReport"
  },
  mounted() {
    if (this.guname != "" && this.dongname != "") this.getAnalyzeReport();
  },
  methods: {
    getAnalyzeReport() {
      this.check = false;
      http
        .get(`api/analyze/${this.guname}/${this.dongname}/`)
        .then(response => {
          this.scores = response.data.scores;

          this.series[0].data = [];
          this.series[0].data.push(this.scores.grothIndex);
          this.series[0].data.push(this.scores.stability);
          this.series[0].data.push(this.scores.salePwr);
          this.series[0].data.push(this.scores.buyingPwr);
          this.series[0].data.push(this.scores.gathPwr);

          this.check = true;
        })
        .catch(err => {
          console.log(err);
        });
    }
  }
};
</script>