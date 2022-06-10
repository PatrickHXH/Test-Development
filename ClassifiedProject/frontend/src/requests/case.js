import request from "../HttpCommon.js";

class CaseApi {
  debugCase(data) {
    return request.post("/api/cases/debug", data);
  }
  assertCase(data) {
    return request.post("/api/cases/assert", data);
  }
  caseDetail(id) {
    return request.get("/api/cases/" + id + "/");
  }
  creatCase(data) {
    return request.post("/api/cases/", data);
  }
}

export default new CaseApi();
