<template>
  <div class="archiveSearch">
    <!-- 表单 -->
    <div ref="formDiv">
      <el-form ref="form" class="unitForm" :model="form" id="form">
        <el-form-item label="类别:" prop="unitName">
          <el-select v-model="form.unitName" placeholder="请选择">
            <el-option label="充电枪" value="充电枪"></el-option>
            <el-option label="充电控制器" value="充电控制器"></el-option>
            <el-option label="液晶屏" value="液晶屏"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="厂商:" prop="status">
          <el-select v-model="form.status" placeholder="请选择">
            <el-option label="南瑞" value="1"></el-option>
            <el-option label="华商三优" value="2"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="型号:" prop="marketName">
          <el-input placeholder="请输入" v-model="form.marketName" clearable> </el-input>
        </el-form-item>
        <el-form-item label="库房:" prop="type">
          <el-select v-model="form.type" placeholder="请选择">
            <el-option label="库房1号" value="0"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" icon="el-icon-search" size="small" @click="onSearch"
            >查询</el-button
          >
          <el-button icon="el-icon-refresh-right" size="small" @click="resetForm('form')"
            >重置</el-button
          >
        </el-form-item>
      </el-form>
    </div>
    <div class="table">
      <!-- 工具栏 -->
      <!-- <div ref="toolbar" class="toolbar">
        <el-row class="btnGroup">
          <el-button
            type="primary"
            size="mini"
            icon="el-icon-arrow-down"
            @click="allExtract"
            >全部抽取</el-button
          >
          <el-button type="primary" size="mini" icon="el-icon-arrow-down" @click="Extract"
            >抽取</el-button
          >
          <el-button type="primary" size="mini" icon="el-icon-plus" @click="add"
            >新增</el-button
          >
          <el-button type="primary" size="mini" icon="el-icon-edit" @click="edit"
            >编辑</el-button
          >

          <el-button
            type="primary"
            size="mini"
            icon="el-icon-upload2"
            @click="exportExcel"
            >导出</el-button
          >

          <el-button
            type="primary"
            size="mini"
            icon="el-icon-upload2"
            @click="exportAllExcel"
            >导出全部</el-button
          >
        </el-row>
      </div> -->
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
        @current-change="clickChange"
      >
        <!-- <el-table-column label="" align="center" min-width="4%">
          <template slot-scope="scope">
            <el-radio v-model="tableRadio" :label="scope.row"><i></i></el-radio>
          </template>
        </el-table-column> -->
        <!-- <el-table-column type="index" label="序号" align="center" min-width="32%">
        </el-table-column> -->
        <el-table-column prop="UNIT_NAME" label="备件名称" align="center" min-width="10%">
        </el-table-column>
        <el-table-column prop="MARKET_NAME" label="类别" align="center" min-width="10%">
        </el-table-column>
        <el-table-column prop="TYPE_NAME" label="库房" align="center" min-width="10%">
        </el-table-column>
        <el-table-column prop="CAPACITY" label="库存数" align="center" min-width="10%">
        </el-table-column>
        <el-table-column prop="START_TIME" label="联系人" align="center" min-width="10%">
        </el-table-column>
        <el-table-column prop="END_TIME" label="联系方式" align="center" min-width="10%">
        </el-table-column>
        <el-table-column prop="FILE_NAME" label="库房地址" align="center" min-width="10%">
        </el-table-column>
        <el-table-column prop="YEAR" label="生产厂商" align="center" min-width="10%">
        </el-table-column>
        <el-table-column prop="perform" label="型号" align="center" min-width="10%">
        </el-table-column>
        <el-table-column label="操作" align="center" min-width="16%">
          <template slot-scope="scope">
            <div class="opr">
              <div class="operate" @click="detail(scope.row)">出入库详情</div>
            </div>
          </template>
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
    <!-- 新增，编辑弹框 -->
    <div class="dialog">
      <Dialog
        :title="title"
        width="70%"
        height="80%"
        :isDetail="isDetail"
        v-if="openDialog"
        ref="testDialog"
      ></Dialog>
    </div>
  </div>
</template>

<script>
import Dialog from "./dialog";
export default {
  name: "unitManagement",
  components: { Dialog },
  data() {
    return {
      form: {
        unitName: "",
        marketName: "",
        status: "",
        type: "",
      },
      tableData: [],
      searchTableData: [],
      TableHeight: 0,
      tableRadio: "",
      currentPage: 1,
      pagesize: 10,
      pagesizes: [5, 10, 20, 50, 100],
      total: 0,
      openDialog: false,
      title: "",
      isDetail: false,
    };
  },
  created() {
    this.getData();

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
    // 单选获取整行数据
    clickChange(item) {
      this.tableRadio = item;
    },

    // 表格选择当前显示行数
    handleSizeChange(val) {
      this.pagesize = val;
    },
    // 切换表格页面
    handleCurrentChange(val) {
      this.currentPage = val;
    },
    // 获取数据
    getData() {
      this.$http({
        url: `static/json/sparePartManager/inventoryOverview.json`,
        method: "get",
        data: {},
      }).then((res) => {
        const data = res.data.data;
        this.tableData = data;
        this.searchTableData = data;
        // 获取表格数据总数量
        this.total = this.searchTableData.length;
      });
    },
    // 详情
    detail(data) {
      this.openDialog = true;
      this.isDetail = true;
      this.title = "详情";
      this.$nextTick(() => {
        this.$refs.testDialog.init(data);
      });
    },

    // 表单查询
    onSearch() {
      this.searchTableData = this.tableRes(this.form.unitName, this.tableData);
      this.total = this.searchTableData.length;
      this.currentPage = 1;
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
  },
};
</script>
<style lang="scss">
.archiveSearch {
  .unitForm {
    display: flex;
    // justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    .el-form-item {
      width: 20%;
      .el-form-item__label {
        width: auto;
      }
      .el-form-item__content {
        margin-left: 10px !important;
        width: 60%;
        .el-date-editor {
          width: 100%;
          .el-input__icon {
            color: #15a193;
          }
        }
      }
    }
  }
  .echarts {
    height: 40vh;
    display: flex;
    justify-content: space-between;
    align-items: center;
    .bar {
      flex: 1;
      height: 100%;
      box-sizing: border-box;
    }
  }
  .toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 15px;

    .btnGroup {
      width: 100%;
    }
  }
  .opr {
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    .operate {
      color: #1ba799;
      cursor: pointer;
    }
  }
}
</style>
