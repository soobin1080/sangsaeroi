<template>
  <v-footer dark padless>
    <v-card flat tile class="lightgray lighten-1 white--text text-right pt-0" width="100%">
      <v-card-text>
        <v-row>
          <v-col>
            <div style="text-align:right; float:right">
              <v-tooltip top>
                <template v-slot:activator="{ on }">
                  <v-img v-on="on" :src="getImgUrl('덕명동클라쓰1.png')" @click="team" width="150px" />
                </template>
                <span>About Developer</span>
              </v-tooltip>
            </div>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-footer>
</template>
<script>
export default {
  name: "Footer",
  data() {
    return {};
  },

  components: {},
  methods: {
    team() {
      this.$router.push("/team");
    },
    getImgUrl(img) {
      return require("../assets/" + img);
    }
  }
};
</script>


