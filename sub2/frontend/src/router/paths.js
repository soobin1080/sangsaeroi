const requireAuth = () => (to, from, next) => {
  console.log(sessionStorage.getItem('token'));
	if (sessionStorage.getItem('token') == null) {	
		alert("접근하실 수 없습니다. 로그인 해주세요!")	
		return next('/');
	}else{
		return next();
	}			
  };

export default [
  {
    path: "",
    view: "Home",
    name: "home"
  }, 
  {
    path: "/signup",
    view: "SignUp",
    name: "signUp"
  },
  {
    path: "/findmyinfo",
    view: "FindMyInfo",
    name: "findMyInfo"
  },
  {
    path: "/team",
    view: "TeamPage",
    name: "teamPage"
  },
  {
    path: '*',
    view: "ErrorPage",
    name: "errorPage"
  }, 
  {
    path: '/map',
    view: "Map",
    name: "Map"
  }, 
  {
    path: '/mypage',
    view: "MyPage",
    name: "myPage",
    beforeEnter:requireAuth()
  }, 
  {
    path: "/searchbydong/",
    view: "SearchByDong",
    name: "searchByDong"
  },
  {
    path: '/board_list',
    view: "board_list",
    name: "board_list"
  },
  {
    path: '/board_detail/:seq',
    view: "board_detail",
    name: "board_detail",
    props: true
  },
  {
    path: '/board_write',
    view: "board_write",
    name: "board_write",
    beforeEnter:requireAuth()
  },
  {
    path: '/board_update/:seq',
    view: "board_update",
    name: "board_update",
    props: true,
    beforeEnter:requireAuth()
  },   
];



