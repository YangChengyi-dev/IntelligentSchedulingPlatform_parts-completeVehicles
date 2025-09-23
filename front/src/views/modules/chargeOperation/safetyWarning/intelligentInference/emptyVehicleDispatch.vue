<template>
  <div id="app" class="contain">
    <div ref="formDiv">
      <el-form ref="form" class="unitForm" :model="form" id="form">
        <el-form-item label="站点:">
          <el-select v-model="form.site" clearable placeholder="请选择">
            <el-option
              v-for="item in siteOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="月份:">
          <el-select v-model="form.month" clearable placeholder="请选择">
            <el-option
              v-for="item in monthOptions"
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
            >优化</el-button
          >
          <el-button
            class="iconfont icon-xiazai"
            type="primary"
            size="small"
            @click="downloadExcel"
            >下载</el-button
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
      <div class="empty">
        <div class="experiment">
          <div class="title">空车智能调度表</div>
          <div ref="emptycharts" class="charts"></div>
        </div>
        <el-table
          :data="tableData"
          id="table"
          stripe
          style="width: 86%; margin: 0 auto;margin-top: 20px;border-bottom: 1px solid #ebeef5;"
          :header-row-style="{ height: '50px' }"
          :row-style="{ height: '50px' }"
        >
          <el-table-column label="" align="center" min-width="10%">
            <el-table-column
              prop="method"
              label="调度方法"
              align="center"
              min-width="10%"
            >
            </el-table-column>
          </el-table-column>
          <el-table-column :label="departure" align="center" min-width="10%">
            <el-table-column
              prop="sales1"
              :label="timeLable"
              align="center"
              min-width="10%"
            >
            </el-table-column>
            <el-table-column
              prop="tt"
              label="铁路吞吐量"
              align="center"
              min-width="10%"
            >
            </el-table-column>
            <el-table-column
              prop="st"
              label="水运吞吐量"
              align="center"
              min-width="10%"
            >
            </el-table-column>
            <el-table-column
              prop="cost1"
              label="辐射成本(铁路+水路+公路)"
              align="center"
              min-width="10%"
            >
              <template slot-scope="scope">
                <span style="font-weight: 600; color: red">
                  {{ scope.row.cost1 }}
                </span>
              </template>
            </el-table-column>
          </el-table-column>
          <el-table-column :label="dest" align="center" min-width="10%">
            <el-table-column
              prop="sales2"
              :label="timeLable"
              align="center"
              min-width="10%"
            >
            </el-table-column>
            <el-table-column
              prop="cost2"
              label="辐射成本(公路)"
              align="center"
              min-width="10%"
            >
              <template slot-scope="scope">
                <span style="font-weight: 600; color: red">
                  {{ scope.row.cost2 }}
                </span>
              </template>
            </el-table-column>
          </el-table-column>
          <el-table-column label="数据分析" align="center" min-width="10%">
            <el-table-column
              prop="save_car"
              label="节约空车数"
              align="center"
              min-width="10%"
            >
              <template slot-scope="scope">
                <span style="font-weight: 600; color: #13ce66">
                  {{ scope.row.save_car }}
                </span>
              </template>
            </el-table-column>
            <el-table-column
              prop="save_mileage"
              label="节约的空驶里程数(km)"
              align="center"
              min-width="10%"
            >
              <template slot-scope="scope">
                <span style="font-weight: 600; color: #13ce66">
                  {{ scope.row.save_mileage }}
                </span>
              </template>
            </el-table-column>
            <el-table-column
              prop="extra_cost"
              :label="extra_describe"
              align="center"
              min-width="10%"
            >
              <template slot-scope="scope">
                <span style="font-weight: 600; color: red">
                  {{ scope.row.extra_cost }}
                </span>
              </template>
            </el-table-column>
            <el-table-column
              prop="save_cost"
              label="汽车分销节约物流成本(元)"
              align="center"
              min-width="10%"
            >
              <template slot-scope="scope">
                <span style="font-weight: 600; color: #13ce66">
                  {{ scope.row.save_cost }}
                </span>
              </template>
            </el-table-column>
            <el-table-column
              prop="all_cost"
              label="两省总的物流成本(元)"
              align="center"
              min-width="12%"
            >
              <template slot-scope="scope">
                <span style="font-weight: 600; color: #13ce66">
                  <span v-if="scope.row.icon"
                    ><i class="el-icon-bottom"></i
                  ></span>
                  {{ scope.row.all_cost }}
                </span>
              </template>
            </el-table-column>
          </el-table-column>
        </el-table>
      </div>
    </div>
    <JobChat></JobChat>
  </div>
</template>

