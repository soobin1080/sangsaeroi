<template>
  <v-container fill-height fluid grid-list-xl>
    <v-layout justify-center wrap mt-5>
      <v-flex xs12 md8>
        <v-card>
          <!-- 행정동 검색 -->
          <div class="ma-1 pt-2">
            <v-row class="py-0 pl-5 pr-0">
              <v-col cols="5" class="px-0 py-0">
                <v-container id="dropdown-example-2" class="py-0">
                  <v-overflow-btn v-model="city" :items="gu" label="구" dense></v-overflow-btn>
                </v-container>
              </v-col>
              <v-col cols="5" class="px-0 py-0">
                <v-container id="dropdown-example-2" class="py-0">
                  <v-overflow-btn v-model="town" :items="dong" label="동" dense></v-overflow-btn>
                </v-container>
              </v-col>
              <v-col cols="auto" style="padding-top:15px">
                <v-btn @click="search" depressed color="orange lighten-2" dark>
                  검색
                  <span class="mdi mdi-magnify"></span>
                </v-btn>
              </v-col>
            </v-row>
          </div>
        </v-card>
        <v-divider class="mt-4" />
        <v-divider />
        <Result
          v-if="(this.guname != '' && this.dongname !='')"
          :guname="this.guname"
          :dongname="this.dongname"
        ></Result>
        <v-flex class="mt-4" v-else>
          <p
            class="infotext"
            style="font-size:20px; text-align:center; color:dimgrey"
          >상새로이는 행정동 기반의 상권 분석과 업종 추천 서비스를 제공합니다 !</p>
          <v-img :src="getImgUrl('빅데이터.png')" width="100%" />
        </v-flex>
      </v-flex>
    </v-layout>
  </v-container>
</template>
<script>
import http from "../http-common";
import Result from "@/components/Result";
export default {
  name: "SearchByDong",
  components: {
    Result
  },
  data() {
    return {
      guname: "",
      dongname: "",

      name: "",
      email: "",
      pwd: "",
      checkpwd: "",
      phonenumber: "",
      business_exp: false,
      duplicate: false,
      show1: false,
      valid: true,
      areas: [],
      nextId: 1,
      city: "", // 구 이름이 들어가는 v-model
      town: "", // 동 이름이 들어가는 v-model
      gu: [
        "강남구",
        "강동구",
        "강북구",
        "강서구",
        "관악구",
        "광진구",
        "구로구",
        "금천구",
        "노원구",
        "도봉구",
        "동대문구",
        "동작구",
        "마포구",
        "서대문구",
        "서초구",
        "성동구",
        "성북구",
        "송파구",
        "양천구",
        "영등포구",
        "용산구",
        "은평구",
        "종로구",
        "중구",
        "중랑구"
      ],
      dong: []
    };
  },
  watch: {
    city: "getdong"
  },
  methods: {
    getImgUrl(img) {
      return require("../assets/" + img);
    },
    getdong() {
      http
        .get(`api/area/${this.city}`)
        .then(response => {
          this.dong = response.data.dong;
        })
        .catch(err => {
          console.log(err);
        });
    },
    search() {
      if (this.city == "" || this.town == "") {
        alert("지역을 선택해주세요!");
      }
      this.guname = this.city;
      this.dongname = this.town;
    }
  }
};
</script>
<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Nanum+Pen+Script&display=swap");
.infotext {
  font-family: "Nanum Pen Script", cursive;
}
</style>