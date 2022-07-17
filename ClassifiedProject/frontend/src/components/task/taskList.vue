<template>
  <div class="task">
    <div style="text-align: left">
      <el-form :inline="true" :model="projectForm" class="demo-form-inline">
        <el-form-item label="项目">
          <el-select
            v-model="projectForm.id"
            placeholder="请选择项目"
            @change="changeproject"
          >
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option>
            <el-pagination
              background
              :page-size="6"
              @current-change="handleCurrentChange"
              :total="projecttotal"
              style="margin: 10px"
            >
            </el-pagination>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="showtask">创建</el-button>
        </el-form-item>
      </el-form>
    </div>
    <!-- 任务列表 -->
    <div>
      <el-table :data="taskData" border style="width: 100%">
        <el-table-column fixed prop="id" label="ID" width="80">
        </el-table-column>
        <el-table-column prop="name" label="姓名"> </el-table-column>
        <el-table-column prop="describe" label="描述"> </el-table-column>
        <el-table-column prop="create_time" label="创建时间"> </el-table-column>
        <el-table-column prop="update_time" label="更新时间"> </el-table-column>
        <el-table-column prop="status" label="状态">
          <template slot-scope="scope">
            <div v-if="scope.row.status === 0">
              <el-tag type="info">未执行</el-tag>
            </div>
            <div v-else-if="scope.row.status === 1">
              <el-tag type="success">执行中</el-tag>
            </div>
            <div v-else-if="scope.row.status === 2">
              <el-tag>已执行</el-tag>
            </div>
            <div v-else>
              <el-tag>未知</el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column fixed="right" label="操作">
          <template slot-scope="scope">
            <el-button @click="runTask(scope.row)" type="text" size="small"
              >执行</el-button
            >
            <el-button type="text" size="small" @click="editTask(scope.row)"
              >编辑</el-button
            >
            <el-button type="text" size="small" @click="deleteTask(scope.row)"
              >删除</el-button
            >
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        background
        :page-size="6"
        @current-change="handleCurrentTaskChange"
        :total="tasktotal"
        style="margin: 10px"
      >
      </el-pagination>
    </div>
    <div>
      <!-- 引入子组件 -->
      <taskDialog
        v-if="show"
        @cancel="closeDialog"
        :title="dialogTitle"
        :pid="projectForm.id"
        @fresh="initTaskList"
        :tid="taskId"
      ></taskDialog>
    </div>
  </div>
</template>

<script>
import ProjectApi from "../../requests/project.js";
import taskDialog from "@/components/task/taskDialog";
import taskApi from "../../requests/task.js";

export default {
  components: {
    taskDialog,
  },
  data() {
    return {
      projectForm: {
        id: 1,
      },
      taskId: "",
      options: [],
      req: {
        page: 1,
        size: 6,
      },
      tasklistreq: {
        project_id: 1,
        page: 1,
        size: 6,
      },
      projecttotal: 0,
      tasktotal: 0,
      show: false,
      currentPorjectId: 0,
      taskData: [],
      taskHeartbeat: null,
    };
  },
  created() {
    this.initProjectList();
    this.taskHeartbeat = setInterval(() => {
      this.initTaskList();
    }, 5000);
    // this.taskHeartbeat = setInterval(this.initTaskList(), 5000);
  },
  destroyed() {
    clearInterval(this.taskHeartbeat);
  },
  methods: {
    //初始化获取项目列表
    async initProjectList() {
      console.log("获取项目列表");
      const resp = await ProjectApi.getproject(this.req);
      console.log(resp);
      if (resp.success === true) {
        this.projectvalue = resp.items[0].id;
        this.projectlabel = resp.items[0].name;
        this.projecttotal = resp.total;
        for (let i = 0; i < resp.items.length; i++) {
          this.options.push({
            value: resp.items[i].id,
            label: resp.items[i].name,
          });
        }
        this.initTaskList();
        // this.$message.success("查询成功");
      } else {
        this.$message.error("查询失败!");
      }
    },
    // 项目跳到第几页
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`);
      this.req.page = val;
      this.options = [];
      this.initProjectList();
    },
    // 任务跳到第几页
    handleCurrentTaskChange(val) {
      console.log(`当前页: ${val}`);
      this.tasklistreq.page = val;
      this.initTaskList();
    },
    //展示和关闭弹窗
    showtask() {
      this.dialogTitle = "create";
      this.show = true;
    },
    closeDialog() {
      this.show = false;
    },
    //编辑任务
    editTask(row) {
      this.dialogTitle = "edite";
      this.taskId = row.id;
      this.show = true;
    },
    //切换项目
    changeproject(value) {
      console.log("当前项目id", value);
      this.tasklistreq.project_id = value;
      this.initTaskList();
      console.log("当前项目名称", this.projectlabel);
    },

    //初始化获取任务列表
    async initTaskList() {
      console.log("获取任务列表");
      console.log(this.projectForm.id);
      const resp = await taskApi.getTaskList(this.tasklistreq);
      if (resp.success === true) {
        this.taskData = resp.items;
        this.tasktotal = resp.total;
        // this.$message.success("查询成功");
      } else {
        this.$message.error("查询失败!");
      }
    },
    //删除任务
    async deleteTask(row) {
      console.log(row);
      const resp = await taskApi.deleteTask(row.id);
      if (resp.success === true) {
        this.initTaskList();
        this.$message.success("删除成功");
      } else {
        this.$message.error("删除失败!");
      }
    },
    //执行任务
    async runTask(row) {
      console.log(row.id);
      const resp = await taskApi.runningTask(row.id);
      if (resp.success === true) {
        this.initTaskList();
        this.$message.success("开始成功");
      } else {
        this.$message.error("执行失败!");
      }
    },
  },
};
</script>
