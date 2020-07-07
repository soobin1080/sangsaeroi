# 특화 - Sub2

## Team

### 팀명

`DC(덕명동 클라쓰)`

### 서비스 명

`상새로이 ( 상권의 활성화를 도와 상권을 새로이 한다 )`

---

### Role & Responsibility 

- Front-end
  - `안지연` : 프로트엔드 팀장
  - `오유경` : 배포
- Back-end
  - `김대래` : 팀장
  - `우동균` : 백엔드 팀장, CTO
  - `김수빈` : 데이터베이스

### 구현 기술 스택

---

##### Front-end

| 기술스택   | 버전   | 학습                                                         |
| ---------- | ------ | ------------------------------------------------------------ |
| JavaScript |        | [Link](https://www.w3schools.com/js/default.asp)             |
| Vue        | 2.6.10 | [Link](https://vuejs.org/v2/guide/)                          |
| Vuex       |        | [Link](https://12bme.tistory.com/452)                        |
| Vuetify    | 2.0.0  | [Link](https://vuetifyjs.com/ko/getting-started/quick-start/) |
| Axios      | 3.1.1  | [Link](https://9105lgm.tistory.com/150) - Promise / Async 개념 이해 |
| Node.js    |        |                                                              |

---

##### Back-end

| 기술스택 | 버전  | 학습                                                |
| -------- | ----- | --------------------------------------------------- |
| Python   | 3.6.8 | [Link](https://wikidocs.net/book/1)                 |
| Django   | 2.2.7 | [Link](https://tutorial.djangogirls.org/ko/django/) |
| MySQL    |       |                                                     |

---

##### Big Data

- Collaborativ Filtering
  - 참고 블로그 [Link](http://bitly.kr/6WGxWXzh)
  - 구현
    - User-based - [Link](https://medium.com/sfu-cspmp/recommendation-systems-user-based-collaborative-filtering-using-n-nearest-neighbors-bf7361dc24e0)
    - Python - 참고 1 [Link](https://kutar37.tistory.com/37)
    - Python - 참고 2 [Link](https://kutar37.tistory.com/38)
    - Python - 참고 3 [Link](https://kutar37.tistory.com/39)
- 유사도
  - 개념 [Link](https://www.fun-coding.org/recommend_basic3.html)

| 기술스택     | 버전   | 학습                                                         |
| ------------ | ------ | ------------------------------------------------------------ |
| Pandas       | 0.25.3 | [Link]()                                                     |
| Numpy        | 1.17.3 | [Link](https://numpy.org/devdocs/user/quickstart.html)       |
| Scipy        | 1.3.1  | [Link](https://datascienceschool.net/view-notebook/175522b819ae4645907179462dabc5d4/) |
| Scikit-learn | 0.22.2 | [Link](https://scikit-learn.org/stable/user_guide.html)      |
| Surprise     |        | [Link 1](https://surprise.readthedocs.io/en/stable/getting_started.html)<br />[Link 2](https://blog.cambridgespark.com/tutorial-practical-introduction-to-recommender-systems-dbe22848392b) |

---

##### Etc.

- Git
- Jira
- Mattermost

---

## 서비스 명세

### 상권분석 및 음식점 업종 추천



#### 개요

`상새로이`는 **상권의 활성화를 도와 상권을 새로이 한다는 목적을 갖는 서비스**입니다.

음식점을 오픈하고자 하는 예비 소상공인과 프랜차이즈화를 원하는 소상공인을 위해
**공공데이터와 다이닝코드의 음식점 리뷰 데이터를 활용하여 상권을 분석한 결과를 제공**합니다.

또한 분석한 정보를 토대로 창업 시 유리한 조건을 갖추거나 경쟁력을 갖추기 위한
**업종이나 지역을 추천**해 줌으로써 **창업 실패율을 낮추고 상권의 활성화를 돕는 효과**를 기대합니다.



추천 시스템은 협업 필터링(Collaborative Filtering) 기법을 주로 사용하며, 
지역 / 업종 별 상권의 정보와 각각의 상황에 맞는 사용자 리뷰 정보를 기반으로 Matrix Factorization을 통해
경쟁력있는 음식점을 추천해주고자 합니다.



#### 상세

- 사용자

  : 소상공인 - 음식점 예비 창업자 또는 기창업자

- 기능

  - 분석

    - 선택한 지역의 상권을 분석하여 결과 제공(매출, 유동인구 등)
    - 주변 시설 확인 - 학교, 교회, 회사, 주차장 유무 등
    - 인기/비인기 카테고리의 분포 및 시세 확인

  - 추천

    - 지역 선택 시
      - 지역(동)의 리뷰를 남긴 유저 클러스터가 좋아하는 음식점을 분석하고 해당 지역에 없는 카테고리 추천
      - 모든 카테고리가 있다면 평점이 가장 낮은 음식점을 추천
      - 최대 3개 복수 선택 가능
    - 업종(카테고리) 선택 시
      - 지역별 해당 업종의 분포도를 확인하고 그 지역의 주변시설과 유동인구를 기준으로 지역을 창업 적합 여부 추천

    - 메커니즘
      - 유저 - 음식점간 Matrix-Factorization와 유저간 유사도를 통해 인기 업종/지역을 분석 및 추천

    - 추후 심화
      - 실제 리뷰데이터들을 분석 및 원인 파악 - W2V, 텍스트 긍/부정 정보 등을 분석

  - 부가 기능

    - 분석한 지역의 부동산 시세 확인 - 네모 서비스 참고
    - 창업 관련 정부 지원 정보 제공
    - 기창업자 성공 인터뷰 - 유튜브 EO(태용) 등
    - 프랜차이즈 정보 제공

- 활용 가능 데이터

  - 기존 제공 데이터(다이닝코드)
    - 음식점 정보
    - 메뉴정보
    - 리뷰
    - 유저 정보
  - 상업용 부동산 임대동향 [링크](https://www.r-one.co.kr/rone/resis/common/sub/sub.do?pageVal=page_4_2)

    - 각 지역별 전/월세 정보
  - 국세통계 연보 이력 변경현황  [링크](https://stats.nts.go.kr/data/data.asp#)

    - 창업 현황
    - 폐업 현황

    - 폐업률 정보
  - 서울시 우리마을 가게 상권분석서비스 - 서울시 한정

    - 행정동별 상권변화지표 [링크](https://data.seoul.go.kr/dataList/OA-15575/A/1/datasetView.do)
    - 상권 - 추정매출 [링크](https://data.seoul.go.kr/dataList/OA-15572/A/1/datasetView.do)
    - 상권배후지 - 추정유동인구 [링크](https://data.seoul.go.kr/dataList/OA-15582/S/1/datasetView.do)
    - 상권배후지 내용이 많이 있다.
  - 상가 업소 개방 DB
    - API [링크](http://data.sbiz.or.kr/sdsc/p06002/go/o/openapi/manual-store)

- 타 서비스

  - 소상공인 상권분석 서비스 : 전국
  - 우리마을 가게 상권분석 서비스 : 서울
  - 서울 공통 프로젝트 - Bizbox : 서울

---

### 요구사항 명세

| 요구사항 | 카테고리                                 |
| -------- | ---------------------------------------- |
| 1        | Sub2 PJT 이관                            |
| 2        | 회원관리                                 |
| 3        | 지역별 상권분석                          |
| 4        | 마이페이지                               |
| 5        | 게시판(멘토링 / 창업지원)                |
| 6        | 배포                                     |


##### Req. 1. Sub2 PJT 이관
- Front
- Back

##### Req. 2. 회원관리
- Front
    - 회원가입 시 이메일체크
    - 이메일, 비밀번호 찾기
    - 로그인
    - 회원 정보 수정
    - 탈퇴
- Back
    - API 구현
        - 회원가입
        - 로그인
        - 이메일체크
        - 이메일 전송(이메일, 비밀번호 찾기)
        - 회원 정보수정
        - 탈퇴

##### Req. 3. 지역별 상권분석
- Front
    - 카카오 Map API 기본 구현
    - 행정동별 다각형 그리기
    - 카테고리별 지도 마커 표시
    - 지역 선택 시 행정동 표시
    - 분석 결과 데이터 표시
    - 추천 결과 데이터 표시
- Back
    - API 구현
        - 지역 선택시 해당 지역 분석 결과 전달
        - 지역 선택시 해당 지역 추천 결과 전달
    - 빅데이터
        - 지역에 따른 상권 분석
        - 지역에 따른 업종 추천
        - K-means 알고리즘 학습 및 구현
        - MF + K-means 하이브리드 추천 시스템 구현

##### Req. 4. 마이페이지
- Front
    - 결과 저장 페이지 (언제, 어느 지역을, 그 결과, 파일로 저장)
    - 파일 다운로드
- Back
    - API
        - 지역 보내면 결과 주기 (Req3. 동일)
        - 사용자가 저장해 둔 결과들 보내주기
        - 파일 업/다운로드

##### Req. 5. 게시판(멘토링 / 창업지원)
- Front
    - 멘토링 게시판 UI
    - 창업지원 게시판
    - 댓글
- Back
    - 게시판 CRUD API
    - 창업 지원 자료 가져오기(API or Crawling)

##### Req. 6. 배포
- Front
    - NginX 를 통해 Front Vue 배포
- Back
    - Django 배포
    - MySQL 마이그레이션