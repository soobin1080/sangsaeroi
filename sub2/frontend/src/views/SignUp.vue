<template>
  <div>
    <v-form ref="form" v-model="valid" lazy-validation>
      <v-container fluid style="width:650px; padding-bottom:100px">
        <h2 class="text-center mt-8">회원가입</h2>
        <br />

        <!-- 이름 -->
        <div>
          <v-row>
            <v-col>
              <v-text-field v-model="name" :rules="nameRules" label="Name" required></v-text-field>
            </v-col>
          </v-row>
        </div>

        <!-- 이메일 -->
        <div>
          <v-row>
            <v-col cols="9">
              <v-text-field v-model="email" :rules="emailRules" label="E-mail" required></v-text-field>
            </v-col>
            <v-col class="mt-5">
              <v-btn
                @click="emailcheck"
                small
                outlined
                color="blue"
                style="float:right; color:white"
              >중복 확인</v-btn>
            </v-col>
          </v-row>
        </div>

        <!-- 패스워드 -->
        <div>
          <v-row>
            <v-col>
              <v-text-field
                v-model="pwd"
                :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                :rules="[rules.required, rules.min_8]"
                :type="show1 ? 'text' : 'password'"
                name="input-10-1"
                label="Password"
                hint="8자 이상의 비밀번호를 입력해주세요!"
                @click:append="show1 = !show1"
              ></v-text-field>
            </v-col>
            <v-col>
              <v-text-field
                type="password"
                label="Check Password"
                v-model="checkpwd"
                required
                :rules="checkPasswordRules"
              ></v-text-field>
            </v-col>
          </v-row>
        </div>

        <!-- 전화번호 -->
        <v-text-field
          v-model="phonenumber"
          label="Phone number"
          :rules="[rules.required, rules.is_num, rules.min_11]"
          required
          autocomplete="tel"
        ></v-text-field>

        <!-- 창업 경험 -->
        <div>
          <v-row>
            <v-col cols="2" class="mt-5">
              <span style="color:dimgray;">
                <strong>창업 경험</strong>
              </span>
            </v-col>
            <v-radio-group v-model="business_exp" row class="ml-3">
              <v-col>
                <v-radio label=" 창업 경험이 있다." value="true"></v-radio>
              </v-col>
              <v-col style="padding-left:90px">
                <v-radio label=" 창업 경험이 없다." value="false"></v-radio>
              </v-col>
            </v-radio-group>
          </v-row>
        </div>

        <!-- 관심 지역 -->
        <div>
          <v-row class="py-0">
            <v-col cols="2" class="pt-5">
              <span style="color:dimgray">
                <strong>관심 지역</strong>
              </span>
            </v-col>
            <v-col class="px-0 py-0">
              <v-container id="dropdown-example-2" class="py-0">
                <v-overflow-btn v-model="city" :items="gu" label="구" dense></v-overflow-btn>
              </v-container>
            </v-col>
            <v-col class="px-0 py-0">
              <v-container id="dropdown-example-2" class="py-0">
                <v-overflow-btn v-model="town" :items="dong" label="동" dense></v-overflow-btn>
              </v-container>
            </v-col>
          </v-row>
        </div>

        <div class="btn py-3" style="float:right">
          <v-btn color="error" class="mr-4" @click="reset">Reset</v-btn>
          <v-btn :disabled="!valid" color="success" class="mr-4" @click="validate">가입!</v-btn>
        </div>
      </v-container>
    </v-form>
  </div>
</template>

<script>
import http from "../http-common";
export default {
  name: "SignUp",
  data() {
    return {
      name: "",
      email: "",
      pwd: "",
      checkpwd: "",
      phonenumber: "",
      business_exp: false,
      duplicate: false,
      show1: false,
      valid: true,
      interest_area: "",
      city: "", // 구 이름이 들어가는 v-model
      town: "",
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
      dong: [],

      rules: {
        required: value => !!value || "필수 입력 항목입니다.",
        min_8: v => v.length >= 8 || "8자 이상의 비밀번호를 입력해주세요!",
        min_11: v => v.length == 11 || " '-'을 제외한 11자리를 입력해주세요!",
        is_num: v => !isNaN(v) || " '-'을 제외한 11자리를 입력해주세요!"
      },
      emailRules: [
        v => !!v || "필수 입력 항목입니다.",
        v => /.+@.+\..+/.test(v) || "E-mail 형식을 지켜주세요!"
      ],
      nameRules: [
        v => !!v || "필수 입력 항목입니다.",
        v => (v && v.length <= 10) || "이름은 10자 이내로 입력해주세요!"
      ],
      checkPasswordRules: [
        v => !!v || "비밀번호를 확인해주세요!",
        v => this.pwd === this.checkpwd || "입력하신 비밀번호와 다릅니다!"
      ]
    };
  },
  watch: {
    user: {
      email(newVal) {
        fetch(`/${newVal}`).then(data => {
          this.email = data;
          this.duplicate = false;
        });
      },
      deep: true,
      immediate: true
    },
    city: "getdong",
    mediumcategory: "getsmall"
  },
  methods: {
    getdong() {
      http
        .get(`api/area/${this.city}`)
        .then(response => {
          console.log(response);
          this.dong = response.data.dong;
        })
        .catch(err => {
          console.log(err);
        });
    },
    validate() {
      this.interest_area = this.city + " " + this.town;
      if (this.duplicate == false) {
        alert("E-mail 중복 확인을 해주세요!");
      } else if (this.$refs.form.validate()) {
        let user = {
          nickname: this.name,
          email: this.email,
          password: this.pwd,
          business_exp: this.business_exp,
          phone: this.phonenumber,
          interest_area: this.interest_area
        };
        http
          .post("accounts/signup/", user)
          .then(res => {
            this.$router.push("/");
          })
          .catch(err => {
            console.log(err);
            alert("회원가입 오류!");
          });
      }
    },
    resetValidation() {
      this.$refs.form.resetValidation();
    },
    reset() {
      this.$refs.form.reset();
    },
    emailcheck() {
      this.duplicate = true;
      http
        .post("accounts/email-check/", {
          email: this.email
        })
        .then(respone => {
          console.log(respone);
          if (respone.data.error == 1) {
            alert("중복된 E-mail입니다. 다른 E-mail을 입력해주세요.");
            this.duplicate = false;
            this.email = "";
          } else {
            alert("사용 가능합니다.");
            this.duplicate = true;
          }
        })
        .catch(error => {
          console.log(error);
        });
    }
  },
  mounted() {
    this.$modal.hide("login-modal");
  }
};
</script>
<style scoped>
</style>