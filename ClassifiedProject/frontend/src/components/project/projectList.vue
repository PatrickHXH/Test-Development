<template>
  <div class="project">
    <!-- 创建按钮 -->
    <div style="height: 50px; width: 100%; text-align: left">
      <el-button type="primary" @click="showDialog" cy-data="ProjectCreate"
        >创建</el-button
      >
    </div>
    <!-- 项目列表 -->
    <div style="height: 700px">
      <div v-for="(item, index) in projectData" :key="index">
        <el-col
          :span="7"
          class="project-card"
          style="width: 29%; height: 280px; margin: 20px"
        >
          <el-card>
            <div slot="header" class="clearfix">
              <span>{{ item.name }}</span>
              <el-dropdown :hide-on-click="false" style="float: right">
                <span class="el-dropdown-link">
                  <i class="el-icon-setting" cy-data="ProjectSetting"></i>
                </span>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item>
                    <el-button
                      type="text"
                      @click="showEdit(item.id)"
                      cy-data="ProjectEdit"
                      >编辑</el-button
                    >
                  </el-dropdown-item>
                  <el-dropdown-item>
                    <el-button
                      type="text"
                      @click="deleteProject(item.id)"
                      cy-data="ProjectDelete"
                      >删除</el-button
                    >
                  </el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </div>
            {{ item.address }}
            <img
              style="width: 200px; height: 200px"
              :src="item.image"
              class="image"
            />
          </el-card>
        </el-col>
      </div>
    </div>
    <!-- 分页组件 -->
    <div style="float: center; margin: 20px 0; height: 50px">
      <el-pagination
        background
        :page-size="6"
        @current-change="handleCurrentChange"
        :total="total"
        style="margin: 10px"
        cy-data="ProjectPagination"
      >
      </el-pagination>
    </div>
    <div>
      <!-- 引入子组件 -->
      <projectDialog
        v-if="show"
        @cancel="closeDialog"
        :title="dialogTitle"
        :pid="currentPorjectId"
      ></projectDialog>
    </div>
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
      total: 0,
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
      // var header = { Authorization: "bearer" + " " + sessionStorage.session };
      var resp = await ProjectApi.getproject(this.req);
      console.log(resp);
      // resp = resp.data;
      if (resp.success === true) {
        // 处理图片路径
        for (let i = 0; i < resp.items.length; i++) {
          resp.items[i].image = "/static/images/" + resp.items[i].image;
        }
        this.projectData = resp.items;
        this.total = resp.total;
        // this.$message.success("查询成功");
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
    //展示和关闭弹窗
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
    //删除项目
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
