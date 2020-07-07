<template>
  <v-flex xs12 md10 lg10 class="main ma-auto pa-5">
    <div class="py-4">
      <h2 class="pa-1">
        자유 게시판 게시글 수정
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
          <v-col cols="12" md="12">
            <v-card class="pa-2" outlined tile>
              <input type="text" v-model="contents.board_subject" style="width:100%" />
            </v-card>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" lg="12" style="height:100%">
            <v-card class="pa-2" outlined tile style="height:400px">
              <textarea auto-grow v-model="contents.board_content" style="width:100%; height:100%"></textarea>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-card>

    <div style="text-align:right; float:right" class="pt-5 pb-12">
      <v-btn v-on:click="updateContent" outlined color="primary" small>
        수정
        <span class="mdi mdi-pencil"></span>
      </v-btn>
    </div>
  </v-flex>
</template>

<script>
import http from "../http-common";

export default {
  name: "Board_update",
  data() {
    return {
      contents: {
        board_writer: "",
        board_subject: "",
        board_content: ""
      }
    };
  },
  props: ["seq"],
  mounted() {
    this.getboarddetail();
  },
  methods: {
    hasAuthorization(){
      let user_pk = sessionStorage.getItem("user_pk");
      if (user_pk == null) {
        alert("권한이 없습니다! 로그인 후 이용해주세요.");
        this.$router.go(-1);
      }
      else{
        const token = sessionStorage.getItem("token");
        const requestHeader = {
          headers: {
            Authorization: "JWT " + token
          }
        };
        http
          .get(`accounts/userdetail/${user_pk}/`, requestHeader)
          .then(res => {
            if (res.data.nickname != this.contents.board_writer) {
              alert("권한이 없습니다!");
              this.$router.go(-1);
              return;
            }
          })
          .catch(err => {
            console.log(err);
          });
      }
    },
    gotoboardlist() {
      this.$router.push({
        path: "/board_list"
      });
    },
    getboarddetail() {
      http
        .get(`boards/board/${this.$route.params.seq}`)
        .then(response => {
          this.contents = response.data;
          this.hasAuthorization();
        })
        .catch(err => {
          console.log(err);
        });
    },
    updateContent() {
      alert("수정 되었습니다!");
      http
        .patch(`boards/board/${this.$route.params.seq}`, {
          board_writer: this.contents.board_writer,
          board_subject: this.contents.board_subject,
          board_content: this.contents.board_content
        })
        .then(res => {
          this.$router.push({
            path: "/board_list"
          });
        })
        .catch(err => {
          console.log(err);
          alert("게시글 수정 오류!");
        });
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