<template>
  <div id="app" class="contain">
    <div ref="formDiv" class="search">
      <div class="searchCondition">
        <el-form ref="form" class="unitForm" :model="form" id="form">
          <el-form-item label="查询时间:">
            <el-select v-model="form.type" clearable placeholder="请选择">
              <el-option
                v-for="item in typeOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="运输方式:">
            <el-select v-model="form.is_limit" clearable placeholder="请选择">
              <el-option
                v-for="item in limitOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="优化方式:">
            <el-select v-model="form.method" clearable placeholder="请选择">
              <el-option
                v-for="item in methodOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
        </el-form>
      </div>
      <div class="searchBtn">
        <el-button
          type="primary"
          icon="el-icon-search"
          size="small"
          @click="onSearch"
          >优化</el-button
        >
        <el-button
          class="iconfont icon-xiazai"
          type="primary"
          size="small"
          @click="downloadExcel"
          >下载</el-button
        >
      </div>
    </div>
    <div
      v-loading="loading"
      element-loading-text="正在查询中..."
      element-loading-spinner="el-icon-loading"
      element-loading-background="rgba(0, 0, 0, 0.8)"
    >
      <div class="allChart">
        <div class="chart1">
          <div class="chartTitle1">
            整车运输成本<span class="cost">({{ allCost }}元)</span>
          </div>
          <div class="partChart1" ref="partChart1"></div>
        </div>
        <div class="chart2">
          <div class="chartTitle2">
            整车运输成本优化<span class="cost">({{ allOptCost }}元)</span>
          </div>
          <div class="partChart2" ref="partChart2"></div>
        </div>
      </div>

      <!-- 表格 -->
      <el-table
        :data="searchTableData"
        id="table"
        stripe
        style="width: 86%; margin: 0 auto;margin-top: 20px;"
        :header-row-style="{ height: '50px' }"
        :row-style="{ height: '50px' }"
      >
        <el-table-column prop="site" label="站点" align="center" min-width="8%">
        </el-table-column>
        <el-table-column
          prop="history_sales"
          :label="this.labelList[0]"
          align="center"
          min-width="10%"
        >
        </el-table-column>
        <el-table-column
          prop="pro_sales"
          :label="this.labelList[0]"
          align="center"
          min-width="10%"
        >
        </el-table-column>
        <el-table-column
          prop="throughput"
          :label="this.labelList[0]"
          align="center"
          min-width="10%"
        >
        </el-table-column>
        <el-table-column
          prop="cost"
          label="辐射成本(元)"
          align="center"
          min-width="10%"
        >
        </el-table-column>
        <el-table-column
          prop="o_throughput"
          :label="this.labelList[0]"
          align="center"
          min-width="10%"
        >
          <template slot-scope="scope">
            <span
              style="font-weight: 600"
              :style="
                scope.row.tCompare <= 0
                  ? { color: '#13ce66' }
                  : { color: 'red' }
              "
            >
              <i
                v-show="scope.row.site != '总和'"
                :class="
                  scope.row.tCompare <= 0 ? 'el-icon-bottom' : 'el-icon-top'
                "
              ></i>
              {{ scope.row.o_throughput }}
            </span>
          </template>
        </el-table-column>
        <el-table-column
          prop="o_cost"
          label="优化辐射成本(元)"
          align="center"
          min-width="10%"
        >
          <template slot-scope="scope">
            <span
              style="font-weight: 600"
              :style="
                scope.row.cCompare < 0 ? { color: '#13ce66' } : { color: 'red' }
              "
            >
              <i
                :class="
                  scope.row.cCompare < 0 ? 'el-icon-bottom' : 'el-icon-top'
                "
              ></i>
              {{ scope.row.o_cost }}
            </span>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <JobChat></JobChat>
  </div>
