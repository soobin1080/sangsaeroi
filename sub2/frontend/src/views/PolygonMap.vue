<template>
  <div id="map" style="width:100%;height:100%;"></div>
</template>
<script>
import Dong from "@/assets/json/HangJeongDong.json";

export default {
  data() {
    return {
      Polylist: [],

      // 마커를 클릭했을 때 해당 장소의 상세정보를 보여줄 커스텀오버레이입니다
      customOverlay: "",
      infowindow: "",
      mapContainer: "", // 지도를 표시할 div //전역변수 선언해야할까
      mapOption: {
        center: "", // 지도의 중심좌표
        level: 5 // 지도의 확대 레벨
      },
      // 지도를 생성합니다
      map: "" //마커추가하려면 객체를 아래와 같이 하나 만든다.
    };
  },
  mounted() {
    window.kakao && window.kakao.maps ? this.initMap() : this.addScript();
  },
  methods: {
    initMap() {
      let areas = Dong; // 좌표 저장할 배열
      let coordinates = []; // 행정 구 이름
      var customOverlay = new kakao.maps.CustomOverlay({});
      var infowindow = new kakao.maps.InfoWindow({ removable: true });
      var mapContainer = document.getElementById("map"); // 지도를 표시할 div
      var mapOption = {
        center: new kakao.maps.LatLng(37.566826, 126.9786567), // 지도의 중심좌표
        level: 8 // 지도의 확대 레벨
      };
      // 지도를 생성합니다
      var map = new kakao.maps.Map(mapContainer, mapOption); //마커추가하려면 객체를 아래와 같이 하나 만든다.

      this.map = map;
      this.customOverlay = customOverlay;
      this.infowindow = infowindow;

      var len = areas.length;

      for (var i = 0; i < len; i++) {
        this.displayArea(areas[i]);
      }

      for (var j = 0, datalen = areas.length; j < datalen; j++) {
        // 동의 경계면 좌표를 받아서 다각형 생성 함수에 전달
        this.coordinates = areas[j].geometry.coordinates;
        var name = areas[j].properties.ADM_DR_NM;

        this.displayArea(
          "polygon",
          this.map,
          this.coordinates[0][0],
          name,
          this.coordinates[0][0].length,
          this.customOverlay
          //color
        );
      }
    },
    addScript() {
      const script = document.createElement("script");
      /* global kakao */

      script.onload = () => kakao.maps.load(this.initMap);
      script.src =
        "http://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=6405ff39dec816a53c42352288e80bab&&libraries=services,clusterer,drawing";
      document.head.appendChild(script);
    },

    displayArea(
      polygon,
      Mmap,
      coordinates,
      name,
      length,
      customOverlay
      //color
    ) {
      let mode = polygon;
      let path = [];
      let points = [];
      for (let i = 0; i < length; i++) {
        // 좌표의 개수만큼 반복문을 돌며 경계 바운더리 생성(path생성)
        var point = new Object();
        point.x = coordinates[i][1];
        point.y = coordinates[i][0];
        points.push(point);
        path.push(new kakao.maps.LatLng(coordinates[i][1], coordinates[i][0]));
      }
      polygon = new kakao.maps.Polygon({
        // 생성된 path를 이용하여 폴리곤(다각형) 생성
        map: Mmap, // 다각형을 표시할 지도 객체
        path: path,
        strokeWeight: 2, // 선두깨
        strokeColor: "#004c80", // 선색
        strokeOpacity: 0.4, // 선 투명도
        fillColor: "#fff",
        fillOpacity: 0.7
      });

      var self = this;
      // 다각형에 mouseover 이벤트를 등록하고 이벤트가 발생하면 폴리곤의 채움색을 변경합니다
      // 지역명을 표시하는 커스텀오버레이를 지도위에 표시합니다
      kakao.maps.event.addListener(polygon, "mouseover", function(mouseEvent) {
        polygon.setOptions({ fillColor: "#09f" });

        self.customOverlay.setContent('<div class="area">' + name + "</div>");

        self.customOverlay.setPosition(mouseEvent.latLng);
        self.customOverlay.setMap(this.map);
      });

      // 다각형에 mousemove 이벤트를 등록하고 이벤트가 발생하면 커스텀 오버레이의 위치를 변경합니다
      kakao.maps.event.addListener(polygon, "mousemove", function(mouseEvent) {
        self.customOverlay.setPosition(mouseEvent.latLng);
      });

      // 다각형에 mouseout 이벤트를 등록하고 이벤트가 발생하면 폴리곤의 채움색을 원래색으로 변경합니다
      // 커스텀 오버레이를 지도에서 제거합니다
      kakao.maps.event.addListener(polygon, "mouseout", function() {
        polygon.setOptions({ fillColor: "#fff" });
        self.customOverlay.setMap(null);
      });

      // 다각형에 click 이벤트를 등록하고 이벤트가 발생하면 다각형의 이름과 면적을 인포윈도우에 표시합니다
      kakao.maps.event.addListener(polygon, "click", function(mouseEvent) {
        var content =
          '<div class="info">' +
          '   <div class="title">' +
          name +
          "</div>" +
          '   <div class="size">총 면적 : 약 ' +
          Math.floor(polygon.getArea()) +
          " m<sup>2</sup></area>" +
          "</div>";
        self.infowindow.setContent(content);
        self.infowindow.setPosition(mouseEvent.latLng);
        self.infowindow.setMap(self.map);
      });
    }
  }
};
</script>



<style>
.area {
  position: absolute;
  background: #fff;
  border: 1px solid #888;
  border-radius: 3px;
  font-size: 12px;
  top: -5px;
  left: 15px;
  padding: 2px;
}

.info {
  font-size: 12px;
  padding: 5px;
}
.info .title {
  font-weight: bold;
}
</style>