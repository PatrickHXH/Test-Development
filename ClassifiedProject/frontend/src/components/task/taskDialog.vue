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
        <el-form-item label="描述">
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
              <el-table-column prop="id" label="ID" style="width: 50%">
              </el-table-column>
              <el-table-column prop="name" label="姓名" style="width: 50%">
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
          <el-button @click="closeDialog"> 关闭</el-button>
          <el-button type="primary" @click="submitTask('taskForm')"
            >创建</el-button
          >
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import ModuleApi from "../../requests/module.js";
import taskApi from "../../requests/task.js";

export default {
  props: ["title", "pid", "tid"],
  components: {},
  data() {
    return {
      showTitle: "",
      dialogVisible: true,
      taskForm: {
        projcet: 0,
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
    this.taskForm.project = this.pid;
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
        if (this.title == "edite") {
          this.initTaskInfo();
        }
        // this.$message.success("查询成功");
      } else {
        this.$message.error("查询失败!");
      }
    },
    //获取任务详情
    async initTaskInfo() {
      const resp = await taskApi.getTaskDetail(this.tid);
      if (resp.success === true) {
        this.taskForm = resp.result;
        this.calculationCase();
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
      // 将用例id取出出来放在列表
      const moduleCases = [];
      for (let i = 0; i < multipleSelection.length; i++) {
        moduleCases.push(multipleSelection[i].id);
      }
      console.log("选择用例", moduleCases);

      //默认该模块没有选择过用例
      var selective = false;
      for (let i = 0; i < this.taskForm.cases.length; i++) {
        // 如果用例列表的模块id等于当前点击的模块，意味着该模块有选择过用例
        if (this.taskForm.cases[i].moduleId == this.currentModule) {
          selective = true;
          // 将现在的选择，重新赋值给用例列表，即casesId
          this.taskForm.cases[i].casesId = moduleCases;
        }
      }
      //没有选择过用例时,moduleId赋值当前选择的模块id，casesId赋值选择的用例列表
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
      // 获取用例列表
      const resp = await ModuleApi.getcaselist(mid, this.req);
      if (resp.success == true) {
        this.caseData = resp.items;
        this.casetotal = resp.total;
        // this.$message.success("查询成功！")
        // 已经选中的用例
        this.$nextTick(() => {
          var casesId = [];
          for (let i = 0; i < this.taskForm.cases.length; i++) {
            //判断当前模块是否有选中的用例
            if (this.taskForm.cases[i].moduleId == mid) {
              console.log("aa", this.taskForm.cases[i].casesId);
              //将当前模块选中的用例列表赋值给caseId
              casesId = this.taskForm.cases[i].casesId;
            }
          }
          console.log("被选中的用例：", casesId);
          let rows = [];
          //被选中用例的个数 ;例子caseId = [1,2,3]
          for (let i = 0; i < casesId.length; i++) {
            console.log("被选中用例的个数：", casesId.length);
            //循环该模块的用例列表数量
            for (let j = 0; j < this.caseData.length; j++) {
              //判断返回的用例id是否等于选中
              if (casesId[i] == this.caseData[j].id) {
                //将选中的用例对象放在rows列表里
                rows.push(this.caseData[j]);
              }
            }
          }
          console.log("该模块下选中的用例对象列表：", rows);
          //遍历用例对象,使用方法objs.forEach((boj) =>{})
          rows.forEach((row) => {
            //输出选中用例对象
            console.log("row", row);
            //选中用例
            this.$refs.multipleTable.toggleRowSelection(row);
          });
        });
      } else {
        this.$message.error(resp.error.message);
      }
    },

    // 创建和更新任务
    submitTask(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          if (this.title == "create") {
            taskApi.createTask(this.taskForm).then((resp) => {
              if (resp.success === true) {
                console.log("创建成功");
                this.closeDialog();
                this.$emit("fresh", {});
                this.$message.success("创建成功！");
              } else {
                this.$message.error(resp.error.message);
              }
            });
          } else if (this.title == "edite") {
            taskApi.updateTask(this.tid, this.taskForm).then((resp) => {
              if (resp.success === true) {
                this.closeDialog();
                this.$emit("fresh", {});
                this.$message.success("更新成功");
              } else {
                this.$message.error(resp.error.message);
              }
            });
            console.log("测试");
          }
        }
      });
    },
  },
};
</script>

<style>
#image {
  text-align: left;
}
</style>
