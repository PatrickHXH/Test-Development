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
      </el-form>
    </div>
    <!-- 任务列表 -->
    <div>
      <el-table :data="reportData" border style="width: 100%">
        <el-table-column fixed prop="id" label="ID" width="80">
        </el-table-column>
        <el-table-column prop="name" label="姓名"> </el-table-column>
        <el-table-column prop="tests" label="总数"> </el-table-column>
        <el-table-column prop="passed" label="通过">
          <template slot-scope="scope">
            <el-tag type="success">{{ scope.row.passed }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="error" label="错误">
          <template slot-scope="scope">
            <el-tag type="danger">{{ scope.row.error }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="failure" label="失败">
          <template slot-scope="scope">
            <el-tag type="warning">{{ scope.row.failure }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="skipped" label="跳过">
          <template slot-scope="scope">
            <el-tag type="info">{{ scope.row.skipped }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="run_time" label="时长"> </el-table-column>
        <el-table-column prop="create_time" label="创建时间"> </el-table-column>
        <el-table-column fixed="right" label="操作">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="shReport(scope.row)"
              >查看</el-button
            >
            <el-button type="text" size="small" @click="deleteReport(scope.row)"
              >删除</el-button
            >
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        background
        :page-size="6"
        @current-change="handleCurrentTaskChange"
        :total="reporttal"
        style="margin: 10px"
      >
      </el-pagination>
    </div>
    <div>
      <!-- 引入子组件 -->
      <reportDialog
        v-if="show"
        @cancel="closeDialog"
        :rid="reportId"
      ></reportDialog>
    </div>
  </div>
</template>

<script>
import ProjectApi from "../../requests/project.js";
import reportDialog from "@/components/report/reportDialog";
import ReportApi from "../../requests/report.js";

export default {
  components: {
    reportDialog,
  },
  data() {
    return {
      projectForm: {
        id: 1,
      },
      reportId: "",
      options: [],
      req: {
        page: 1,
        size: 6,
      },
      reportlistreq: {
        project_id: 1,
        page: 1,
        size: 6,
      },
      projecttotal: 0,
      reporttal: 0,
      show: false,
      currentPorjectId: 0,
      reportData: [],
      taskHeartbeat: null,
    };
  },
  created() {
    this.initProjectList();
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
        this.initReportList();
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
      this.reportlistreq.page = val;
      this.initReportList();
    },
    //展示和关闭弹窗
    showReport() {
      this.dialogTitle = "create";
      this.show = true;
    },
    closeDialog() {
      this.show = false;
    },
    //查看报告
    shReport(row) {
      this.reportId = row.id;
      this.show = true;
    },
    //切换项目
    changeproject(value) {
      console.log("当前项目id", value);
      this.reportlistreq.project_id = value;
      this.initReportList();
      console.log("当前项目名称", this.projectlabel);
    },

    //初始化获取任务列表
    async initReportList() {
      console.log("获取任务列表");
      console.log(this.projectForm.id);
      const resp = await ReportApi.getReportList(this.reportlistreq);
      if (resp.success === true) {
        this.reportData = resp.items;
        this.reporttal = resp.total;
        // this.$message.success("查询成功");
      } else {
        this.$message.error("查询失败!");
      }
    },
    //删除任务
    async deleteReport(row) {
      const resp = await ReportApi.deleteReport(row.id);
      if (resp.success === true) {
        this.initReportList();
        this.$message.success("删除成功");
      } else {
        this.$message.error("删除失败!");
      }
    },
  },
};
</script>
