<template>
  <v-card class="ma-auto pa-5 pb-12">
    <div class="list-group-item">
      <div>
        <v-badge offset-y="10" v-if="checkWriter()==true" x-small color="warning">
          <span style="font-size:7pt" slot="badge">작성자</span>
          <b class="mr-4" style>{{reply.reply_writer}}</b>
        </v-badge>
        <b v-else class="mr-2" style>{{reply.reply_writer}}</b>

        <span
          class="d-inline"
          style="float:right; text-align:right; font-size:0.8rem"
        >{{dateformat(reply.reply_update_date)}}</span>
        <br />
        <br />
      </div>
      <div v-if="isModify">
        <v-textarea
          outlined
          name="input-7-4"
          label="Outlined textarea"
          :value="reply.reply_content"
          v-model="modifyContent"
        ></v-textarea>
      </div>
      <div v-else>
        <span style="font-size:1.1rem">{{reply.reply_content}}</span>
      </div>
    </div>
    <div v-if="userCheck" class="d-inline float-right">
      <div v-if="isModify">
        <v-btn style="cursor:pointer" x-small @click="replyModify">
          <span class="mdi mdi-pencil"></span>
        </v-btn>
        <v-btn style="cursor:pointer" class="ml-2" x-small @click="modifyBtn">
          <span class="mdi mdi-close"></span>
        </v-btn>
      </div>
      <div v-else>
        <v-btn style="cursor:pointer" x-small @click="modifyBtn">
          <span class="mdi mdi-pencil"></span>
        </v-btn>
        <v-btn style="cursor:pointer" class="ml-2" x-small @click="replyDelete">
          <span class="mdi mdi-delete"></span>
        </v-btn>
      </div>
    </div>
  </v-card>
</template>

<script>
import http from "../http-common";
export default {
  name: "Reply",
  props: {
    contentId: { type: String },
    writer: { type: String },
    reply: {
      type: Object
    }
  },
  data() {
    return {
      userCheck: false,
      writerCheck: false,
      isModify: false,
      modifyContent: this.reply.reply_content
    };
  },
  methods: {
    checkWriter() {
      if (this.writer == this.reply.reply_writer) {
        this.writerCheck = true;
        return true;
      } else {
        return false;
      }
    },
    checkUser() {
      if (sessionStorage.getItem("user_name") == this.reply.reply_writer) {
        this.userCheck = true;
        return true;
      } else {
        return false;
      }
    },
    dateformat(date) {
      var time = date;
      date = time.substr(0, 10) + " ";
      date += time.substr(11, 8);

      return date;
    },

    modifyBtn() {
      this.isModify = !this.isModify;
    },

    replyDelete() {
      let conf = confirm("댓글을 정말 삭제하시겠습니까?");
      if (conf === true) {
        if (this.reply.reply_writer !== sessionStorage.getItem("user_name")) {
          alert("작성자만 댓글을 삭제할 수 있습니다");
          return;
        } else {
          http
            .delete(`boards/reply/${this.reply.id}`)
            .then(res => {
              alert("삭제되었습니다");
              this.$emit("replyChange");
            })
            .catch(err => {
              console.log(err);
            });
        }
      }
    },

    replyModify() {
      if (
        this.modifyContent === this.reply.reply_content ||
        this.modifyContent === ""
      ) {
        alert("같거나 빈 내용으로 수정할 수 없습니다");
        return;
      } else if (
        this.reply.reply_writer !== sessionStorage.getItem("user_name")
      ) {
        alert("작성자만 수정이 가능합니다.");
      } else {
        http
          .patch(
            `boards/reply/${this.reply.id}`,
            {
              board: this.reply.contentId,
              reply_content: this.modifyContent,
              user_name: this.reply.user_name
            },
            this.$store.state.requestHeader
          )
          .then(res => {
            console.log(res);
            alert("댓글 수정 완료");
            this.$emit("replyChange");
            this.isModify = false;
          })
          .catch(err => {
            console.log(err);
          });
      }
    }
  },
  computed: {},

  mounted() {
    this.checkUser();
  }
};
</script>
<style scoped>
.h3 {
  color: #ff8a8a;
}
</style>