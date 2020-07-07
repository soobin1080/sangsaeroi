<template>
  <div class="map_wrap">
    <!-- 지도를 표시할 div 입니다 -->
    <div id="map" style="width:100%;height:100%;"></div>
    <ul id="category">
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
  </div>
</template>



<script>
export default {
  data() {
    return {
      // 마커를 클릭했을 때 해당 장소의 상세정보를 보여줄 커스텀오버레이입니다
      placeOverlay: "",
      contentNode: "", // 커스텀 오버레이의 컨텐츠 엘리먼트 입니다
      currCategory: "", // 현재 선택된 카테고리를 가지고 있을 변수입니다
      markers: [], // 마커를 담을 배열입니다
      mapContainer: "", // 지도를 표시할 div
      mapOption: {
        center: "", // 지도의 중심좌표
        level: 5 // 지도의 확대 레벨
      },
      // 지도를 생성합니다
      map: "", //마커추가하려면 객체를 아래와 같이 하나 만든다.
      // 장소 검색 객체를 생성합니다
      ps: ""
    };
  },
  mounted() {
    window.kakao && window.kakao.maps ? this.initMap() : this.addScript();
  },
  methods: {
    initMap() {
      var placeOverlay = new kakao.maps.CustomOverlay({ zIndex: 1 }),
        contentNode = document.createElement("div"), // 커스텀 오버레이의 컨텐츠 엘리먼트 입니다
        markers = [], // 마커를 담을 배열입니다
        currCategory = ""; // 현재 선택된 카테고리를 가지고 있을 변수입니다
      var mapContainer = document.getElementById("map"); // 지도를 표시할 div
      var mapOption = {
        center: new kakao.maps.LatLng(37.565882, 126.976853), // 지도의 중심좌표
        level: 3 // 지도의 확대 레벨
      };
      // 지도를 생성합니다
      var map = new kakao.maps.Map(mapContainer, mapOption); //마커추가하려면 객체를 아래와 같이 하나 만든다.
      var marker = new kakao.maps.Marker({
        position: map.getCenter()
      });
      marker.setMap(map);

      // 장소 검색 객체를 생성합니다
      var ps = new kakao.maps.services.Places(map);
      this.ps = ps;
      // 지도에 idle 이벤트를 등록합니다
      kakao.maps.event.addListener(map, "idle", this.searchPlaces);
      this.map = map;
      // 커스텀 오버레이의 컨텐츠 노드에 css class를 추가합니다
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
    },
    addScript() {
      const script = document.createElement("script");

      script.onload = () => kakao.maps.load(this.initMap);
      script.src =
        "http://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=6405ff39dec816a53c42352288e80bab&&libraries=services,clusterer,drawing";
      document.head.appendChild(script);
    },

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
      var imageSrc =
        //"https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/places_category.png", // 마커 이미지 url, 스프라이트 이미지를 씁니다
        //url('../assets/test2.png') ;
        //"localhot:8080/assets/test2.png"
        require("../assets/markers.png");
      var imageSize = new kakao.maps.Size(27, 28); // 마커 이미지의 크기
      var imgOptions = {
        spriteSize: new kakao.maps.Size(72, 416), // 스프라이트 이미지의 크기
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
#category {
  position: absolute;
  top: 10px;
  left: 10px;
  border-radius: 5px;
  border: 1px solid #909090;
  box-shadow: 0 1px 1px rgba(0, 0, 0, 0.4);
  background: #fff;
  overflow: hidden;
  z-index: 2;
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
</style>