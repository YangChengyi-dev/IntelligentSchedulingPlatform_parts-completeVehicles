<template>
  <div class="recipientsWarehouse">
    <!-- 表单 -->
    <div ref="formDiv">
      <el-form ref="form" class="unitForm" :model="form" id="form">
        <el-form-item label="运维人员:" prop="unitName">
          <el-input placeholder="请输入" v-model="form.unitName" clearable> </el-input>
        </el-form-item>
        <el-form-item label="备件类别:" prop="status">
          <el-select v-model="form.status" placeholder="请选择">
            <el-option label="南瑞" value="1"></el-option>
            <el-option label="华商三优" value="2"></el-option>
          </el-select>
        </el-form-item>
       
        <el-form-item label="备件厂商:" prop="type">
          <el-select v-model="form.type" placeholder="请选择">
            <el-option label="库房1号" value="0"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="备件型号:" prop="person">
          <el-input placeholder="请输入" v-model="form.person" clearable> </el-input>
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
      <table-first :table1Data="searchTableData" :height="TableHeight"></table-first>
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
        unitName: "",
        status: "",
        type: "",
        person: "",
      },
      tableData: [],
      searchTableData: [],
      TableHeight: 0,
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
    // 获取数据
    getData() {
      this.$http({
        url: `static/json/sparePartManager/recipientsWarehouse.json`,
        method: "get",
        data: {},
      }).then((res) => {
        const data = res.data.data;
        this.tableData = data;
        this.searchTableData = data;
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
  },
};
</script>
<style lang="scss">
.recipientsWarehouse {
  .unitForm {
    display: flex;
    // justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    .el-form-item {
      width: 20%;
      .el-form-item__label {
        // width: auto !important;
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
}
</style>
