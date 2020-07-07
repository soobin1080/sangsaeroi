<template>
  <div class="map_wrap">
    <div id="map" style="width:100%;height:100%;"></div>
    <!-- info -->
    <v-tooltip left style="z-index:3">
      <template v-slot:activator="{ on }">
        <v-btn class="infobtn blinking" fab small color="error" dark v-on="on">
          <span style="font-size:25px" class="mdi mdi-information"></span>
        </v-btn>
      </template>
      <span class="infotext" style="font-size:15pt">지역을 클릭해보세요 !</span>
    </v-tooltip>
    <!-- category -->
    <v-tooltip right style="z-index:3">
      <template v-slot:activator="{ on }">
        <ul id="category" v-on="on">
          <li @click="onClickCategory('MT1')" id="MT1" data-order="0">
            <span class="category_bg mart"></span>
            마트
          </li>
          <li @click="onClickCategory('SC4')" id="SC4" data-order="1">
            <span class="category_bg school"></span>
            학교
          </li>
          <li @click="onClickCategory('PK6')" id="PK6" data-order="2">
            <span class="category_bg parking"></span>
            주차장
          </li>
          <li @click="onClickCategory('SW8')" id="SW8" data-order="3">
            <span class="category_bg subway"></span>
            지하철역
          </li>
          <li @click="onClickCategory('CT1')" id="CT1" data-order="4">
            <span class="category_bg culture"></span>
            문화시설
          </li>
          <li @click="onClickCategory('AT4')" id="AT4" data-order="5">
            <span class="category_bg tour"></span>
            관광명소
          </li>
          <li @click="onClickCategory('FD6')" id="FD6" data-order="6">
            <span class="category_bg restaurant"></span>
            음식점
          </li>
          <li @click="onClickCategory('HP8')" id="HP8" data-order="7">
            <span class="category_bg hospital"></span>
            병원
          </li>
        </ul>
      </template>
      <span class="infotext" style="font-size:15pt">주변 시설을 확인해보세요 !</span>
    </v-tooltip>
    <!-- 상권 분석  dialog -->
    <v-dialog v-model="dialog" class="ml-3" max-width="970px" transition="dialog-bottom-transition">
      <template v-slot:activator="{ on }">
        <div style="text-align:center">
          <v-btn
            large
            v-if="selectarea"
            style=" position: absolute; bottom: 0px; z-index: 2;"
            color="warning"
            dark
            v-on="on"
          >
            <div class="mdi mdi-chevron-double-up pr-1" style="font-size:20px"></div>
            <br />
            <span class="analyzebtn pt-1">상권 분석</span>
          </v-btn>
        </div>
      </template>
      <Result :guname="this.guname" :dongname="this.dongname" class="result"></Result>
    </v-dialog>
  </div>
