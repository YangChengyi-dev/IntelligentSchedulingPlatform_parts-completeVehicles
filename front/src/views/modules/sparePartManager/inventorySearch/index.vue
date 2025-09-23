<template>
  <div class="inventorySearch">
    <!-- 表单 -->
    <div ref="formDiv">
      <el-form ref="form" class="unitForm" :model="form" id="form">
        <el-form-item label="地市" prop="unitName">
          <el-select v-model="form.unitName" placeholder="请选择活动区域">
            <el-option label="区域一" value="shanghai"></el-option>
            <el-option label="区域二" value="beijing"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" size="small" @click="onSearch"
            >检索</el-button
          >
        </el-form-item>
      </el-form>
    </div>
    <!-- echarts -->
    <div class="echarts">
      <div class="bar">
        <h3 class="h">备件使用量TOP10</h3>
        <div class="echart" id="bar1" ref="bar1"></div>
      </div>
      <div class="bar">
        <h3 class="h">下季度备件使用量预测</h3>
        <table1 class="echart" height="90%" :table1Data="table1Data"></table1>
      </div>
      <div class="bar">
        <h3 class="h">备件库存数量告警</h3>
        <div class="echart" id="line1" ref="line1"></div>
      </div>
    </div>
    <div class="echarts table">
      <div class="bar">
        <h3 class="h">备件库存</h3>
        <table2 class="echart" height="90%" :table2Data="table2Data"></table2>
      </div>
      <div class="bar">
        <h3 class="h">换件记录</h3>
        <table3 class="echart" height="90%" :table3Data="table3Data"></table3>
      </div>
    </div>
  </div>
