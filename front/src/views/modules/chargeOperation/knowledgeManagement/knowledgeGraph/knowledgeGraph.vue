<template>
  <div class="userContainer">
    <div class="tree">
      <el-tree
        :data="treeData"
        :props="defaultProps"
        @node-click="handleNodeClick"
      ></el-tree>
    </div>
    <div class="recipientsApply">
      <!-- 表单 -->
      <div ref="formDiv">
        <el-form ref="form" class="unitForm" :model="form" id="form">
          <el-form-item label="" prop="unitName">
            <el-input placeholder="请输入" v-model="form.unitName" clearable> </el-input>
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
        <!-- 表格 -->
      <el-table
        :data="
          searchTableData.slice((currentPage - 1) * pagesize, currentPage * pagesize)
        "
        id="table"
        stripe
        style="width: 100%"
        :header-row-style="{ height: '35px' }"
        :row-style="{ height: '35px' }"
        :height="TableHeight"
      >
        <el-table-column label="" align="center" min-width="5%">
          <template slot-scope="scope">
            <el-radio v-model="tableRadio" :label="scope.row"><i></i></el-radio>
          </template>
        </el-table-column>
        <el-table-column
          prop="ZSBT"
          label="知识标题"
          align="center"
          min-width="10%"
        >
        </el-table-column>
        <el-table-column
          prop="JJFA"
          label="解决方案"
          align="center"
          min-width="10%"
        >
        </el-table-column>
        <el-table-column
          prop="SLRQ"
          label="收录日期"
          align="center"
          min-width="10%"
        >
        </el-table-column>
      </el-table>
      <!-- 分页 -->
      <el-pagination
        background
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="pagesizes"
        :page-size="pagesize"
        layout=" prev, pager, next, jumper, sizes,total"
        :total="total"
      >
      </el-pagination>
      </div>
    </div>
  </div>
</template>

<script>
// import tableFirst from "./table";
export default {
  name: "unitManagement",
  components: {  },
  data() {
    return {
      form: {
        unitName: "",
        marketName: "",
        status: "",
        type: "",
        person: "",
        time: "",
      },
      tableData: [],
      searchTableData: [{
        "ZSBT": "电器元件",
        "JJFA": "",
        "SLRQ": "2021-03-23 14:25:56"
      },{
        "ZSBT": "模块",
        "JJFA": "",
        "SLRQ": "2021-03-23 14:25:56"
      },{
        "ZSBT": "内部环境",
        "JJFA": "",
        "SLRQ": "2021-03-23 14:25:56"
      },{
        "ZSBT": "逻辑类",
        "JJFA": "",
        "SLRQ": "2021-03-23 14:25:56"
      },{
        "ZSBT": "通信类",
        "JJFA": "",
        "SLRQ": "2021-03-23 14:25:56"
      },{
        "ZSBT": "车辆相关",
        "JJFA": "",
        "SLRQ": "2021-03-23 14:25:56"
      }],
      TableHeight: 0,

      treeData: [{
        "label": "电气元件",
        "children": []
      },{
        "label": "模块",
        "children": []
      },{
        "label": "内部环境",
        "children": []
      },{
        "label": "逻辑类",
        "children": []
      },{
        "label": "通信类",
        "children": []
      },{
        "label": "车辆相关",
        "children": []
      }],
      defaultProps: {
        children: "children",
        label: "label",
      },
      TableHeight: 0,
      tableRadio: {},
      currentPage: 1,
      pagesize: 10,
      pagesizes: [5, 10, 20, 50, 100],
      total: 0,
      isopenDialog: "false",
      title: "",
    };
  },
  created() {
    // this.getData();

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
      this.$http({
        url: `static/json/systemManager/userManager.json`,
        method: "get",
        data: {},
      }).then((res) => {
        this.treeData = res.data.treeData;
      });
      this.$http({
        url: this.$http.adornUrl("/index"),
        method: "get",
        data: {},
      }).then((res) => {
        // const data = res.data.data;
        // this.tableData = data;
        // this.searchTableData = data;
      });
    },

    // 表单查询
    onSearch() {
      this.searchTableData = this.tableRes(this.form.unitName, this.tableData);
    },
    tableRes(searchData, table, array) {
      const search = searchData;

      return table.filter((data) => {
        return Object.keys(data).some((key) => {
          if (array) {
            if (array.indexOf(key) == -1) {
              return String(data[key]).toLowerCase().indexOf(search) > -1;
            }
          } else {
            return String(data[key]).toLowerCase().indexOf(search) > -1;
          }
        });
      });
      return table;
    },

    // 重置
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },

    // 获取点击的数节点数据
    handleNodeClick(data) {
      this.searchTableData = this.tableRes(data.label, this.tableData);
      this.total = this.searchTableData.length;
      this.currentPage = 1;
    },

     // 表格选择当前显示行数
    handleSizeChange(val) {
      this.pagesize = val;
    },
    // 切换表格页面
    handleCurrentChange(val) {
      this.currentPage = val;
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
