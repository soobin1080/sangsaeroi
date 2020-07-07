<template>
  <div>
    <v-form ref="form" v-model="valid" lazy-validation>
      <v-container fluid style="width:650px; padding-bottom:30px">
        <h2 class="text-center mt-8">내 정보 수정하기</h2>
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
            <v-col>
              <v-text-field readonly v-model="email" :rules="emailRules" label="E-mail" required></v-text-field>
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
              <span style="color:dimgray">
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

        <v-row>
          <v-col>
            <v-btn color="error" class="mr-4" outlined style="float:left" @click="withdraw">탈퇴하기</v-btn>
            <v-dialog v-model="dialog" width="450" height="350">
              <template v-slot:activator="{ on }">
                <v-btn color="primary" outlined dark v-on="on">비밀번호 변경</v-btn>
              </template>
              <v-card class="ma-auto" style="width:450px; height:350px">
                <!-- 패스워드 -->
                <div class="px-8 pt-12">
                  <h2 class="text-center">비밀번호 변경하기</h2>
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
                  </v-row>
                  <v-row>
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
                  <v-row>
                    <v-col style="float:right; text-align:right">
                      <v-btn color="success" @click="changepwd">수정</v-btn>
                    </v-col>
                  </v-row>
                </div>
              </v-card>
            </v-dialog>
          </v-col>

          <v-col class="py-3" style="float:right; text-align:right">
            <v-btn color="error" class="mr-4" @click="reset">Reset</v-btn>
            <v-btn :disabled="!valid" color="success" @click="validate">수정</v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-form>
  </div>
</template>

<script>
import http from "../http-common";
export default {
  name: "MyInfoModi",
  components: {
  },
  data() {
    return {
      dialog: false,
      name: "",
      email: "",
      phonenumber: "",
      business_exp: "",
      duplicate: false,
      show1: false,
      pwd: "",
      checkpwd: "",
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
    city: "getdong"
  },
   mounted() {
    this.getUserDetail();
  },
  methods: {
    changepwd() {
      var user_pk = sessionStorage.getItem("user_pk");
      http
        .put(`accounts/changepassword/${user_pk}/`, {
          password: this.pwd
        })
        .then(res => {})
        .catch(err => {
          console.log(err);
        })
        .finally(() => {
          this.dialog = false;
        });
    },
    getdong() {
      http
        .get(`api/area/${this.city}`)
        .then(response => {
          this.dong = response.data.dong;
        })
        .catch(err => {
          console.log(err);
        });
    },
    getUserDetail() {
      let user_pk = sessionStorage.getItem("user_pk");
      if (user_pk == null) {
        this.$router.push("/");
        alert("권한이 없습니다! 로그인 후 이용해주세요.");
      }
      const token = sessionStorage.getItem("token");
      const requestHeader = {
        headers: {
          Authorization: "JWT " + token
        }
      };
      http
        .get(`accounts/userdetail/${user_pk}/`, requestHeader)
        .then(res => {
          this.email = res.data.email;
          this.name = res.data.nickname;
          this.phonenumber = res.data.phone;
          this.business_exp = res.data.business_exp.toString();
          this.interest_area = res.data.interest_area;
          var split_area = this.interest_area.split(" ");
          this.city = split_area[0];
          this.town = split_area[1];
        })
        .catch(err => {
          console.log(err);
        });
    },
    validate() {
      let user_pk = sessionStorage.getItem("user_pk");
      var body = {
        email: this.email,
        nickname: this.name,
        phone: this.phonenumber,
        interest_area: this.city + " " + this.town,
        business_exp: this.business_exp
      };
      if (this.$refs.form.validate()) {
        http
          .put(`accounts/user/${user_pk}/updatedelete/`, body)
          .then(res => {
            if (res.status == 200) {
              alert("수정 성공하였습니다.");
              sessionStorage.setItem("interest_area", body.interest_area);
            } else {
              alert("수정 오류입니다.");
            }
          })
          .catch(err => {
            console.log(err);
          })
          .finally(() => {
            this.getUserDetail();
          });
        this.snackbar = true;
      }
    },
    resetValidation() {
      this.$refs.form.resetValidation();
    },
    reset() {
      this.$refs.form.reset();
    },
    withdraw() {
      let user_pk = sessionStorage.getItem("user_pk");

      if (confirm("탈퇴하시겠습니까?") == true) {
        http
          .delete(`accounts/user/${user_pk}/updatedelete/`)
          .then(response => {
            if (response.status == 200) {
              alert("탈퇴 하였습니다.");
              this.logout();
              this.$router.push("/");
              location.reload();
            } else {
              alert("오류가 발생했습니다. 다시 시도해 주세요.");
              this.$router.push("/mypage");
            }
          })
          .catch(() => {
            this.errored = true;
          })
          .finally(() => (this.loading = false));
      } else {
        return false;
      }
    },
    logout() {
      sessionStorage.clear();
      this.$router.push("/");
    }
  },
 
};
</script>