</template>
<script>
import table1 from "./table1";
import table2 from "./table2";
import table3 from "./table3";
export default {
  name: "unitManagement",
  components: {
    table1,
    table2,
    table3,
  },
  data() {
    return {
      form: {
        unitName: "",
        marketName: "",
        unitType: "",
        status: "",
        startTime: "",
      },

      table1Data: [],
      table2Data: [],
      table3Data: [],
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
    setTimeout(() => {
      this.bar1();
      this.line1();
    }, 0);
  },
  methods: {
    // 获取数据
    getData() {
      this.$http({
        url: `static/json/sparePartManager/inventorySearch.json`,
        method: "get",
        data: {},
      }).then((res) => {
        this.table1Data = res.data.table1Data;
        this.table2Data = res.data.table2Data;
        this.table3Data = res.data.table3Data;
      });
    },
    // 表单查询
    onSearch() {
      // this.searchTableData = this.tableRes(this.form.unitName, this.tableData);
      // this.total = this.searchTableData.length;
      // this.currentPage = 1;
      this.$message("查询");
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

    bar1() {
      const color = ["#3ba272", "#91cc75", "#fac858", "#ee6666", "#73c0de"]; //2个以上的series就需要用到color数组
      const legend = {
        show: true,
        //data，就是取得每个series里面的name属性。
        orient: "horizontal",
        icon: "react", //图例形状
        padding: 0,
        top: 15,
        right: "center",
        itemWidth: 20, //小圆点宽度
        itemHeight: 14, // 小圆点高度
        borderRadius: 20,
        itemGap: 21, // 图例每项之间的间隔。[ default: 10 ]横向布局时为水平间隔，纵向布局时为纵向间隔。
        textStyle: {
          fontSize: 14,
          color: "#fff",
        },
      };
      const tooltip = {
        show: true,
        trigger: "axis",
        axisPointer: {
          type: "shadow",
        },
      };
      const originData = [
        { name: "使用量", data: [620, 732, 701, 734, 1090, 1130, 1120] },
        { name: "库存量", data: [120, 132, 101, 134, 290, 230, 220] },
      ];
      const commonSeriesFn = (index) => ({
        type: "bar",
        barWidth: "40%", //柱条的宽度，不设时自适应。
        // stack: 'total',
        emphasis: {
          focus: "series",
          itemStyle: {
            shadowColor: "rgba(0, 0, 0, 0.5)",
            shadowBlur: 8,
            shadowOffsetX: 2,
            shadowOffsetY: 2,
          },
        },

        showBackground: false, //柱子是否带有背景，默认是没有的
        backgroundStyle: {
          //只有showBackground=true，设置backgroundStyle才会有效果
          color: "rgba(180, 180, 180, .2)", //
        },
      });
      const series = originData.map((item, index) => ({
        ...item,
        ...commonSeriesFn(index),
      }));
      const option = {
        color,
        legend,
        tooltip,
        grid: {
          top: "15%",
          left: "3%",
          right: "4%",
          bottom: "10%",
          containLabel: true,
        },
        xAxis: {
          type: "value",
          axisLabel: {
            margin: 10,
            color: "#7e9fb6",
            textStyle: {
              fontSize: 14,
            },
          },
          axisLine: {
            show: true, //显示X轴
          },
          axisTick: {
            show: false, //不显示小的刻度线
          },
          splitLine: {
            show: true, //不显示横向分割线
            lineStyle: {
              color: "rgba(126,159,182,0.12)",
            },
          },
        },
        yAxis: {
          type: "category",
          axisLabel: {
            color: "#7e9fb6",
          },
          axisLine: {
            show: false, //显示Y轴
          },
          axisTick: {
            show: false, //不显示小的刻度线
          },
          splitLine: {
            show: false, //不显示竖向分割线
          },
          data: ["南通市", "苏州市", "常州市", "徐州市", "无锡市", "南京市"],
        },

        series,
      };
      const myChart = this.$echarts.init(this.$refs.bar1);
      myChart.setOption(option);
      window.addEventListener("resize", () => {
        myChart.resize();
      });
    },
    line1() {
      const option = {
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "shadow",
          },
        },
        legend: {
          textStyle: {
            fontSize: 14,
            color: "#fff",
          },
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true,
        },
        xAxis: [
          {
            type: "category",
            axisLine: {
              lineStyle: {
                color: "#7e9fb6",
              },
            },
            axisLabel: {
              margin: 10,
              rotate: 25,
              color: "#7e9fb6",
              textStyle: {
                fontSize: 14,
              },
            },
            data: [
              "充电枪",
              "充电控制器",
              "液晶屏",
              "充点模块",
              "电能表",
              "分流器",
              "采集通信单元",
            ],
          },
        ],
        yAxis: [
          {
            type: "value",
            axisLabel: {
              color: "#7e9fb6",
            },
            axisLine: {
              show: false,
              lineStyle: {
                color: "#7e9fb6",
              },
            },
            splitLine: {
              lineStyle: {
                color: "rgba(126,159,182,0.12)",
              },
            },
          },
        ],
        series: [
          {
            name: "库存量",
            type: "bar",
            data: [320, 332, 301, 334, 390, 330, 320],
          },

          {
            name: "预测用量",
            type: "bar",
            data: [862, 1018, 964, 1026, 1679, 1600, 1570],
            emphasis: {
              focus: "series",
            },
          },
        ],
      };
      const myChart = this.$echarts.init(this.$refs.line1);
      myChart.setOption(option);
      window.addEventListener("resize", () => {
        myChart.resize();
      });
    },
  },
};
</script>
<style lang="scss">
.inventorySearch {
  .unitForm {
    display: flex;
    // justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    .el-form-item {
      width: 24%;
      .el-form-item__label {
        width: 40%;
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
      padding: 0 5px;
      .h {
        height: 8%;
        padding-bottom: 5px;
      }
      .h::before {
        content: "";
        width: 3px;
        height: 100%;
        background: #15a193;
        display: inline-block;
        vertical-align: middle;
        margin-right: 5px;
      }
      .echart {
        height: 90%;
      }
    }
  }
  .table {
    height: 50vh;
  }
}
</style>
