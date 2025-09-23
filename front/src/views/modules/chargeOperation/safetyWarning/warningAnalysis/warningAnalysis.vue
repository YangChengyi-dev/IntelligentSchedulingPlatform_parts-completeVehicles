<template>
  <div class="warningAnalysis">
    <div>
      <el-button
        type="primary"
        icon="el-icon-search"
        size="small"
        @click="onSearch"
        style="margin-left: 75%"
        >{{ searchTitle }}</el-button
      >
      <div class="single" v-if="change">
        <div class="experiment">
          <div class="title">整车多式联运实验结果</div>
          <el-table
            :data="tableData1"
            id="table"
            stripe
            style="width: 86%; margin: 0 auto;margin-top: 20px;"
            :header-row-style="{ height: '50px' }"
            :row-style="{ height: '50px' }"
          >
            <el-table-column
              prop="method"
              label="算法"
              align="center"
              min-width="10%"
            >
            </el-table-column>
            <el-table-column
              prop="route"
              label="运输路线"
              align="center"
              min-width="12%"
            >
            </el-table-column>
            <el-table-column
              prop="way"
              label="运输方式"
              align="center"
              min-width="10%"
            >
            </el-table-column>
            <el-table-column
              prop="totalCost"
              label="总成本"
              align="center"
              min-width="10%"
            >
              <template slot-scope="scope">
                <span
                  style="font-weight: 600"
                  :style="
                    scope.row.compare
                      ? { color: '#13ce66' }
                      : { color: '#ffffff' }
                  "
                >
                  <span v-if="scope.row.compare"
                    ><i class="el-icon-bottom"></i
                  ></span>
                  {{ scope.row.totalCost }}
                </span>
              </template>
            </el-table-column>
            <el-table-column
              prop="carbonCost"
              label="碳排放成本"
              align="center"
              min-width="10%"
            >
              <template slot-scope="scope">
                <span
                  style="font-weight: 600"
                  :style="
                    scope.row.compare
                      ? { color: '#13ce66' }
                      : { color: '#ffffff' }
                  "
                >
                  <span v-if="scope.row.compare"
                    ><i class="el-icon-bottom"></i
                  ></span>
                  {{ scope.row.carbonCost }}
                </span>
              </template>
            </el-table-column>
            <el-table-column
              prop="cost"
              label="燃烧消耗成本"
              align="center"
              min-width="10%"
            >
              <template slot-scope="scope">
                <span
                  v-if="scope.row.timeCompare"
                  style="font-weight: 600"
                  :style="
                    scope.row.compare
                      ? { color: '#13ce66' }
                      : { color: '#ffffff' }
                  "
                >
                  <span v-if="scope.row.compare"
                    ><i class="el-icon-bottom"></i
                  ></span>
                  {{ scope.row.cost }}
                </span>
                <span
                  v-else
                  style="font-weight: 600"
                  :style="
                    scope.row.compare ? { color: 'red' } : { color: '#ffffff' }
                  "
                >
                  <span v-if="scope.row.compare"
                    ><i class="el-icon-top"></i
                  ></span>
                  {{ scope.row.cost }}
                </span>
              </template>
            </el-table-column>
            <el-table-column
              prop="timeCost"
              label="时间惩罚成本"
              align="center"
              min-width="10%"
            >
              <template slot-scope="scope">
                <span
                  v-if="scope.row.timeCompare"
                  style="font-weight: 600"
                  :style="
                    scope.row.compare
                      ? { color: '#13ce66' }
                      : { color: '#ffffff' }
                  "
                >
                  <span v-if="scope.row.compare"
                    ><i class="el-icon-bottom"></i
                  ></span>
                  {{ scope.row.timeCost }}
                </span>
                <span
                  v-else
                  style="font-weight: 600"
                  :style="
                    scope.row.compare ? { color: 'red' } : { color: '#ffffff' }
                  "
                >
                  <span v-if="scope.row.compare"
                    ><i class="el-icon-top"></i
                  ></span>
                  {{ scope.row.timeCost }}
                </span>
              </template>
            </el-table-column>
          </el-table>
        </div>
        <div class="statistics">
          <div class="title">真实销售案例统计表</div>
          <el-table
            :data="tableData2"
            id="table2"
            stripe
            style="width: 86%; margin: 0 auto;margin-top: 20px;"
            :header-row-style="{ height: '50px' }"
            :row-style="{ height: '50px' }"
          >
            <el-table-column
              prop="route"
              label="路线"
              align="center"
              min-width="8%"
            >
            </el-table-column>
            <el-table-column
              prop="month"
              label="月份"
              align="center"
              min-width="5%"
            >
            </el-table-column>
            <el-table-column
              prop="sales"
              label="销量"
              align="center"
              min-width="5%"
            >
            </el-table-column>
            <!-- <el-table-column label="不同优化算法优化结果(路径、运输方式、成本)" align="center" min-width="80%"> -->
            <el-table-column
              prop="aco"
              label="蚁群"
              align="center"
              min-width="14%"
            >
              <template slot-scope="{ row }">
                <span v-html="formatText(row.aco)"></span>
              </template>
            </el-table-column>
            <el-table-column
              prop="sa"
              label="遗传"
              align="center"
              min-width="12%"
            >
              <template slot-scope="{ row }">
                <span v-html="formatText(row.sa)"></span>
              </template>
            </el-table-column>
            <el-table-column
              prop="pso"
              label="粒子群"
              align="center"
              min-width="12%"
            >
              <template slot-scope="{ row }">
                <span v-html="formatText(row.pso)"></span>
              </template>
            </el-table-column>
            <el-table-column
              prop="scso"
              label="沙猫算法"
              align="center"
              min-width="12%"
            >
              <template slot-scope="{ row }">
                <span v-html="formatText(row.scso)"></span>
              </template>
            </el-table-column>
            <el-table-column
              prop="hscso"
              label="混合沙猫算法"
              align="center"
              min-width="14%"
            >
              <template slot-scope="{ row }">
                <span v-html="formatText(row.hscso)"></span>
              </template>
            </el-table-column>
            <!-- </el-table-column> -->
          </el-table>
        </div>
      </div>
      <div class="multi " v-else>
        <div class="empty">
          <div class="experiment">
            <div class="title">多末端节点优化图</div>
            <div ref="emptycharts" class="charts"></div>
          </div>
          <el-table
            :data="tableData"
            id="table"
            stripe
            style="width: 86%; margin: 0 auto;margin-top: 20px;"
            :header-row-style="{ height: '50px' }"
            :row-style="{ height: '50px' }"
          >
            <el-table-column
              prop="site"
              label="站点"
              align="center"
              min-width="10%"
            >
            </el-table-column>
            <el-table-column
              prop="site_sales"
              label="站点销量"
              align="center"
              min-width="10%"
            >
            </el-table-column>
            <el-table-column
              prop="prov_sales"
              label="省销量"
              align="center"
              min-width="10%"
            >
            </el-table-column>
            <el-table-column
              prop="capacity"
              label="运力"
              align="center"
              min-width="10%"
            >
            </el-table-column>
            <el-table-column
              prop="cost"
              label="成本"
              align="center"
              min-width="10%"
            >
            </el-table-column>
            <el-table-column
              prop="o_capacity"
              label="运力"
              align="center"
              min-width="10%"
            >
              <template slot-scope="scope">
                <span
                  :style="
                    scope.row.o_capacity <= scope.row.capacity
                      ? { color: '#13ce66' }
                      : { color: 'red' }
                  "
                >
                  <i
                    :class="
                      scope.row.o_capacity <= scope.row.capacity
                        ? 'el-icon-bottom'
                        : 'el-icon-top'
                    "
                  ></i>
                  {{ scope.row.o_capacity }}
                </span>
              </template>
            </el-table-column>
            <el-table-column
              prop="o_cost"
              label="优化成本"
              align="center"
              min-width="10%"
            >
              <template slot-scope="scope">
                <span
                  :style="
                    scope.row.o_cost < scope.row.cost
                      ? { color: '#13ce66' }
                      : { color: 'red' }
                  "
                >
                  <i
                    :class="
                      scope.row.o_cost < scope.row.cost
                        ? 'el-icon-bottom'
                        : 'el-icon-top'
                    "
                  ></i>
                  {{ scope.row.o_cost }}
                </span>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </div>
    <JobChat></JobChat>
  </div>
