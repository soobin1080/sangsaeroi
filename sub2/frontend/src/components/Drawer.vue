<template>
  <v-navigation-drawer
    id="app-drawer"
    v-model="inputValue"
    app
    dark
    floating
    persistent
    mobile-break-point="900"
    width="250"
    style="background-color:#004F6F"
  >
    <div class="mx-12 mt-8">
      <v-img :src="getImgUrl('상세로이2.png')" width="150px" />
    </div>

    <v-layout>
      <v-list rounded>
        <v-list-item :to="'/'" active-class="orange darken-1 white--text" class="v-list-item ma-2">
          <v-list-item-action>
            <v-icon>{{ "mdi-home" }}</v-icon>
          </v-list-item-action>
          <v-list-item-title v-text="'HOME'" />
        </v-list-item>

        <v-list-group prepend-icon="mdi-google-analytics" no-action class="white--text pl-1">
          <template v-slot:activator>
            <v-list-item-content>
              <v-list-item-title class="white--text">상권 분석</v-list-item-title>
            </v-list-item-content>
          </template>

          <v-list-item
            v-for="(Analysis_menu, i) in Analysis"
            :key="i"
            :to="Analysis_menu[1]"
            active-class="orange darken-1 white--text"
            style="height:48px !important;"
          >
            <v-list-item-title v-text="Analysis_menu[0]"></v-list-item-title>
          </v-list-item>
        </v-list-group>
        <v-list-item
          :to="'/board_list'"
          active-class="orange darken-1 white--text"
          class="v-list-item ma-2"
        >
          <v-list-item-action>
            <v-icon>{{ "mdi-bulletin-board" }}</v-icon>
          </v-list-item-action>
          <v-list-item-title v-text="'게시판'" />
        </v-list-item>
      </v-list>
    </v-layout>
  </v-navigation-drawer>
</template>

<script>
import { mapMutations, mapState } from "vuex";

export default {
  props: {
    opened: {
      type: Boolean,
      default: false
    }
  },
  data: () => ({
    Analysis: [
      ["행정동 검색", "/searchbydong"],
      ["지도 검색", "/map"]
    ]
  }),
  computed: {
    ...mapState("app", ["drawer"]),
    inputValue: {
      get() {
        return this.drawer;
      },
      set(val) {
        this.setDrawer(val);
      }
    }
  },

  methods: {
    ...mapMutations("app", ["setDrawer"]),
    getImgUrl(img) {
      return require("../assets/" + img);
    }
  }
};
</script>
