<!--  -->
<template>
  <div id="app">
    <div ref="formDiv">
      <el-form ref="form" class="unitForm" :model="form" id="form">
        <el-form-item label="省份:">
          <el-select v-model="form.prov" clearable placeholder="请选择">
            <el-option
              v-for="item in provOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <!--<el-form-item label="城市:">
          <el-select v-model="form.city" clearable placeholder="请选择">
            <el-option v-for="item in cityOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>-->
        <el-form-item>
          <el-button
            type="primary"
            icon="el-icon-search"
            size="small"
            @click="onSearch"
            >查询</el-button
          >
          <el-button
            type="primary"
            icon="el-icon-reset"
            size="small"
            @click="reset"
            >重置</el-button
          >
        </el-form-item>
      </el-form>
    </div>
    <!-- 表格 -->
    <el-table
      :data="
        searchTableData.slice(
          (currentPage - 1) * pagesize,
          currentPage * pagesize
        )
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
      <el-table-column prop="id" label="序号" align="center" min-width="5%">
      </el-table-column>
      <el-table-column prop="prov" label="省份" align="center" min-width="10%">
      </el-table-column>
      <el-table-column prop="city" label="城市" align="center" min-width="10%">
      </el-table-column>
      <el-table-column
        prop="sales"
        label="销售量（辆/年）"
        align="center"
        min-width="10%"
      >
      </el-table-column>
      <el-table-column
        prop="dealership_num"
        label="经销店数量"
        align="center"
        min-width="10%"
      >
      </el-table-column>
      <!-- <el-table-column prop="YHMS" label="隐患描述" align="center" min-width="10%">
      </el-table-column>
      <el-table-column prop="ZT" label="状态" align="center" min-width="10%">
      </el-table-column> -->
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
      :total="searchTableData.length"
    >
    </el-pagination>
  </div>
</template>

<script>
//这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）
//例如：import 《组件名称》 from '《组件路径》';
import FileSaver from "file-saver";
import * as XLSX from "xlsx";
import axios from "axios";
export default {
  //import引入的组件需要注入到对象中才能使用
  components: {},
  data() {
    return {
      form: {
        id: "",
        prov: "",
        city: "",
        sales: "",
        dealership_num: ""
      },
      searchFormParams: {
        prov: null,
        city: null
      },
      tableData: [],
      searchTableData: [],
      TableHeight: 0,
      tableRadio: {},
      currentPage: 1,
      pagesize: 10,
      pagesizes: [5, 10, 20, 50, 100],
      total: 0,
      isopenDialog: "false",
      title: "",
      provOptions: [
        { value: "安徽省", label: "安徽省" },
        { value: "福建省", label: "福建省" },
        { value: "江苏省", label: "江苏省" },
        { value: "山东省", label: "山东省" },
        { value: "上海市", label: "上海市" },
        { value: "浙江省", label: "浙江省" }
      ],
      cityOptions: []
    };
  },
  //监听属性 类似于data概念
  computed: {},
  //监控data中的数据变化
  watch: {},
  //方法集合
  methods: {
    getData() {
      this.$http({
        url: this.baseurl + "/vehicle/index",
        method: "get",
        data: {}
      }).then(res => {
        const data = res.data.data;
        this.tableData = data;
        this.searchTableData = data;
        // 获取表格数据总数量
        this.total = this.searchTableData.length;
      });
    },
    // 表单查询
    onSearch() {
      if (this.form.prov == "" && this.form.city == "") {
        this.$message({
          message: "查询不能为空",
          type: "error"
        });
      } else {
        const params = { ...this.searchFormParams };
        params.prov = this.form.prov;
        params.city = this.form.city;
        // console.log(params)
        axios.post(this.baseurl + "/vehicle/search", params).then(res => {
          const datas = res.data.data;
          console.log(datas);
          this.tableData = datas;
          this.searchTableData = datas;
          // 获取表格数据总数量
          this.total = this.searchTableData.length;
        });
      }
    },
    tableRes(searchData, table, array) {
      const search = searchData;
      return table.filter(data => {
        return Object.keys(data).some(key => {
          if (array) {
            if (array.indexOf(key) == -1) {
              return (
                String(data[key])
                  .toLowerCase()
                  .indexOf(search) > -1
              );
            }
          } else {
            return (
              String(data[key])
                .toLowerCase()
                .indexOf(search) > -1
            );
          }
        });
      });
      return table;
    },
    // 表格选择当前显示行数
    handleSizeChange(val) {
      this.pagesize = val;
    },
    // 切换表格页面
    handleCurrentChange(val) {
      this.currentPage = val;
    },
    reset() {
      this.form.prov = "";
      this.form.city = "";
      this.getData();
    }
  },
  //生命周期 - 创建完成（可以访问当前this实例）
  created() {
    this.getData();
  },
  //生命周期 - 挂载完成（可以访问DOM元素）
  mounted() {
    //动态计算表格高度
    let windowHeight =
      document.documentElement.clientHeight || document.bodyclientHeight;
    this.$nextTick(() => {
      this.TableHeight = windowHeight - this.$refs.formDiv.offsetHeight - 175; //数值"140"根据需要调整
    });
  },
  beforeCreate() {}, //生命周期 - 创建之前
  beforeMount() {}, //生命周期 - 挂载之前
  beforeUpdate() {}, //生命周期 - 更新之前
  updated() {}, //生命周期 - 更新之后
  beforeDestroy() {}, //生命周期 - 销毁之前
  destroyed() {}, //生命周期 - 销毁完成
  activated() {} //如果页面有keep-alive缓存功能，这个函数会触发
};
</script>
<style lang="scss" scoped>
.unitForm {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;

  .el-form-item {
    width: 24%;

    .el-form-item__label {
      width: 40%;
      // width: 150px;
    }

    .el-form-item__content {
      margin-left: 10px !important;

      .el-date-editor {
        width: 100%;

        // width: 202px;
        .el-input__icon {
          color: #15a193;
        }
      }
    }
  }
}

.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 15px;

  .btnGroup {
    width: 35%;
  }
}
</style>
