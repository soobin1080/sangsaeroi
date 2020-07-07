<template>
  <v-row style="margin:auto; width:80%; padding-top:80px; padding-bottom:80px">
    <v-col>
      <v-form ref="form" v-model="valid" lazy-validation>
        <v-container fluid>
          <h2 style="text-align:center;">E-mail 찾기</h2>
          <br />
          <v-text-field
            label="Name"
            v-model="name"
            type="text"
            required
            :rules="[v => !!v || '이름을 입력해주세요!']"
          ></v-text-field>
          <v-text-field
            label="Phone number"
            v-model="phone"
            autocomplete="tel"
            :rules="[rules.required, rules.is_num]"
          ></v-text-field>
          <div style="text-align:center; margin:auto; padding-top:20px">
            <v-btn
              :disabled="!valid"
              color="success"
              outlined
              class="mr-4"
              @click="findEmail"
            >이메일 찾기</v-btn>
          </div>
        </v-container>
      </v-form>
    </v-col>

    <v-divider class="mx-4" inset vertical></v-divider>
    <v-col>
      <v-form ref="form2" v-model="valid" lazy-validation>
        <v-container fluid>
          <h2 style="text-align:center;">비밀번호 찾기</h2>
          <br />
          <v-text-field
            label="Name"
            v-model="name2"
            type="text"
            required
            :rules="[v => !!v || '이름을 입력해주세요!']"
          ></v-text-field>
          <v-text-field label="E-mail" v-model="email" type="text" :rules="emailRules"></v-text-field>
          <div style="text-align:center; margin:auto; padding-top:20px">
            <v-btn
              :disabled="!valid"
              color="success"
              outlined
              class="mr-4"
              @click="findPwd"
            >이메일로 비밀번호 전송</v-btn>
          </div>
        </v-container>
      </v-form>
    </v-col>
  </v-row>
</template>

<script>
import http from "../http-common";
export default {
  name: "FindMyInfo",
  data() {
    return {
      valid: false,
      emailCheck: true,

      name: "",
      phone: "",
      name2: "",
      email: "",

      rules: {
        required: value => !!value || "Required.",
        min_8: v => v.length >= 8 || "Min 8 characters",
        min_4: v => v.length >= 4 || "Min 8 characters",
        is_num: v => !isNaN(v) || "Please input number",
        emailMatch: () => "The email and password you entered don't match"
      },
      emailRules: [
        v => !!v || "가입한 E-mail을 입력해주세요!",
        v => /.+@.+\..+/.test(v) || "E-mail must be valid"
      ]
    };
  },
  methods: {
    findEmail() {
      if (this.$refs.form.validate()) {
        http
          .post(`accounts/findemail/`, {
            nickname: this.name,
            phone: this.phone
          })
          .then(res => {
            if (res.data.email != null) {
              alert(
                "회원님이 가입하신 E-mail는 " + res.data.email + " 입니다."
              );
            } else {
              alert("정보를 찾을 수 없습니다. 다시 입력해주세요.");
            }
          })
          .catch(err => {
            console.log(err);
          });
        this.emailCheck = false;
      }
    },
    findPwd() {
      if (this.$refs.form2.validate()) {
        http
          .post("accounts/findpassword/", {
            email: this.email,
            nickname: this.name2
          })
          .then(res => {
            if (res.data.error == null) {
              alert(
                "E-mail로 임시 비밀번호가 전송되었습니다. E-mail을 확인해주세요!"
              );
            } else {
              alert("정보를 찾을 수 없습니다. 다시 입력해주세요.");
            }
          })
          .catch(err => {
            console.log(err);
          });
        this.emailCheck = false;
      }
    }
  }
};
</script>