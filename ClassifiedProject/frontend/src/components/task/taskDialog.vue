<template>
  <div>
    <el-dialog
      :title="showTitle"
      :visible.sync="dialogVisible"
      width="70%"
      :before-close="closeDialog"
    >
      <el-form
        :model="taskForm"
        :rules="rules"
        ref="taskForm"
        label-width="100px"
        class="demo-ruleForm"
      >
        <el-form-item label="名称" prop="name">
          <el-input v-model="taskForm.name"></el-input>
        </el-form-item>
        <el-form-item label="描述" prop="describe">
          <el-input type="textarea" v-model="taskForm.describe"></el-input>
        </el-form-item>
        <el-form-item>
          <!-- 查看模块树 -->
          <div style="width: 20%; float: left">
            <el-card>
              <el-tree
                :data="ModuleData"
                node-key="id"
                default-expand-all
                :expand-on-click-node="false"
                @node-click="NodeClick"
              >
                <!-- <span class="custom-tree-node" slot-scope="{ node, data }">
            <span>{{ node.label }}</span>
            </span> -->
              </el-tree>
            </el-card>
          </div>
          <!-- 查看用例表格 -->
          <div style="width: 77%; height: 100%; float: right">
            <el-table
              ref="multipleTable"
              :data="caseData"
              style="width: 100%"
              border
              @select="selectionOneCase"
              @select-all="selectionAllCases"
            >
              <el-table-column type="selection" width="55"> </el-table-column>
              <el-table-column prop="id" label="ID" width="50">
              </el-table-column>
              <el-table-column prop="name" label="姓名" width="180">
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
        </el-form-item>
        <el-form-item>
          已选择【{{ this.caseNum }}】条用例
          <el-button @click="closeDialog">关闭</el-button>
          <el-button type="primary" @click="submitProject('taskForm')"
            >创建</el-button
          >
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import ModuleApi from "../../requests/module.js";

export default {
  props: ["title", "pid"],
  components: {},
  data() {
    return {
      showTitle: "",
      dialogVisible: true,
      taskForm: {
        name: "",
        describe: "",
        cases: [],
      },
      req: {
        page: 1,
        size: 6,
      },
      rules: {
        name: [{ required: true, message: "请填写项目名称", trigger: "blur" }],
        describe: [
          { required: true, message: "请填写项目描述", trigger: "blur" },
        ],
      },
      ModuleData: [],
      caseData: [],
      currentModule: 0,
      casetotal: 0,
      caseNum: 0,
    };
  },
  mounted() {
    if (this.title == "create") {
      this.showTitle = "创建任务";
    } else if (this.title == "edite") {
      this.showTitle = "编辑任务";
    }
    this.initModuleList();
  },
  methods: {
    //调用子组件 关闭弹窗
    closeDialog() {
      console.log("closeDialog");
      this.$emit("cancel", {});
    },
    //获取模块树
    async initModuleList() {
      const req = { project_id: this.pid };
      const resp = await ModuleApi.getmodulelist(req);
      if (resp.success === true) {
        this.ModuleData = resp.result;
        // this.$message.success("查询成功");
      } else {
        this.$message.error("查询失败!");
      }
    },
    // 点击模块节点
    NodeClick(data) {
      console.log("点击节点", data);
      this.currentModule = data.id;
      //   this.initCaseList(data.id);
      this.req.page = 1; 
      this.getModuleCaseList(data.id);
    },
    //获取用例树
    // async initCaseList(mid) {
    //   const resp = await ModuleApi.getcaselist(mid, this.req);
    //   if (resp.success === true) {
    //     this.caseData = resp.items;
    //     this.casetotal = resp.total;
    //     this.$message.success("查询成功");
    //   } else {
    //     this.$message.error("查询失败!");
    //   }
    // },
    // 用例跳到第几页
    handleCurrentcaseChange(val) {
      console.log(`当前页: ${val}`);
      this.req.page = val;
      this.getModuleCaseList(this.currentModule);
    },
    // 选择所有用例
    selectionAllCases(val) {
      console.log("选择所有用例", val);
      this.selectiveCase(val);
    },
    // 选择一条用例
    selectionOneCase(val, row) {
      console.log("selection-one-change", val);
      console.log("selection-one-change", row);
      this.selectiveCase(val);
    },
    // 公共方法：选择用例
    selectiveCase(multipleSelection) {
      const moduleCases = [];
      for (let i = 0; i < multipleSelection.length; i++) {
        moduleCases.push(multipleSelection[i].id);
      }
      console.log("选择用例", moduleCases);

      var selective = false;
      for (let i = 0; i < this.taskForm.cases.length; i++) {
        if (this.taskForm.cases[i].moduleId == this.currentModule) {
          selective = true;
          this.taskForm.cases[i].casesId = moduleCases;
        }
      }
      if (selective == false) {
        this.taskForm.cases.push({
          moduleId: this.currentModule,
          casesId: moduleCases,
        });
      }
      console.log("该模块有无选择过用例：", selective);
      console.log("this.taskForm.cases", this.taskForm.cases);
      this.calculationCase();
    },
    // 公共方法：计算用例数量
    calculationCase() {
      this.caseNum = 0;
      for (let i = 0; i < this.taskForm.cases.length; i++) {
        this.caseNum += this.taskForm.cases[i].casesId.length;
      }
    },

    // 初始化用例数据
    async getModuleCaseList(mid) {
      const resp = await ModuleApi.getcaselist(mid, this.req);
      if (resp.success == true) {
        this.caseData = resp.items;
        this.casetotal = resp.total;
        // this.$message.success("查询成功！")
        // 已经选中的用例
        this.$nextTick(() => {
          var casesId = [];
          for (let i = 0; i < this.taskForm.cases.length; i++) {
            if (this.taskForm.cases[i].moduleId == mid) {
              console.log("aa", this.taskForm.cases[i].casesId);
              casesId = this.taskForm.cases[i].casesId;
            }
          }
          let rows = [];
          for (let i = 0; i < casesId.length; i++) {
            for (let j = 0; j < this.caseData.length; j++) {
              if (casesId[i] == this.caseData[j].id) {
                rows.push(this.caseData[j]);
              }
            }
          }
          rows.forEach((row) => {
            this.$refs.multipleTable.toggleRowSelection(row);
          });
        });
      } else {
        this.$message.error(resp.error.message);
      }
    },
  },
};
</script>

<style>
#image {
  text-align: left;
}
</style>
