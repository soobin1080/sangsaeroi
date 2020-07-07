<template>
  <v-card class="mx-auto" width="360" max-height="400">
    <v-card-text>
      <div>상권 평가 등급</div>
      <p class="display-1 text--primary">
        {{ scores.grade }}
        <span style="font-size:20px">등급</span>
      </p>
      <apexchart type="radialBar" height="350" :options="gradechartOptions" :series="gradeseries"></apexchart>
    </v-card-text>
  </v-card>
</template>

<script>
import http from "../../http-common";
import VueApexCharts from "vue-apexcharts";

export default {
  name: "Grade",
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
      /////// 등급 //////
      gradeseries: [],
      gradechartOptions: {
        chart: {
          height: 350,
          type: "radialBar",
          offsetY: -10
        },
        plotOptions: {
          radialBar: {
            startAngle: -90,
            endAngle: 90,
            dataLabels: {
              name: {
                fontSize: "16px",
                color: undefined,
                offsetY: 120
              },
              value: {
                offsetY: 76,
                fontSize: "22px",
                color: undefined,
                formatter: function(val) {
                  return val / 16;
                }
              }
            }
          }
        },
        fill: {
          type: "gradient",
          gradient: {
            shade: "dark",
            shadeIntensity: 0.15,
            inverseColors: false,
            opacityFrom: 1,
            opacityTo: 1,
            stops: [0, 50, 65, 91]
          }
        },
        stroke: {
          dashArray: 4
        },
        labels: ["등급"]
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

          this.gradeseries = [];
          this.gradeseries.push(this.scores.grade * 16);
          this.check = true;
        })
        .catch(err => {
          console.log(err);
        });
    }
  }
};
</script>