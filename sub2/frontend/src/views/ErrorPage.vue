<template>
  <div class="main">
    <v-img :src="getImgUrl('경고.png')" style="margin:auto; float:center; height:100px; width:100px" />
    <br />

    <h3>요청하신 페이지를 찾을 수 없습니다!</h3>
    <br />
    <v-btn color="#ffd900" @click="gobackhome">
      <strong>홈으로</strong>
    </v-btn>
  </div>
</template>
<script>
export default {
  name: "HomePage",
  components: {},
  methods: {
    getImgUrl(img) {
      return require("../assets/" + img);
    },
    gobackhome() {
      this.$router.push("/");
    }
  }
};
</script>
<style scoped>
.main {
  margin: auto;
  text-align: center;
  padding-top: 160px;
}
</style>