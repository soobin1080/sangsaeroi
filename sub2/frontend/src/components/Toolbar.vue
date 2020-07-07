<template>
  <div>
    <v-app-bar id="app-toolbar" app flat color="#FFC107">
      <v-btn v-if="responsive" dark icon @click.stop="onClickDrawer">
        <v-icon>mdi-view-list</v-icon>
      </v-btn>
      <v-spacer />
      <v-toolbar-items>
        <v-btn text v-if="isLogin" class="text-center" style="padding-top:20px;">
          <v-menu offset-y open-on-hover>
            <template v-slot:activator="{ on }">
              <span
                class="infotext"
                text
                v-on="on"
                style="padding-bottom:15px; font-size:20pt; color:white"
              >
                <span class="mdi mdi-account-circle"></span>
                {{name}} 님
              </span>
            </template>

            <v-list dense shaped width="150px">
              <v-list-item @click="entermypage">
                <v-list-item-action>
                  <v-list-item-content
                    style="font-weight:bold; font-size:15px; color:dimgrey"
                  >My Page</v-list-item-content>
                </v-list-item-action>
              </v-list-item>
              <v-list-item @click="logout">
                <v-list-item-action>
                  <v-list-item-content
                    style="font-weight:bold; font-size:15px; color:dimgrey"
                  >Logout</v-list-item-content>
                </v-list-item-action>
              </v-list-item>
            </v-list>
          </v-menu>
        </v-btn>
        <v-btn v-else text width="15%" color="white" @click="$modal.show('login-modal')">Login</v-btn>
      </v-toolbar-items>
    </v-app-bar>

    <LoginModal style="justify:center;"></LoginModal>
  </div>
</template>

<script>
import LoginModal from "../components/LoginModal";
import { mapMutations, mapState } from "vuex";
import http from "../http-common";
import jwtDecode from "jwt-decode";

export default {
  components: {
    LoginModal
  },
  data: () => ({
    responsive: false,
    id: "",
    isLogin: false,
    email: "",
    name: ""
  }),
  computed: {
    ...mapState("app", ["drawer"])
  },
  mounted() {
    if (sessionStorage.getItem("token") != null) {
      this.isLogin = true;
      const token = sessionStorage.getItem("token");
      const requestHeader = {
        headers: {
          Authorization: "JWT " + token
        }
      };
      const user_pk = jwtDecode(token).user_id;
      sessionStorage.setItem("user_pk", user_pk);
      http.get(`accounts/userdetail/${user_pk}/`, requestHeader).then(res => {
        this.email = res.data.email;
        this.name = res.data.nickname;
        sessionStorage.setItem("user_name", res.data.nickname);
        sessionStorage.setItem("busi_exp", res.data.business_exp);
        sessionStorage.setItem("interest_area", res.data.interest_area);
      });
    }
    this.onResponsiveInverted();
    window.addEventListener("resize", this.onResponsiveInverted);
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.onResponsiveInverted);
  },

  methods: {
    ...mapMutations("app", ["setDrawer"]),
    onClickDrawer() {
      this.setDrawer(!this.drawer);
    },
    onResponsiveInverted() {
      if (window.innerWidth < 900) {
        this.responsive = true;
      } else {
        this.responsive = false;
      }
    },

    /////////////////////////////////////////////////
    getUserName() {
      this.id = sessionStorage.getItem("id");
    },
    modalAppear() {
      this.dialog = true;
    },
    logout() {
      let conf = confirm("로그아웃 하시겠습니까?");
      if (conf == true) {
        sessionStorage.clear();
        this.$router.push("/");
        this.$router.go();
      }
    },
    /////////////////////////////////////////////////////
    entermypage() {
      this.$router.push("/mypage");
    }
  }
};
</script>
<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Nanum+Pen+Script&display=swap");
.infotext {
  font-family: "Nanum Pen Script", cursive;
}
</style>
