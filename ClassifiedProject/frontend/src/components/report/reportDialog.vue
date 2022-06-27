<template>
  <div>
    <el-dialog
      :title="showTitle"
      :visible.sync="dialogVisible"
      width="70%"
      :before-close="closeDialog"
    >
      <el-form label-width="100px" class="demo-ruleForm">
        <el-form-item label="统计">
          <div
            id="MyChart"
            :style="{ width: '380px', height: '380px' }"
            style="margin: 0 auto"
          ></div>
          <el-table :data="reportData" style="width: 100%" border>
            <el-table-column prop="name" label="名称"></el-table-column>
            <el-table-column prop="tests" label="总数"></el-table-column>
            <el-table-column prop="passed" label="通过"></el-table-column>
            <el-table-column prop="failure" label="失败"></el-table-column>
            <el-table-column prop="error" label="错误"></el-table-column>
            <el-table-column prop="skipped" label="跳过 "></el-table-column>
            <el-table-column prop="run_time" label="时长"></el-table-column>
            <el-table-column
              prop="create_time"
              label="创建时间"
            ></el-table-column>
          </el-table>
        </el-form-item>
        <el-form-item label="详细日志">
          <el-input type="textarea" :rows="10" v-model="detailLog"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button @click="closeDialog"> 关闭</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import * as echarts from "echarts";
import ReportApi from "../../requests/report.js";

export default {
  props: ["rid"],
  components: {},
  data() {
    return {
      showTitle: "查看报告",
      detailLog: "",
      dialogVisible: true,
      req: {
        page: 1,
        size: 6,
      },
      reportData: [],
      chartOption: {
        tooltip: {
          trigger: "item",
        },
        legend: {
          top: "5%",
          left: "center",
        },
        series: [
          {
            name: "比例",
            type: "pie",
            radius: "50%",
            data: [],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)",
              },
            },
          },
        ],
      },
    };
  },
  mounted() {
    this.$nextTick(() => {
      this.initEchart();
    });
  },
  methods: {
    //调用子组件 关闭弹窗
    closeDialog() {
      console.log("closeDialog");
      this.$emit("cancel", {});
    },
    //初始化任务图表
    async initEchart() {
      var chartDom = document.getElementById("MyChart");
      const resp = await ReportApi.getReportDetail(this.rid);
      var mychart = echarts.init(chartDom);
      this.chartOption.series[0].data = [];
      if (resp.success === true) {
        this.reportData.push(resp.result);
        this.chartOption.series[0].data.push({
          value: resp.result.skipped,
          name: "跳过",
        });
        this.chartOption.series[0].data.push({
          value: resp.result.passed,
          name: "通过",
        });
        this.chartOption.series[0].data.push({
          value: resp.result.failure,
          name: "失败",
        });
        this.chartOption.series[0].data.push({
          value: resp.result.error,
          name: "错误",
        });
        this.detailLog = resp.result.result;
      } else {
        this.$message.error("查询失败！");
      }
      mychart.setOption(this.chartOption);
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
  },
};
</script>

<style>
#image {
  text-align: left;
}
</style>
