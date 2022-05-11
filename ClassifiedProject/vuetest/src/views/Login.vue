<template>
  <div class="home">
    <h1>这是一个登录页面</h1>
    <el-card class="box-card" style="margin: auto">
      <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
        <el-tab-pane label="登录" name="first">
          <el-form
            :model="loginForm"
            :rules="rules"
            ref="loginForm"
            label-position="left"
            label-width="100px"
            class="demo-loginForm"
          >
            <el-form-item label="用户名" prop="username">
              <el-input v-model="loginForm.username"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input v-model="loginForm.password" type="password"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button
                type="primary"
                style="width: 350px"
                @click="submitLogin('loginForm')"
                >登录</el-button
              >
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="注册" name="second">
          <el-form
            :model="registerForm"
            :rules="rules"
            ref="registerForm"
            label-width="100px"
            class="demo-registerForm"
            label-position="left"
          >
            <el-form-item label="用户名" prop="username">
              <el-input v-model="registerForm.username"></el-input>
            </el-form-item>
            <el-form-item label="设置密码" prop="password">
              <el-input
                v-model="registerForm.password"
                type="password"
              ></el-input>
            </el-form-item>
            <el-form-item label="确认密码" prop="confirm_password">
              <el-input
                v-model="registerForm.confirm_password"
                type="password"
              ></el-input>
            </el-form-item>
            <el-form-item size="large">
              <el-button
                type="primary"
                @click="submitRegister('registerForm')"
                style="width: 350px"
                >创建</el-button
              >
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from "@/components/HelloWorld.vue";

import UserApi from "../requests/user.js";

export default {
  data() {
    return {
      activeName: "first",
      loginForm: {
        username: "",
        password: "",
      },
      registerForm: {
        username: "",
        password: "",
        confirm_password: "",
      },
      rules: {
        username: [
          { required: true, message: "请输入用户名", trigger: "blur" },
        ],
        password: [{ required: true, message: "请输入密码", trigger: "blur" }],
        confirm_password: [
          { required: true, message: "请输入确认密码", trigger: "blur" },
        ],
      },
    };
  },
  methods: {
    handleClick(tab, event) {
      console.log(tab, event);
    },
    // 用户登录
    submitLogin(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          // alert("submit!");
          UserApi.login(this.loginForm).then((resp) => {
            if (resp.success === true) {
              sessionStorage.session = resp.result.session;
              sessionStorage.user = resp.result.username;
              this.$router.push({ path: "/main" });
              this.$message.success("登录成功！");
            } else {
              this.$message.error("登录失败！");
            }
          });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    // 用户注册
    submitRegister(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          // alert('submit!');
          UserApi.register(this.registerForm).then((resp) => {
            if (resp.success === true) {
              this.$message.success("注册成功！");
            } else {
              this.$message.error(resp.error.msg);
            }
          });
        } else {
          console.log("错误提交");
          return false;
        }
      });
    },
  },
};
</script>

<style>
.box-card {
  width: 480px;
}
</style>
