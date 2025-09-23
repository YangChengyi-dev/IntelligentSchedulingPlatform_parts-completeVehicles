<template>
  <div class="userContainer">
    <div class="recipientsApply">
      <!-- 表单 -->
      <div ref="formDiv">
        <el-form ref="form" class="unitForm" :model="form" id="form">
          <el-form-item label="公告标题:" prop="noticeTitle">
            <el-input placeholder="请输入" v-model="form.noticeTitle" clearable> </el-input>
          </el-form-item>
          <el-form-item label="操作人员:" prop="createBy">
            <el-input placeholder="请输入" v-model="form.createBy" clearable> </el-input>
          </el-form-item>

          <el-form-item label="公告类型:" prop="noticeType">
            <el-select v-model="form.noticeType" placeholder="请选择">
              <el-option v-for="(item,index) in options" :key="index" :label="item.dictLabel" :value="item.dictValue">
              </el-option>
            </el-select>
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
  provide(){
    return {
      getData:this.getData,
    }
  },
  data() {
    return {
      form: {
        noticeTitle: "",
        createBy: "",
        noticeType: "",
      },
      tableData: [],
      searchTableData: [],
      TableHeight: 0,

      options:[],
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
      let data = {
        noticeTitle: this.form.noticeTitle,
        createBy: this.form.createBy,
        noticeType: this.form.noticeType,
      }
      this.$http({
        url: this.$http.adornUrl("/system/notice/list"),
        method: "post",
        params: this.$http.adornParams(data),
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

    // 菜单状态接口
    statusFun() {
      this.$http({
        url: this.$http.adornUrl("/demo/modal/getType"),
        method: "get",
        params: this.$http.adornParams(
          {
            "type": "sys_notice_type"
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
