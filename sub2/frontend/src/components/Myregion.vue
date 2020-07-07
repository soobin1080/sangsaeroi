<template>
  <div v-if="(this.guname != null && this.dongname != null)">
    <Result :guname="this.guname" :dongname="this.dongname"></Result>
  </div>
  <div v-else>
    <h3 class="pa-3">먼저 관심 지역을 선택해주세요!</h3>
  </div>
</template>
  
<script>
import http from "../http-common";
import Result from "@/components/Result";
export default {
  name: "Myregion",
  data() {
    return {
      guname: "",
      dongname: ""
    };
  },
  components: {
    Result
  },
  watch: {},
  methods: {},
  mounted() {
    var interest_area = sessionStorage.getItem("interest_area").split(" ");
    this.guname = interest_area[0];
    this.dongname = interest_area[1];
  }
};
</script>