</template>
<script>
import Dong from "@/assets/json/HangJeongDong.json";
import Result from "@/components/Result";
export default {
  name: "Map",
  components: {
    Result
  },

  data() {
    return {
      selectarea: false,
      dongname: "",
      guname: "",
      dialog: false,
      Polylist: [],
      dong: "",
      checkOn: false,
      // 마커를 클릭했을 때 해당 장소의 상세정보를 보여줄 커스텀오버레이입니다
      customOverlay: "",
      placeOverlay: "",
      contentNode: "", // 커스텀 오버레이의 컨텐츠 엘리먼트 입니다
      currCategory: "", // 현재 선택된 카테고리를 가지고 있을 변수입니다
      markers: [], // 마커를 담을 배열입니다
      infowindow: "",
      mapContainer: "", // 지도를 표시할 div
      mapOption: {
        center: "", // 지도의 중심좌표
        level: 5 // 지도의 확대 레벨
      },
      // 지도를 생성합니다
      map: "", //마커추가하려면 객체를 아래와 같이 하나 만든다.
      ps: "", // +
      clicked: "",
      geocoder: ""
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
      var placeOverlay = new kakao.maps.CustomOverlay({ zIndex: 1 }),
        contentNode = document.createElement("div"), // 커스텀 오버레이의 컨텐츠 엘리먼트 입니다
        markers = [], // 마커를 담을 배열입니다
        currCategory = ""; // 현재 선택된 카테고리를 가지고 있을 변수입니다
      var mapContainer = document.getElementById("map"); // 지도를 표시할 div
      this.mapContainer = mapContainer;
      var mapOption = {
        center: new kakao.maps.LatLng(37.566826, 126.9786567), // 지도의 중심좌표
        level: 8 // 지도의 확대 레벨
      };
      // 지도를 생성합니다
      var map = new kakao.maps.Map(mapContainer, mapOption); //마커추가하려면 객체를 아래와 같이 하나 만든다.
      var geocoder = new kakao.maps.services.Geocoder();
      this.geocoder = geocoder;
      var marker = new kakao.maps.Marker({
        //+
        // position: map.getCenter()
      });
      marker.setMap(map);
      // 장소 검색 객체를 생성합니다
      var ps = new kakao.maps.services.Places(map);
      this.ps = ps;
      // 지도에 idle 이벤트를 등록합니다
      kakao.maps.event.addListener(map, "idle", this.searchPlaces);
      this.map = map;
      this.customOverlay = customOverlay;
      this.infowindow = infowindow;
      contentNode.className = "placeinfo_wrap";
      // 커스텀 오버레이의 컨텐츠 노드에 mousedown, touchstart 이벤트가 발생했을때
      // 지도 객체에 이벤트가 전달되지 않도록 이벤트 핸들러로 kakao.maps.event.preventMap 메소드를 등록합니다
      this.addEventHandle(
        contentNode,
        "mousedown",
        kakao.maps.event.preventMap
      );
      this.addEventHandle(
        contentNode,
        "touchstart",
        kakao.maps.event.preventMap
      );

      // 커스텀 오버레이 컨텐츠를 설정합니다
      placeOverlay.setContent(contentNode);
      this.placeOverlay = placeOverlay;
      this.contentNode = contentNode;

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
        );
      }
    },
    addScript() {
      const script = document.createElement("script");
      script.onload = () => kakao.maps.load(this.initMap);
      script.src =
        "http://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=6405ff39dec816a53c42352288e80bab&&libraries=services,clusterer,drawing";
      document.head.appendChild(script);
    },
    displayArea(polygon, Mmap, coordinates, name, length, customOverlay) {
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
        strokeWeight: 2, // 선두께
        strokeColor: "#004c80", // 선색
        strokeOpacity: 0.4, // 선 투명도
        fillColor: "#fff",
        fillOpacity: 0.4
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
        self.selectarea = true;
        self.searchDetailAddrFromCoords(mouseEvent.latLng, function(
          result,
          status
        ) {
          var resultArr = result[0].address.address_name.split(" ");

          self.guname = resultArr[1];

          if (status === kakao.maps.services.Status.OK) {
            var detailAddr =
              result[0].road_address != null
                ? "<div>도로명주소 : " +
                  result[0].road_address.address_name +
                  "</div>"
                : "";
            detailAddr +=
              "<div>지번 주소 : " + result[0].address.address_name + "</div>";

            var content =
              '<div class="bAddr">' +
              '<span class="title">법정동 주소정보</span>' +
              detailAddr +
              "</div>";
          }
        });
        polygon.setOptions({ fillColor: "#03f" });
        self.clicked = polygon;
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
        var moveLocation = new kakao.maps.LatLng(
          mouseEvent.latLng.Ha,
          mouseEvent.latLng.Ga
        );
        self.map.setCenter(moveLocation);
        self.map.setLevel(5);
        self.dongname = name;
      });
    },
    // 좌표로 '구' 나오게!!
    searchDetailAddrFromCoords(coords, callback) {
      // 좌표로 법정동 상세 주소 정보를 요청합니다
      this.geocoder.coord2Address(coords.getLng(), coords.getLat(), callback);
    },
    //카테고리 함수 추가
    // 엘리먼트에 이벤트 핸들러를 등록하는 함수입니다
    addEventHandle(target, type, callback) {
      if (target.addEventListener) {
        target.addEventListener(type, callback);
      } else {
        target.attachEvent("on" + type, callback);
      }
    },

    // 카테고리 검색을 요청하는 함수입니다
    searchPlaces() {
      if (!this.currCategory) {
        return;
      }

      // 커스텀 오버레이를 숨깁니다
      this.placeOverlay.setMap(null);

      // 지도에 표시되고 있는 마커를 제거합니다
      this.removeMarker(this.markers);

      this.ps.categorySearch(this.currCategory, this.placesSearchCB, {
        useMapBounds: true
      });
    },

    // 장소검색이 완료됐을 때 호출되는 콜백함수 입니다
    placesSearchCB(data, status, pagination) {
      if (status === kakao.maps.services.Status.OK) {
        // 정상적으로 검색이 완료됐으면 지도에 마커를 표출합니다
        this.displayPlaces(data);
      } else if (status === kakao.maps.services.Status.ZERO_RESULT) {
        // 검색결과가 없는경우 해야할 처리가 있다면 이곳에 작성해 주세요
      } else if (status === kakao.maps.services.Status.ERROR) {
        // 에러로 인해 검색결과가 나오지 않은 경우 해야할 처리가 있다면 이곳에 작성해 주세요
      }
    },

    // 지도에 마커를 표출하는 함수입니다
    displayPlaces(places) {
      // 몇번째 카테고리가 선택되어 있는지 얻어옵니다
      // 이 순서는 스프라이트 이미지에서의 위치를 계산하는데 사용됩니다
      var order = document
        .getElementById(this.currCategory)
        .getAttribute("data-order");
      for (var i = 0; i < places.length; i++) {
        // 마커를 생성하고 지도에 표시합니다
        this.marker = this.addMarker(
          new kakao.maps.LatLng(places[i].y, places[i].x),
          order
        );

        let vm = this;
        // 마커와 검색결과 항목을 클릭 했을 때
        // 장소정보를 표출하도록 클릭 이벤트를 등록합니다
        (function(marker, place) {
          kakao.maps.event.addListener(marker, "click", function() {
            vm.displayPlaceInfo(place);
          });
        })(this.marker, places[i]);
      }
    },

    // 마커를 생성하고 지도 위에 마커를 표시하는 함수입니다
    addMarker(position, order) {
      let vm = this;
      var imageSrc = require("../assets/markers.png");
      var imageSize = new kakao.maps.Size(27, 28); // 마커 이미지의 크기
      var imgOptions = {
        spriteSize: new kakao.maps.Size(72, 280), // 스프라이트 이미지의 크기
        spriteOrigin: new kakao.maps.Point(46, order * 36), // 스프라이트 이미지 중 사용할 영역의 좌상단 좌표
        offset: new kakao.maps.Point(11, 28) // 마커 좌표에 일치시킬 이미지 내에서의 좌표
      };
      var markerImage = new kakao.maps.MarkerImage(
        imageSrc,
        imageSize,
        imgOptions
      );
      var marker = new kakao.maps.Marker({
        position: position, // 마커의 위치
        image: markerImage
      });
      marker.setMap(vm.map); // 지도 위에 마커를 표출합니다
      this.markers.push(marker); // 배열에 생성된 마커를 추가합니다

      return marker;
    },

    // 지도 위에 표시되고 있는 마커를 모두 제거합니다
    removeMarker(markers) {
      for (var i = 0; i < this.markers.length; i++) {
        this.markers[i].setMap(null);
      }
      this.markers = [];
    },

    // 클릭한 마커에 대한 장소 상세정보를 커스텀 오버레이로 표시하는 함수입니다
    displayPlaceInfo(place) {
      var content =
        '<div class="placeinfo">' +
        '   <a class="title" href="' +
        place.place_url +
        '" target="_blank" title="' +
        place.place_name +
        '">' +
        place.place_name +
        "</a>";

      if (place.road_address_name) {
        content +=
          '    <span title="' +
          place.road_address_name +
          '">' +
          place.road_address_name +
          "</span>" +
          '  <span class="jibun" title="' +
          place.address_name +
          '">(지번 : ' +
          place.address_name +
          ")</span>";
      } else {
        content +=
          '    <span title="' +
          place.address_name +
          '">' +
          place.address_name +
          "</span>";
      }

      content +=
        '    <span class="tel">' +
        place.phone +
        "</span>" +
        "</div>" +
        '<div class="after"></div>';

      this.contentNode.innerHTML = content;
      this.placeOverlay.setPosition(new kakao.maps.LatLng(place.y, place.x));
      this.placeOverlay.setMap(this.map);
    },
    // 카테고리를 클릭했을 때 호출되는 함수입니다
    onClickCategory(id) {
      var className;

      var category = document.getElementById("category"),
        children = category.children,
        i;

      for (i = 0; i < children.length; i++) {
        if (children[i].id == id) {
          className = children[i].className;
        }
      }

      this.placeOverlay.setMap(null);

      if (className === "on") {
        this.currCategory = "";
        this.changeCategoryClass();
        this.removeMarker(this.markers);
      } else {
        this.currCategory = id;
        this.changeCategoryClass(id);
        this.searchPlaces();
      }
    },

    // 클릭된 카테고리에만 클릭된 스타일을 적용하는 함수입니다
    changeCategoryClass(el) {
      var category = document.getElementById("category"),
        children = category.children,
        i;

      for (i = 0; i < children.length; i++) {
        if (children[i].id == el) {
          children[i].className = "on";
        } else {
          children[i].className = "";
        }
      }
    }
    //카테고리 함수 끝
  }
};
</script>



