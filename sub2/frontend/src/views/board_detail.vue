<template>
  <v-flex xs12 md10 lg10 class="main ma-auto pa-5">
    <div class="py-4">
      <h2 class="pa-1">
        자유 게시판
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
          <v-col cols="12" md="7">
            <v-card class="pa-2" outlined tile>{{this.contents.board_subject}}</v-card>
          </v-col>
          <v-col cols="12" md="2">
            <v-card
              class="pa-2"
              outlined
              tile
              style="text-align:center"
            >{{this.contents.board_writer}}</v-card>
          </v-col>
          <v-col cols="12" md="3">
            <v-card
              class="pa-2"
              outlined
              tile
              style="text-align:center"
            >{{dateformat(this.contents.board_update_date)}}</v-card>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" lg="12" style="height:100%">
            <v-card class="pa-2" outlined tile style="height:400px">{{this.contents.board_content}}</v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-card>

    <v-row v-if="isMine" class="d-flex flex-row-reverse pr-4">
      <div class="pt-6 pb-8">
        <v-btn v-on:click="updateContent" outlined color="primary" small>
          <span class="mdi mdi-pencil"></span>수정
        </v-btn>
        <v-btn class="ml-2" v-on:click="deleteContent" outlined color="primary" small>
          <span class="mdi mdi-delete">삭제</span>
        </v-btn>
      </div>
    </v-row>
    <div>
      <v-divider></v-divider>
      <v-container>
        <ul class>
          <v-card>
            <v-form>
              <v-container fluid>
                <v-layout wrap>
                  <v-row class="ma-auto">
                    <v-col class="ma-auto px-5" cols="1" style="text-align:center">
                      <h4 class="ma-auto px-5" slot="label">댓글</h4>
                    </v-col>
                    <v-col cols="9">
                      <v-textarea
                        hide-details
                        height="140px"
                        class="pa-3"
                        v-model="reply.reply_content"
                        auto-grow
                        solo
                        placeholder="댓글을 입력하세요."
                      ></v-textarea>
                    </v-col>
                    <v-col cols="2" class="pt-4">
                      <v-card-actions>
                        <v-btn
                          class="py-5"
                          @click="writeComment"
                          large
                          style="width:100px; height:140px;"
                          color="blue lighten-5"
                        >
                          <span style="color:#1A237E; font-weight:bold">등록</span>
                        </v-btn>
                      </v-card-actions>
                    </v-col>
                  </v-row>
                </v-layout>
              </v-container>
            </v-form>
          </v-card>
          <br />
          <li
            v-for="reply in allReplys"
            :key="reply.id"
            style="list-style-type:none;width:100%;left:0"
            class="position-relative"
          >
            <Reply :reply="reply" :writer="contents.board_writer" @replyChange="getAllReplysByArg"></Reply>
            <br />
          </li>
        </ul>
      </v-container>
      <!-- <ReplyList :contentId="contentId"></ReplyList> -->
    </div>
  </v-flex>
</template>

<script>
import http from "../http-common";
import Reply from "@/components/Reply";

export default {
  name: "Board_detail",
  data() {
    return {
      isMine: false,
      contents: {
        board_writer: "",
        board_subject: "",
        board_update_date: "",
        board_content: ""
      },
      contentId: "",
      allReplys: [],
      reply: {
        reply_writer: "",
        reply_content: ""
      }
    };
  },
  props: ["seq"],
  components: {
    Reply
  },
  mounted() {
    this.getboarddetail();
    this.getAllReplysByArg();
  },
  methods: {
    writeComment() {
      var user = sessionStorage.getItem("token");
      if (user != null) {
        http
          .post("boards/reply/", {
            board: this.contentId,
            reply_writer: sessionStorage.getItem("user_name"),
            reply_content: this.reply.reply_content
          })
          .then(res => {
            this.reply.reply_content = "";
            alert("댓글 작성이 완료되었습니다.");
          })
          .catch(err => {
            console.log(err);
            alert("댓글 작성 오류!");
          })
          .finally(() => {
            this.allReplys = [];
            this.getAllReplysByArg();
          });
      } else {
        alert("로그인 후 댓글 작성이 가능합니다!");
      }
    },
    getAllReplysByArg() {
      http
        .get(`boards/reply/`)
        .then(res => {
          this.allReplys.splice(0);
          for (var i = 0; i < res.data.count; i++) {
            if (this.contentId == res.data.results[i].board) {
              this.allReplys.push(res.data.results[i]);
            }
          }
        })
        .catch(err => {
          console.log(err);
        });
    },
    getboarddetail() {
      http
        .get(`boards/board/${this.$route.params.seq}`)
        .then(response => {
          this.contents = response.data;
          this.contentId = this.$route.params.seq;

          if (
            this.contents.board_writer == sessionStorage.getItem("user_name")
          ) {
            this.isMine = true;
          } else if (sessionStorage.getItem("user_name") === null) {
            this.isMine = false;
          } else {
            this.isMine = false;
          }
        })
        .catch(err => {
          console.log(err);
        });
    },
    dateformat(date) {
      var time = date;
      date = time.substr(0, 10) + " ";
      date += time.substr(11, 8);

      return date;
    },
    gotoboardlist() {
      this.$router.push({
        path: "/board_list"
      });
    },
    updateContent() {
      this.$router.push({
        path: "/board_update/" + this.$route.params.seq
      });
    },
    deleteContent() {
      let conf = confirm("게시글을 삭제하시겠습니까?");
      if (conf) {
        http
          .delete(`boards/board/${this.$route.params.seq}`)
          .then(response => {
            if (response.status == 204) {
              alert("삭제 처리 하였습니다!");
              this.$router.push("/board_list");
            } else {
              alert("삭제 처리하지 못하였습니다!");
            }
          })
          .catch(err => {
            console.log(err);
            this.errored = true;
          })
          .finally(() => (this.loading = false));
      } else {
        return;
      }
    }
  },
  computed: {
    rows() {
      return this.items.length;
    }
  }
};
</script>
<style>
.content-detail-comment {
  border: 1px solid black;
  margin-top: 1rem;
  padding: 2rem;
}

.main {
  padding-top: 80px;
  padding-bottom: 80px;
  margin: auto;
}
</style>