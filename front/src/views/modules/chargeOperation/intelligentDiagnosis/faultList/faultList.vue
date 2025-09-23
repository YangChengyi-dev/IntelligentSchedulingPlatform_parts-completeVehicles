<!--  -->
<template>
  <div id="app">
    <div ref="formDiv">
      <el-form ref="form" class="unitForm" :model="form" id="form">
        <el-form-item label="省份:">
          <el-select v-model="form.prov" @change="updateCitySelector" clearable placeholder="请选择">
            <el-option v-for="item in provOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="城市:">
          <el-select v-model="form.city" clearable placeholder="请选择">
            <el-option v-for="item in cityOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="发往方向:">
          <el-select v-model="form.dest" clearable placeholder="请选择">
            <el-option v-for="item in destOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" size="small" @click="onSearch">查询</el-button>
          <el-button type="primary" icon="el-icon-reset" size="small" @click="reset">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
    <!-- 表格 -->
    <el-table :data="searchTableData.slice((currentPage - 1) * pagesize, currentPage * pagesize)
      " id="table" stripe style="width: 100%" :header-row-style="{ height: '35px' }" :row-style="{ height: '35px' }"
      :height="TableHeight">
      <el-table-column label="" align="center" min-width="4%">
        <template slot-scope="scope">
          <el-radio v-model="tableRadio" :label="scope.row"><i></i></el-radio>
        </template>
      </el-table-column>
      <el-table-column prop="supplier_name" label="序号" align="center" min-width="6%">
      </el-table-column>
      <el-table-column prop="supplier_addr" label="供应商地址" align="center" min-width="32%">
      </el-table-column>
      <el-table-column prop="prov" label="省份" align="center" min-width="6%">
      </el-table-column>
      <el-table-column prop="city" label="城市" align="center" min-width="6%">
      </el-table-column>
      <el-table-column prop="dest" label="发往方向" align="center" min-width="6%">
      </el-table-column>
      <el-table-column prop="distance" label="距离" align="center" min-width="8%">
      </el-table-column>
      <el-table-column prop="quantity" label="货量" align="center" min-width="8%">
      </el-table-column>
    </el-table>
    <!-- 分页 -->
    <el-pagination background @size-change="handleSizeChange" @current-change="handleCurrentChange"
      :current-page="currentPage" :page-sizes="pagesizes" :page-size="pagesize"
      layout=" prev, pager, next, jumper, sizes,total" :total="searchTableData.length">
    </el-pagination>
  </div>
</template>

