<template>
  <v-card class="mx-auto" width="800px">
    <v-card-text v-if="this.sales.error == 0" class="text--primary">골목 상권 데이터가 없습니다.</v-card-text>
    <v-card-text v-else>
      <div>
        추정 매출액
        <span style="float:right">['19년 2분기 기준]</span>
      </div>
      <p class="display-1 text--primary">
        <span class="mdi mdi-cash-multiple pr-3"></span>
        {{ sales.sale.month }}
        <span style="font-size:20px">만원</span>
        <span style="font-size:12px">/월</span>
      </p>
      <v-flex lg12>
        <v-row class="mx-auto">
          <apexchart type="donut" height="200" :options="GenderchartOptions" :series="Genderseries"></apexchart>
          <apexchart type="bar" :options="AgechartOptions" :series="Ageseries"></apexchart>
          <apexchart
            class="px-1"
            type="bar"
            height="250"
            :options="DaychartOptions"
            :series="Dayseries"
          ></apexchart>
          <apexchart
            class="px-1"
            type="area"
            height="250"
            :options="TimechartOptions"
            :series="Timeseries"
          ></apexchart>
        </v-row>
      </v-flex>
    </v-card-text>
  </v-card>
</template>

<script>
import http from "../../http-common";
import VueApexCharts from "vue-apexcharts";

export default {
  name: "Sales",
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
      sales: {
        sale: {
          month: 0,
          week: 0,
          weekend: 0,
          mon: 0,
          tue: 0,
          wed: 0,
          thr: 0,
          fri: 0,
          sat: 0,
          sun: 0,
          time1: 0,
          time2: 0,
          time3: 0,
          time4: 0,
          time5: 0,
          time6: 0,
          men: 0,
          women: 0,
          teen: 0,
          twenty: 0,
          thirty: 0,
          fourty: 0,
          fifty: 0,
          sixty: 0
        },
        rate: {
          week: 0,
          weekend: 0,
          mon: 0,
          tue: 0,
          wed: 0,
          thr: 0,
          fri: 0,
          sat: 0,
          sun: 0,
          time1: 0,
          time2: 0,
          time3: 0,
          time4: 0,
          time5: 0,
          time6: 0,
          men: 0,
          women: 0,
          teen: 0,
          twenty: 0,
          thirty: 0,
          fourty: 0,
          fifty: 0,
          sixty: 0
        }
      }, // 매출액

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
      ////////// 주중/주말 /////////
      Dayseries: [
        {
          name: "월",
          data: []
        },
        {
          name: "화",
          data: []
        },
        {
          name: "수",
          data: []
        },
        {
          name: "목",
          data: []
        },
        {
          name: "금",
          data: []
        },
        {
          name: "토",
          data: []
        },
        {
          name: "일",
          data: []
        }
      ],
      DaychartOptions: {
        chart: {
          type: "bar",
          height: 250,
          stacked: true
        },
        plotOptions: {
          bar: {
            horizontal: true
          }
        },
        stroke: {
          width: 1,
          colors: ["#fff"]
        },
        xaxis: {
          categories: ["주중", "주말"],
          labels: {
            formatter: function(val) {
              return val + "만";
            }
          }
        },
        yaxis: {
          title: {
            text: undefined
          }
        },
        tooltip: {
          y: {
            formatter: function(val) {
              return val + "만";
            }
          }
        },
        fill: {
          opacity: 1
        },
        legend: {
          position: "top",
          horizontalAlign: "left",
          offsetX: 40
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
      // alert("분석");
      http
        .get(`api/analyze/${this.guname}/${this.dongname}/`)
        .then(response => {
          this.sales = response.data.sales;
          this.sales.sale = response.data.sales.sale;
          this.sales.sale.month = this.sales.sale.month.toLocaleString();

          this.Genderseries = [];
          this.Genderseries.push(this.sales.sale.men);
          this.Genderseries.push(this.sales.sale.women);

          this.Ageseries = [];
          var Agearray = [];
          Agearray.push(this.sales.sale.teen);
          Agearray.push(this.sales.sale.twenty);
          Agearray.push(this.sales.sale.thirty);
          Agearray.push(this.sales.sale.fourty);
          Agearray.push(this.sales.sale.fifty);
          Agearray.push(this.sales.sale.sixty);
          var agedata = {
            data: Agearray
          };
          this.Ageseries.push(agedata);

          this.Timeseries = [];
          var Timearray = [];
          Timearray.push(this.sales.sale.time1);
          Timearray.push(this.sales.sale.time2);
          Timearray.push(this.sales.sale.time3);
          Timearray.push(this.sales.sale.time4);
          Timearray.push(this.sales.sale.time5);
          Timearray.push(this.sales.sale.time6);
          var timedata = {
            data: Timearray
          };
          this.Timeseries.push(timedata);

          this.Dayseries = [];
          var DayArray = [
            { data: [this.sales.sale.mon, 0] },
            { data: [this.sales.sale.tue, 0] },
            { data: [this.sales.sale.wed, 0] },
            { data: [this.sales.sale.thr, 0] },
            { data: [this.sales.sale.fri, 0] },
            { data: [0, this.sales.sale.sat] },
            { data: [0, this.sales.sale.sun] }
          ];
          var MonArray = [];
          MonArray.push(this.sales.sale.mon);
          MonArray.push(0);
          var TueArray = [];
          TueArray.push(this.sales.sale.tue);
          TueArray.push(0);
          var WedArray = [];
          WedArray.push(this.sales.sale.wed);
          WedArray.push(0);
          var ThrArray = [];
          ThrArray.push(this.sales.sale.thr);
          ThrArray.push(0);
          var FriArray = [];
          FriArray.push(this.sales.sale.fri);
          FriArray.push(0);
          var SatArray = [];
          SatArray.push(0);
          SatArray.push(this.sales.sale.sat);
          var SunArray = [];
          SunArray.push(0);
          SunArray.push(this.sales.sale.sun);
          var dataMon = {
            data: MonArray
          };
          var dataTue = {
            data: TueArray
          };
          var dataWed = {
            data: WedArray
          };
          var dataThr = {
            data: ThrArray
          };
          var dataFri = {
            data: FriArray
          };
          var dataSat = {
            data: SatArray
          };
          var dataSun = {
            data: SunArray
          };

          this.Dayseries.push(dataMon);
          this.Dayseries.push(dataTue);
          this.Dayseries.push(dataWed);
          this.Dayseries.push(dataThr);
          this.Dayseries.push(dataFri);
          this.Dayseries.push(dataSat);
          this.Dayseries.push(dataSun);

          this.check = true;
        })
        .catch(err => {
          console.log(err);
        });
    }
  }
};
</script>