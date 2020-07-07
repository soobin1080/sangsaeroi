<template>
  <modal name="login-modal" transition="pop-out" :width="380" :height="400">
    <div class="box">
      <div class="partition">
        <div class="mt-3 partition-title">LOGIN</div>
        <div class="partition-form">
          <input
            id="n-email"
            name="email"
            type="text"
            placeholder="Email"
            v-model="credentials.email"
          />
          <div style="margin-top:20px"></div>
          <input
            id="n-password2"
            type="password"
            name="pwd"
            placeholder="Password"
            v-model="credentials.password"
          />

          <div class="button-set">
            <v-btn color="primary" block outlined class="my-6" @click="login">Login</v-btn>
            <v-btn color="success" block outlined class="my-6" @click="findmyinfo">E-mail / 비밀번호 찾기</v-btn>
            <v-btn color="error" block outlined class="my-6" @click="signup">회원가입</v-btn>
          </div>
        </div>
      </div>
    </div>
  </modal>
</template>
<script>
import http from "../http-common";

export default {
  name: "LoginModal",

  data() {
    return {
      credentials: {
        email: "",
        password: ""
      }
    };
  },

  methods: {
    signup() {
      this.$router.push("/signup");
      this.$modal.hide("login-modal");
    },
    login() {
      http
        .post("accounts/login/", this.credentials)
        .then(res => {
          if (res.data.token !== "") {
            // 토큰 받아서 decode
            sessionStorage.setItem("token", res.data.token);

            this.$emit("checkLogIn");
            this.$emit("checkIsAdmin");
            if(this.$route.name == 'signUp'){
              this.$router.push("/")
              location.reload();
            }else{
              this.$router.go();
            }
          } else {
            alert("로그인 오류!");
          }
          this.$modal.hide("login-modal");
        })
        .catch(error => {
          alert("회원정보가 올바르지 않습니다!");
          console.log(error);
        });
    },
    findmyinfo() {
      this.$modal.hide("login-modal");
      this.$router.push("/findmyinfo");
    }
  }
};
</script>
<style lang="scss">
$background_color: #404142;

.box {
  background: white;
  overflow: hidden;
  width: 380px;
  height: 400px;
  border-radius: 2px;
  box-sizing: border-box;
  box-shadow: 0 0 40px black;
  color: #8b8c8d;
  font-size: 0;

  .box-part {
    display: inline-block;
    position: relative;
    vertical-align: top;
    box-sizing: border-box;
    height: 100%;
    width: 100%;
  }

  .box-messages {
    position: absolute;
    left: 0;
    bottom: 0;
    width: 100%;
  }

  .box-error-message {
    position: relative;
    overflow: hidden;
    box-sizing: border-box;
    height: 0;
    line-height: 32px;
    padding: 0 12px;
    text-align: center;
    width: 100%;
    font-size: 11px;
    color: white;
    background: #f38181;
  }

  .partition {
    width: 100%;
    height: 100%;

    .partition-title {
      box-sizing: border-box;
      padding: 30px;
      width: 100%;
      text-align: center;
      letter-spacing: 1px;
      font-size: 20px;
      font-weight: 300;
    }

    .partition-form {
      padding: 0 20px;
      box-sizing: border-box;
    }
  }

  input[type="password"],
  input[type="text"] {
    display: block;
    box-sizing: border-box;
    margin-bottom: 4px;
    width: 100%;
    font-size: 12px;
    line-height: 2;
    border: 0;
    border-bottom: 1px solid #dddedf;
    padding: 4px 8px;
    font-family: inherit;
    transition: 0.5s all;
    outline: none;
  }

  .button-set {
    text-align: center;
  }
}
</style>