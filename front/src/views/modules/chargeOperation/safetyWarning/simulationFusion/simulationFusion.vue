<template>
  <div id="app" class="contain">
    <div ref="formDiv">
      <el-form ref="form" class="unitForm" :model="form" id="form">
        <el-form-item label="运输方式:">
          <el-select v-model="form.way" clearable placeholder="请选择">
            <el-option
              v-for="item in wayOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <!--<el-form-item label="站点性质:">
					<el-select v-model="form.site_type" clearable placeholder="请选择">
						<el-option v-for="item in siteTypeOptions" :key="item.value" :label="item.label"
							:value="item.value" />
					</el-select>
				</el-form-item>-->
        <el-form-item label="中转站点:">
          <el-select v-model="form.site" clearable placeholder="请选择">
            <el-option
              v-for="item in siteOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
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
          <!-- <el-button class="iconfont icon-huifu" type="primary" size="small" @click="restore()">&nbsp;返回</el-button> -->
        </el-form-item>
      </el-form>
    </div>
    <div
      v-loading="loading"
      element-loading-text="正在优化中..."
      element-loading-spinner="el-icon-loading"
      element-loading-background="rgba(0, 0, 0, 0.8)"
    >
      <!-- 表格 -->
      <el-table
        :data="
          searchTableData.slice(
            (currentPage - 1) * pagesize,
            currentPage * pagesize
          )
        "
        ref="table"
        id="table"
        stripe
        style="width: 100%"
        :header-row-style="{ height: '35px' }"
        :row-style="{ height: '35px' }"
        :height="TableHeight"
      >
        <el-table-column
          type="selection"
          label=""
          align="center"
          min-width="5%"
        >
        </el-table-column>
        <el-table-column prop="id" label="序号" align="center" min-width="5%">
        </el-table-column>
        <el-table-column
          prop="route"
          label="路径"
          align="center"
          min-width="10%"
        >
        </el-table-column>
        <!--<el-table-column
          prop="site_type"
          label="站点性质"
          align="center"
          min-width="10%"
        >
        </el-table-column>-->
        <el-table-column
          prop="highway"
          label="公路距离(公里)"
          align="center"
          min-width="10%"
        >
        </el-table-column>
        <el-table-column
          prop="railway"
          label="铁路距离(公里)"
          align="center"
          min-width="10%"
        >
        </el-table-column>
        <el-table-column
          prop="waterway"
          label="水路距离(公里)"
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
        :total="searchTableData.length"
      >
      </el-pagination>
    </div>
  </div>
</template>
<script>
//这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）
//例如：import 《组件名称》 from '《组件路径》';
import axios from "axios";
export default {
  //import引入的组件需要注入到对象中才能使用
  components: {},
  data() {
    return {
      form: {
        way: "",
        site_type: "合资车",
        site: ""
      },
      tableData: [],
      searchTableData: [],
      TableHeight: 2,
      tableRadio: {},
      currentPage: 1,
      pagesize: 10,
      pagesizes: [10, 20, 50, 100, 200],
      total: 0,
      isopenDialog: "false",
      title: "",
      loading: false,
      wayOptions: [
        { value: "铁路", label: "铁路" },
        { value: "公路", label: "公路" },
        { value: "水路", label: "水路" }
      ],
      siteTypeOptions: [
        { value: "品牌车", label: "品牌车" },
        { value: "合资车", label: "合资车" }
      ],
      siteOptions: [
        { value: "北京", label: "北京" },
        { value: "成都", label: "成都" },
        { value: "大连", label: "大连" },
        { value: "佛山", label: "佛山" },
        { value: "贵阳", label: "贵阳" },
        { value: "哈尔滨", label: "哈尔滨" },
        { value: "杭州", label: "杭州" },
        { value: "呼和浩特", label: "呼和浩特" },
        { value: "济南", label: "济南" },
        { value: "昆明", label: "昆明" },
        { value: "兰州", label: "兰州" },
        { value: "柳州", label: "柳州" },
        { value: "宁波", label: "宁波" },
        { value: "上海", label: "上海" },
        { value: "沈阳", label: "沈阳" },
        { value: "石家庄", label: "石家庄" },
        { value: "天津", label: "天津" },
        { value: "乌鲁木齐", label: "乌鲁木齐" },
        { value: "芜湖", label: "芜湖" },
        { value: "武汉", label: "武汉" },
        { value: "西安", label: "西安" },
        { value: "徐州", label: "徐州" },
        { value: "长沙", label: "长沙" },
        { value: "广州", label: "广州" },
        // { value: "宁波", label: "宁波" },
        // { value: "上海", label: "上海" },
        { value: "烟台", label: "烟台" }
      ]
    };
  },
  //监听属性 类似于data概念
  computed: {},
  //监控data中的数据变化
  watch: {},
  //方法集合
  methods: {
    // 表单查询
    getData() {
      this.$http({
        url: this.baseurl + "/transport/index",
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
    onSearch() {
      if (
        this.form.way == "" &&
        this.form.site_type == "" &&
        this.form.site == ""
      ) {
        this.$http({
          url: this.baseurl + "/transport/index",
          method: "get",
          data: {}
        }).then(res => {
          const data = res.data.data;
          this.tableData = data;
          this.searchTableData = data;
          // 获取表格数据总数量
          this.total = this.searchTableData.length;
        });
        this.$message.success("查询成功");
      }
      // else if (this.form.way == "" || this.form.site_type == "") {
      // 	this.$message({
      // 		message: "运输方式不能为空",
      // 		type: 'error'
      // 	})
      // }
      else {
        this.loading = true;
        axios.post(this.baseurl + "/transport/search", this.form).then(res => {
          const datas = res.data.data;
          // console.log(datas);
          this.tableData = datas;
          this.searchTableData = datas;
          // 获取表格数据总数量
          this.total = this.searchTableData.length;
        });
        setTimeout(() => {
          this.loading = false;
          this.$message.success("查询成功");
        }, 200);
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
      this.form.fault_name = "";
      this.form.fault_detection = "";
      this.form.severity_rating = "";
      this.getData();
      this.$message.success("已重置");
    }
  },
  //生命周期 - 创建完成（可以访问当前this实例）
  created() {},
  //生命周期 - 挂载完成（可以访问DOM元素）
  mounted() {
    //动态计算表格高度
    let windowHeight =
      document.documentElement.clientHeight || document.bodyclientHeight;
    this.$nextTick(() => {
      this.TableHeight = windowHeight - this.$refs.formDiv.offsetHeight - 175; //数值"140"根据需要调整
    });
    setTimeout(() => {
      this.getData();
    }, 0);
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
  color: rgb(125, 180, 173);

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
          color: rgb(125, 180, 173);
        }
      }
    }
  }
}

.allChart {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  text-align: center;
  color: rgb(125, 180, 173);
  font-size: 19px;
  width: 90%;
  height: 360px;
  margin: 0 auto;

  .chart1 {
    display: flex;
    flex-direction: column;
    width: 49%;
    height: 100%;
    background-color: #0623208c;
    border-radius: 5px;

    .chartTitle1 {
      padding-top: 15px;
      height: 12%;
    }

    .partChart1 {
      height: 85%;
    }
  }

  .chart2 {
    display: flex;
    flex-direction: column;
    width: 49%;
    height: 100%;
    background-color: #0623208c;
    border-radius: 5px;

    .chartTitle2 {
      padding-top: 15px;
      height: 12%;
    }

    .partChart2 {
      height: 85%;
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
