import request from "../HttpCommon.js";

class ModuleApi {
  getmodulelist(data) {
    return request.get("/api/modules/tree", data);
  }
  createmodule(data) {
    return request.post("/api/modules/create/", data);
  }
  deletemodule(id) {
    return request.get("/api/modules/delete/" + id);
  }
  getcaselist(id, data) {
    return request.get("/api/modules/" + id + "/cases", data);
  }
}

export default new ModuleApi();
