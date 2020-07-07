<template>
  <v-card outlined>
    <div color="white">
      <v-col class="text-center">
        <span class="grey--text caption font-italic">{{tag}}</span>
      </v-col>
    </div>
    <v-list v-if="items.length > 0" class="px-0 mx-0">
      <v-list-item-group class="px-0 mx-0">
        <v-list-item v-for="(item, i) in items" :key="i" class="mx-0">
          <v-col cols="9" class="px-0 mx-0">
            <span class="caption">{{item.key}}</span>
          </v-col>
          <v-col cols="4" class="px-0 mx-0">
            <span style="font-size:9pt;">{{item.score}}{{sufix}}</span>
          </v-col>
        </v-list-item>
      </v-list-item-group>
    </v-list>
    <v-list v-else>
      <v-list-item>
        <span class="caption">선택 지역의 골목상권 정보가 없습니다.</span>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script>
import http from "../http-common";
export default {
  name: "StoreListCard",
  data() {
    return {};
  },
  props: {
    items: {
      type: Array
    },
    tag: {
      type: String,
      default: ""
    },
    sufix: {
      type: String,
      default: ""
    }
  }
};
</script>
