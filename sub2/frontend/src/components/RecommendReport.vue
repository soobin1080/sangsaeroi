<template>
  <v-flex xs12 md12 lg12 class="ma-auto" style="width:800px;">
    <h3 class="pa-3">{{guname}} {{dongname}}의 "유사 지역 기반 업종 추천" 결과입니다.</h3>

    <div class="ml-4 mt-5">
      <v-chip :color="`orange lighten-3`" class="mr-1 black--text" label x-small>HINT</v-chip>유사지역은 선택하신 지역의 상권 분석의 특성(평가지수, 매출액, 유동인구, 분포도 등)과 유사한 패턴을 갖는 지역을 의미합니다.
      <br />
    </div>
    <br />
    <div v-if="existResult">
      <v-layout v-if="existTop" row>
        <v-flex xs12 sm6 lg12>
          <v-card>
            <h3 class="pa-3">
              유사 지역의 Top3 중 선택한 지역에 없는 카테고리입니다.
              <span
                class="recommendtext blinking"
                style="font-size:15pt; text-align:right; float:right; color:dimgrey "
              >
                추천
                <span class="mdi mdi-thumb-up-outline mx-1" style="color:blue"></span>
              </span>
            </h3>
            <v-list>
              <v-list-item v-for="item in recommend_top" :key="item.title">
                <v-list-item-content>
                  <v-list-item-title v-text="item.title"></v-list-item-title>
                </v-list-item-content>
                <v-list-item-avatar>
                  <v-img :src="item.img"></v-img>
                </v-list-item-avatar>
              </v-list-item>
            </v-list>
          </v-card>
          <div class="ml-4 mt-5">
            <v-chip :color="`orange lighten-3`" class="mr-1 black--text" label x-small>HINT</v-chip>선택한 지역과 유사한 지역에서 인기있는 업종 Top3 중 선택한 지역에 없는 업종을 의미합니다.
            <br />해당 추천은 유사 상권에 따라 추천하지만 지역적 특성을 고려하지 못할 수 있습니다.
          </div>
        </v-flex>
      </v-layout>
      <v-card v-if="existRegion" class="pa-5 mt-5">
        <apexchart
          type="scatter"
          width="100%"
          height="350px"
          :options="chartOptions"
          :series="series"
        ></apexchart>
      </v-card>
      <div v-if="existRegion" class="ml-4 mt-5">
        <v-chip :color="`orange lighten-3`" class="mr-1 black--text" label x-small>HINT</v-chip>해당 그래프는 선택 지역의 리뷰데이터를 기반으로 인기 업종과 시장개척률 정도에 따라 유사 지역과 비교 분석을 통해 나타낸 정보입니다.
      </div>

      <div class="text-center pt-5 mt-5 pt-3" style="font-weight:bold; margin:auto">상위 업종 리스트</div>
      <v-layout row>
        <v-flex xs12 sm6 lg3>
          <StoreListCard :items="this.sim_score" :tag="'유사지역 평점 순'" :sufix="'점'"></StoreListCard>
        </v-flex>
        <v-flex xs12 sm6 lg3>
          <StoreListCard :items="this.sim_count" :tag="'유사지역 리뷰 순'" :sufix="'개'"></StoreListCard>
        </v-flex>
        <v-flex xs12 sm6 lg3>
          <StoreListCard :items="this.reg_score" :tag="'선택지역 평점 순'" :sufix="'점'"></StoreListCard>
        </v-flex>
        <v-flex xs12 sm6 lg3>
          <StoreListCard :items="this.reg_count" :tag="'선택지역 리뷰 순'" :sufix="'개'"></StoreListCard>
        </v-flex>
      </v-layout>
      <div class="ml-4 mt-5">
        <v-chip :color="`orange lighten-3`" class="mr-1 black--text" label x-small>HINT</v-chip>유사 지역의 평점/리뷰 순, 선택 지역의 평점/리뷰 순 상위 업종 리스트입니다.
        <br />상권 정보에 따라 데이터가 부족할 수 있습니다.
      </div>
    </div>
    <div v-else>
      <h3 class="pa-3">
        상권을 분석할 자료가 충분하지 않습니다!
        <br />다른 지역을 선택해보세요!
      </h3>
    </div>
  </v-flex>
</template>
<script>
import http from "../http-common";
import VueApexCharts from "vue-apexcharts";
import StoreListCard from "./StoreListCard";
import img1 from "../assets/food/기타음식업.png";
import img2 from "../assets/food/닭.png";
import img3 from "../assets/food/별식.png";
import img4 from "../assets/food/부페.png";
import img5 from "../assets/food/분식.png";
import img6 from "../assets/food/양식.png";
import img7 from "../assets/food/유흥주점.png";
import img8 from "../assets/food/음식배달서비스.png";
import img9 from "../assets/food/일식.png";
import img10 from "../assets/food/제과제빵떡케익.png";
import img11 from "../assets/food/중식.png";
import img12 from "../assets/food/커피점.png";
import img13 from "../assets/food/패스트푸드.png";
import img14 from "../assets/food/한식.png";

