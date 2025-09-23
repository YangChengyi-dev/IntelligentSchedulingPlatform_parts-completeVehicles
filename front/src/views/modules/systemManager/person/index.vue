<template>
  <div class="userContainer">
    <div class="tree">
      <el-tree :data="treeData" :props="defaultProps" default-expand-all @node-click="handleNodeClick"></el-tree>
    </div>
    <div class="recipientsApply">
      <!-- 表单 -->
      <div ref="formDiv">
        <el-form ref="form" class="unitForm" :model="form" id="form">
          <el-form-item label="登录名称:" prop="loginName">
            <el-input placeholder="请输入" v-model="form.loginName" clearable> </el-input>
          </el-form-item>
          <el-form-item label="手机号码:" prop="phonenumber">
            <el-input placeholder="请输入" v-model="form.phonenumber" clearable> </el-input>
          </el-form-item>

          <el-form-item label="用户状态:" prop="status">
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
  provide() {
    return {
      getData: this.getData,
    }
  },
  data() {
    return {
      form: {
        deptId: "",
        parentId: "",
        loginName: "",
        phonenumber: "",
        status: "",
        time: "",
      },
      searchTableData: [],
      TableHeight: 0,

      treeData: [],
      defaultProps: {
        children: "children",
        label: "title",
      },

      options: []
    };
  },
  created() {
    this.getData();
    this.getTree();
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
    // 树接口
    getTree() {
      this.$http({
        url: this.$http.adornUrl(`/system/dept/treeData`),
        method: "get",
        data: {},
      }).then((res) => {
        // this.treeData = res.data.treeData;
        if (res.data.length) {
          const data = res.data;
          for (let i = 0; i < data.length; i++) {
            data[i].children = [];
            if (data[i].pId == 0) {
              this.treeData.push(data[i]);
            }
            for (let j = 1; j < data.length; j++) {
              if (data[j].pId == data[i].id) {
                data[i].children.push(data[j])
              }
            }
          }
        }

      });
    },
    // table数据
    getData() {

      let formData = new FormData();
      formData.append("deptId", this.form.deptId);
      formData.append("parentId", this.form.parentId);
      formData.append("loginName", this.form.loginName);
      formData.append("phonenumber", this.form.phonenumber);
      formData.append("status", this.form.status);
      formData.append("params[beginTime]", this.form.time[0]?this.form.time[0]:"");
      formData.append("params[endTime]", this.form.time[1]?this.form.time[1]:"");
      this.$http({
        url: this.$http.adornUrl("/system/user/list"),
        method: "post",
        // params: this.$http.adornParams(params),
        data: formData
      }).then((res) => {
        if (res.data.code == 0) {
          const data = res.data.rows;
          this.searchTableData = data;

        }
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

    // 获取点击的数节点数据
    handleNodeClick(data) {
      this.form.deptId = data.id;
      this.form.parentId = data.pId;
      this.getData()
      this.total = this.searchTableData.length;
      this.currentPage = 1;
    },

    // 用户状态接口
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

  .tree {
    width: 10%;
  }

  .recipientsApply {
    width: 89%;

    .unitForm {
      display: flex;
      // justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;

      .el-form-item {
        width: 33%;
      }
    }
  }
}
</style>
