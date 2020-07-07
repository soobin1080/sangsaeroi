<template>
  <div id="tabs" class="container">
    <div class="tabs">
      <a v-on:click="activetab=1" v-bind:class="[ activetab === 1 ? 'active' : '' ]">분석</a>
      <a v-on:click="activetab=2" v-bind:class="[ activetab === 2 ? 'active' : '' ]">추천</a>
    </div>

    <div class="content">
      <div v-if="activetab === 1" class="tabcontent">
        <AnalyzeReport :guname="this.guname" :dongname="this.dongname"></AnalyzeReport>
      </div>
      <div v-if="activetab === 2" class="tabcontent">
        <RecommendReport :guname="this.guname" :dongname="this.dongname"></RecommendReport>
      </div>
    </div>
  </div>
</template>
<script>
import AnalyzeReport from "@/components/AnalyzeReport";
import RecommendReport from "@/components/RecommendReport";
export default {
  name: "Result",
  components: {
    AnalyzeReport,
    RecommendReport
  },
  props: {
    guname: { type: String },
    dongname: { type: String }
  },
  data() {
    return { activetab: 1 };
  },
  watch: {
    guname: "reRendering",
    dongname: "reRendering"
  },
  methods: {
    reRendering() {
      this.activetab = 1;
    }
  }
};
</script>
<style scoped>
/* RESET */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.container {
  margin: 10px auto;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 0.9em;
  color: #888;
}

/* Style the tabs */
.tabs {
  overflow: hidden;
  margin-left: 10px;
  margin-bottom: -2px; /* hide bottom border */
}

.tabs ul {
  list-style-type: none;
  margin-left: 20px;
}

.tabs a {
  float: left;
  cursor: pointer;
  padding: 8px 25px;
  /* transition: background-color 0.2s; */
  border: 1px solid #ccc;
  border-right: none;
  background-color: #f1f1f1;
  border-radius: 10px 10px 0 0;
  font-weight: bold;
}
.tabs a:last-child {
  border-right: 1px solid #ccc;
}

/* Change background color of tabs on hover */
.tabs a:hover {
  background-color: #aaa;
  color: #fff;
}

/* Styling for active tab */
.tabs a.active {
  background-color: #fff;
  color: #484848;
  border-bottom: 2px solid #fff;
  cursor: default;
}

/* Style the tab content */
.tabcontent {
  padding: 30px;
  border: 1px solid #ccc;
  border-radius: 10px;
  box-shadow: 3px 3px 6px #e1e1e1;
}
.content {
  background-color: white;
  border-radius: 10px;
}
</style>