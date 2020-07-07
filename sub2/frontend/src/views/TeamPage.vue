<template>
  <v-flex lg9 class="ma-auto pa-8">
    <v-container fluid mb-12>
      <h2 class="headline mb-3">
        About
        <strong>Service</strong>
      </h2>
      <br />
      <p class="infotext" style="text-align:center">
        상새로이는
        <span style="color:darkorange">' 상권의 활성화를 도와 상권을 새로이 한다는 목적을 갖는 서비스 '</span>를 제공합니다!
      </p>
      <br />
      <v-row>
        <v-col lg="4">
          <v-flex d-sm-flex>
            <v-img :src="getImgUrl('상새로이.png')" aspect-ratio="2.9" />
          </v-flex>
        </v-col>
        <v-col lg="8">
          <v-flex d-sm-flex>
            <p class="infocontent">
              음식점을 오픈하고자 하는 예비 소상공인과 프랜차이즈화를 원하는 소상공인을 위해
              <strong
                style="color:darkblue"
              >공공데이터와 다이닝코드의 음식점 리뷰 데이터</strong>를 활용하여
              <strong style="color:darkblue">상권을 분석</strong>한 결과를 제공합니다.
              <br />
              <br />또한 분석한 정보를 토대로 창업 시 유리한 조건을 갖추거나 경쟁력을 갖추기 위한
              <strong style="color:darkblue">업종을 추천</strong>해 줌으로써
              <strong style="color:darkblue">창업 실패율을 낮추고 상권의 활성화를 돕는 효과</strong>를 기대합니다.
            </p>
          </v-flex>
        </v-col>
      </v-row>
    </v-container>
    <v-container fluid mb-12>
      <h2 class="headline mb-3">
        About
        <strong>Developers</strong>
      </h2>
      <br />

      <v-expansion-panels popout>
        <v-expansion-panel hide-actions>
          <v-expansion-panel-header>
            <v-row align="center" class="spacer" no-gutters>
              <v-col cols="4" sm="2" md="1">
                <v-avatar size="36px">
                  <img alt="Avatar" :src="getImgUrl('김대래.jpg')" />
                </v-avatar>
              </v-col>

              <v-col class="hidden-xs-only" sm="5" md="3">
                <v-chip
                  :color="`blue  lighten-3`"
                  class="ml-0 mr-6 black--text"
                  label
                  small
                >Back-end</v-chip>
                <strong>김대래</strong>
              </v-col>

              <v-col class="text-no-wrap hidden-xs-only" cols="5" sm="3">
                <span>Leader</span>
              </v-col>

              <v-col class="grey--text text-truncate">drk0830@naver.com</v-col>
            </v-row>
          </v-expansion-panel-header>

          <v-expansion-panel-content>
            <v-divider></v-divider>
            <v-card-text>
              <v-row>
                <v-col cols="4">Rest API 구축</v-col>
                <v-col>상권 관련 API 구축</v-col>
              </v-row>
              <v-row>
                <v-col cols="4">BigData</v-col>
                <v-col>데이터 가공 및 Hybrid 추천 시스템 구현</v-col>
              </v-row>
            </v-card-text>
          </v-expansion-panel-content>
        </v-expansion-panel>

        <v-expansion-panel hide-actions>
          <v-expansion-panel-header>
            <v-row align="center" class="spacer" no-gutters>
              <v-col cols="4" sm="2" md="1">
                <v-avatar size="36px">
                  <img alt="Avatar" :src="getImgUrl('우동균.jpg')" />
                </v-avatar>
              </v-col>

              <v-col class="hidden-xs-only" sm="5" md="3">
                <v-chip :color="`blue lighten-3`" class="ml-0 mr-6 black--text" label small>Back-end</v-chip>
                <strong>우동균</strong>
              </v-col>

              <v-col class="text-no-wrap hidden-xs-only" cols="5" sm="3">
                <span>Back 팀장, CTO</span>
              </v-col>

              <v-col class="grey--text text-truncate">wdj1207@naver.com</v-col>
            </v-row>
          </v-expansion-panel-header>

          <v-expansion-panel-content>
            <v-divider></v-divider>
            <v-card-text>
              <v-row>
                <v-col cols="4">DB 마이그레이션</v-col>
                <v-col>Pandas DataFrame DB 마이그레이션</v-col>
              </v-row>
              <v-row>
                <v-col cols="4">Rest API 구축</v-col>
                <v-col>회원 정보 및 상권 관련 API 구축</v-col>
              </v-row>
            </v-card-text>
          </v-expansion-panel-content>
        </v-expansion-panel>

        <v-expansion-panel hide-actions>
          <v-expansion-panel-header>
            <v-row align="center" class="spacer" no-gutters>
              <v-col cols="4" sm="2" md="1">
                <v-avatar size="36px">
                  <img alt="Avatar" :src="getImgUrl('김수빈.jpg')" />
                </v-avatar>
              </v-col>

              <v-col class="hidden-xs-only" sm="5" md="3">
                <v-chip :color="`blue lighten-3`" class="ml-0 mr-6 black--text" label small>Back-end</v-chip>
                <strong>김수빈</strong>
              </v-col>

              <v-col class="text-no-wrap hidden-xs-only" cols="5" sm="3">
                <span>데이터베이스</span>
              </v-col>

              <v-col class="grey--text text-truncate">soobin1080@naver.com</v-col>
            </v-row>
          </v-expansion-panel-header>

          <v-expansion-panel-content>
            <v-divider></v-divider>
            <v-card-text>
              <v-row>
                <v-col cols="4">DataBase 설계</v-col>
                <v-col>테이블 설계 및 생성</v-col>
              </v-row>
              <v-row>
                <v-col cols="4">Rest API 구축</v-col>
                <v-col>회원 정보 및 게시판 API 구축</v-col>
              </v-row>
            </v-card-text>
          </v-expansion-panel-content>
        </v-expansion-panel>

        <v-expansion-panel hide-actions>
          <v-expansion-panel-header>
            <v-row align="center" class="spacer" no-gutters>
              <v-col cols="4" sm="2" md="1">
                <v-avatar size="36px">
                  <img alt="Avatar" :src="getImgUrl('안지연.jpg')" />
                </v-avatar>
              </v-col>

              <v-col class="hidden-xs-only" sm="5" md="3">
                <v-chip
                  :color="`orange lighten-3`"
                  class="ml-0 mr-6 black--text"
                  label
                  small
                >Front-end</v-chip>
                <strong>안지연</strong>
              </v-col>

              <v-col class="text-no-wrap hidden-xs-only" cols="5" sm="3">
                <span>Front 팀장</span>
              </v-col>

              <v-col class="grey--text text-truncate">jennyahn94@naver.com</v-col>
            </v-row>
          </v-expansion-panel-header>

          <v-expansion-panel-content>
            <v-divider></v-divider>
            <v-card-text>
              <v-row>
                <v-col cols="4">Front-end (Javascript, Axios, Vuex)</v-col>
                <v-col>상권 분석 및 추천 페이지 구현</v-col>
              </v-row>
              <v-row>
                <v-col cols="4">API 활용</v-col>
                <v-col>Kakao MAP API 활용 - 상권 분석 및 추천</v-col>
              </v-row>
            </v-card-text>
          </v-expansion-panel-content>
        </v-expansion-panel>

        <v-expansion-panel hide-actions>
          <v-expansion-panel-header>
            <v-row align="center" class="spacer" no-gutters>
              <v-col cols="4" sm="2" md="1">
                <v-avatar size="36px">
                  <img alt="Avatar" :src="getImgUrl('오유경.jpg')" />
                </v-avatar>
              </v-col>

              <v-col class="hidden-xs-only" sm="5" md="3">
                <v-chip
                  :color="`orange lighten-3`"
                  class="ml-0 mr-6 black--text"
                  label
                  small
                >Front-end</v-chip>
                <strong>오유경</strong>
              </v-col>

              <v-col class="text-no-wrap hidden-xs-only" cols="5" sm="3">
                <span>AWS 배포</span>
              </v-col>

              <v-col class="grey--text text-truncate">action713@naver.com</v-col>
            </v-row>
          </v-expansion-panel-header>

          <v-expansion-panel-content>
            <v-divider></v-divider>
            <v-card-text>
              <v-row>
                <v-col cols="4">AWS 배포</v-col>
                <v-col>서버 배포 (Nginx, Gunicorn, Doker)</v-col>
              </v-row>
              <v-row>
                <v-col cols="4">API 활용</v-col>
                <v-col>Kakao MAP API 활용 - 행정동 다각형, 카테고리</v-col>
              </v-row>
            </v-card-text>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-container>
  </v-flex>
</template>

<script>
export default {
  name: "TeamPage",
  components: {},
  methods: {
    getImgUrl(img) {
      return require("../assets/" + img);
    }
  }
};
</script>
<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Nanum+Pen+Script&display=swap");
.text-no-wrap {
  font-size: 15pt;
  font-family: "Nanum Pen Script", cursive;
}

@import url("https://fonts.googleapis.com/css2?family=Black+Han+Sans&display=swap");
.infotext {
  font-family: "Black Han Sans", sans-serif;
  font-size: 23px;
}

@import url("https://fonts.googleapis.com/css2?family=Nanum+Gothic+Coding:wght@700&display=swap");
.infocontent {
  font-family: "Nanum Gothic Coding", monospace;
}
</style>
