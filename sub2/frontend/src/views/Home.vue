<template>
  <v-container>
    <v-card-text class="text-center py-10 mt-10">
      <ImageBanner :imgSrc="bannerImg"></ImageBanner>
    </v-card-text>

    <v-flex lg9 class="ma-auto blinking" style="cursor:pointer">
      <div style="text-align:center; color:dimgrey" class="pa-8" @click="scrolltoInfo">
        <span class="mdi mdi-chevron-double-up"></span>
        <h3 class="guide" id="info">이용 가이드</h3>
      </div>
    </v-flex>

    <v-flex fluid lg12 xs12 class="ma-auto py-8 px-0 mx-0">
      <vueper-slides fixed-height="600px" bullets-outside fade :touchable="false" height="630px">
        <vueper-slide
          style="height:100%"
          v-for="(slide, i) in slides"
          :key="i"
          :image="slide.image"
        />
      </vueper-slides>
    </v-flex>
  </v-container>
</template>

<script>
import ImageBanner from "@/components/ImageBanner";
import { VueperSlides, VueperSlide } from "vueperslides";
import "vueperslides/dist/vueperslides.css";
export default {
  components: {
    ImageBanner,
    VueperSlides,
    VueperSlide
  },
  data() {
    return {
      bannerImg: [this.getImgUrl("골목1.png"), this.getImgUrl("골목2.png")],
      slides: [
        {
          // You can also provide a URL for the image.
          image: this.getImgUrl("guide1.png")
        },
        {
          // You can also provide a URL for the image.
          image: this.getImgUrl("guide2.png")
        },
        {
          // You can also provide a URL for the image.
          image: this.getImgUrl("guide3.png")
        },
        {
          // You can also provide a URL for the image.
          image: this.getImgUrl("guide4.png")
        }
      ]
    };
  },
  methods: {
    getImgUrl(img) {
      return require("../assets/" + img);
    },
    scrolltoInfo() {
      document.getElementById("info").scrollIntoView();
    }
  }
};
</script>
<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Nanum+Pen+Script&display=swap");
.guide {
  font-family: "Nanum Pen Script", cursive;
}

.blinking {
  -webkit-animation: blink 1s ease-in-out infinite alternate;
  -moz-animation: blink 1s ease-in-out infinite alternate;
  animation: blink 1s ease-in-out infinite alternate;
}
@-webkit-keyframes blink {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
@-moz-keyframes blink {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
@keyframes blink {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
</style>
