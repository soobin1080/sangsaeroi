<template>
  <v-flex xs12 md10 lg10 class="main ma-auto pa-5">
    <div class="py-4">
      <h2 class="pa-1">
        자유 게시판 새 글 작성
        <span style="text-align:right; float:right">
          <v-btn v-on:click="gotoboardlist" outlined color="primary" small>
            <span class="mdi mdi-clipboard-text"></span>
            목록
          </v-btn>
        </span>
      </h2>
    </div>

    <v-card>
      <v-container class="blue lighten-4">
        <v-row>
          <v-col
            cols="4"
            style="    padding-top: 0px;
    padding-right: 0px;
    padding-bottom: 0px;
    padding-left: 0px;"
          >
            <v-container class="py-0">
              <v-overflow-btn v-model="tag" :items="tags" label="선택" dense></v-overflow-btn>
            </v-container>
          </v-col>
          <v-col cols="12" md="8">
            <v-card class="pa-2" outlined tile>
              <input
                type="text"
                v-model="contents.board_subject"
                style="width:100%"
                placeholder="제목"
              />
            </v-card>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" lg="12" style="height:100%">
            <v-card class="pa-2" outlined tile style="height:400px">
              <textarea
                auto-grow
                v-model="contents.board_content"
                style="width:100%; height:100%"
                placeholder="내용을 입력해주세요."
              ></textarea>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-card>

    <div style="text-align:right; float:right" class="pt-5 pb-12">
      <v-btn v-on:click="writeContent" outlined color="primary" small>
        글쓰기
        <span class="mdi mdi-pencil"></span>
      </v-btn>
    </div>
  </v-flex>
</template>

<script>
import http from "../http-common";

export default {
  name: "Board_write",
  data() {
    return {
      contents: {
        board_writer: "",
        board_subject: "",
        board_content: ""
      },
      tags: ["멘토링", "가맹 모집"],
      tag: ""
    };
  },
  methods: {
    gotoboardlist() {
      this.$router.push({
        path: "/board_list"
      });
    },
    writeContent() {
      var board_writer = sessionStorage.getItem("user_name");
      http
        .post("boards/board/", {
          board_writer: board_writer,
          board_subject:
            "[" + this.tag + "]" + " " + this.contents.board_subject,
          board_content: this.contents.board_content
        })
        .then(res => {
          this.$router.push({
            path: "/board_list"
          });
        })
        .catch(err => {
          console.log(err);
          alert("게시글 작성 오류!");
        });
    }
  },
  mounted() {
    let user_pk = sessionStorage.getItem("user_pk");
    if (user_pk == null) {
      this.$router.push("/");
      alert("권한이 없습니다! 로그인 후 이용해주세요.");
    }
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
}
</style>