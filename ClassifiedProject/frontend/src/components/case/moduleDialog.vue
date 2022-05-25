<template>
  <div>
    <el-dialog
      :title="showTitle"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="closeDialog"
    >
      <el-form
        :model="moduleForm"
        :rules="rules"
        ref="moduleForm"
        label-width="100px"
        class="demo-ruleForm"
      >
        <el-form-item label="项目" prop="name">
          <el-input :value="plabel" disabled></el-input>
        </el-form-item>
        <el-form-item label="根节点" prop="name" v-if="showrootname">
          <el-input :value="parname" disabled></el-input>
        </el-form-item>
        <el-form-item label="名称" prop="name">
          <el-input v-model="moduleForm.name"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button @click="closeDialog">关闭</el-button>
          <el-button type="primary" @click="submitModule('moduleForm')"
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
  props: ["rootID", "pid", "plabel", "parid", "parname"],
  components: {},
  data() {
    return {
      showTitle: "",
      showrootname: false,
      dialogVisible: true,
      moduleForm: {
        name: "",
        project_id: "",
        parent_id: 0,
      },
      rules: {
        name: [{ required: true, message: "请填写模块名称", trigger: "blur" }],
      },
    };
  },
  mounted() {
    this.moduleForm.project_id = this.pid;
    if (this.rootID == 1) {
      this.showTitle = "创建根节点";
    } else if (this.rootID == 2) {
      this.showTitle = "创建子节点";
      this.showrootname = true;
    }
  },
  methods: {
    //调用子组件 关闭弹窗
    closeDialog() {
      console.log("closeDialog");
      this.$emit("cancel", {});
    },
    // 创建模块
    submitModule(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          if (this.rootID == 1) {
            ModuleApi.createmodule(this.moduleForm).then((resp) => {
              if (resp.success === true) {
                console.log("创建成功");
                this.closeDialog();
                this.$message.success("创建成功！");
              } else {
                this.$message.error(resp.error.message);
              }
            });
          } else if (this.rootID == 2) {
            this.moduleForm.parent_id = this.parid;
            ModuleApi.createmodule(this.moduleForm).then((resp) => {
              if (resp.success === true) {
                console.log("创建成功");
                this.closeDialog();
                this.$message.success("创建成功！");
              } else {
                this.$message.error(resp.error.message);
              }
            });
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
