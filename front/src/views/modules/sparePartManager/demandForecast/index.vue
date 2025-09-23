<template>
  <div class="demandForecast">
    <!-- 表单 -->
    <div ref="formDiv">
      <el-form ref="form" class="unitForm" :model="form" id="form">
        <el-form-item label="地市:" prop="unitName">
          <el-select v-model="form.unitName" placeholder="请选择">
            <el-option label="南京" value="南京"></el-option>
            <el-option label="无锡" value="无锡"></el-option>
            <el-option label="苏州" value="苏州"></el-option>
            <el-option label="淮安" value="淮安"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="备件类别:" prop="linkman">
          <el-select v-model="form.linkman" placeholder="请选择">
            <el-option label="充电控制器" value="充电控制器"></el-option>
            <el-option label="液晶屏" value="液晶屏"></el-option>
            <el-option label="充电模块" value="充电模块"></el-option>
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
    <table-first :table1Data="searchTableData" height="35vh"></table-first>
    <div class="echarts">
      <div id="bar" class="bar" ref="bar"></div>
    </div>
    <div>
      <h3>采购计划</h3>
      <table-second :table2Data="searchTableData2" height="20vh"></table-second>
    </div>
  </div>
</template>

<script>
import tableFirst from "./table";
import tableSecond from "./table2";
export default {
  name: "unitManagement",
  components: { tableFirst, tableSecond },
  data() {
    return {
      form: {
        unitName: "",
        linkman: "",
      },

      table1Data: [],
      searchTableData: [],
      table2Data: [],
      searchTableData2: [],
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
    }, 0);
  },
  methods: {
    // 获取数据
    getData() {
      this.$http({
        url: `static/json/sparePartManager/demandForecast.json`,
        method: "get",
        data: {},
      }).then((res) => {
        const data = res.data.table1Data;
        this.table1Data = data;
        this.searchTableData = data;

        this.table2Data = res.data.table2Data;
        this.searchTableData2 = res.data.table2Data;
      });
    },

    // 表单查询
    onSearch() {
      this.searchTableData = this.tableRes(this.form.unitName, this.table1Data);
      this.searchTableData2 = this.tableRes(this.form.unitName, this.table2Data);
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
      var xData = [
        "2020-10",
        "2020-11",
        "2020-12",
        "2021-01",
        "2021-02",
        "2021-03",
        "2021-04",
        "2021-15",
        "2021-16",
        "2021-17",
      ];
      var data = {
        bqs: [95284.5, 110640.25, 88141.5, 111738.25, 27134.25, 0, 0, 0, 0, 0],
        hbl: [15, 17, 20, 27, 75, 100, 100, 100, 100, 100],
        sqs: [83108.5, 95284.5, 110640.25, 88141.5, 111738.25, 27134.25, 0, 0, 0, 0],
        tbl: [248, 98, 66, 53, 63, 100, 100, 100, 100, 100],
        tqs: [
          27425,
          55983.25,
          53158,
          73186,
          74439.75,
          86922.75,
          107109.25,
          102578.5,
          126522.25,
          123338.75,
        ],
      };
      let series = [];

      series = [
        {
          type: "bar",
          name: "充电控制器",
          yAxisIndex: 0,
          itemStyle: {
            color: "#15a193",
          },
          barWidth: 16,
          data: data.bqs,
        },
        {
          type: "bar",
          name: "液晶屏",
          yAxisIndex: 0,
          itemStyle: {
            color: "#17d799",
          },
          barWidth: 16,
          data: data.tqs,
        },

        {
          name: "充电模块",
          yAxisIndex: 1,
          type: "line",
          stack: "总量",
          smooth: true,
          data: data.hbl,
          symbolSize: 8,
        },
      ];
      const option = {
        color: ["#3ba272", "#91cc75"],
        title: {
          text: "近一年备件量变化走势",
          textStyle: {
            color: "#fff",
          },
        },
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "shadow",
          },
          borderWidth: 1,
        },

        grid: {
          left: "20px",
          right: "20px",
          top: "20%",
          bottom: "20px",
          containLabel: true,
        },
        xAxis: [
          {
            type: "category",
            boundaryGap: true,

            data: xData,
            axisLine: {
              lineStyle: {
                color: "#7e9fb6",
              },
            },
            axisLabel: {
              margin: 10,
              color: "#7e9fb6",
              textStyle: {
                fontSize: 14,
              },
            },
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
            axisTick: {
              show: false,
            },
          },
          {
            type: "value",
            axisLabel: {
              color: "#7e9fb6",
              formatter: "{value}%",
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
            axisTick: {
              show: false,
            },
          },
        ],
        series: series,
      };
      const myChart = this.$echarts.init(this.$refs.bar);
      myChart.setOption(option, true);
      window.addEventListener("resize", () => {
        myChart.resize();
      });
    },
  },
};
</script>
<style lang="scss">
.demandForecast {
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

  h3 {
    margin-bottom: 10px;
  }
}
</style>
