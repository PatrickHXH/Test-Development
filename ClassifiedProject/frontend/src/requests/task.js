import request from "../HttpCommon.js";

class TaskApi {
  createTask(data) {
    return request.post("/api/tasks/", data);
  }
  getTaskList(data) {
    return request.get("/api/tasks/list/", data);
  }
  deleteTask(id) {
    return request.post("/api/tasks/delete/" + id);
  }
  getTaskDetail(tid) {
    return request.get("/api/tasks/" + tid);
  }
  updateTask(tid, data) {
    return request.post("/api/tasks/update/" + tid, data);
  }
  runningTask(tid) {
    return request.post("/api/tasks/" + tid + "/running");
  }
  getTaskCaseList(tid) {
    return request.get("/api/tasks/" + tid + "/caseList");
  }
  updateTaskCaseList(tid, data) {
    return request.put("/api/tasks/" + tid + "/caseList", data);
  }
}

export default new TaskApi();
