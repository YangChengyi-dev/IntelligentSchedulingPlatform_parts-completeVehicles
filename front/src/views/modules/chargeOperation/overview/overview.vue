<!--  -->
<template>
  <div class="overview">
    <div class="leftDiv">
      <div class="leftTop">
        <div class="jrxz">中转站点</div>
        <div class="leftNum1">18</div>
        <div class="leftSpan1">总数</div>
        <div class="leftNum2">15</div>
        <div class="leftSpan2">铁路站点</div>
        <div class="leftNum3">&nbsp;3</div>
        <div class="leftSpan3">水路站点</div>
      </div>
      <div class="leftCenter">
        <div id="container"></div>
        <!-- <div class="layui-form buttonDiv2">
          <el-button icon="el-icon-search" size="small" class="query1" @click="warnFun">铁路分布</el-button>
          <el-button icon="el-icon-search" size="small" class="query2" @click="errorFun">水路分布</el-button>
        </div> -->
      </div>
      <div class="leftBottom">
        <div class="l-bdiv1">
          <div class="iconfont icon-qitafeiyong l-bpic"></div>
          <div class="l-bnum1">&le;500</div>
          <div class="l-bnum2">&gt;500</div>
          <div class="l-btext1">费用</div>
        </div>
        <div class="l-bdiv1">
          <div class="iconfont icon-dahuoche l-bpic"></div>
          <div class="l-bnum1">2.0元</div>
          <div class="l-bnum2">1.8元</div>
          <div class="l-btext1">公路运输</div>
        </div>
        <div class="l-bdiv1">
          <div class="iconfont icon-tielu l-bpic"></div>
          <div class="l-bnum1">1.6元</div>
          <div class="l-bnum2">1.4元</div>
          <div class="l-btext1">铁路运输</div>
        </div>
        <div class="l-bdiv1">
          <div class="iconfont icon-shuilu l-bpic"></div>
          <div class="l-bnum1">1.2元</div>
          <div class="l-bnum2">1.0元</div>
          <div class="l-btext1">水路运输</div>
        </div>
      </div>
    </div>

    <div class="midDiv">
      <div class="midTop">
        <div class="dnlj">运输模式</div>
        <div class="midNum1">60%</div>
        <div class="midSpan1">公路运输</div>
        <div class="midNum2">32%</div>
        <div class="midSpan2">铁路运输</div>
        <div class="midNum3">8%</div>
        <div class="midSpan3">水路运输</div>
      </div>
      <div class="midCenter">
        <div class="layui-form buttonDiv">
          <el-button
            icon="el-icon-search"
            size="small"
            class="query1"
            @click="warnFun"
            >铁路分布</el-button
          >
          <el-button
            icon="el-icon-search"
            size="small"
            class="query2"
            @click="errorFun"
            >水路分布</el-button
          >
        </div>
        <div class="gdzsDiv">
          <div class="chartTitle">车辆销售指数</div>
          <div id="gdzsChart" ref="gdzsChart"></div>
        </div>
      </div>
      <div class="midBottom">
        <div class="b-ldiv">
          <!-- <div class="midNum4">{{ midNum4 }}%</div> -->
          <div class="midSpan4">运输能力</div>
          <div class="midLeftTitle">运输方式</div>
          <div class="midSpan5">公路运输</div>
          <div class="midSpan6">铁路运输</div>
          <div class="midSpan7">水路运输</div>
          <div class="midRightTitle">容量</div>
          <div class="midNum5">8</div>
          <div class="midNum6">290</div>
          <div class="midNum7">1000</div>
        </div>
        <div class="b-rdiv">
          <!-- <div class="midNum9">{{ midNum9 }}%</div> -->
          <div class="midSpan9">华东区域零件分布</div>
          <div class="yjgdzbDiv">
            <div id="yjgdzbChart" ref="yjgdzbChart"></div>
          </div>
        </div>
      </div>
    </div>
    <div class="rightDiv">
      <div class="rightTop">
        <div class="gdzlzsDiv">
          <div class="chartTitle">一汽车辆销售分布</div>
          <div id="gdzlzsChart" ref="gdzlzsChart"></div>
        </div>
      </div>
      <div class="rightCenter">
        <div class="jkzkzsDiv">
          <div class="chartTitle">站点车辆运输销售情况</div>
          <div id="jkzkzsChart" ref="jkzkzsChart"></div>
        </div>
      </div>
      <div class="rightBottom">
        <div class="bjfxsDiv">
          <div class="chartTitle">华东区域整车物流</div>
          <div id="bjfxChart" ref="bjfxChart"></div>
        </div>
      </div>
    </div>
    <JobChat></JobChat>
  </div>
</template>

