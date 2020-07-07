<template>
  <v-card class="mx-auto" width="800px">
    <v-card-text v-if="this.foottraffic.error == 0" class="text--primary">골목 상권 데이터가 없습니다.</v-card-text>
    <v-card-text v-else>
      <div>
        유동 인구
        <span style="float:right">['19년 2분기 기준]</span>
      </div>
      <p class="display-1 text--primary">
        <span class="mdi mdi-walk pr-3"></span>
        {{foottraffic.total}}
        <span style="font-size:20px">명</span>
      </p>
      <v-row class="mx-auto">
        <apexchart type="donut" height="200" :options="GenderchartOptions" :series="Genderseries"></apexchart>
        <apexchart type="bar" :options="AgechartOptions" :series="Ageseries"></apexchart>
        <apexchart
          class="px-1"
          type="line"
          height="250"
          :options="WeekchartOptions"
          :series="Weekseries"
        ></apexchart>
        <apexchart
          class="px-1"
          type="area"
          height="250"
          :options="TimechartOptions"
          :series="Timeseries"
        ></apexchart>
      </v-row>
    </v-card-text>
  </v-card>
</template>
<script>
import http from "../../http-common";
import VueApexCharts from "vue-apexcharts";

export default {
  name: "Foottraffic",
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
      colors: [
        "#2E93fA",
        "#66DA26",
        "#546E7A",
        "#E91E63",
        "#FF9800",
        "#E1E1E1"
      ],
      ////////유동인구/////////
      foottraffic: {
        total: 0,
        men: 0,
        women: 0,
        teen: 0,
        twenty: 0,
        thirty: 0,
        fourty: 0,
        fifty: 0,
        sixty: 0,
        time1: 0, // 00~06시
        time2: 0, // 06~11시
        time3: 0, // 11~14시
        time4: 0, // 14~17시
        time5: 0, // 17~21시
        time6: 0, // 21~24시
        mon: 0,
        tue: 0,
        wed: 0,
        thr: 0,
        fri: 0,
        sat: 0,
        sun: 0
      },
      ////////// 성별 ///////////
      Genderseries: [],
      GenderchartOptions: {
        markers: {
          colors: ["#059fff", "#ff9caf"]
        },
        colors: ["#059fff", "#ff9caf"],
        chart: {
          type: "donut",
          dropShadow: {
            enabled: true,
            color: "#111",
            top: -1,
            left: 3,
            blur: 3,
            opacity: 0.2
          }
        },
        plotOptions: {
          pie: {
            donut: {
              labels: {
                show: true,
                total: {
                  showAlways: true,
                  show: true
                },
                name: {
                  colors: ["#059fff", "#ff9caf"]
                },
                value: {
                  colors: ["#059fff", "#ff9caf"]
                }
              }
            }
          }
        },
        labels: ["남", "여"],
        dataLabels: {
          dropShadow: {
            blur: 3,
            opacity: 0.8
          }
        },
        states: {
          hover: {
            filter: "none"
          }
        },
        fill: {
          colors: ["#059fff", "#ff9caf"]
        },
        responsive: [
          {
            breakpoint: 480,
            options: {
              chart: {
                width: 200
              },
              legend: {
                position: "bottom"
              },
              colors: ["#059fff", "#ff9caf"]
            }
          }
        ]
      },
      ////////// 연령 ////////////
      Ageseries: [
        {
          data: []
        }
      ],
      AgechartOptions: {
        chart: {
          height: 250,
          width: 330,
          type: "bar"
        },
        colors: this.colors,
        plotOptions: {
          bar: {
            columnWidth: "45%",
            distributed: true
          }
        },
        dataLabels: {
          enabled: false
        },
        legend: {
          show: false
        },
        xaxis: {
          categories: ["10대", "20대", "30대", "40대", "50대", "60대 이상"],
          labels: {
            style: {
              colors: this.colors,
              fontSize: "12px"
            }
          }
        }
      },
      ///////////// 요일 //////////
      Weekseries: [
        {
          data: []
        }
      ],
      WeekchartOptions: {
        chart: {
          height: 250,
          type: "line",
          zoom: {
            enabled: false
          }
        },
        dataLabels: {
          enabled: false
        },
        stroke: {
          curve: "straight"
        },

        grid: {
          row: {
            colors: ["#f3f3f3", "transparent"],
            opacity: 0.5
          }
        },
        xaxis: {
          categories: ["월", "화", "수", "목", "금", "토", "일"]
        }
      },
      /////////// 시간대 /////////
      Timeseries: [
        {
          data: []
        }
      ],
      TimechartOptions: {
        chart: {
          height: 250,
          type: "area"
        },
        dataLabels: {
          enabled: false
        },
        stroke: {
          curve: "smooth"
        },
        xaxis: {
          categories: [
            "00시~06시",
            "06시~11시",
            "11시~14시",
            "14시~17시",
            "17시~21시",
            "21시~24시"
          ]
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
          this.foottraffic = response.data.foottraffic;
          this.foottraffic.total = this.foottraffic.total.toLocaleString();

          this.Genderseries = [];
          this.Genderseries.push(this.foottraffic.men);
          this.Genderseries.push(this.foottraffic.women);

          this.Ageseries = [];
          var Agearray = [];
          Agearray.push(this.foottraffic.teen);
          Agearray.push(this.foottraffic.twenty);
          Agearray.push(this.foottraffic.thirty);
          Agearray.push(this.foottraffic.fourty);
          Agearray.push(this.foottraffic.fifty);
          Agearray.push(this.foottraffic.sixty);
          var data = {
            data: Agearray
          };
          this.Ageseries.push(data);

          this.Weekseries = [];
          var Weekarray = [];
          Weekarray.push(this.foottraffic.mon);
          Weekarray.push(this.foottraffic.tue);
          Weekarray.push(this.foottraffic.wed);
          Weekarray.push(this.foottraffic.thr);
          Weekarray.push(this.foottraffic.fri);
          Weekarray.push(this.foottraffic.sat);
          Weekarray.push(this.foottraffic.sun);
          var weekdata = {
            data: Weekarray
          };
          this.Weekseries.push(weekdata);

          this.Timeseries = [];
          var Timearray = [];
          Timearray.push(this.foottraffic.time1);
          Timearray.push(this.foottraffic.time2);
          Timearray.push(this.foottraffic.time3);
          Timearray.push(this.foottraffic.time4);
          Timearray.push(this.foottraffic.time5);
          Timearray.push(this.foottraffic.time6);
          var timedata = {
            data: Timearray
          };
          this.Timeseries.push(timedata);

          this.check = true;
        })
        .catch(err => {
          console.log(err);
        });
    }
  }
};
</script>