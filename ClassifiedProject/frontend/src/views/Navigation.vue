<template>
  <div calss="navigation" style="height: 100%">
    <el-container style="height: 100%; border: 0px solid #eee">
      <el-aside width="200px" style="background-color: #343a40">
        <img
          class="logo"
          alt="itest logo"
          style="margin-top: 20px"
          src="../assets/logo.svg"
        />
        <el-menu
          default-active="onRoutes"
          background-color="#343a40"
          text-color="#fff"
          active-text-color="#ffd04b"
        >
          <router-link to="/main/project">
            <el-menu-item index="1" class="menu-option">
              <i class="el-icon-s-home"></i>
              <template #title> 项目管理</template>
            </el-menu-item>
          </router-link>
          <router-link to="/main/about">
            <el-menu-item index="1" class="menu-option">
              <i class="el-icon-s-home"></i>
              <template #title> 测试平台</template>
            </el-menu-item>
          </router-link>
        </el-menu>
      </el-aside>

      <el-container>
        <el-header style="text-align: right; font-size: 12px">
          <el-dropdown>
            <i class="el-icon-setting" style="margin-right: 15px"></i>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item>查看</el-dropdown-item>
              <el-dropdown-item>新增</el-dropdown-item>
              <el-dropdown-item>删除</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
          <span>欢迎,{{ user }}</span>
        </el-header>

        <el-main>
          <!-- <h1>渲染home</h1> -->
          <router-view> </router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<style>
.el-header {
  background-color: #b3c0d1;
  color: #333;
  line-height: 60px;
}

.el-aside {
  color: #333;
}
</style>

<script>
export default {
  data() {
    return {
      user: "",
    };
  },
  created() {
    this.user = sessionStorage.getItem("user");
  },
};
</script>
