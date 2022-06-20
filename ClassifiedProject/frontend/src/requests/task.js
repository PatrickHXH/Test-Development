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
}

export default new TaskApi();
