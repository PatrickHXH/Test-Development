import request from "../HttpCommon.js";

class ModuleApi {
  getmodulelist(data) {
    return request.get("/api/modules/tree", data);
  }
  createmodule(data) {
    return request.post("/api/modules/create/", data);
  }
}

export default new ModuleApi();