<script>
//这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）
//例如：import 《组件名称》 from '《组件路径》';
import FileSaver from "file-saver";
import * as XLSX from "xlsx";
import axios from 'axios';
export default {
  //import引入的组件需要注入到对象中才能使用
  components: {},
  data() {
    return {
      form: {
        id: "",
        supplier_name: "",
        supplier_addr: "",
        prov: "",
        city: "",
        dest: '',
        distance: "",
        quantity: "",
      },
      searchFormParams: {
        prov: null,
        city: null,
        dest: null
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
        {
          value: '安徽',
          label: '安徽'
        },
        {
          value: '河南',
          label: '河南'
        }, {
          value: '湖北',
          label: '湖北'
        }, {
          value: '湖南',
          label: '湖南'
        }, {
          value: '江苏',
          label: '江苏'
        }, {
          value: '江西',
          label: '江西'
        }, {
          value: '上海',
          label: '上海'
        }, {
          value: '浙江',
          label: '浙江'
        }
      ],
      cityOptions: [],
      destOptions: [
        {
          value: '成都',
          label: '成都'
        },
        {
          value: '大连',
          label: '大连'
        }, {
          value: '佛山',
          label: '佛山'
        }, {
          value: '青岛',
          label: '青岛'
        }, {
          value: '天津',
          label: '天津'
        }, {
          value: '长春',
          label: '长春'
        }
      ],
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
        url: this.baseurl + "/part/index",
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
    // 表单查询
    onSearch() {
      if (this.form.prov == "" && this.form.city == "" && this.form.dest == "") {
        this.$message({
          message: "查询不能为空",
          type: 'error'
        })
      }
      else {
        const params = { ...this.searchFormParams };
        params.prov = this.form.prov;
        params.city = this.form.city;
        params.dest = this.form.dest;
        console.log(params)
        axios.post(this.baseurl + "/part/search", params).then(res => {
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
      this.form.dest = "";
      this.getData();
    },
    updateCitySelector() {
      if (this.form.prov === "安徽") {
        this.cityOptions = [
          { value: '合肥', label: '合肥' },
          { value: '滁州', label: '滁州' },
          { value: '宜城', label: '宜城' },
          { value: '宁国', label: '宁国' },
          { value: '安庆', label: '安庆' },
          { value: '芜湖', label: '芜湖' },
        ]
        this.form.city = "";
      }
      else if (this.form.prov === "河南") {
        this.cityOptions = [
          { value: '郑州', label: '郑州' },
          { value: '鹤壁', label: '鹤壁' },
          { value: '洛阳', label: '洛阳' },
          { value: '鹤壁', label: '鹤壁' },
        ]
        this.form.city = "";
      }
      else if (this.form.prov === "湖北") {
        this.cityOptions = [
          { value: '武汉', label: '武汉' },
          { value: '钟祥', label: '钟祥' },
          { value: '麻城', label: '麻城' },
          { value: '十堰', label: '十堰' },
        ]
        this.form.city = "";
      }
      else if (this.form.prov === "湖南") {
        this.cityOptions = [
          { value: '长沙', label: '长沙' },
        ]
        this.form.city = "";
      }
      else if (this.form.prov === "江苏") {
        this.cityOptions = [
          { value: '镇江', label: '镇江' },
          { value: '海门', label: '海门' },
          { value: '苏州', label: '苏州' },
          { value: '常州', label: '常州' },
          { value: '扬中', label: '扬中' },
          { value: '太仓', label: '太仓' },
          { value: '无锡', label: '无锡' },
          { value: '常熟', label: '常熟' },
          { value: '丹阳', label: '丹阳' },
          { value: '江阴', label: '江阴' },
          { value: '靖江', label: '靖江' },
          { value: '昆山', label: '昆山' },
          { value: '连云港', label: '连云港' },
          { value: '南京', label: '南京' },
          { value: '南通', label: '南通' },
          { value: '如皋', label: '如皋' },
          { value: '徐州', label: '徐州' },
          { value: '扬州', label: '扬州' },
          { value: '仪征', label: '仪征' },
          { value: '宜兴', label: '宜兴' },
          { value: '张家港', label: '张家港' },

        ]
        this.form.city = "";
      }
      else if (this.form.prov === "江西") {
        this.cityOptions = [
          { value: '南昌', label: '南昌' },
        ]
        this.form.city = "";
      }
      else if (this.form.prov === "上海") {
        this.cityOptions = [
          { value: '宝山', label: '宝山' },
          { value: '崇明', label: '崇明' },
          { value: '奉贤', label: '奉贤' },
          { value: '嘉定', label: '嘉定' },
          { value: '金山区', label: '金山区' },
          { value: '闵行', label: '闵行' },
          { value: '浦东', label: '浦东' },
          { value: '青浦', label: '青浦' },
          { value: '上海', label: '上海' },
          { value: '松江', label: '松江' },
        ]
        this.form.city = "";
      }
      else if (this.form.prov === "浙江") {
        this.cityOptions = [
          { value: '慈溪', label: '慈溪' },
          { value: '杭州', label: '杭州' },
          { value: '湖州', label: '湖州' },
          { value: '嘉兴', label: '嘉兴' },
          { value: '乐清', label: '乐清' },
          { value: '丽水', label: '丽水' },
          { value: '宁波', label: '宁波' },
          { value: '上虞', label: '上虞' },
          { value: '台州', label: '台州' },
          { value: '温州', label: '温州' },
          { value: '象山', label: '象山' },
          { value: '萧山', label: '萧山' },
          { value: '鄞州区', label: '鄞州区' },
          { value: '余姚', label: '余姚' },
          { value: '玉环', label: '玉环' },
          { value: '舟山', label: '舟山' },
          { value: '诸暨', label: '诸暨' },
        ]
        this.form.city = "";
      }
    },
  },
  //生命周期 - 创建完成（可以访问当前this实例）
  created() {
    this.getData();
  },
  //生命周期 - 挂载完成（可以访问DOM元素）
  mounted() {
    //动态计算表格高度
    let windowHeight = document.documentElement.clientHeight || document.bodyclientHeight;
    this.$nextTick(() => {
      this.TableHeight =
        windowHeight -
        this.$refs.formDiv.offsetHeight -
        175; //数值"140"根据需要调整
    });
  },
  beforeCreate() { }, //生命周期 - 创建之前
  beforeMount() { }, //生命周期 - 挂载之前
  beforeUpdate() { }, //生命周期 - 更新之前
  updated() { }, //生命周期 - 更新之后
  beforeDestroy() { }, //生命周期 - 销毁之前
  destroyed() { }, //生命周期 - 销毁完成
  activated() { }, //如果页面有keep-alive缓存功能，这个函数会触发
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
