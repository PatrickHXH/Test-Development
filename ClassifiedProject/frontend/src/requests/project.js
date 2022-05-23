import axios from "axios";
import request from "../HttpCommon.js";

class ProjectApi {
  getproject(data) {
    return request.get("/api/projects/list", data);
  }

  getoneproject(id) {
    return request.get("/api/projects/" + id);
  }
  updateproject(id, data) {
    return request.put("/api/projects/" + id, data);
  }
  createproject(data) {
    return request.post("/api/projects/create", data);
  }
  deleteproject(id) {
    return request.delete("/api/projects/" + id);
  }
  updateImage(data) {
    return axios({
      method: "post",
      url: "/api/projects/upload/",
      timeout: 20000,
      data: data,
    });
  }
}

export default new ProjectApi();
