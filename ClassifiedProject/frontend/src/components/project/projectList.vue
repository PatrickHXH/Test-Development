<template>
  <div class="home">
    <el-card class="box-card" style="width: 100%">
      <div style="height: 50px; width: 100%; text-align: left">
        <el-button type="primary" @click="showDialog">创建</el-button>
      </div>
      <div v-for="(item, index) in projectData" :key="index" class="text item">
        <el-col :span="7" class="project-card" style="width: 29%; margin: 2%">
          <el-card>
            <div slot="header" class="clearfix">
              <span>{{ item.name }}</span>
              <el-dropdown :hide-on-click="false" style="float: right">
                <span class="el-dropdown-link">
                  <i class="el-icon-setting"></i>
                </span>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item>
                    <el-button type="text" @click="showEdit(item.id)"
                      >编辑</el-button
                    >
                  </el-dropdown-item>
                  <el-dropdown-item>
                    <el-button type="text" @click="deleteProject(item.id)"
                      >删除</el-button
                    >
                  </el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </div>
            {{ item.address }}
            <img
              style="width: 100%"
              src="https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png"
              class="image"
            />
          </el-card>
        </el-col>
      </div>
    </el-card>
    <el-pagination
      background
      :page-size="6"
      @current-change="handleCurrentChange"
      :total="total"
      style="margin: 10px"
    >
    </el-pagination>

    <!-- 引入子组件 -->
    <projectDialog
      v-if="show"
      @cancel="closeDialog"
      :title="dialogTitle"
      :pid="currentPorjectId"
    ></projectDialog>
  </div>
</template>

<script>
import ProjectApi from "../../requests/project.js";
import projectDialog from "@/components/project/projectDialog";
export default {
  components: {
    projectDialog,
  },
  data() {
    return {
      dialogTitle: "create",
      show: false,
      currentPorjectId: "",
      projectData: [],
      req: {
        page: 1,
        size: 6,
      },
      total: "",
    };
  },
  created() {
    console.log("打印");
    this.initProjectList();
  },
  methods: {
    //获取项目列表
    async initProjectList() {
      console.log("获取项目列表");
      const resp = await ProjectApi.getproject(this.req);
      console.log(resp);
      if (resp.success === true) {
        this.projectData = resp.items;
        this.total = resp.total;
        this.$message.success("查询成功");
      } else {
        this.$message.error("查询失败!");
      }
    },
    // 跳到第几页
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`);
      this.req.page = val;
      this.initProjectList();
    },
    //展示关闭弹窗
    showDialog() {
      this.dialogTitle = "create";
      this.show = true;
    },
    closeDialog() {
      this.show = false;
      this.initProjectList();
    },
    //点击编辑，展示创建弹窗，标题替换为编辑
    showEdit(id) {
      this.currentPorjectId = id;
      this.dialogTitle = "edite";
      this.show = true;
    },
    //获取项目列表
    async deleteProject(id) {
      console.log("删除项目");
      const resp = await ProjectApi.deleteproject(id);
      if (resp.success === true) {
        this.initProjectList();
        this.$message.success("删除成功");
      } else {
        this.$message.error("删除失败!");
      }
    },
  },
};
</script>
