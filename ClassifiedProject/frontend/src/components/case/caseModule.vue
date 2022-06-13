<template>
  <div class="caseModeule" style="height: 100%">
    <!-- 选择项目，创建用例按钮 -->
    <div style="margin-bottom: 10px; text-align: left; width: 100%">
      <span>
        <b>项目：</b>
      </span>
      <span>
        <el-select
          v-model="methodOptions"
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
            :total="total"
            style="margin: 10px"
          >
          </el-pagination>
        </el-select>
      </span>
      <span>
        <el-button @click="CreateCase" type="primary" style="margin-left: 16px">
          创建
        </el-button>
      </span>
    </div>
    <!-- 添加删除节点 -->
    <div style="width: 20%; float: left">
      <el-card>
        <el-button
          type="text"
          class="el-icon-circle-plus-outline"
          @click="createRootModule"
          >根节点</el-button
        >
        <el-tree
          :data="ModuleData"
          show-checkbox
          node-key="id"
          default-expand-all
          :expand-on-click-node="false"
          @node-click="NodeClick"
        >
          <span class="custom-tree-node" slot-scope="{ node, data }">
            <span>{{ node.label }}</span>
            <span>
              <el-button type="text" size="mini" @click="append(data)">
                <i class="el-icon-circle-plus-outline"></i>
              </el-button>
              <el-button type="text" size="mini" @click="remove(node, data)">
                <i class="el-icon-delete"></i>
              </el-button>
            </span>
          </span>
        </el-tree>
      </el-card>
    </div>
    <!-- 查看用例表格 -->
    <div style="width: 77%; height: 100%; float: right">
      <el-table :data="caseData" style="width: 90%" border>
        <el-table-column prop="id" label="ID" width="50"> </el-table-column>
        <el-table-column prop="name" label="姓名" width="180">
        </el-table-column>
        <el-table-column prop="method" label="请求方法" width="80">
        </el-table-column>
        <el-table-column prop="url" label="URL" width="180"> </el-table-column>
        <el-table-column prop="create_time" label="创建时间"> </el-table-column>
        <el-table-column fixed="right" label="操作" width="100">
          <template slot-scope="scope">
            <el-button @click="caseRowclick(scope.row)" type="text" size="small"
              >查看</el-button
            >
            <el-button type="text" size="small" @click="deleteCase(scope.row)"
              >删除</el-button
            >
          </template>
        </el-table-column>
      </el-table>
      <div>
        <el-pagination
          background
          :page-size="6"
          @current-change="handleCurrentcaseChange"
          :total="casetotal"
          style="margin-top: 10px"
        >
        </el-pagination>
      </div>
    </div>
    <!-- 引入创建模块弹窗 -->
    <div>
      <moduleDialog
        v-if="show"
        @cancel="closeDialog"
        :rootID="rootFlag"
        :pid="projectvalue"
        :plabel="projectlabel"
        :parid="parent_id"
        :parname="parentname"
        :moduleid="moduleid"
      ></moduleDialog>
    </div>
    <!-- 引入创建用例弹窗 -->
    <div>
      <el-drawer
        :title="CaseTitle"
        :visible.sync="drawer"
        :direction="direction"
        size="50%"
      >
        <caseDialog
          v-if="drawer"
          :caseFlag="caseFlag"
          :caseid="caseid"
          :currentModule="currentModule"
          @cancel="closecasedialog"
          @fresh="initCaseList(currentModule)"
        ></caseDialog>
      </el-drawer>
    </div>
  </div>
</template>

<script>
import ProjectApi from "../../requests/project.js";
import ModuleApi from "../../requests/module.js";
import moduleDialog from "@/components/case/moduleDialog";
import CaseApi from "../../requests/case.js";
import caseDialog from "@/components/case/caseDialog";

// let id = 1000;

export default {
  components: {
    moduleDialog,
    caseDialog,
  },
  data() {
    const ModuleData = [];
    return {
      options: [],
      show: false,
      rootFlag: 1,
      ModuleData: JSON.parse(JSON.stringify(ModuleData)),
      projectvalue: 1,
      projectlabel: "",
      req: {
        page: 1,
        size: 6,
      },
      total: 0,
      casetotal: 0,
      parent_id: 1,
      parentname: "",
      moduleid: 1,
      caseData: [],
      drawer: false,
      direction: "ltr",
      CaseTitle: "",
      methodOptions: [
        {
          value: "get",
          label: "GET",
        },
        {
          value: "post",
          label: "POST",
        },
      ],
      caseFlag: 1,
      caseid: 1,
      currentModule: 0,
    };
  },
  mounted() {
    console.log("打印");
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
    // 用例跳到第几页
    handleCurrentcaseChange(val) {
      console.log(`当前页: ${val}`);
      this.req.page = val;
      this.initCaseList(this.moduleid);
    },
    // 项目跳到第几页
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`);
      this.req.page = val;
      this.options = [];
      this.initProjectList();
    },
    //切换项目
    changeproject(value) {
      this.initModuleList(value);
      this.projectvalue = value;
      console.log("当前项目id", this.projectvalue);
      this.projectlabel = this.options.find(
        (item) => item.value === value
      ).label;
      console.log("当前项目名称", this.projectlabel);
    },
    //获取模块树
    async initModuleList(pid) {
      const req = { project_id: pid };
      const resp = await ModuleApi.getmodulelist(req);
      if (resp.success === true) {
        this.ModuleData = resp.result;
        // this.$message.success("查询成功");
      } else {
        this.$message.error("查询失败!");
      }
    },
    // 添加模块节点data
    append(data) {
      console.log("创建子节点", data);
      this.createChildernModule();
      this.moduleid = data.id;
      this.parent_id = data.id;
      this.parentname = data.label;
    },
    // 删除模块节点node, data
    remove(node, data) {
      console.log("删除节点", node, data);
      this.moduleid = data.id;
      this.rootFlag = 3;
      this.show = true;
    },
    //关闭弹窗
    closeDialog() {
      this.show = false;
      this.initModuleList(this.projectvalue);
    },
    //创建根节点
    createRootModule() {
      this.show = true;
      this.rootFlag = 1;
    },
    //创建子节点
    createChildernModule() {
      this.show = true;
      this.rootFlag = 2;
    },
    // 点击模块节点
    NodeClick(data) {
      console.log("点击节点", data);
      this.currentModule = data.id;
      this.initCaseList(data.id);
    },
    //获取用例树
    async initCaseList(mid) {
      const resp = await ModuleApi.getcaselist(mid, this.req);
      if (resp.success === true) {
        this.caseData = resp.items;
        this.casetotal = resp.total;
        this.$message.success("查询成功");
      } else {
        this.$message.error("查询失败!");
      }
    },
    //创建用例弹窗
    CreateCase() {
      this.drawer = true;
      this.CaseTitle = "创建用例";
      this.caseFlag = 1;
    },
    //编辑查看用例弹窗
    caseRowclick(row) {
      console.log("点击用例节点", row);
      this.drawer = true;
      this.caseFlag = 2;
      this.CaseTitle = "查看用例";
      this.caseid = row.id;
      // console.log("点击用例节点", data);
    },
    //关闭用例弹窗
    closecasedialog() {
      console.log("关闭用例弹窗");
      this.drawer = false;
    },
    //删除用例
    async deleteCase(row) {
      this.caseid = row.id;
      const resp = await CaseApi.deleteCase(this.caseid);
      if (resp.success === true) {
        this.initCaseList(this.moduleid);
        this.$message.success("删除成功");
      } else {
        this.$message.error("删除失败!");
      }
    },
  },
};
</script>
