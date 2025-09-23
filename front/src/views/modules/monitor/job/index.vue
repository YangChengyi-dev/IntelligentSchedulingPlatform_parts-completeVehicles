<template>
  <div class="userContainer">
    <div class="recipientsApply">
      <!-- 表单 -->
      <div ref="formDiv">
        <el-form ref="form" class="unitForm" :model="form" id="form">
          <el-form-item label="任务名称:" prop="jobName">
            <el-input placeholder="请输入" v-model="form.jobName" clearable> </el-input>
          </el-form-item>

          <el-form-item label="任务分组:" prop="jobGroup">
            <el-select v-model="form.jobGroup" placeholder="请选择">
              <el-option v-for="(item,index) in options" :key="index" :label="item.dictLabel" :value="item.dictValue">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="任务状态:" prop="status">
            <el-select v-model="form.status" placeholder="请选择">
              <el-option v-for="(item,index) in statusArr" :key="index" :label="item.dictLabel" :value="item.dictValue">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" icon="el-icon-search" size="small" @click="onSearch">查询</el-button>
            <el-button icon="el-icon-refresh-right" size="small" @click="resetForm('form')">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      <div class="table">
        <table-first :table1Data="searchTableData" :height="TableHeight" :options="options" ></table-first>
      </div>
    </div>
  </div>
</template>

<script>
import tableFirst from "./table";
export default {
  name: "unitManagement",
  components: { tableFirst },
  provide(){
    return {
      getData:this.getData,
    }
  },
  data() {
    return {
      form: {
        jobName: "",
        jobGroup: "",
        status: "",
      },
      tableData: [],
      searchTableData: [],
      TableHeight: 0,
      options: [],
      statusArr: [],
    };
  },
  created() {
    this.getData();
    this.groupFun();
     this.statusFun();

    var _this = this;
    document.onkeydown = function (e) {
      //按下回车提交
      let key = window.event.keyCode;
      //事件中keycode=13为回车事件
      if (key == 13) {
        _this.onSearch();
      }
    };
  },
  mounted() {
    //动态计算表格高度
    let windowHeight = document.documentElement.clientHeight || document.bodyclientHeight;
    this.$nextTick(() => {
      this.TableHeight = windowHeight - this.$refs.formDiv.offsetHeight - 175; //数值"140"根据需要调整
    });
  },
  methods: {
    // 获取数据
    getData() {
      let params = {
        jobName: this.form.jobName,
        jobGroup: this.form.jobGroup,
        status: this.form.status,
      }
      this.$http({
        url: this.$http.adornUrl("/monitor/job/list"),
        method: "post",
        params: this.$http.adornParams(params),
      }).then((res) => {
        const data = res.data.rows;
        this.searchTableData = data;
      });
    },

    // 表单查询
    onSearch() {
      this.getData();
    },

    // 重置
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },

    // 任务分组接口
    groupFun() {
      this.$http({
        url: this.$http.adornUrl("/tool/dict/getType"),
        method: "get",
        params: this.$http.adornParams(
          {
            "type": "sys_job_group"
          }
        ),
      }).then((res) => {
        if (res.data.length) {
          const data = res.data;
          this.options = data;
        }
      });
    },
    // 用户状态接口
    statusFun() {
      this.$http({
        url: this.$http.adornUrl("/tool/dict/getType"),
        method: "get",
        params: this.$http.adornParams(
          {
            "type": "sys_job_status"
          }
        ),
      }).then((res) => {
        if (res.data.length) {
          const data = res.data;
          this.statusArr = data;
        }
      });
    }
  },
};
</script>
<style lang="scss">
.el-form-item__label {
  // width: auto !important;
}
</style>
<style lang="scss" scoped>
.userContainer {
  display: flex;
  justify-content: space-between;

  .recipientsApply {
    width: 100%;

    .unitForm {
      display: flex;
      // justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;

      .el-form-item {
        width: 25%;
      }
    }
  }
}
</style>