<style>
.map_wrap,
.map_wrap * {
  margin: 0;
  padding: 0;
  font-family: "Malgun Gothic", dotum, "돋움", sans-serif;
  font-size: 12px;
}
.map_wrap {
  position: relative;
  width: 100%;
  height: 100%;
}
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
  background-color: white;
  font-size: 12px;
  padding: 5px;
}
.v-application .info {
  background-color: white !important;
  border-color: white !important;
}
.info .title {
  font-weight: bold;
  font-size: 17px !important;
}

.mapinfo {
  position: absolute;
  top: 80px;
  z-index: 2;
}
.result {
  width: 80%;
  margin: auto;
  bottom: 100px;
  position: absolute;
  overflow-y: scroll;
  overflow-x: hidden;
  height: 500px;
  z-index: 2;
}
.result::-webkit-scrollbar {
  width: 10px;
}
.result::-webkit-scrollbar-thumb {
  background-color: #30487c;
  border-radius: 10px;
  background-clip: padding-box;
  border: 2px solid transparent;
}
.result::-webkit-scrollbar-track {
  background-color: grey;
  border-radius: 10px;
  box-shadow: inset 0px 0px 5px white;
}
.area {
  position: absolute;
  top: 80px;
  z-index: 2;
}

#category {
  position: absolute;
  top: 10px;
  left: 10px;
  border-radius: 5px;
  border: 1px solid #909090;
  box-shadow: 0 1px 1px rgba(0, 0, 0, 0.4);
  background: #fff;
  overflow: hidden;
  z-index: 3;
}
#category li {
  float: left;
  list-style: none;
  width: 50px;
  border-right: 1px solid #acacac;
  padding: 6px 0;
  text-align: center;
  cursor: pointer;
}
#category li.on {
  background: #eee;
}
#category li:hover {
  background: #ffe6e6;
  border-left: 1px solid #acacac;
  margin-left: -1px;
}
#category li:last-child {
  margin-right: 0;
  border-right: 0;
}
#category li span {
  display: block;
  margin: 0 auto 3px;
  width: 27px;
  height: 28px;
}
#category li .category_bg {
  /* background: url(https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/places_category.png) */
  background: url(../assets/markers.png) no-repeat;
}
#category li .mart {
  background-position: -10px 0;
}
#category li .school {
  background-position: -10px -36px;
}
#category li .parking {
  background-position: -10px -72px;
}
#category li .subway {
  background-position: -10px -108px;
}
#category li .culture {
  background-position: -10px -144px;
}
#category li .tour {
  background-position: -10px -180px;
}
#category li .restaurant {
  background-position: -10px -216px;
}
#category li .hospital {
  background-position: -10px -252px;
}
#category li.on .category_bg {
  background-position-x: -46px;
}
.placeinfo_wrap {
  position: absolute;
  bottom: 28px;
  left: -150px;
  width: 300px;
}
.placeinfo {
  position: relative;
  width: 100%;
  border-radius: 6px;
  border: 1px solid #ccc;
  border-bottom: 2px solid #ddd;
  padding-bottom: 10px;
  background: #fff;
}
.placeinfo:nth-of-type(n) {
  border: 0;
  box-shadow: 0px 1px 2px #888;
}
.placeinfo_wrap .after {
  content: "";
  position: relative;
  margin-left: -12px;
  left: 50%;
  width: 22px;
  height: 12px;
  background: url("https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/vertex_white.png");
}
.placeinfo a,
.placeinfo a:hover,
.placeinfo a:active {
  color: #fff;
  text-decoration: none;
}
.placeinfo a,
.placeinfo span {
  display: block;
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
}
.placeinfo span {
  margin: 5px 5px 0 5px;
  cursor: default;
  font-size: 13px;
}
.placeinfo .title {
  font-weight: bold;
  font-size: 14px;
  border-radius: 6px 6px 0 0;
  margin: -1px -1px 0 -1px;
  padding: 10px;
  color: #fff;
  background: #d95050;
  background: #d95050
    url(https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/arrow_white.png)
    no-repeat right 14px center;
}
.placeinfo .tel {
  color: #0f7833;
}
.placeinfo .jibun {
  color: #999;
  font-size: 11px;
  margin-top: 0;
}
.infobtn {
  position: absolute;
  z-index: 3;
  top: 10px;
  right: 10px;
}

@import url("https://fonts.googleapis.com/css2?family=Nanum+Pen+Script&display=swap");
.infotext {
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

@import url("https://fonts.googleapis.com/css2?family=Do+Hyeon&display=swap");
.analyzebtn {
  font-family: "Do Hyeon", sans-serif;
  font-size: 13pt;
}
</style>