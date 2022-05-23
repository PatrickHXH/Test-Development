<template>
  <div>
    <el-dialog
      :title="showTitle"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="closeDialog"
    >
      <el-form
        :model="projectForm"
        :rules="rules"
        ref="projectForm"
        label-width="100px"
        class="demo-ruleForm"
      >
        <el-form-item label="名称" prop="name">
          <el-input v-model="projectForm.name"></el-input>
        </el-form-item>
        <el-form-item label="描述" prop="describe">
          <el-input type="textarea" v-model="projectForm.describe"></el-input>
        </el-form-item>
        <el-form-item label="图片:" prop="desc">
          <div id="image">
            <el-upload
              list-type="picture-card"
              action="#"
              :before-upload="beforeUpload"
              :file-list="fileList"
            >
              <i class="el-icon-plus"></i>
            </el-upload>
          </div>
        </el-form-item>
        <el-form-item>
          <el-button @click="closeDialog">关闭</el-button>
          <el-button type="primary" @click="submitProject('projectForm')"
            >创建</el-button
          >
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import ProjectApi from "../../requests/project.js";

export default {
  props: ["title", "pid"],
  components: {},
  data() {
    return {
      showTitle: "",
      updateURL: "http://127.0.0.1:8000/api/projects/upload/",
      dialogVisible: true,
      projectForm: {
        name: "",
        describe: "",
        image: "xxx.jpg",
      },
      rules: {
        name: [
          { min: 3, max: 5, message: "长度在 3 到 5 个字符", trigger: "blur" },
        ],
        describe: [
          { required: true, message: "请填写项目描述", trigger: "blur" },
        ],
      },
      fileList: [
        {
          name: "food.jpeg",
          url: "http://127.0.0.1:8000/static/images/1abb2dc3d76311944ffdbe9980fbaadd.jpg",
        },
      ],
      imageUrl: "",
    };
  },
  mounted() {
    if (this.title == "create") {
      this.showTitle = "创建项目";
    } else if (this.title == "edite") {
      this.showTitle = "编辑项目";
      this.initProjectList();
    }
  },
  methods: {
    //调用子组件 关闭弹窗ffdd
    closeDialog() {
      console.log("closeDialog");
      this.$emit("cancel", {});
    },
    // 获取项目列表
    async initProjectList() {
      console.log("获取项目列表");
      const resp = await ProjectApi.getoneproject(this.pid);
      console.log(resp);
      if (resp.success === true) {
        this.projectForm = resp.result;
        this.$message.success("项目详情查询成功");
      } else {
        this.$message.error("项目详情查询失败!");
      }
    },
    // 创建和更新项目
    submitProject(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          if (this.title == "create") {
            ProjectApi.createproject(this.projectForm).then((resp) => {
              if (resp.success === true) {
                console.log("创建成功");
                this.closeDialog();
                this.$message.success("创建成功！");
              } else {
                this.$message.error(resp.error.message);
              }
            });
          } else if (this.title == "edite") {
            ProjectApi.updateproject(this.pid, this.projectForm).then(
              (resp) => {
                if (resp.success === true) {
                  this.closeDialog();
                  this.$message.success("编辑成功！");
                } else {
                  this.$message.error(resp.error.message);
                }
              }
            );
            console.log("测试");
          }
        }
      });
    },
    beforeUpload(file) {
      console.log("上传文件对象", file);
      let fd = new FormData();
      fd.append("file", file);

      ProjectApi.updateImage(fd).then((resp) => {
        console.log("resp", resp.data);
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
