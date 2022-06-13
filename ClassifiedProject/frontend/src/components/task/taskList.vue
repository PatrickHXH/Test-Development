<template>
  <div class="task">
    <div style="text-align: left">
      <el-form :inline="true" :model="projectForm" class="demo-form-inline">
        <el-form-item label="项目">
          <el-select v-model="projectForm.id" placeholder="请选择项目">
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
              :total="total"
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
    <div>
      <!-- 引入子组件 -->
      <taskDialog
        v-if="show"
        @cancel="closeDialog"
        :title="dialogTitle"
        :pid="projectForm.id"
      ></taskDialog>
    </div>
  </div>
</template>

<script>
import ProjectApi from "../../requests/project.js";
import taskDialog from "@/components/task/taskDialog";
export default {
  components: {
    taskDialog,
  },
  data() {
    return {
      projectForm: {
        id: "",
      },
      options: [],
      req: {
        page: 1,
        size: 6,
      },
      total: 0,
      show: false,
      currentPorjectId: 0,
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
        this.total = resp.total;
        for (let i = 0; i < resp.items.length; i++) {
          this.options.push({
            value: resp.items[i].id,
            label: resp.items[i].name,
          });
        }
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
    //展示和关闭弹窗
    showtask() {
      this.dialogTitle = "create";
      this.show = true;
    },
    closeDialog() {
      this.show = false;
    },
  },
};
</script>