<script>
//这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）
//例如：import 《组件名称》 from '《组件路径》';
import AMapLoader from "@amap/amap-jsapi-loader";
import FileSaver from "file-saver";
import yajiankang from "@@/img/chargeOperation/yajiankang.png";
import guzhang from "@@/img/chargeOperation/guzhang.png";
import JobChat from "../AI_chat/JobChat.vue";
export default {
  //import引入的组件需要注入到对象中才能使用
  components: {
    JobChat
  },
  data() {
    //这里存放数据
    return {
      map: "",
      dnlj: "当月累计",
      midNum1: 120,
      midNum2: 78,
      midNum3: 136,
      midNum4: 87.5,
      midNum5: 60,
      midNum6: 60,
      midNum7: 60,
      midNum8: 60,
      midNum9: 98.8
    };
  },
  //监听属性 类似于data概念
  computed: {},
  //监控data中的数据变化
  watch: {},
  //方法集合
  methods: {
    initGdzsChart(time) {
      let xData = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
      let gzgdData = [];
      // let zdywgdData = [1.035696615, 0.726920968, 1.134841831, 0.796793503, 1.101750407, 1.14640474, 0.920832519, 0.926983305, 1.110325905, 1.001575635, 0.962809952, 1.135064621];
      let zdywgdData = [
        1.038818159,
        0.725013207,
        1.131863506,
        0.794702366,
        1.098858928,
        1.143396069,
        0.918415849,
        0.924550492,
        1.107411921,
        1.000931436,
        0.9640458,
        1.151992269
      ];
      // for (var i = 0; i < xData.length; i++) {
      //   gzgdData.push((Math.random() * 50 + 50).toFixed(0));
      //   zdywgdData.push((Math.random() * 50 + 50).toFixed(0));
      // }
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
          // data: ["故障工单", "主动运维工单"],
          right: "3%",
          textStyle: {
            fontSize: 14,
            color: "#fff"
          }
        },
        /*grid: {
              left: '3%',
              right: '4%',
              bottom: '3%',
              containLabel: true
          },*/
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
              // interval: 0,
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
            max: 1.2,
            interval: 0.2,
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
          // {
          //   name: "故障工单",
          //   type: "line",
          //   smooth: true,
          //   symbol: "circle",
          //   symbolSize: 5,
          //   showSymbol: false,
          //   lineStyle: {
          //     normal: {
          //       width: 1,
          //     },
          //   },
          //   areaStyle: {
          //     normal: {
          //       color: new echarts.graphic.LinearGradient(
          //         0,
          //         0,
          //         0,
          //         1,
          //         [
          //           {
          //             offset: 0,
          //             color: "rgba(137, 189, 27, 0.3)",
          //           },
          //           {
          //             offset: 0.8,
          //             color: "rgba(137, 189, 27, 0)",
          //           },
          //         ],
          //         false
          //       ),
          //       shadowColor: "rgba(0, 0, 0, 0.1)",
          //       shadowBlur: 10,
          //     },
          //   },
          //   itemStyle: {
          //     normal: {
          //       color: "rgb(137,189,27)",
          //       borderColor: "rgba(137,189,2,0.27)",
          //       borderWidth: 12,
          //     },
          //   },
          //   data: gzgdData,
          // },
          {
            name: "月份指数",
            type: "line",
            smooth: true,
            symbol: "circle",
            symbolSize: 5,
            showSymbol: false,
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
            data: zdywgdData
          }
        ]
      };
      const myChart = this.$echarts.init(this.$refs.gdzsChart);
      myChart.setOption(option);
      window.addEventListener("resize", () => {
        myChart.resize();
      });
    },
    initYjgdzdChart() {
      // let color = ["#6597FB", "#5FF5E8", "#18BEF7", "#F67C2D"];
      const dataArray = [
        {
          value: 18649.46,
          name: "安徽"
        },
        {
          value: 597.53,
          name: "河南"
        },
        {
          value: 8998.28,
          name: "湖北"
        },
        {
          value: 1522.9,
          name: "湖南"
        },
        {
          name: "江苏",
          value: 203497.2
        },
        {
          value: 276.41,
          name: "江西"
        },
        {
          name: "上海",
          value: 275692.9
        },
        {
          value: 239450.5,
          name: "浙江"
        }
      ];
      const option = {
        // tooltip: {
        //   trigger: 'item'
        // },
        // legend: {
        //   // top: '1%',
        //   left: 'center',
        //   textStyle: {
        //     fontSize: 8,//字体大小
        //     color: 'rgb(125, 180, 173)'//字体颜色
        //   },
        // },
        // color: color,
        series: [
          {
            type: "pie",
            radius: ["45%", "85%"],
            // center: ["50%", "50%"],
            data: dataArray,
            // hoverAnimation: false,
            avoidLabelOverlap: false,
            labelLine: {
              show: false
              // length: 10,
              // length2: 20,
              // lineStyle: {
              //   color: "rgba(75, 219, 198, 1)",
              // },
            },
            label: {
              show: false,
              position: "center",
              formatter: params => {
                return params.name + "\n" + params.value;
              }
            },
            emphasis: {
              label: {
                show: true,
                fontSize: 14
                // fontWeight: 'bold'
              }
            }
          }
        ]
      };
      const myChart = this.$echarts.init(this.$refs.yjgdzbChart);
      myChart.setOption(option);
      window.addEventListener("resize", () => {
        myChart.resize();
      });
    },
    initGdzlzsChart(time) {
      let xData = [
        "武汉",
        "成都",
        "郑州",
        "济南",
        "杭州",
        "芜湖",
        "昆明",
        "佛山",
        "西安",
        "天津",
        "北京",
        "长沙",
        "贵州",
        "乌鲁木齐",
        "福州",
        "宁波",
        "上海",
        "广州"
      ];
      let jkData = [
        8756,
        10360,
        7186,
        10947,
        2979,
        2059,
        10348,
        3016,
        3842,
        151,
        669,
        9861,
        2353,
        201,
        4957,
        10686,
        8408,
        11601
      ];
      // let yjkData = [];
      let gzData = [
        3765,
        9134,
        4144,
        5944,
        5674,
        934,
        5714,
        3035,
        4068,
        4025,
        12276,
        5409,
        3693,
        756,
        2511,
        3804,
        8535,
        5486
      ];
      // for (var i = 0; i < xData.length; i++) {
      //   jkData.push((Math.random() * 50 + 50).toFixed(0));
      //   yjkData.push((Math.random() * 50 + 50).toFixed(0));
      //   gzData.push((Math.random() * 50 + 50).toFixed(0));
      // }
      const option = {
        legend: {
          left: "38%",
          top: 30,
          itemWidth: 16.7,
          itemHeight: 7.6,
          type: "plain",
          textStyle: {
            color: "RGBA(154, 209, 253, 1)"
          }
        },
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "shadow",
            textStyle: {
              color: "#fff"
            }
          }
        },
        calculable: true,
        xAxis: [
          {
            type: "category",
            boundaryGap: true,
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
              fontSize: 10,
              rotate: 60 //代表逆时针旋转45度
            },
            data: xData
          }
        ],
        yAxis: [
          {
            name: "kWh",
            nameTextStyle: {
              color: "rgba(255,255,255,0.5)",
              padding: [0, 0, 0, -50]
            },
            nameGap: 15,
            type: "value",
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
              fontSize: 10
            },
            splitArea: {
              show: false
            }
          }
        ],
        series: [
          {
            name: "吞吐量",
            type: "bar",
            stack: "1",
            barMaxWidth: 30,
            barGap: "10%",
            itemStyle: {
              normal: {
                color: "#63f927",
                opacity: 1
              }
            },
            data: jkData
          },

          // {
          //   name: "亚健康",
          //   type: "bar",
          //   stack: "1",
          //   itemStyle: {
          //     normal: {
          //       color: "#5ff5e8",
          //       opacity: 0.9,
          //       barBorderRadius: 0,
          //     },
          //   },
          //   data: yjkData,
          // },
          {
            name: "年运量",
            type: "bar",
            stack: "1",
            itemStyle: {
              normal: {
                color: "#18bef7",
                opacity: 0.9,
                barBorderRadius: 0
              }
            },
            data: gzData
          }
        ]
      };
      const myChart = this.$echarts.init(this.$refs.jkzkzsChart);
      myChart.setOption(option);
      window.addEventListener("resize", () => {
        myChart.resize();
      });
    },
    initJkzkzsChart(time) {
      let xData = [
        "2023/10",
        "2023/11",
        "2023/12",
        "2024/1",
        "2024/2",
        "2024/3",
        "2024/4",
        "2024/5",
        "2024/6",
        "2024/7",
        "2024/8",
        "2024/9"
      ];
      let gzgdData = [
        91204,
        97005,
        123461,
        98000,
        53007,
        76260,
        63011,
        71015,
        74003,
        65001,
        76005,
        87010
      ];
      let zdywgdData = [
        37280,
        39650,
        45169,
        40374,
        25006,
        32975,
        27570,
        30714,
        34064,
        30773,
        34648,
        41891
      ];
      // for (var i = 0; i < xData.length; i++) {
      //   gzgdData.push((Math.random() * 50 + 50).toFixed(0));
      //   zdywgdData.push((Math.random() * 50 + 50).toFixed(0));
      // }
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
          data: ["一汽-大众", "一汽-解放"],
          right: "3%",
          textStyle: {
            fontSize: 14,
            color: "#fff"
          }
        },
        /*grid: {
              left: '3%',
              right: '4%',
              bottom: '3%',
              containLabel: true
          },*/
        xAxis: [
          {
            type: "category",
            boundaryGap: false,
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
              fontSize: 12,
              rotate: 45 //代表逆时针旋转45度
            },
            data: xData
          }
        ],
        yAxis: [
          {
            type: "value",
            scale: true,
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
              fontSize: 10
            },
            splitArea: {
              show: false
            }
          }
        ],
        series: [
          {
            name: "一汽-大众",
            type: "line",
            smooth: true,
            symbol: "circle",
            symbolSize: 5,
            showSymbol: false,
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
                      color: "rgba(137, 189, 27, 0.3)"
                    },
                    {
                      offset: 0.8,
                      color: "rgba(137, 189, 27, 0)"
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
                color: "rgb(137,189,27)",
                borderColor: "rgba(137,189,2,0.27)",
                borderWidth: 12
              }
            },
            data: gzgdData
          },
          {
            name: "一汽-解放",
            type: "line",
            smooth: true,
            symbol: "circle",
            symbolSize: 5,
            showSymbol: false,
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
            data: zdywgdData
          }
        ]
      };
      const myChart = this.$echarts.init(this.$refs.gdzlzsChart);
      myChart.setOption(option);
      window.addEventListener("resize", () => {
        myChart.resize();
      });
    },
    initBjfxChart() {
      let xData = ["安徽省", "江苏省", "福建省", "山东省", "上海市", "浙江省"];
      // let xData = ["安徽", "河南", "湖北", "湖南", "江苏", "江西", "上海", "浙江"];
      // let ycylData = [18649.46, 597.53, 8998.28, 1522.90, 203497.2, 276.41, 275692.9, 239450.5];
      let ycylData = [33221, 81589, 17972, 79881, 33943, 86059];
      // let kclData = [];
      // for (var i = 0; i < xData.length; i++) {
      //   ycylData.push((Math.random() * 50 + 50).toFixed(0));
      //   kclData.push((Math.random() * 50 + 50).toFixed(0));
      // }
      const option = {
        tooltip: {
          trigger: "axis",
          axisPointer: {
            // 坐标轴指示器，坐标轴触发有效
            type: "shadow" // 默认为直线，可选为：'line' | 'shadow'
          }
        },
        grid: {
          left: "2%",
          right: "4%",
          bottom: "14%",
          top: "16%",
          containLabel: true
        },
        legend: {
          data: ["销售量"],
          // data: ["预测用量", "库存量"],
          right: 10,
          top: 12,
          textStyle: {
            color: "#fff"
          },
          left: "38%",
          top: 10,
          itemWidth: 12,
          itemHeight: 10
          // itemGap: 35
        },
        xAxis: {
          type: "category",
          data: xData,
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
            // interval: 0,
            color: "rgba(255,255,255,0.7)",
            fontSize: 12
          }
        },

        yAxis: {
          type: "value",
          //max: '1200',
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
        },
        /*"dataZoom": [{
              "show": true,
              "height": 12,
              "xAxisIndex": [
                  0
              ],
              bottom: '8%',
              "start": 0,
              "end": 100,
              handleIcon: 'path://M306.1,413c0,2.2-1.8,4-4,4h-59.8c-2.2,0-4-1.8-4-4V200.8c0-2.2,1.8-4,4-4h59.8c2.2,0,4,1.8,4,4V413z',
              handleSize: '110%',
              handleStyle: {
                  color: "#d3dee5",

              },
              textStyle: {
                  color: "#fff"
              },
              borderColor: "#90979c"
          }, {
              "type": "inside",
              "show": true,
              "height": 15,
              "start": 1,
              "end": 35
          }],*/
        series: [
          {
            name: "销售量",
            type: "bar",
            barWidth: "20%",
            itemStyle: {
              normal: {
                color: "#38A4DD"
              }
            },
            data: ycylData
          }
          // {
          //   name: "库存量",
          //   type: "bar",
          //   barWidth: "15%",
          //   itemStyle: {
          //     normal: {
          //       color: "#A8E52E",
          //     },
          //   },
          //   data: kclData,
          // },
        ]
      };
      const myChart = this.$echarts.init(this.$refs.bjfxChart);
      myChart.setOption(option);
      window.addEventListener("resize", () => {
        myChart.resize();
      });
    },
    initMap() {
      AMapLoader.load({
        key: "b039c6c138fa652d28abf0e62e665b32", //设置您的key
        version: "2.0", // 高德地图版本
        plugins: ["AMap.ToolBar", "AMap.Driving"], // 插件
        AMapUI: {
          // 高德地图UI组件库，可不写，内部提供了覆盖物标注点，以及部分模块的封装
          version: "1.1",
          plugins: []
        },
        Loca: {
          // Loca版本(高性能地图数据可视化库) 可不写
          version: "2.0"
        }
      })
        .then(AMap => {
          // container渲染的id
          this.map = new AMap.Map("container", {
            zoom: 10, // 当前缩放级别
            zooms: [2, 22], // 缩放级别范围
            center: [125.323544, 43.817071] // 中心点
          });
          // 点标记显示内容，HTML要素字符串
          var markerContent =
            "" +
            '<div class="custom-content-marker" v-if="www" style="position: relative;width: 40px;height: 40px;">' +
            '   <img src="../../../../../../static/img/poi-marker-light.png" style="width: 100%;height: 100%;opacity:0.7">' +
            '   <div class="close-btn" style="position: absolute;top: 4px;right: 8px;width: 30px;height: 30px;font-size: 16px;color: #fff;text-align: center;line-height: 30px;"></div>' +
            "</div>";

          var position1 = new AMap.LngLat(114.30525, 30.59276); //武汉 经纬度对象，也可以是经纬度构成的一维数组
          this.marker1 = new AMap.Marker({
            position: position1,
            // 将 html 传给 content
            content: markerContent,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "武汉"
          });

          var position2 = new AMap.LngLat(104.0668, 30.5728); //成都
          this.marker2 = new AMap.Marker({
            position: position2,
            // 将 html 传给 content
            content: markerContent,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "成都"
          });

          var position3 = new AMap.LngLat(113.6254, 34.7466); //郑州
          this.marker3 = new AMap.Marker({
            position: position3,
            // 将 html 传给 content
            content: markerContent,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "郑州"
          });

          var position4 = new AMap.LngLat(117.1201, 36.6512); //济南
          this.marker4 = new AMap.Marker({
            position: position4,
            // 将 html 传给 content
            content: markerContent,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "济南"
          });

          var position5 = new AMap.LngLat(120.2, 30.24); //杭州
          this.marker5 = new AMap.Marker({
            position: position5,
            // 将 html 传给 content
            content: markerContent,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "杭州"
          });

          var position6 = new AMap.LngLat(102.7183, 25.0389); //昆明
          this.marker6 = new AMap.Marker({
            position: position6,
            // 将 html 传给 content
            content: markerContent,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "昆明"
          });

          var position7 = new AMap.LngLat(113.1216, 23.0219); //佛山
          this.marker7 = new AMap.Marker({
            position: position7,
            // 将 html 传给 content
            content: markerContent,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "佛山"
          });

          var position8 = new AMap.LngLat(108.9398, 34.3416); //西安
          this.marker8 = new AMap.Marker({
            position: position8,
            // 将 html 传给 content
            content: markerContent,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "西安"
          });

          var position9 = new AMap.LngLat(117.30983, 39.71755); //天津
          this.marker9 = new AMap.Marker({
            position: position9,
            // 将 html 传给 content
            content: markerContent,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "天津"
          });

          var position10 = new AMap.LngLat(116.3912757, 39.906217); //北京
          this.marker10 = new AMap.Marker({
            position: position10,
            // 将 html 传给 content
            content: markerContent,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "北京"
          });

          var position11 = new AMap.LngLat(112.9388, 28.2282); //长沙
          this.marker11 = new AMap.Marker({
            position: position11,
            // 将 html 传给 content
            content: markerContent,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "长沙"
          });

          var position12 = new AMap.LngLat(107.2903, 26.8447); //贵阳
          this.marker12 = new AMap.Marker({
            position: position12,
            // 将 html 传给 content
            content: markerContent,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "贵阳"
          });

          var position13 = new AMap.LngLat(87.6168, 43.8256); //乌鲁木齐
          this.marker13 = new AMap.Marker({
            position: position13,
            // 将 html 传给 content
            content: markerContent,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "乌鲁木齐"
          });

          var position14 = new AMap.LngLat(119.2965, 26.0745); //福州
          this.marker14 = new AMap.Marker({
            position: position14,
            // 将 html 传给 content
            content: markerContent,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "福州"
          });

          var position15 = new AMap.LngLat(118.4277477, 31.3536127); //芜湖
          this.marker15 = new AMap.Marker({
            position: position15,
            // 将 html 传给 content
            content: markerContent,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "芜湖"
          });

          // 点击事件
          var that = this;
          // AMap.Event.addListener(that.marker1, "click", function (e) {
          //   that.$router.push({ path: '/index/chargeOperation/safetyWarning/warningList/warningList', query: { leftNum1: that.leftNum1 } })
          // });
          // AMap.Event.addListener(that.marker2, "click", function (e) {
          //   that.$router.push({ path: '/index/chargeOperation/safetyWarning/warningList/warningList', query: { leftNum1: that.leftNum1 } })
          // });

          // 点标记显示内容，HTML要素字符串
          var markerContent2 =
            "" +
            '<div class="custom-content-marker" v-if="www" style="position: relative;width: 40px;height: 40px;">' +
            '   <img src="../../../../../../static/img/poi-marker-blue.png"  style="width: 100%;height: 100%;opacity:0.7">' +
            '   <div class="close-btn" style="position: absolute;top: 4px;right: 8px;width: 30px;height: 30px;font-size: 16px;color: #fff;text-align: center;line-height: 30px;"></div>' +
            "</div>";
          var position16 = new AMap.LngLat(113.2644, 23.1291); //广州
          this.marker16 = new AMap.Marker({
            position: position16,
            // 将 html 传给 content
            content: markerContent2,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "广州"
          });

          var position17 = new AMap.LngLat(121.544, 29.8683); //宁波
          this.marker17 = new AMap.Marker({
            position: position17,
            // 将 html 传给 content
            content: markerContent2,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "宁波"
          });

          var position18 = new AMap.LngLat(121.4737, 31.23037); //上海
          this.marker18 = new AMap.Marker({
            position: position18,
            // 将 html 传给 content
            content: markerContent2,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "上海"
          });
          AMap.Event.addListener(that.marker3, "click", function(e) {
            that.$router.push({
              path:
                "/index/chargeOperation/intelligentDiagnosis/faultList/faultList",
              query: {}
            });
          });
          AMap.Event.addListener(that.marker4, "click", function(e) {
            that.$router.push({
              path:
                "/index/chargeOperation/intelligentDiagnosis/faultList/faultList",
              query: {}
            });
          });
        })
        .catch(e => {
          console.log(e);
        });
    },

    warnFun() {
      this.map.add(this.marker1);
      this.map.add(this.marker2);
      this.map.add(this.marker3);
      this.map.add(this.marker4);
      this.map.add(this.marker5);
      this.map.add(this.marker6);
      this.map.add(this.marker7);
      this.map.add(this.marker8);
      this.map.add(this.marker9);
      this.map.add(this.marker10);
      this.map.add(this.marker11);
      this.map.add(this.marker12);
      this.map.add(this.marker13);
      this.map.add(this.marker14);
      this.map.add(this.marker15);
    },
    errorFun() {
      this.map.add(this.marker16);
      this.map.add(this.marker17);
      this.map.add(this.marker18);
    },

    currentMonthDays(time) {
      // 获取标准时间
      const date = new Date();
      // 获取当天日期
      const currentDay = date.getDate();
      // 获取当前月份（实际月份需要加1）
      const currentMonth =
        date.getMonth() + 1 < 10
          ? "0" + date.getMonth() + 1
          : date.getMonth() + 1;
      // 获取当前年份
      const currentYear = date.getFullYear();
      // 获取当前月有多少天
      const currentMonthDays = new Date(currentYear, currentMonth, 0).getDate();
      // 当前月份所有日期集合
      const currentMonthArr = [];
      if (time == "month") {
        for (let day = 1; day <= currentMonthDays; day++) {
          // 截至当前日期为止
          if (day <= currentDay) {
            // 年月日(yyyy-MM-dd)
            let dateItem = currentMonth + "-" + (day < 10 ? "0" + day : day);
            currentMonthArr.push(dateItem);
          }
        }
      }
      if (time == "year") {
        for (let day = 1; day <= 12; day++) {
          // 截至当前日期为止
          if (day <= currentMonth) {
            // 年月日(yyyy-MM-dd)
            let dateItem = currentYear + "-" + (day < 10 ? "0" + day : day);
            currentMonthArr.push(dateItem);
          }
        }
      }
      return currentMonthArr;
    },
    monthFun() {
      this.initGdzsChart("month");
      this.initYjgdzdChart();
      this.initJkzkzsChart("month");
      this.initGdzlzsChart("month");
      this.initBjfxChart();
      this.dnlj = "当月累计";
      this.chartTitle = "当月工单走势";
      this.chartTitle2 = "当月工单总量走势";
      this.chartTitle3 = "当月健康状况走势";

      this.midNum1 = (Math.random() * 50 + 50).toFixed(0);
      this.midNum2 = (Math.random() * 50 + 50).toFixed(0);
      this.midNum3 = (Math.random() * 50 + 50).toFixed(0);
      this.midNum4 = (Math.random() * 50 + 50).toFixed(1);
      this.midNum5 = (Math.random() * 50 + 50).toFixed(0);
      this.midNum6 = (Math.random() * 50 + 50).toFixed(0);
      this.midNum7 = (Math.random() * 50 + 50).toFixed(0);
      this.midNum8 = (Math.random() * 50 + 50).toFixed(0);
      this.midNum9 = (Math.random() * 50 + 50).toFixed(1);
    },
    yearFun() {
      this.initGdzsChart("year");
      this.initYjgdzdChart();
      this.initJkzkzsChart("year");
      this.initGdzlzsChart("year");
      this.initBjfxChart();
      this.dnlj = "当年累计";
      this.chartTitle = "当年工单走势";
      this.chartTitle2 = "当年工单总量走势";
      this.chartTitle3 = "当年健康状况走势";

      this.midNum1 = (Math.random() * 50 + 50).toFixed(0);
      this.midNum2 = (Math.random() * 50 + 50).toFixed(0);
      this.midNum3 = (Math.random() * 50 + 50).toFixed(0);
      this.midNum4 = (Math.random() * 50 + 50).toFixed(1);
      this.midNum5 = (Math.random() * 50 + 50).toFixed(0);
      this.midNum6 = (Math.random() * 50 + 50).toFixed(0);
      this.midNum7 = (Math.random() * 50 + 50).toFixed(0);
      this.midNum8 = (Math.random() * 50 + 50).toFixed(0);
      this.midNum9 = (Math.random() * 50 + 50).toFixed(1);
    }
  },
  //生命周期 - 创建完成（可以访问当前this实例）
  created() {},
  //生命周期 - 挂载完成（可以访问DOM元素）
  mounted() {
    setTimeout(() => {
      this.initGdzsChart("month");
      this.initYjgdzdChart();
      this.initGdzlzsChart("month");
      this.initJkzkzsChart("month");
      this.initBjfxChart();
      this.initMap();
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
//@import url(); 引入公共css类
.overview {
  // font-family: "宋体";

  .leftDiv {
    position: absolute;
    top: 0;
    left: 0;
    width: 32%;
    height: 100%;

    .leftTop {
      position: absolute;
      top: 0%;
      left: 2%;
      width: 98%;
      height: 14%;
      background-color: #0623208c;

      .jrxz {
        position: absolute;
        top: 35%;
        left: 5%;
        color: #00bbee;
        font-size: 20px;
      }

      .leftNum1 {
        position: absolute;
        top: 25%;
        left: 35%;
        color: #00bbee;
        font-size: 20px;
      }

      .leftSpan1 {
        position: absolute;
        top: 60%;
        left: 34.5%;
        color: #00bbee;
        font-size: 14px;
      }

      .leftNum2 {
        position: absolute;
        top: 25%;
        left: 56%;
        color: #00bbee;
        font-size: 20px;
      }

      .leftSpan2 {
        position: absolute;
        top: 60%;
        left: 54.5%;
        color: #00bbee;
        font-size: 14px;
      }

      .leftNum3 {
        position: absolute;
        top: 25%;
        left: 77%;
        color: #00bbee;
        font-size: 20px;
      }

      .leftSpan3 {
        position: absolute;
        top: 60%;
        left: 76.5%;
        color: #00bbee;
        font-size: 14px;
      }
    }

    .leftCenter {
      position: absolute;
      top: 15%;
      left: 0%;
      width: 100%;
      height: 60%;

      #container {
        margin-left: 2%;
        width: 98%;
        height: 100%;
      }

      .buttonDiv2 {
        position: absolute;
        top: 0%;
        left: 30%;
        width: 70%;
        height: 12%;

        .query1,
        .query2 {
          background-color: #009688;
          border: 1px solid #009688;
          color: #fff;
        }
      }
    }

    .leftBottom {
      position: absolute;
      top: 75%;
      left: 0%;
      width: 100%;
      height: 25%;

      .l-bdiv1 {
        position: relative;
        top: 3%;
        width: 22%;
        height: 92%;
        left: 0%;
        float: left;
        // margin-left: 5%;
        background-color: #0623208c;

        .l-bpic {
          position: absolute;
          font-size: 34px;
          color: #00bbee;
          top: 5%;
          left: 35%;
          height: 37%;
          width: 60%;
        }

        .l-bnum1 {
          position: absolute;
          top: 35%;
          left: 5%;
          height: 20%;
          width: 100%;
          color: #00bbee;
          font-size: 20px;
          text-align: center;
        }

        .l-bnum2 {
          position: absolute;
          top: 55%;
          left: 5%;
          height: 20%;
          width: 100%;
          color: #00bbee;
          font-size: 20px;
          text-align: center;
        }

        .l-btext1 {
          position: absolute;
          top: 80%;
          left: 5%;
          height: 20%;
          width: 100%;
          color: #00bbee;
          font-size: 16px;
          text-align: center;
        }

        .l-btext2 {
          position: absolute;
          top: 80%;
          left: 0%;
          height: 20%;
          width: 100%;
          color: #00bbee;
          font-size: 16px;
          text-align: center;
        }

        #pic1 {
          background: url("../../../../../static/img/chargeOperation/yhl.png")
            no-repeat center center;
        }

        #pic2 {
          background: url("../../../../../static/img/chargeOperation/gzl.png")
            no-repeat center center;
        }

        #pic3 {
          background: url("../../../../../static/img/chargeOperation/tyl.png")
            no-repeat center center;
        }

        #pic4 {
          background: url("../../../../../static/img/chargeOperation/gdjsl.png")
            no-repeat center center;
        }
      }
    }
  }

  .midDiv {
    position: absolute;
    top: 0;
    left: 33%;
    width: 32%;
    height: 100%;

    .midTop {
      position: absolute;
      top: 0%;
      left: 0%;
      width: 100%;
      height: 14%;
      background-color: #0623208c;

      .dnlj {
        position: absolute;
        top: 35%;
        left: 5%;
        color: #00bbee;
        font-size: 20px;
      }

      .midNum1 {
        position: absolute;
        top: 25%;
        left: 35%;
        color: #00bbee;
        font-size: 20px;
      }

      .midSpan1 {
        position: absolute;
        top: 60%;
        left: 33%;
        color: #00bbee;
        font-size: 14px;
      }

      .midNum2 {
        position: absolute;
        top: 25%;
        left: 56%;
        color: #00bbee;
        font-size: 20px;
      }

      .midSpan2 {
        position: absolute;
        top: 61%;
        left: 55%;
        color: #00bbee;
        font-size: 14px;
      }

      .midNum3 {
        position: absolute;
        top: 25%;
        left: 77%;
        color: #00bbee;
        font-size: 20px;
      }

      .midSpan3 {
        position: absolute;
        top: 60%;
        left: 76%;
        color: #00bbee;
        font-size: 14px;
      }
    }

    .midCenter {
      position: absolute;
      top: 15%;
      left: 0%;
      width: 100%;
      height: 50%;

      .buttonDiv {
        position: absolute;
        top: 0%;
        left: 0%;
        width: 100%;
        height: 12%;

        .query1,
        .query2 {
          background-color: #009688;
          border: 1px solid #009688;
          color: #fff;
        }
      }

      .gdzsDiv {
        position: absolute;
        top: 20%;
        left: 0%;
        width: 100%;
        height: 80%;

        .chartTitle {
          position: absolute;
          top: 0%;
          left: 6%;
          width: 100%;
          height: 80%;
          color: #00bbee;
          font-size: 16px;
          font-weight: bold;
        }

        #gdzsChart {
          position: absolute;
          top: 10%;
          left: 0%;
          width: 100%;
          height: 90%;
        }
      }
    }

    .midBottom {
      position: absolute;
      top: 62%;
      left: 0%;
      width: 100%;
      height: 38%;

      .b-ldiv {
        position: absolute;
        top: 0%;
        left: 0%;
        width: 48%;
        height: 97%;
        background-color: #0623208c;

        .midSpan4 {
          position: absolute;
          top: 5%;
          left: 20%;
          color: #00bbee;
          font-size: 24px;
        }

        .midLeftTitle {
          position: absolute;
          top: 25%;
          left: 10%;
          color: #00bbee;
          font-size: 18px;
        }

        .midSpan5 {
          position: absolute;
          top: 40%;
          left: 12%;
          color: #00bbee;
          // font-size: 18px;
        }

        .midSpan6 {
          position: absolute;
          top: 60%;
          left: 12%;
          color: #00bbee;
          // font-size: 18px;
        }

        .midSpan7 {
          position: absolute;
          top: 80%;
          left: 12%;
          color: #00bbee;
          // font-size: 18px;
        }

        .midRightTitle {
          position: absolute;
          top: 25%;
          left: 60%;
          color: #00bbee;
          font-size: 18px;
        }

        .midNum5 {
          position: absolute;
          top: 40%;
          left: 62%;
          color: #00bbee;
          // font-size: 18px;
        }

        .midNum6 {
          position: absolute;
          top: 60%;
          left: 62%;
          color: #00bbee;
          // font-size: 18px;
        }

        .midNum7 {
          position: absolute;
          top: 80%;
          left: 62%;
          color: #00bbee;
          // font-size: 18px;
        }
      }

      .b-rdiv {
        position: absolute;
        top: 0%;
        left: 52%;
        width: 50%;
        height: 97%;
        background-color: #0623208c;

        .midNum9 {
          position: absolute;
          top: 2%;
          left: 32%;
          color: #00bbee;
          font-size: 36px;
        }

        .midSpan9 {
          position: absolute;
          top: 10%;
          left: 10%;
          color: #00bbee;
          font-size: 20px;
        }

        .yjgdzbDiv {
          position: absolute;
          top: 28%;
          left: 0%;
          height: 75%;
          width: 100%;
        }

        #yjgdzbChart {
          position: absolute;
          top: 0%;
          left: 0%;
          width: 100%;
          height: 100%;
        }
      }
    }
  }

  .rightDiv {
    position: absolute;
    top: 0;
    left: 66%;
    width: 32%;
    height: 100%;

    .rightTop {
      position: absolute;
      top: 0%;
      left: 0%;
      width: 100%;
      height: 33%;
    }

    .rightCenter {
      position: absolute;
      top: 33%;
      left: 0%;
      width: 100%;
      height: 33%;
    }

    .rightBottom {
      position: absolute;
      top: 66%;
      left: 0%;
      width: 100%;
      height: 33%;
    }

    #gdzlzsChart,
    #jkzkzsChart,
    #bjfxChart {
      position: absolute;
      top: 5%;
      left: 0%;
      width: 100%;
      height: 100%;
    }

    .chartTitle {
      position: absolute;
      top: 0%;
      left: 6%;
      width: 100%;
      height: 80%;
      color: #00bbee;
      font-size: 16px;
      font-weight: bold;
    }
  }
}
</style>