</template>
<script>
//这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）
//例如：import 《组件名称》 from '《组件路径》';
import axios from "axios";
import JobChat from "../../AI_chat/JobChat.vue";
export default {
  //import引入的组件需要注入到对象中才能使用
  components: {
    JobChat
  },
  data() {
    return {
      form: {
        type: "全年",
        is_limit: "吞吐量受限",
        method: "粒子群算法"
      },
      allData: [],
      // tableData: [],
      searchTableData: [],
      TableHeight: 2,
      // tableRadio: {},
      // isopenDialog: "false",
      title: "",
      loading: false,
      typeOptions: [
        { value: "全年", label: "全年" },
        { value: "二月", label: "二月" },
        { value: "十月", label: "十月" },
        { value: "十二月", label: "十二月" }
      ],
      limitOptions: [
        { value: "吞吐量受限", label: "吞吐量受限" },
        { value: "吞吐量不限", label: "吞吐量不限" }
      ],
      methodOptions: [
        { value: "粒子群算法", label: "粒子群算法" },
        { value: "模拟退火算法", label: "退火算法" },
        { value: "遗传算法", label: "遗传算法" }
      ],
      labelList: [
        "历史销量(年)",
        "对应省销量(年)",
        "吞吐量(年)",
        "优化吞吐量(年)"
      ],
      allCost: 0.0,
      allOptCost: 0.0,
      maxNum1: 1,
      maxNum2: 1
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
      const params = { ...this.form };
      // params.type = this.form.type;
      // params.limit = this.form.is_limit;
      // params.method = this.form.method;
      axios
        .post(this.baseurl + "/transport/cost", params)
        .then(res => {
          this.allData = res.data.data;
          const tempData = this.allData.all_data;
          const updatedData = [];
          tempData.forEach(obj => {
            const newObj = { ...obj }; // 创建新的对象并复制原对象的属性
            newObj["cCompare"] = newObj["o_cost"] - newObj["cost"]; // 添加 cCompare 属性
            newObj["tCompare"] = newObj["o_throughput"] - newObj["throughput"]; // 添加 tCompare 属性
            updatedData.push(newObj);
          });
          // 将更新后的数据赋值回 searchTableData 数组
          this.searchTableData = updatedData;

          //获取成本和优化后的成本
          this.allCost = this.searchTableData[
            this.searchTableData.length - 1
          ].cost;
          this.allOptCost = this.searchTableData[
            this.searchTableData.length - 1
          ].o_cost;

          //用来动态替换标签显示的年月
          if (this.form.type != "全年") {
            this.labelList.forEach((item, index) => {
              this.labelList[index] = item.replace("(年)", "(月)");
            });
          } else {
            if (this.labelList[0].includes("(月)"))
              this.labelList.forEach((item, index) => {
                this.labelList[index] = item.replace("(月)", "(年)");
              });
          }
        })
        .catch(error => console.log(error));
    },
    onSearch() {
      if (this.form.type == "") {
        this.$message({
          message: "时间不能为空",
          type: "error"
        });
      } else {
        this.maxNum1 = this.form.type == "全年" ? 1 : 10;
        this.maxNum2 = this.form.type == "全年" ? 1 : 10;
        this.loading = true;
        this.getData();
        setTimeout(() => {
          this.initCharts1();
          this.initCharts2();
          this.loading = false;
          this.$message.success("优化成功");
        }, 1000);
      }
    },
    downloadExcel() {
      if (
        this.form.type == "" &&
        this.form.is_limit == "" &&
        this.form.method == ""
      ) {
        this.$message({
          message: "优化方法不能为空",
          type: "error"
        });
      } else {
        let filename =
          this.form.type +
          "品牌车运输成本" +
          this.form.method +
          "优化结果.xlsx";
        axios({
          url: this.baseurl + "/transport/cost/download", // 替换为实际的后端接口
          method: "POST",
          responseType: "blob", // 设置响应类型为 blob
          data: {
            // method: this.form.programme,
            // 添加其他必要的参数
            type: this.form.type,
            is_limit: this.form.is_limit,
            method: this.form.method
          }
        })
          .then(response => {
            // console.log(response.data)
            if (response.data.size > 60) {
              const blob = new Blob([response.data]);
              saveAs(blob, filename);
              this.$message({
                message: "文件下载成功！！！",
                type: "success"
              });
            } else {
              this.$message({
                message: "文件下载失败！！！请先进行优化",
                type: "error"
              });
            }
          })
          .catch(error => {
            this.$message({
              message: "文件下载失败！！！",
              type: "error"
            });
            console.error("下载excel文件出错:", error);
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
    // // 表格选择当前显示行数
    // handleSizeChange(val) {
    //   this.pagesize = val;
    // },
    // // 切换表格页面
    // handleCurrentChange(val) {
    //   this.currentPage = val;
    // },
    // reset() {
    //   this.form.fault_name = "";
    //   this.form.fault_detection = "";
    //   this.form.severity_rating = "";
    //   this.getData();
    //   this.$message.success("已重置");
    // },
    initCharts1() {
      let option = {
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "cross",
            crossStyle: {
              color: "#999"
            }
          }
        },
        toolbox: {
          feature: {
            dataView: { show: true, readOnly: false },
            magicType: { show: true, type: ["line", "bar"] },
            restore: { show: true },
            saveAsImage: { show: true }
          }
        },
        legend: {
          data: ["辐射成本", "吞吐量"],
          textStyle: {
            color: "rgb(125, 180, 173)" //字体颜色
          }
        },
        xAxis: [
          {
            type: "category",
            data: this.allData.site,
            axisPointer: {
              type: "shadow"
            }
          }
        ],
        yAxis: [
          {
            type: "value",
            name: "辐射成本",
            min: 0,
            max: 1200 / this.maxNum1,
            interval: 200 / this.maxNum1,
            axisLabel: {
              fontSize: 9,
              formatter: "{value} 万元"
            }
          },
          {
            type: "value",
            name: "吞吐量",
            min: 0,
            max: 18000 / this.maxNum2,
            interval: 3000 / this.maxNum2,
            axisLabel: {
              fontSize: 9,
              formatter: "{value} 辆"
            }
          }
        ],
        series: [
          {
            name: "辐射成本",
            type: "bar",
            tooltip: {
              valueFormatter: function(value) {
                return value + " 元";
              }
            },
            data: this.allData.cost
          },
          {
            name: "吞吐量",
            type: "line",
            yAxisIndex: 1,
            tooltip: {
              valueFormatter: function(value) {
                return value + " 辆";
              }
            },
            data: this.allData.throughput
          }
        ]
      };
      const myChart = this.$echarts.init(this.$refs.partChart1);
      myChart.setOption(option);
      window.addEventListener("resize", () => {
        myChart.resize();
      });
    },
    initCharts2() {
      let option = {
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "cross",
            crossStyle: {
              color: "#999"
            }
          }
        },
        toolbox: {
          feature: {
            dataView: { show: true, readOnly: false },
            magicType: { show: true, type: ["line", "bar"] },
            restore: { show: true },
            saveAsImage: { show: true }
          }
        },
        legend: {
          data: ["辐射成本", "吞吐量"],
          textStyle: {
            color: "rgb(125, 180, 173)" //字体颜色
          }
        },
        xAxis: [
          {
            type: "category",
            data: this.allData.site,
            axisPointer: {
              type: "shadow"
            }
          }
        ],
        yAxis: [
          {
            type: "value",
            name: "辐射成本",
            min: 0,
            max: 1200 / this.maxNum1,
            interval: 200 / this.maxNum1,
            axisLabel: {
              fontSize: 9,
              formatter: "{value} 万元"
            }
          },
          {
            type: "value",
            name: "吞吐量",
            min: 0,
            max: 18000 / this.maxNum2,
            interval: 3000 / this.maxNum2,
            axisLabel: {
              fontSize: 9,
              formatter: "{value} 辆"
            }
          }
        ],
        series: [
          {
            name: "辐射成本",
            type: "bar",
            tooltip: {
              valueFormatter: function(value) {
                return value + " 元";
              }
            },
            data: this.allData.o_cost
          },
          {
            name: "吞吐量",
            type: "line",
            yAxisIndex: 1,
            tooltip: {
              valueFormatter: function(value) {
                return value + " 辆";
              }
            },
            data: this.allData.o_throughput
          }
        ]
      };
      const myChart = this.$echarts.init(this.$refs.partChart2);
      myChart.setOption(option);
      window.addEventListener("resize", () => {
        myChart.resize();
      });
    }
  },
  //生命周期 - 创建完成（可以访问当前this实例）
  created() {
    // this.getData();
  },
  //生命周期 - 挂载完成（可以访问DOM元素）
  mounted() {
    this.getData();
    //动态计算表格高度
    let windowHeight =
      document.documentElement.clientHeight || document.bodyclientHeight;
    this.$nextTick(() => {
      this.TableHeight = windowHeight - this.$refs.formDiv.offsetHeight - 175; //数值"140"根据需要调整
    });
    setTimeout(() => {
      this.initCharts1();
      this.initCharts2();
    }, 800);
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
.search {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
  margin-bottom: 10px;

  .searchCondition {
    width: 90%;

    .unitForm {
      display: flex;
      justify-content: left;
      align-items: center;
      flex-wrap: wrap;
      color: rgb(125, 180, 173);
      // width: 90%;

      .el-form-item {
        width: 27%;

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
  }

  .searchBtn {
    width: 24%;
    padding-right: 4%;
    font-size: 16px;
  }
}

.allChart {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  text-align: center;
  color: rgb(125, 180, 173);
  font-size: 19px;
  width: 92%;
  height: 310px;
  margin: 0 auto;

  .cost {
    font-size: 14px;
    font-weight: 600;
  }

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
      padding-top: 12px;
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
      padding-top: 12px;
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
