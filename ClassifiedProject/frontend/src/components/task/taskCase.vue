<template>
  <div>
    <el-dialog
      :title="showTitle"
      :visible.sync="dialogVisible"
      width="70%"
      :before-close="closeDialog"
    >
      <el-table
        class="edit-case"
        :data="tableData"
        border
        row-key="id"
        align="left"
        height="250"
      >
        <el-table-column
          v-for="(item, index) in col"
          :key="`col_${index}`"
          :prop="dropCol[index].prop"
          :label="item.label"
        >
        </el-table-column>
      </el-table>
      <div style="margin-top: 20px; text-align: right">
        <el-button
          type="primary"
          size="small"
          @click="saveCaseList()"
          style="margin-bottom: 20px"
          >保存</el-button
        >
      </div>
    </el-dialog>
  </div>
</template>

<script>
import taskApi from "../../requests/task.js";
import Sortable from "sortablejs";

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
      col: [
        {
          label: "ID",
          prop: "id",
        },
        {
          label: "名称",
          prop: "name",
        },
        {
          label: "方法",
          prop: "method",
        },
        {
          label: "地址",
          prop: "url",
        },
      ],
      dropCol: [
        {
          label: "ID",
          prop: "id",
        },
        {
          label: "名称",
          prop: "name",
        },
        {
          label: "方法",
          prop: "method",
        },
        {
          label: "地址",
          prop: "url",
        },
      ],
      tableData: [],
    };
  },
  created() {
    this.showTitle = "调整用例顺序任务";
    this.initCaseList();
  },
  mounted() {
    this.$nextTick(() => {
      this.rowDrop();
      this.columnDrop();
    });
  },
  methods: {
    //调用子组件 关闭弹窗
    closeDialog() {
      console.log("closeDialog");
      this.$emit("cancel", {});
    },
    //获取任务用例详情
    async initCaseList() {
      const resp = await taskApi.getTaskCaseList(this.tid);
      if (resp.success === true) {
        this.tableData = resp.result;
      } else {
        this.$message.error("查询失败!");
      }
    },

    //行拖拽
    rowDrop() {
      const tbody = document.querySelectorAll(
        ".el-table__body-wrapper tbody"
      )[1];
      const _this = this;
      Sortable.create(tbody, {
        onEnd({ newIndex, oldIndex }) {
          console.log("拖动了行", "当前序号: " + newIndex);
          const currRow = _this.tableData.splice(oldIndex, 1)[0];
          _this.tableData.splice(newIndex, 0, currRow);
        },
      });
    },
    //列拖拽
    columnDrop() {
      const wrapperTr = document.querySelectorAll(
        ".el-table__header-wrapper tr"
      )[1];
      this.sortable = Sortable.create(wrapperTr, {
        animation: 180,
        delay: 0,
        onEnd: (evt) => {
          console.log("拖动了列");
          const oldItem = this.dropCol[evt.oldIndex];
          this.dropCol.splice(evt.oldIndex, 1);
          this.dropCol.splice(evt.newIndex, 0, oldItem);
        },
      });
    },

    // 保存用例列表
    async saveCaseList() {
      console.log("tableData-->", this.tableData);
      var caseList = [];
      for (let i = 0; i < this.tableData.length; i++) {
        console.log(this.tableData[i].id);
        caseList.push(this.tableData[i].id);
      }
      console.log(caseList);
      var req = { caseList: caseList };
      const resp = await taskApi.updateTaskCaseList(this.tid, req);
      if (resp.success === true) {
        // this.tableData = resp.items
        this.$message.success("保存成功");
        this.closeDialog();
      } else {
        this.$message.error("查询失败！");
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
