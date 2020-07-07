import axios from "axios";

export default axios.create({
 baseURL : "http://i02b206.p.ssafy.io/dc/" // AWS
//  baseURL: "http://localhost:8000/dc/" // 로컬
});