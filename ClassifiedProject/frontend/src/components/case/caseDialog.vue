<template>
  <div>
    <!-- 选择请求方法，填写URL,请求发送按钮 -->
    <div style="width: 100%">
      <el-select
        v-model="caseForm.method"
        placeholder="方法"
        style="width: 10%"
      >
        <el-option
          v-for="item in methodOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        >
        </el-option>
      </el-select>
      <el-input
        v-model="caseForm.url"
        placeholder="URL"
        style="width: 75%; margin: 0 10px"
      ></el-input>
      <el-button type="primary" style="width: 10%" @click="sendClick"
        >发送</el-button
      >
    </div>
    <!-- 选择请求参数类型 -->
    <div style="margin: 10px 0">
      <el-radio v-model="caseForm.params_type" label="params">Params</el-radio>
      <el-radio v-model="caseForm.params_type" label="form">Form-data</el-radio>
      <el-radio v-model="caseForm.params_type" label="json">JSON</el-radio>
    </div>
    <!-- 切换标签填写请求头和请求参数 -->
    <div style="margin: 0 10px">
      <el-tabs v-model="activeName" :stretch="true">
        <el-tab-pane label="Headers" name="first">
          <vueJsonEditor
            v-model="caseForm.header"
            :mode="'code'"
            @json-change="onJsonChange"
            style="text-align: left"
          ></vueJsonEditor>
        </el-tab-pane>
        <el-tab-pane label="Params/Body" name="second">
          <vueJsonEditor
            v-model="caseForm.params_body"
            :mode="'code'"
            style="text-align: left"
          ></vueJsonEditor>
        </el-tab-pane>
      </el-tabs>
    </div>
    <!-- 返回框 -->
    <div style="margin: 20px 10px">
      <el-input
        v-model="caseForm.response"
        type="textarea"
        :rows="5"
        placeholder="Response"
      >
      </el-input>
    </div>
    <!-- 选择断言类型 -->
    <div style="margin: 0 10px">
      <el-collapse v-model="activeNames">
        <el-collapse-item title="断言" name="1">
          <el-radio class="radio" v-model="caseForm.assert_type" label="include"
            >Include</el-radio
          >
          <el-radio class="radio" v-model="caseForm.assert_type" label="equal"
            >Equal</el-radio
          >
          <el-button
            type="success"
            style="margin: 10px 10px; float: right"
            @click="assertCase"
            >断言</el-button
          >
          <el-input
            v-model="caseForm.assert_text"
            type="textarea"
            :rows="5"
            placeholder="断言内容"
          >
          </el-input>
        </el-collapse-item>
      </el-collapse>
    </div>
    <!-- 保存 -->
    <div style="margin: 10px 0">
      <el-input
        v-model="caseForm.name"
        placeholder="请输入用例名称"
        style="width: 75%; margin: 0 10px"
      ></el-input>
      <el-button type="primary" style="width: 10%" @click="createCase"
        >保存</el-button
      >
    </div>
  </div>
</template>

<script>
import vueJsonEditor from "vue-json-editor";
import CaseApi from "../../requests/case.js";

export default {
  props: ["caseid", "caseFlag", "moduleid", "currentModule"],
  components: {
    vueJsonEditor,
  },
  mounted() {
    if (this.caseFlag === 1) {
      console.log("创建用例");
    } else {
      console.log("进入用例详情");
      console.log("当前用例id:", this.caseid);
      this.caseDetail(this.caseid);
    }
  },
  data() {
    return {
      drawer: false,
      direction: "rtl",
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
      json: {
        msg: "测试",
      },
      activeName: "first",
      activeNames: "include",
      select: "",
      input: "",
      caseForm: {
        module_id: 0,
        name: "",
        url: "",
        method: "get",
        header: {},
        params_type: "params",
        params_body: {},
        response: "",
        assert_type: "include",
        assert_text: "",
      },
    };
  },
  methods: {
    onJsonChange(value) {
      console.log("value", value);
    },
    //调式接口
    async sendClick() {
      const resp = await CaseApi.debugCase(this.caseForm);
      if (resp.success === true) {
        this.caseForm.response = resp.result;
      } else {
        this.$message.error(resp.error.msg);
      }
    },
    //断言接口
    async assertCase() {
      const req = {
        response: this.caseForm.response,
        assert_type: this.caseForm.assert_type,
        assert_text: this.caseForm.assert_text,
      };
      const resp = await CaseApi.assertCase(req);
      if (resp.success === true) {
        this.$message.success("断言成功");
      } else {
        this.$message.error("断言失败");
      }
    },
    //创建用例
    async createCase() {
      if (this.caseFlag === 1) {
        console.log("创建用例");
        const req = {
          module_id: this.currentModule,
          name: this.caseForm.name,
          url: this.caseForm.url,
          method: this.caseForm.method,
          header: this.caseForm.header,
          params_type: this.caseForm.params_type,
          params_body: this.caseForm.params_body,
          response: this.caseForm.response,
          assert_type: this.caseForm.assert_type,
          assert_text: this.caseForm.assert_text,
        };
        const resp = await CaseApi.creatCase(req);
        if (resp.success === true) {
          this.$message.success("创建成功");
          this.$emit("fresh", {});
          this.closecasedialog();
        } else {
          this.$message.error("创建失败");
        }
      } else {
        console.log("更新用例");
        const req = {
          module_id: this.currentModule,
          name: this.caseForm.name,
          url: this.caseForm.url,
          method: this.caseForm.method,
          header: this.caseForm.header,
          params_type: this.caseForm.params_type,
          params_body: this.caseForm.params_body,
          response: this.caseForm.response,
          assert_type: this.caseForm.assert_type,
          assert_text: this.caseForm.assert_text,
        };
        const resp = await CaseApi.updateCase(this.caseid, req);
        if (resp.success === true) {
          this.$message.success("更新成功");
          this.$emit("fresh", {});
          this.closecasedialog();
        } else {
          this.$message.error("更新失败");
        }
      }
    },

    //获取用例详情
    async caseDetail(id) {
      const resp = await CaseApi.caseDetail(id);
      if (resp.success === true) {
        this.caseForm = resp.result;
        const header = resp.result.header.replace(/'/g, '"');
        console.log("header", header);
        const params_body = resp.result.params_body.replace(/'/g, '"');
        this.caseForm.header = JSON.parse(header);
        this.caseForm.params_body = JSON.parse(params_body);
      } else {
        this.$message.error(resp.error.msg);
      }
    },
    //调用父组件，关闭弹窗
    closecasedialog() {
      this.$emit("cancel", {});
    },
  },
};
</script>

<style>
div.jsoneditor {
  border: thin solid #ced4da;
}
div.jsoneditor-menu {
  display: none;
}
.ace-jsoneditor .ace_gutter {
  background: white;
}
div.jsoneditor-outer.has-main-menu-bar {
  margin-top: 0px;
  padding-top: 0px;
}
.per-label {
  margin-right: 10px;
  margin-bottom: 4px;
  font-size: 1rem;
}
</style>

<style scoped>
.radio {
  float: left;
  margin-top: 20px;
}
</style>
