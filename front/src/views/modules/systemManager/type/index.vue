<template>
  <div class="userContainer">
    <div class="recipientsApply">
      <!-- 表单 -->
      <div ref="formDiv">
        <el-form ref="form" class="unitForm" :model="form" id="form">
          <el-form-item label="字典名称:" prop="dictName">
            <el-input placeholder="请输入" v-model="form.dictName" clearable> </el-input>
          </el-form-item>
          <el-form-item label="字典类型:" prop="dictType">
            <el-input placeholder="请输入" v-model="form.dictType" clearable> </el-input>
          </el-form-item>

          <el-form-item label="字典状态:" prop="status">
            <el-select v-model="form.status" placeholder="请选择">
              <el-option v-for="(item,index) in options" :key="index" :label="item.dictLabel" :value="item.dictValue">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="创建时间:" prop="time">
            <el-date-picker v-model="form.time" type="daterange" unlink-panels range-separator="-" start-placeholder="开始日期"
              end-placeholder="结束日期" value-format="yyyy-MM-dd">
            </el-date-picker>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" icon="el-icon-search" size="small" @click="onSearch">查询</el-button>
            <el-button icon="el-icon-refresh-right" size="small" @click="resetForm('form')">重置</el-button>
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
  provide(){
    return {
      getData:this.getData,
    }
  },
  data() {
    return {
      form: {
        dictName: "",
        dictType: "",
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
      let formData = new FormData();
      formData.append("dictName", this.form.dictName);
      formData.append("dictType", this.form.dictType);
      formData.append("status", this.form.status);
      formData.append("params[beginTime]", this.form.time[0]?this.form.time[0]:"");
      formData.append("params[endTime]", this.form.time[1]?this.form.time[1]:"");
      this.$http({
        url: this.$http.adornUrl("/system/dict/list"),
        method: "post",
        data: formData
      }).then((res) => {
          const data = res.data.rows;
          this.searchTableData = data.reverse();
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

    // 菜单状态接口
    statusFun() {
      this.$http({
        url: this.$http.adornUrl("/tool/dict/getType"),
        method: "get",
        params: this.$http.adornParams(
          {
            "type": "sys_normal_disable"
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
