import request from "../HttpCommon.js";

class ReprotApi {
  getReportList(data) {
    return request.get("/api/reports/list", data);
  }
  getReportDetail(rid) {
    return request.get("/api/reports/" + rid + "/detail");
  }
  deleteReport(rid) {
    return request.post("/api/reports/" + rid + "/delete");
  }
}

export default new ReprotApi();