</template>

<script>
// import Dialog from "./dialog";
import JobChat from "../../AI_chat/JobChat.vue";
export default {
  name: "unitManagement",
  components: {
    JobChat
  },
  data() {
    return {
      change: true,
      searchTitle: "多末端节点优化",
      tableData1: [
        {
          method: "沙猫群算法",
          route: "长春->徐州->嘉兴",
          way: "铁路->公路",
          totalCost: "3571000",
          carbonCost: "20649.9",
          cost: "22624.2",
          timeCost: "3652.7",
          compare: false,
          timeCompare: true
        },
        {
          method: "混合沙猫群算法",
          route: "长春->大连->上海->嘉兴",
          way: "铁路->水路->公路",
          totalCost: "2630800",
          carbonCost: "7351.9",
          cost: "73256.9",
          timeCost: "16921.7",
          compare: true,
          timeCompare: false
        },
        {
          method: "沙猫群算法",
          route: "长春->大连->上海->福州",
          way: "铁路->水路->公路",
          totalCost: "3964600",
          carbonCost: "24957.9",
          cost: "283979.9",
          timeCost: "22348.1",
          compare: false,
          timeCompare: true
        },
        {
          method: "混合沙猫群算法",
          route: "长春->大连->宁波->福州",
          way: "铁路->水路->公路",
          totalCost: "3618200",
          carbonCost: "14538.9",
          cost: "159277.4",
          timeCost: "20230.5",
          compare: true,
          timeCompare: true
        }
      ],
      tableData2: [
        {
          route: "长春—>嘉兴",
          month: "2月",
          sales: "911",
          aco: "长春—大连—宁波—嘉兴<br>（铁—水—公）<br>2669958.8",
          sa: "长春—济南—嘉兴<br>(铁—公)<br>3300735.2",
          pso: "长春—上海—嘉兴<br>(铁—公)<br>3306565.6",
          scso: "长春—上海—嘉兴<br>(铁—公)<br>3306565.6",
          hscso: "长春—大连—上海—嘉兴<br>(铁—水—公)<br>2474928.4"
        },
        {
          route: "长春—>嘉兴",
          month: "10月",
          sales: "1258",
          aco: "长春—大连—上海—苏州—嘉兴<br>（铁—水—公—公）<br>3539760.4",
          sa: "长春—金华—嘉兴<br>(公—公)<br>4566036.8",
          pso: "长春—上海—嘉兴<br>(铁—公)<br>4566036.8",
          scso: "长春—临沂—嘉兴<br>(公—公)<br>4816630.4",
          hscso: "长春—大连—上海—嘉兴<br>(铁—水—公)<br>3416813.5"
        },
        {
          route: "长春—>嘉兴",
          month: "12月",
          sales: "1448",
          aco: "长春—大连—上海—嘉兴<br>（铁—水—公）<br>3932478.4",
          sa: "长春—烟台—嘉兴<br>(公—公)<br>5478652.8",
          pso: "长春—济南—嘉兴<br>(铁—公)<br>5246393.6",
          scso: "长春—上海—嘉兴<br>(铁—公)<br>5253888.5",
          hscso: "长春—大连—上海—嘉兴<br>(铁—水—公)<br>3932478.4"
        },
        {
          route: "长春—>福州",
          month: "2月",
          sales: "669",
          aco: "长春—芜湖—福州<br>（铁—公）<br>3325006.1",
          sa: "长春—芜湖—福州<br>（铁—公）<br>3325006.1",
          pso: "长春—大连—上海—福州<br>(铁—水—公)<br>3608097.0",
          scso: "长春—芜湖—福州<br>（铁—公）<br>3325006.1",
          hscso: "长春—大连—宁波—福州<br>(铁—水—公)<br>2689533.2"
        },
        {
          route: "长春—>福州",
          month: "10月",
          sales: "924",
          aco: "长春—大连—上海—福州<br>（公—水—公）<br>5553838.7",
          sa: "长春—芜湖—福州<br>(铁—公)<br>4592385.0",
          pso: "长春—大连—福州<br>(铁—公)<br>4867491.6",
          scso: "长春—大连—上海—福州<br>（铁—水—公）<br>4070338.0",
          hscso: "长春—大连—宁波—福州<br>（铁—水—公）<br>3714691.6"
        },
        {
          route: "长春—>福州",
          month: "12月",
          sales: "1064",
          aco: "长春—大连—福州<br>（铁—公）<br>5477502.2",
          sa: "长春—芜湖—福州<br>(铁—公)<br>5288200.9",
          pso: "长春—徐州—福州<br>(铁—公)<br>6394736.5",
          scso: "长春—芜湖—福州<br>(铁—公)<br>5288200.9",
          hscso: "长春—大连—宁波—福州<br>(铁—水—公)<br>4277523.7"
        }
      ],
      tableData: [
        {
          site: "杭州",
          site_sales: 22502,
          prov_sales: 69329,
          capacity: 78,
          cost: 18654919,
          o_capacity: 121,
          o_cost: 9820176
        },
        {
          site: "济南",
          site_sales: 22412,
          prov_sales: 49255,
          capacity: 78,
          cost: 8046222,
          o_capacity: 0,
          o_cost: 14929342
        },
        {
          site: "芜湖",
          site_sales: 11209,
          prov_sales: 27316,
          capacity: 39,
          cost: 16819158,
          o_capacity: 85,
          o_cost: 1850633
        },
        {
          site: "徐州",
          site_sales: 17537,
          prov_sales: 45734,
          capacity: 61,
          cost: 11935479,
          o_capacity: 50,
          o_cost: 12992048
        },
        {
          site: "宁波(水)",
          site_sales: 19701,
          prov_sales: 69329,
          capacity: 20,
          cost: 18654919,
          o_capacity: 30,
          o_cost: 9820176
        },
        {
          site: "上海(水)",
          site_sales: 33943,
          prov_sales: 33943,
          capacity: 34,
          cost: 5134175,
          o_capacity: 28,
          o_cost: 6852363
        },
        {
          site: "烟台(水)",
          site_sales: 3213,
          prov_sales: 49255,
          capacity: 4,
          cost: 8046222,
          o_capacity: 0,
          o_cost: 14929342
        },
        {
          site: "总计",
          site_sales: "——",
          prov_sales: "——",
          capacity: 314,
          cost: 50589953,
          o_capacity: 314,
          o_cost: 46444562
        }
      ]
    };
  },
  // created() {
  //   // this.getData();
  //   var _this = this;
  //   document.onkeydown = function (e) {
  //     //按下回车提交
  //     let key = window.event.keyCode;
  //     //事件中keycode=13为回车事件
  //     if (key == 13) {
  //       _this.onSearch();
  //     }
  //   };
  // },
  // mounted() {
  //   setTimeout(() => {

  //   }, 0);
  //   if (this.$route.query.leftNum1) {
  //     this.leftNum1 = this.$route.query.leftNum1
  //     this.num1 = parseInt((Math.random() * 50).toFixed(0));
  //     this.num2 = parseInt((Math.random() * 50).toFixed(0));
  //     this.num3 = this.leftNum1 - this.num1 - this.num2;
  //   }
  // },
  methods: {
    // 获取数据
    getData() {},
    // 编辑
    edit(data) {
      this.openDialog = true;
      this.title = "详情";
      this.$nextTick(() => {
        this.$refs.testDialog.init(data);
      });
    },
    // 表单查询
    onSearch() {
      setTimeout(() => {
        this.change = !this.change;
        this.searchTitle =
          this.change == false ? "单末端节点优化" : "多末端节点优化";
      }, 200);

      setTimeout(() => {
        this.initCharts();
      }, 500);
    },

    initCharts() {
      let option = {
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "shadow"
          }
        },
        legend: {
          data: [
            "杭州",
            "济南",
            "芜湖",
            "徐州",
            "宁波(水)",
            "上海(水)",
            "烟台(水)",
            "总成本"
          ],
          textStyle: {
            color: "rgb(125, 180, 173)"
          }
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true
        },
        xAxis: [
          {
            type: "value",
            splitLine: {
              show: true,
              lineStyle: {
                type: "dashed",
                color: "RGBA(3, 75, 97, 1)"
              }
            },
            axisLabel: {
              color: "rgb(125, 180, 173)" // 设置 y 轴字体颜色为蓝色
            }
          }
        ],
        yAxis: [
          {
            type: "category",
            axisTick: {
              show: false
            },
            axisLabel: {
              color: "rgb(125, 180, 173)" // 设置 y 轴字体颜色为蓝色
            },
            data: ["粒子群优化成本", "贪心优化成本", "原始成本"]
          }
        ],
        series: [
          {
            name: "杭州",
            type: "bar",
            label: {
              show: true,
              position: "inside",
              color: "rgb(125, 180, 173)"
            },
            emphasis: {
              focus: "series"
            },
            data: [9820176, 12145240, 18654919]
          },
          {
            name: "济南",
            type: "bar",
            stack: "Total",
            label: {
              show: true,
              color: "#0623208c"
            },
            emphasis: {
              focus: "series"
            },
            data: [14929342, 14049739, 8046222]
          },
          {
            name: "芜湖",
            type: "bar",
            label: {
              show: true,
              color: "#0623208c"
            },
            emphasis: {
              focus: "series"
            },
            data: [1850633, 1094975, 6819158]
          },
          {
            name: "徐州",
            type: "bar",
            // stack: 'Total',
            label: {
              show: true,
              color: "rgb(125, 180, 173)"
            },
            emphasis: {
              focus: "series"
            },
            data: [12992048, 15096834, 11935479]
          },
          {
            name: "宁波(水)",
            type: "bar",
            label: {
              show: true,
              color: "#0623208c"
            },
            emphasis: {
              focus: "series"
            },
            data: [9820176, 12145240, 18654919]
          },
          {
            name: "上海(水)",
            type: "bar",
            label: {
              show: true,
              color: "#0623208c"
            },
            emphasis: {
              focus: "series"
            },
            data: [6852363, 6274218, 5134175]
          },
          {
            name: "烟台(水)",
            type: "bar",
            label: {
              show: true,
              color: "#0623208c"
            },
            emphasis: {
              focus: "series"
            },
            data: [14929342, 14049739, 8046222]
          },
          {
            name: "总成本",
            type: "bar",
            label: {
              show: true,
              color: "#0623208c"
            },
            emphasis: {
              focus: "series"
            },
            data: [46444562, 48661007.3, 50589953]
          }
        ]
      };
      const myChart = this.$echarts.init(this.$refs.emptycharts);
      myChart.setOption(option);
      window.addEventListener("resize", () => {
        myChart.resize();
      });
    },

    // 重置
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    formatText(text) {
      return text.replace(/<br>/g, "<br/>"); // 将 <br> 替换为 <br/> 实现换行
    }
  }
};
</script>
<style lang="scss" scoped>
.warningAnalysis {
  // display: flex;
  // justify-content: space-between;
  // flex-wrap: wrap;
  text-align: center;
  // color: rgb(125, 180, 173);
  color: #00bbee;
  font-weight: bold;
  font-size: 19px;
  // height: 360px;
  margin: 0 auto;
  scroll-behavior: smooth;

  .single {
    scroll-behavior: smooth;

    .experiment {
      // margin-top: 2%;
      background-color: #0623208c;
      border-radius: 5px;

      .title {
        line-height: 150%;
      }
    }

    .statistics {
      margin-top: 4%;
      background-color: #0623208c;
      border-radius: 5px;
    }
  }

  .multi {
    scroll-behavior: smooth;

    .empty {
      text-align: center;
      // color: rgb(125, 180, 173);
      color: #00bbee;
      font-weight: bold;
      font-size: 19px;
      // height: 360px;
      margin: 0 auto;

      .experiment {
        width: 85%;
        height: 400px;
        margin: 0 auto;
        background-color: #0623208c;
        border-radius: 5px;

        .title {
          padding-top: 1%;
          line-height: 150%;
        }

        .charts {
          padding-top: 1%;
          height: 80%;
        }
      }
    }
  }
}
</style>
