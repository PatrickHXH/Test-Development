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
              action="#"
              list-type="picture-card"
              :before-upload="beforeUpload"
              :on-remove="handleRemove"
              :on-preview="handlePreview"
              :file-list="fileList"
            >
              <i class="el-icon-plus"></i>
            </el-upload>
            <el-dialog :visible.sync="imageVisible">
              <img width="100%" :src="imageUrl" alt="" />
            </el-dialog>
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
        image: "",
      },
      rules: {
        name: [{ required: true, message: "请填写项目名称", trigger: "blur" }],
        describe: [
          { required: true, message: "请填写项目描述", trigger: "blur" },
        ],
      },
      fileList: [],
      imageUrl: "",
      imageVisible: false,
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
    //调用子组件 关闭弹窗
    closeDialog() {
      console.log("closeDialog");
      this.$emit("cancel", {});
    },
    // 获取项目详情
    async initProjectList() {
      console.log("获取项目列表");
      const resp = await ProjectApi.getoneproject(this.pid);
      this.fileList.push({
        name: resp.result.name,
        url: "/static/images/" + resp.result.image,
      });
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
    // 上传图片
    beforeUpload(file) {
      console.log("上传文件对象", file);
      let fd = new FormData();
      fd.append("file", file);
      this.fileList = [];
      ProjectApi.updateImage(fd).then((resp) => {
        if (resp.data.success === true) {
          console.log("resp", resp.data);
          this.projectForm.image = resp.data.result.name;
          const imagePath = "/static/images/" + resp.data.result.name;
          this.fileList.push({
            name: file.name,
            url: imagePath,
          });
          console.log("图片路径：", imagePath);
          this.$message.success("上传成功！");
        } else {
          this.$message.success("上传失败！");
        }
      });
    },
    // 预览图片
    handlePreview(file) {
      console.log("上传成功", file);
      this.imageUrl = file.url;
      this.imageVisible = true;
    },
    // 删除图片
    handleRemove(file) {
      console.log("删除", file);
    },
  },
};
</script>

<style>
#image {
  text-align: left;
}
</style>
