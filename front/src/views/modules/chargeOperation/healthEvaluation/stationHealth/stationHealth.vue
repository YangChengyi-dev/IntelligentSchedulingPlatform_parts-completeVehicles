<!--  -->
<template>
  <div id="app">
    <div ref="formDiv">
      <el-form ref="form" class="unitForm" :model="form" id="form">
        <el-form-item label="预测方式:">
          <el-select v-model="form.method" clearable placeholder="请选择">
            <el-option
              v-for="item in methodOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="开始时间:">
          <el-date-picker
            v-model="form.start"
            type="month"
            value-format="yyyy/MM"
            placeholder="请选择"
          ></el-date-picker>
        </el-form-item>
        <el-form-item label="结束时间:">
          <el-date-picker
            v-model="form.end"
            type="month"
            value-format="yyyy/MM"
            placeholder="请选择"
          ></el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            icon="el-icon-search"
            size="small"
            @click="onSearch"
            >预测</el-button
          >
          <el-button
            class="iconfont icon-xiazai"
            type="primary"
            size="small"
            @click="downloadExcel"
            >下载</el-button
          >
          <el-button
            class="iconfont icon-huifu"
            type="primary"
            size="small"
            @click="restore()"
            >&nbsp;返回</el-button
          >
        </el-form-item>
      </el-form>
    </div>
    <!-- 表格 -->
    <el-table
      class="table"
      v-show="isRegress"
      :data="
        searchTableData.slice(
          (currentPage - 1) * pagesize,
          currentPage * pagesize
        )
      "
      ref="table"
      id="table"
      stripe
      :header-row-style="{ height: '35px' }"
      :row-style="{ height: '35px' }"
      :height="TableHeight"
      @row-click="queryRecord"
    >
      <el-table-column type="selection" label="" align="center" min-width="8%">
      </el-table-column>
      <el-table-column prop="id" label="序号" align="center" min-width="10%">
      </el-table-column>
      <el-table-column
        prop="operate"
        label="操作"
        align="center"
        min-width="20%"
      >
      </el-table-column>
      <el-table-column
        prop="create_time"
        label="创建时间"
        align="right"
        min-width="10%"
      >
      </el-table-column>
      <el-table-column align="right" min-width="5%">
        <template slot-scope="scope">
          <i
            class="el-icon-delete delete-icon"
            @click.stop="handleDelete(scope.row)"
          ></i>
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        </template>
      </el-table-column>
    </el-table>
    <!-- 分页 -->
    <el-pagination
      v-show="isRegress"
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
    <div
      class="gdzsDiv"
      v-loading="loading"
      element-loading-text="正在预测中..."
      element-loading-spinner="el-icon-loading"
      element-loading-background="rgba(0, 0, 0, 0.8)"
    ></div>
    <div v-show="!isRegress" class="gdzsDiv">
      <div class="chartTitle">一汽销量预测</div>
      <div class="gdzsChart" ref="gdzsChart"></div>
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
        method: "",
        start: "",
        end: ""
      },
      searchFormParams: {
        method: null,
        start: null,
        end: null
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
      selected: "",
      isRegress: true,
      loading: false,
      regressData: {},
      hovered: false,

      methodOptions: [
        { value: "线性回归", label: "线性回归" },
        { value: "多元线性回归", label: "多元线性回归" },
        { value: "随机森林回归", label: "随机森林回归" },
        { value: "弹性网络回归", label: "弹性网络回归" },
        { value: "支持向量机回归", label: "支持向量机回归" },
        { value: "循环神经网络", label: "循环神经网络" }
      ]
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
        url: this.baseurl + "/sales/index",
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
      let [startYear, startMonth] = this.form.start.split("/");
      let [endYear, endMonth] = this.form.end.split("/");
      if (
        this.form.method == "" ||
        this.form.start == "" ||
        this.form.end == ""
      ) {
        this.$message({
          message: "预测方法不能为空",
          type: "error"
        });
      } else if (
        endYear < startYear ||
        (endYear == startYear && endMonth < startMonth)
      ) {
        this.$message({
          message: "日期输入错误，请重新输入！！！",
          type: "error"
        });
      } else {
        this.loading = true;
        const params = { ...this.searchFormParams };
        params.method = this.form.method;
        params.start = this.form.start;
        params.end = this.form.end;
        console.log(params);
        axios.post(this.baseurl + "/sales/regress", params).then(res => {
          const allDatas = res.data.data;
          // console.log(datas);
          this.tableData = allDatas.regress_record;
          this.searchTableData = allDatas.regress_record;
          // 获取表格数据总数量
          this.total = this.searchTableData.length;
          this.regressData = allDatas.regress_result;
          console.log(this.regressData);
        });

        this.isRegress = false;
        setTimeout(() => {
          this.loading = false;
          this.initGdzsChart();
        }, 2000);
        this.$message({
          message: "预测成功",
          type: "success"
        });
      }
    },
    // 点击查询之前预测的图表
    queryRecord(row) {
      this.regressData = row.regress_data;
      this.isRegress = false;
      setTimeout(() => {
        this.initGdzsChart();
      }, 50);
    },
    handleDelete(row) {
      axios
        .post(this.baseurl + "/sales/delete", {
          delId: row.id,
          filename: row.operate
        })
        .then(res => {
          if (res.data.code == 200) {
            this.$message({
              message: "删除成功",
              type: "success"
            });
            // 找到要删除元素的索引
            let index = this.searchTableData.findIndex(
              item => item.id === row.id
            );
            // 如果找到了索引，则从数组中删除该元素
            if (index !== -1) {
              this.searchTableData.splice(index, 1);
            }
          } else {
            this.$message({
              message: "删除失败",
              type: "error"
            });
          }
        })
        .catch(error => console.log(error));
    },
    restore() {
      this.isRegress = true;
    },

    // 表格选择当前显示行数
    handleSizeChange(val) {
      this.pagesize = val;
    },
    // 切换表格页面
    handleCurrentChange(val) {
      this.currentPage = val;
    },
    getIndexUrl() {
      var searchUrl = window.location.search;
      if (
        typeof searchUrl == "undefined" ||
        searchUrl == null ||
        searchUrl == ""
      ) {
      } else {
        this.selected = searchUrl.split("=")[1];
      }
    },
    fixMap() {
      this.$router.push({ name: "销售量预测" });
    },
    initGdzsChart() {
      let xData = this.regressData.time;
      let yData = this.regressData.result;
      console.log(xData, yData);
      const option = {
        tooltip: {
          trigger: "axis",
          axisPointer: {
            lineStyle: {
              color: "#fff"
            }
          }
        },
        legend: {
          right: "3%",
          textStyle: {
            fontSize: 14,
            color: "#fff"
          }
        },
        xAxis: [
          {
            type: "category",
            axisLine: {
              lineStyle: {
                color: "rgba(255,255,255,.5)"
              }
            },
            splitLine: {
              show: false
            },
            axisTick: {
              show: false
            },
            splitArea: {
              show: false
            },
            axisLabel: {
              interval: 0,
              color: "rgba(255,255,255,0.7)",
              fontSize: 12
            },
            data: xData
          }
        ],
        yAxis: [
          {
            type: "value",
            scale: true,
            min: 0,
            max: 140000,
            interval: 20000,
            splitLine: {
              show: true,
              lineStyle: {
                type: "dashed",
                color: "RGBA(3, 75, 97, 1)"
              }
            },
            axisLine: {
              show: false
            },
            axisTick: {
              show: false
            },
            axisLabel: {
              interval: 0,
              color: "rgba(255,255,255,0.5)",
              fontSize: 12
            },
            splitArea: {
              show: false
            }
          }
        ],
        series: [
          {
            name: "销量",
            type: "line",
            smooth: true,
            symbol: "circle",
            symbolSize: 5,
            showSymbol: false,
            zlevel: 1,
            z: 1,
            lineStyle: {
              normal: {
                width: 1
              }
            },
            areaStyle: {
              normal: {
                color: new echarts.graphic.LinearGradient(
                  0,
                  0,
                  0,
                  1,
                  [
                    {
                      offset: 0,
                      color: "rgba(0, 136, 212, 0.3)"
                    },
                    {
                      offset: 0.8,
                      color: "rgba(0, 136, 212, 0)"
                    }
                  ],
                  false
                ),
                shadowColor: "rgba(0, 0, 0, 0.1)",
                shadowBlur: 10
              }
            },
            itemStyle: {
              normal: {
                color: "rgb(0,136,212)",
                borderColor: "rgba(0,136,212,0.2)",
                borderWidth: 12
              }
            },
            data: yData
          }
        ]
      };
      const myChart = this.$echarts.init(this.$refs.gdzsChart);
      myChart.setOption(option);
      window.addEventListener("resize", () => {
        myChart.resize();
      });
    },
    downloadExcel() {
      let [startYear, startMonth] = this.form.start.split("/");
      let [endYear, endMonth] = this.form.end.split("/");
      if (
        this.form.method == "" ||
        this.form.start == "" ||
        this.form.end == ""
      ) {
        this.$message({
          message: "预测方法不能为空",
          type: "error"
        });
      } else if (
        endYear < startYear ||
        (endYear == startYear && endMonth < startMonth)
      ) {
        this.$message({
          message: "日期输入错误，请重新输入！！！",
          type: "error"
        });
      } else {
        this.form.start = this.form.start.replace("/", "-");
        this.form.end = this.form.end.replace("/", "-");
        let filename =
          this.form.method +
          "预测" +
          this.form.start +
          "~" +
          this.form.end +
          ".xlsx";
        // console.log(this.form)
        axios({
          url: this.baseurl + "/sales/download", // 替换为实际的后端接口
          method: "POST",
          responseType: "blob", // 设置响应类型为 blob
          data: {
            method: this.form.method,
            start: this.form.start,
            end: this.form.end
          }
        })
          .then(response => {
            console.log(response.data);
            if (response.data.size > 60) {
              console.log(response.data.size);
              const blob = new Blob([response.data]);
              saveAs(blob, filename);
              this.$message({
                message: "文件下载成功！！！",
                type: "success"
              });
            } else {
              this.$message({
                message: "文件下载失败！！！请先进行预测",
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
    }
  },
  //生命周期 - 创建完成（可以访问当前this实例）
  created() {
    this.getData();
    // this.getSearchData();
  },
  //生命周期 - 挂载完成（可以访问DOM元素）
  mounted() {
    //动态计算表格高度
    let windowHeight =
      document.documentElement.clientHeight || document.bodyclientHeight;
    this.getIndexUrl();
    this.$nextTick(() => {
      this.TableHeight = windowHeight - this.$refs.formDiv.offsetHeight - 170; //数值"140"根据需要调整
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

// .toolbar {
//   display: flex;
//   align-items: center;
//   justify-content: space-between;
//   padding-bottom: 15px;

//   .btnGroup {
//     width: 35%;
//   }
// }

.table {
  width: 96%;
  margin-left: 2%;

  .delete-icon {
    color: rgb(247, 137, 137);
    visibility: hidden;
  }

  tbody tr:hover .delete-icon {
    visibility: visible;
    cursor: pointer;
  }
}

.gdzsDiv {
  position: absolute;
  top: 10%;
  left: 8%;
  width: 80%;
  height: 80%;
  // background-color: #00bbee;

  .chartTitle {
    position: absolute;
    top: 2%;
    left: 6%;
    width: 100%;
    height: 20%;
    color: #00bbee;
    font-size: 16px;
    font-weight: bold;
  }

  .gdzsChart {
    position: absolute;
    top: 5%;
    left: 6%;
    width: 90%;
    height: 90%;
    // background-color: #15a193;
  }
}
</style>
