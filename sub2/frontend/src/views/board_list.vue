<template>
  <v-flex xs12 md10 lg10 class="main ma-auto pa-5">
    <div class="py-4">
      <h2 class="pa-1">
        자유 게시판
        <span style="text-align:right; float:right">
          <v-btn v-on:click="writeContent" outlined color="primary" small>
            글쓰기
            <span class="mdi mdi-pencil"></span>
          </v-btn>
        </span>
      </h2>
      <p
        class="pa-1 boardinfo"
        style="font-size:10pt; font-weight:bold; color:#004b40"
      >" 기창업자의 프랜차이즈화와 예비창업자의 멘토링 활동을 위한 게시판입니다. "</p>
    </div>

    <v-app>
      <div>
        <v-data-table
          :headers="headers"
          :items="lists"
          :page.sync="page"
          :items-per-page="itemsPerPage"
          hide-default-footer
          class="elevation-1"
          @page-count="pageCount = $event"
          @click:row="rowClick"
        ></v-data-table>
        <div class="text-center pt-2">
          <v-pagination v-model="page" :length="pageCount"></v-pagination>
        </div>
      </div>
    </v-app>
  </v-flex>
</template>

<script>
import http from "../http-common";

export default {
  name: "Board_list",
  data() {
    return {
      page: 1,
      pageCount: 0,
      itemsPerPage: 15,
      headers: [
        { text: "no", value: "id" },
        { text: "제목", value: "board_subject" }, //데이터 읽어오면 값 바꿔야 함.
        { text: "작성자", value: "board_writer" },
        { text: "작성시간", value: "board_update_date" }
      ],
      lists: [{}]
    };
  },
  methods: {
    getboardlists() {
      http
        .get(`boards/board/`)
        .then(response => {
          this.lists = response.data.results;
          for (var i = 0; i < this.lists.length; i++) {
            var time = this.lists[i].board_update_date;
            this.lists[i].board_update_date = time.substr(0, 10) + " ";
            this.lists[i].board_update_date += time.substr(11, 8);
          }
        })
        .catch(err => {
          console.log(err);
        });
    },
    rowClick(value) {
      this.$router.push({
        path: "/board_detail/" + value.id
      });
    },
    writeContent() {
      var user = sessionStorage.getItem("token");
      if (user != null) {
        this.$router.push({
          path: "/board_write"
        });
      } else {
        alert("로그인 후 게시글 작성이 가능합니다!");
      }
    }
  },
  mounted() {
    this.getboardlists();
  },
  computed: {
    rows() {
      return this.items.length;
    }
  }
};
</script>
<style scoped>
.main {
  padding-top: 80px;
  padding-bottom: 80px;
  margin: auto;
  width: 80%;
}

@import url("https://fonts.googleapis.com/css2?family=Nanum+Gothic+Coding&display=swap");
.boardinfo {
  font-family: "Nanum Gothic Coding", monospace;
}
</style>