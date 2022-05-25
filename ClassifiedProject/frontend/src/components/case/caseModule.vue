<template>
  <div class="caseModeule" style="height: 100%; float: left">
    <div style="margin-bottom: 10px">
      <span>
        <b>项目：</b>
      </span>
      <span>
        <el-select
          v-model="projectvalue"
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
    </div>
    <div>
      <el-card style="width: 100%">
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
    <div>
      <!-- 引入子组件 -->
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
  </div>
</template>

<script>
import ProjectApi from "../../requests/project.js";
import ModuleApi from "../../requests/module.js";
import moduleDialog from "@/components/case/moduleDialog";
// let id = 1000;

export default {
  components: {
    moduleDialog,
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
      total: "",
      parent_id: 1,
      parentname: "",
      moduleid: 1,
    };
  },
  mounted() {
    console.log("打印");
    this.initProjectList();
    this.initModuleList(1);
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
    // 跳到第几页
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
  },
};
</script>
