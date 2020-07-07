<template>
  <v-flex xs12 md12 lg12 class="ma-auto" style="width:800px;">
    <h3 class="pa-3">{{guname}} {{dongname}}의 상권 분석 결과입니다.</h3>
    <br />
    <v-row>
      <Score xs12 :guname="this.guname" :dongname="this.dongname"></Score>
      <Grade xs12 :guname="this.guname" :dongname="this.dongname"></Grade>
      <div class="ml-4 mt-5">
        <v-chip :color="`orange lighten-3`" class="mr-1 black--text" label x-small>HINT</v-chip>상권 평가 등급
        <br />상권 내 음식, 소매, 서비스업의 전반적인 업종 경기와 상권의 인구수, 교통시설, 집객시설 등을 종합하여 산출한 등급으로서, 점수가 1등급에 가까울수록 상권이 활성화되어 있음을 의미합니다.
      </div>
    </v-row>
    <br />
    <Foottraffic xs12 :guname="this.guname" :dongname="this.dongname"></Foottraffic>
    <div class="ml-4 mt-5">
      <v-chip :color="`orange lighten-3`" class="mr-1 black--text" label x-small>HINT</v-chip>유동인구는 19년 2분기를 기준으로 하며, 통신사 휴대전화 통화량을 바탕으로 추정한 정보입니다.
      <br />상권 정보가 부족하여 선택한 지역의 분석 정보가 나오지 않을 수 있습니다.
      <br />
      <v-chip :color="`blue lighten-3`" class="mr-1 black--text" label x-small>TIP</v-chip>남녀의 비율, 시간대별, 요일별 유동인구를 보고 주요 고객군에 대한 정보를 확인해보세요!
    </div>
    <br />
    <Sales xs12 :guname="this.guname" :dongname="this.dongname"></Sales>
    <div class="ml-4 mt-5">
      <v-chip :color="`orange lighten-3`" class="mr-1 black--text" label x-small>HINT</v-chip>추정매출은 19년 2분기를 기준으로 하며, 카드사 가맹점 매출 통계를 기반으로 추정한 정보입니다.
      <br />상권 정보가 부족하여 선택한 지역의 분석 정보가 나오지 않을 수 있습니다.
      <br />
      <v-chip :color="`blue lighten-3`" class="mr-1 black--text" label x-small>TIP</v-chip>요일별, 시간대별 매출 비율 현황을 통해 평균 매출이 낮은 요일에 할인행사를 진행하는 등의 영업/마케팅 및 점포 운영 시간의 조정 등 점포 운영 방안 수립에 활용해보세요!
    </div>
  </v-flex>
</template>

<script>
import http from "../http-common";
import Score from "@/components/analyzechart/Score";
import Grade from "@/components/analyzechart/Grade";
import Foottraffic from "@/components/analyzechart/Foottraffic";
import Sales from "@/components/analyzechart/Sales";

export default {
  name: "AnalyzeReport",
  components: {
    Score,
    Grade,
    Foottraffic,
    Sales
  },
  props: {
    guname: { type: String },
    dongname: { type: String }
  },
  data() {
    return {};
  },

  methods: {}
};
</script>