<script>
// import Dialog from "./dialog";
import axios from "axios";
import JobChat from "../../AI_chat/JobChat.vue";
export default {
  name: "unitManagement",
  components: {
    JobChat
  },
  data() {
    return {
      form: {
        site: "广州",
        month: "12月"
      },
      siteOptions: [
        { value: "广州", label: "广州" },
        { value: "宁波", label: "宁波" },
        { value: "上海", label: "上海" }
      ],
      monthOptions: [
        { value: "12月", label: "12月" },
        { value: "10月", label: "10月" },
        { value: "2月", label: "2月" }
      ],
      departure: "广东",
      dest: "广西",
      extra_describe: "汽车额外去广东的取货成本(元)",
      timeLable: "12月省销量",
      loading: false,
      tableData: [
        {
          method: "粒子群算法优化",
          sales1: 2738,
          tt: 1096,
          st: 1536,
          cost1: 411964,
          sales2: 650,
          cost2: 493318,
          save_car: 0,
          save_mileage: 0,
          extra_cost: 0,
          save_cost: 0,
          all_cost: 905282,
          icon: false
        },
        {
          method: "水运累积送2000辆商品车",
          sales1: 2738,
          tt: 1096,
          st: 2000,
          cost1: 427391,
          sales2: 650,
          cost2: 493318,
          save_car: 45,
          save_mileage: 112593,
          extra_cost: 38480,
          save_cost: 202667,
          all_cost: 756522,
          icon: true
        },
        {
          method: "水运累积送2292辆商品车",
          sales1: 2738,
          tt: 1096,
          st: 2292,
          cost1: 477543,
          sales2: 650,
          cost2: 493318,
          save_car: 82,
          save_mileage: 196161,
          extra_cost: 78086,
          save_cost: 353089,
          all_cost: 695858,
          icon: true
        }
      ]
    };
  },

  methods: {
    // // 重置
    // resetForm(formName) {
    //     this.$refs[formName].resetFields();
    // },
    // formatText(text) {
    //     return text.replace(/<br>/g, '<br/>'); // 将 <br> 替换为 <br/> 实现换行
    // },
    getData() {
      // 假设从后端获取数据
      // this.tableData = [
      // ...
      //]
      axios
        .post(this.baseurl + "/empty/search", this.form)
        .then(res => {
          this.tableData = res.data.data;
          this.tableData[0].icon = false;
          this.tableData[1].icon = true;
          this.tableData[2].icon = true;
          const city_arr = this.tableData[0].city.split("-");
          this.departure = city_arr[0];
          this.dest = city_arr[1];
          this.extra_describe =
            "汽车额外去" + this.form.site + "的取货成本(元)";
          this.timeLable = this.form.month + "省销量";
        })
        .catch(error => console.log(error));
    },
    onSearch() {
      if (this.form.site == "" && this.form.month == "") {
        this.$message({
          message: "优化方法不能为空",
          type: "error"
        });
      } else {
        this.loading = true;
        this.getData();
        setTimeout(() => {
          this.loading = false;
          this.$message.success("优化成功");
          this.initCharts();
        }, 800);
      }
    },
    downloadExcel() {
      if (this.form.site == "" && this.form.month == "") {
        this.$message({
          message: "优化方法不能为空",
          type: "error"
        });
      } else {
        let filename = this.form.month + this.form.site + "空车优化结果.xlsx";
        axios({
          url: this.baseurl + "/empty/download", // 替换为实际的后端接口
          method: "POST",
          responseType: "blob", // 设置响应类型为 blob
          data: {
            // method: this.form.programme,
            // 添加其他必要的参数
            site: this.form.site,
            month: this.form.month
          }
        })
          .then(response => {
            // console.log(response.data)
            if (response.data.size > 40) {
              const blob = new Blob([response.data]);
              saveAs(blob, filename);
              this.$message({
                message: "文件下载成功！！！",
                type: "success"
              });
            } else {
              this.$message({
                message: "文件下载失败！！！",
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
            this.departure + "辐射成本",
            this.dest + "辐射成本",
            this.departure + "取货成本",
            "分销节约物流成本",
            "两省总物流成本"
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
            data: [
              this.tableData[2].method,
              this.tableData[1].method,
              this.tableData[0].method
            ]
          }
        ],
        series: [
          {
            name: this.departure + "辐射成本",
            type: "bar",
            label: {
              show: true,
              position: "inside",
              color: "rgb(125, 180, 173)"
            },
            emphasis: {
              focus: "series"
            },
            data: [
              this.tableData[2].cost1,
              this.tableData[1].cost1,
              this.tableData[0].cost1
            ]
          },
          {
            name: this.dest + "辐射成本",
            type: "bar",
            stack: "Total",
            label: {
              show: true,
              color: "#0623208c"
            },
            emphasis: {
              focus: "series"
            },
            data: [
              this.tableData[2].cost2,
              this.tableData[1].cost2,
              this.tableData[0].cost2
            ]
          },
          {
            name: this.departure + "取货成本",
            type: "bar",
            label: {
              show: true,
              color: "#0623208c"
            },
            emphasis: {
              focus: "series"
            },
            data: [
              this.tableData[2].extra_cost,
              this.tableData[1].extra_cost,
              this.tableData[0].extra_cost
            ]
          },
          {
            name: "分销节约物流成本",
            type: "bar",
            // stack: 'Total',
            label: {
              show: true,
              position: "left",
              color: "rgb(125, 180, 173)"
            },
            emphasis: {
              focus: "series"
            },
            data: [
              -this.tableData[2].save_cost,
              -this.tableData[1].save_cost,
              -this.tableData[0].save_cost
            ]
          },
          {
            name: "两省总物流成本",
            type: "bar",
            label: {
              show: true,
              color: "#0623208c"
            },
            emphasis: {
              focus: "series"
            },
            data: [
              this.tableData[2].all_cost,
              this.tableData[1].all_cost,
              this.tableData[0].all_cost
            ]
          }
        ]
      };
      const myChart = this.$echarts.init(this.$refs.emptycharts);
      myChart.setOption(option);
      window.addEventListener("resize", () => {
        myChart.resize();
      });
    }
  },

  mounted() {
    setTimeout(() => {
      this.initCharts();
    }, 100);
  }
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
    height: 350px;
    margin: 0 auto;
    background-color: #0623208c;
    border-radius: 5px;

    .title {
      padding-top: 2%;
      line-height: 150%;
    }

    .charts {
      padding-top: 2%;
      height: 80%;
    }
  }
}
</style>