export default {
  name: "RecommendReport",
  components: {
    apexchart: VueApexCharts,
    StoreListCard
  },
  props: {
    guname: { type: String },
    dongname: { type: String }
  },
  data() {
    return {
      existRegion: false,
      existTop: false,
      existResult: false,
      result: {},
      sim_score: [],
      sim_count: [],
      reg_score: [],
      reg_count: [],
      recommend_top: [],
      series: [{}],
      chartOptions: {
        chart: {
          height: 350,
          type: "scatter",
          animations: {
            enabled: false
          },
          zoom: {
            enabled: false
          },
          toolbar: {
            show: false
          }
        },
        colors: ["#00CED1", "#ADFF2F", "#F08080", "#ADD8E6"],
        xaxis: {
          title: { text: "업종 별 인기 척도" },
          tickAmount: 2,
          min: -1,
          max: 1
        },
        yaxis: {
          title: {
            text: "시장 개척률"
          },
          tickAmount: 2,
          min: -1,
          max: 1
        },
        markers: {
          size: 20
        },
        fill: {
          type: "image",
          opacity: 1,
          image: {
            src: [],
            width: 40,
            height: 40
          }
        }
      }
    };
  },
  mounted() {
    if (this.guname != "" && this.dongname != "") this.getRecommendResult();
  },
  methods: {
    getRecommendResult() {
      this.existRegion = false;
      this.existTop = false;
      this.existResult = false;
      http
        .get(`api/recommend/${this.guname}/${this.dongname}/`)
        .then(res => {
          // 아무 결과 없네?
          if (res.data == "{}") {
            this.existResult = false;
          }
          // 뭐라도 있네?
          else {
            let res_data = res.data;
            res_data = res_data.replace(/\'/g, '"');
            let to_json = JSON.parse(res_data);

            // 추천 결과
            let recommend = to_json.recommend;
            // this.recommend_top = recommend.top;

            var ot = {
              name: recommend.ot,
              data: [[-0.5, -0.5]]
            };
            var tt = {
              name: recommend.tt,
              data: [[0.5, -0.5]]
            };
            var oo = {
              name: recommend.oo,
              data: [[-0.5, 0.5]]
            };
            var to = {
              name: recommend.to,
              data: [[0.5, 0.5]]
            };
            this.series = [ot, tt, oo, to];
            var columns = {
              기타음식업: img1,
              닭: img2,
              별식: img3,
              부페: img4,
              분식: img5,
              양식: img6,
              유흥주점: img7,
              음식배달서비스: img8,
              일식: img9,
              제과제빵떡케익: img10,
              중식: img11,
              커피점: img12,
              패스트푸드: img13,
              한식: img14
            };

            var top = [];
            for (var t = 0; t < recommend.top.length; t++) {
              var store = {
                title: recommend.top[t],
                img: columns[recommend.top[t].split("/")[0]]
              };
              top.push(store);
            }
            this.recommend_top = top;
            if (this.recommend_top.length > 0) {
              this.existTop = true;
            }
            if (recommend.ot.length > 0) {
              var name_ot = ot.name[0].split("/")[0];
              var name_tt = tt.name[0].split("/")[0];
              var name_oo = oo.name[0].split("/")[0];
              var name_to = to.name[0].split("/")[0];
              this.chartOptions.fill.image.src.push(columns[name_ot]);
              this.chartOptions.fill.image.src.push(columns[name_tt]);
              this.chartOptions.fill.image.src.push(columns[name_oo]);
              this.chartOptions.fill.image.src.push(columns[name_to]);
            }

            this.recommend = recommend;

            // 유사 지역
            let sim_score =
              to_json.similar_scores_small_code_sort_by_score.data;
            let sim_count =
              to_json.similar_scores_small_code_sort_by_count.data;

            // 선택 지역
            let reg_score = to_json.region_scores_small_code_sort_by_score.data;
            let reg_count = to_json.region_scores_small_code_sort_by_count.data;

            // init
            this.sim_score = [];
            this.sim_count = [];
            this.reg_score = [];
            this.reg_count = [];

            // 유사 지역 결과 보자
            for (var i = 0; i < sim_score.length; i++) {
              if (i == 5) {
                break;
              }
              var sim_score_store = {
                key: sim_score[i].medium_category,
                score: sim_score[i].score.toFixed(2)
              };
              var sim_count_store = {
                key: sim_count[i].medium_category,
                score: sim_count[i].count
              };
              this.sim_score.push(sim_score_store);
              this.sim_count.push(sim_count_store);
            }
            // 선택한 지역에 리뷰 정보가 있니?
            // 선택지역 결과 보자
            if (reg_score.length != 0) {
              for (var j = 0; j < reg_score.length; j++) {
                if (j == 5) {
                  break;
                }
                var reg_score_store = {
                  key: reg_score[j].medium_category,
                  score: reg_score[j].score.toFixed(2)
                };
                var reg_count_store = {
                  key: reg_count[j].medium_category,
                  score: reg_count[j].count
                };
                this.reg_score.push(reg_score_store);
                this.reg_count.push(reg_count_store);
              }
              this.existRegion = true;
            }
            this.existResult = true;
          }
        })
        .catch(err => {
          console.log(err);
        });
    }
  }
};
</script>
<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Nanum+Pen+Script&display=swap");
.recommendtext {
  font-family: "Nanum Pen Script", cursive;
}

.blinking {
  -webkit-animation: blink 1s ease-in-out infinite alternate;
  -moz-animation: blink 1s ease-in-out infinite alternate;
  animation: blink 1s ease-in-out infinite alternate;
}
@-webkit-keyframes blink {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
@-moz-keyframes blink {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
@keyframes blink {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
</style>