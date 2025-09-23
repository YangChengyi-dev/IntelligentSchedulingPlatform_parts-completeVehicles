<template>
  <div class="userContainer">
    <div class="recipientsApply">
      <!-- 表单 -->
      <div ref="formDiv">
        <el-form ref="form" class="unitForm" :model="form" id="form">
          <el-form-item label="登录地址:" prop="ipaddr">
            <el-input placeholder="请输入" v-model="form.ipaddr" clearable>
            </el-input>
          </el-form-item>
          <el-form-item label="登录名称:" prop="loginName">
            <el-input placeholder="请输入" v-model="form.loginName" clearable> </el-input>
          </el-form-item>

      
          <el-form-item label="登录状态:" prop="status">
            <el-select v-model="form.status" placeholder="请选择">
              <el-option v-for="(item,index) in options" :key="index" :label="item.dictLabel" :value="item.dictValue">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="登录时间:" prop="time">
            <el-date-picker
              v-model="form.time"
              type="daterange"
              range-separator="-"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              unlink-panels
              value-format="yyyy-MM-dd"
            >
            </el-date-picker>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" icon="el-icon-search" size="small" @click="onSearch"
              >查询</el-button
            >
            <el-button
              icon="el-icon-refresh-right"
              size="small"
              @click="resetForm('form')"
              >重置</el-button
            >
          </el-form-item>
        </el-form>
      </div>
      <div class="table">
        <table-first :table1Data="searchTableData" :height="TableHeight"></table-first>
      </div>
    </div>
  </div>
</template>

<script>
import tableFirst from "./table";
export default {
  name: "unitManagement",
  components: { tableFirst },
  data() {
    return {
      form: {
        ipaddr: "",
        loginName: "",
        status: "",
        time: "",
      },
      tableData: [],
      searchTableData: [],
      TableHeight: 0,

      options: [],

    };
  },
  created() {
    this.getData();
    this.typeFun();

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
      let formData = new FormData();
      formData.append("ipaddr", this.form.ipaddr);
      formData.append("loginName", this.form.loginName);
      formData.append("status", this.form.status);
      formData.append("params[beginTime]", this.form.time[0]?this.form.time[0]:"");
      formData.append("params[endTime]", this.form.time[1]?this.form.time[1]:"");
      this.$http({
        url: this.$http.adornUrl("/monitor/logininfor/list"),
        method: "post",
        data: formData
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

     //操作类型接口
     typeFun() {
      this.$http({
        url: this.$http.adornUrl("/demo/modal/getType"),
        method: "get",
        params: this.$http.adornParams(
          {
            "type": "sys_common_status"
          }
        ),
      }).then((res) => {
        if (res.data.length) {
          const data = res.data;
          this.options = data;
        }
      });
    },
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
