<template>
  <div id="app" class="contain">
    <div ref="formDiv">
      <el-form ref="form" class="unitForm" :model="form" id="form">
        <el-form-item label="优化方式:">
          <el-select v-model="form.programme" clearable placeholder="贪心算法">
            <el-option
              v-for="item in progOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="优化策略:">
          <el-select v-model="form.method" clearable placeholder="请输入">
            <el-option
              v-for="item in methodOptions"
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
      v-if="!comprehensive"
      element-loading-text="正在优化中..."
      element-loading-spinner="el-icon-loading"
      element-loading-background="rgba(0, 0, 0, 0.8)"
    >
      <div class="allChart">
        <div class="chart1">
          <div class="chartTitle1">{{ originalTitle }}</div>
          <div class="partChart1" ref="partChart1"></div>
        </div>
        <div class="chart2">
          <div class="chartTitle2">{{ optimizeTitle }}</div>
          <div class="partChart2" ref="partChart2"></div>
        </div>
      </div>

      <!-- 优化表格 -->
      <el-table
        v-show="!loading"
        :data="saveData"
        id="table"
        stripe
        style="width: 86%; margin: 0 auto;margin-top: 20px;font-weight: 600;"
        :header-row-style="{ height: '50px' }"
        :row-style="{ height: '50px' }"
      >
        <el-table-column
          prop="programme"
          label="类别"
          align="center"
          min-width="8%"
        >
        </el-table-column>
        <el-table-column prop="cc" label="长春" align="center" min-width="10%">
          <template slot-scope="scope">
            <span
              :style="
                scope.row.ccColor < 0 ? { color: '#13ce66' } : { color: 'red' }
              "
            >
              <i
                :class="
                  scope.row.ccColor < 0 ? 'el-icon-bottom' : 'el-icon-top'
                "
              ></i>
              {{ scope.row.cc }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="cd" label="成都" align="center" min-width="10%">
          <template slot-scope="scope">
            <span
              :style="
                scope.row.cdColor < 0 ? { color: '#13ce66' } : { color: 'red' }
              "
            >
              <i
                :class="
                  scope.row.cdColor < 0 ? 'el-icon-bottom' : 'el-icon-top'
                "
              ></i>
              {{ scope.row.cd }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="fs" label="佛山" align="center" min-width="10%">
          <template slot-scope="scope">
            <span
              :style="
                scope.row.fsColor < 0 ? { color: '#13ce66' } : { color: 'red' }
              "
            >
              <i
                :class="
                  scope.row.fsColor < 0 ? 'el-icon-bottom' : 'el-icon-top'
                "
              ></i>
              {{ scope.row.fs }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="qd" label="青岛" align="center" min-width="10%">
          <template slot-scope="scope">
            <span
              :style="
                scope.row.qdColor < 0 ? { color: '#13ce66' } : { color: 'red' }
              "
            >
              <i
                :class="
                  scope.row.qdColor < 0 ? 'el-icon-bottom' : 'el-icon-top'
                "
              ></i>
              {{ scope.row.qd }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="tj" label="天津" align="center" min-width="10%">
          <template slot-scope="scope">
            <span
              :style="
                scope.row.tjColor < 0 ? { color: '#13ce66' } : { color: 'red' }
              "
            >
              <i
                :class="
                  scope.row.tjColor < 0 ? 'el-icon-bottom' : 'el-icon-top'
                "
              ></i>
              {{ scope.row.tj }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="dl" label="大连" align="center" min-width="10%">
          <template slot-scope="scope">
            <span
              :style="
                scope.row.dlColor < 0 ? { color: '#13ce66' } : { color: 'red' }
              "
            >
              <i
                :class="
                  scope.row.dlColor < 0 ? 'el-icon-bottom' : 'el-icon-top'
                "
              ></i>
              {{ scope.row.dl }}
            </span>
          </template>
        </el-table-column>
        <el-table-column
          prop="allCost"
          label="总成本"
          align="center"
          min-width="10%"
        >
          <template slot-scope="scope">
            <span
              :style="
                scope.row.costColor < 0
                  ? { color: '#13ce66' }
                  : { color: 'red' }
              "
            >
              <i
                :class="
                  scope.row.costColor < 0 ? 'el-icon-bottom' : 'el-icon-top'
                "
              ></i>
              {{ scope.row.allCost }}
            </span>
          </template>
        </el-table-column>
      </el-table>

      <el-table
        :data="tableData"
        id="table"
        stripe
        style="width: 86%; margin: 0 auto;margin-top: 20px;"
        :header-row-style="{ height: '50px' }"
        :row-style="{ height: '50px' }"
      >
        <el-table-column prop="prov" label="省份" align="center" min-width="8%">
        </el-table-column>
        <el-table-column prop="city" label="城市" align="center" min-width="8%">
        </el-table-column>
        <el-table-column prop="cc" label="长春" align="center" min-width="10%">
        </el-table-column>
        <el-table-column prop="cd" label="成都" align="center" min-width="10%">
        </el-table-column>
        <el-table-column prop="fs" label="佛山" align="center" min-width="10%">
        </el-table-column>
        <el-table-column prop="qd" label="青岛" align="center" min-width="10%">
        </el-table-column>
        <el-table-column prop="tj" label="天津" align="center" min-width="10%">
        </el-table-column>
        <el-table-column prop="dl" label="大连" align="center" min-width="10%">
        </el-table-column>
        <el-table-column
          prop="cost"
          label="运输成本(元)"
          align="center"
          min-width="10%"
        >
        </el-table-column>
      </el-table>
    </div>

    <!-- 综合优化概览 -->
    <div v-if="comprehensive">
      <div class="chart">
        <div class="chartTitle">零件物流成本综合概览图</div>
        <div class="partChart" ref="partChart"></div>
      </div>
      <el-table
        :data="saveData"
        id="table"
        stripe
        style="width: 86%; margin: 0 auto;margin-top: 20px; font-weight: 600;"
        :header-row-style="{ height: '50px' }"
        :row-style="{ height: '50px' }"
      >
        <el-table-column
          prop="programme"
          label="方案"
          align="center"
          min-width="12%"
        >
        </el-table-column>
        <el-table-column prop="cc" label="长春" align="center" min-width="11%">
          <template slot-scope="scope">
            <span
              :style="{
                color:
                  scope.row.ccColor === 0
                    ? 'white'
                    : scope.row.ccColor < 0
                    ? '#13ce66'
                    : 'red'
              }"
            >
              <i
                v-if="scope.row.ccColor !== 0"
                :class="
                  scope.row.ccColor < 0 ? 'el-icon-bottom' : 'el-icon-top'
                "
              ></i>
              {{ scope.row.cc }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="cd" label="成都" align="center" min-width="10%">
          <template slot-scope="scope">
            <span
              :style="{
                color:
                  scope.row.cdColor === 0
                    ? 'white'
                    : scope.row.cdColor < 0
                    ? '#13ce66'
                    : 'red'
              }"
            >
              <i
                v-if="scope.row.cdColor !== 0"
                :class="
                  scope.row.cdColor < 0 ? 'el-icon-bottom' : 'el-icon-top'
                "
              ></i>
              {{ scope.row.cd }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="fs" label="佛山" align="center" min-width="10%">
          <template slot-scope="scope">
            <span
              :style="{
                color:
                  scope.row.fsColor === 0
                    ? 'white'
                    : scope.row.fsColor < 0
                    ? '#13ce66'
                    : 'red'
              }"
            >
              <i
                v-if="scope.row.fsColor !== 0"
                :class="
                  scope.row.fsColor < 0 ? 'el-icon-bottom' : 'el-icon-top'
                "
              ></i>
              {{ scope.row.fs }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="qd" label="青岛" align="center" min-width="10%">
          <template slot-scope="scope">
            <span
              :style="{
                color:
                  scope.row.qdColor === 0
                    ? 'white'
                    : scope.row.qdColor < 0
                    ? '#13ce66'
                    : 'red'
              }"
            >
              <i
                v-if="scope.row.qdColor !== 0"
                :class="
                  scope.row.qdColor < 0 ? 'el-icon-bottom' : 'el-icon-top'
                "
              ></i>
              {{ scope.row.qd }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="tj" label="天津" align="center" min-width="10%">
          <template slot-scope="scope">
            <span
              :style="{
                color:
                  scope.row.tjColor === 0
                    ? 'white'
                    : scope.row.tjColor < 0
                    ? '#13ce66'
                    : 'red'
              }"
            >
              <i
                v-if="scope.row.tjColor !== 0"
                :class="
                  scope.row.tjColor < 0 ? 'el-icon-bottom' : 'el-icon-top'
                "
              ></i>
              {{ scope.row.tj }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="dl" label="大连" align="center" min-width="10%">
          <template slot-scope="scope">
            <span
              :style="{
                color:
                  scope.row.dlColor === 0
                    ? 'white'
                    : scope.row.dlColor < 0
                    ? '#13ce66'
                    : 'red'
              }"
            >
              <i
                v-if="scope.row.dlColor !== 0"
                :class="
                  scope.row.dlColor < 0 ? 'el-icon-bottom' : 'el-icon-top'
                "
              ></i>
              {{ scope.row.dl }}
            </span>
          </template>
        </el-table-column>
        <el-table-column
          prop="allCost"
          label="总成本"
          align="center"
          min-width="11%"
        >
          <template slot-scope="scope">
            <span
              :style="{
                color:
                  scope.row.costColor === 0
                    ? 'white'
                    : scope.row.costColor < 0
                    ? '#13ce66'
                    : 'red'
              }"
            >
              <i
                v-if="scope.row.costColor !== 0"
                :class="
                  scope.row.costColor < 0 ? 'el-icon-bottom' : 'el-icon-top'
                "
              ></i>
              {{ scope.row.allCost }}
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
// import { color } from 'highcharts';
export default {
  //import引入的组件需要注入到对象中才能使用
  components: {
    JobChat
  },
  data() {
    return {
      form: {
        programme: "综合优化概览",
        method: "原始方法"
      },
      allTableData: [
        {
          type: "原始成本",
          programme: "原始方法",
          cc: 33442900.47,
          cd: 7920157.53,
          fs: 3943806.94,
          qd: 2044375.79,
          tj: 1045296.84,
          dl: 589063.18,
          allCost: 48985600.74,
          ccColor: 0,
          cdColor: 0,
          fsColor: 0,
          qdColor: 0,
          tjColor: 0,
          dlColor: 0,
          allCostColor: 0
        },
        {
          type: "优化成本",
          programme: "原始成本+遗传算法",
          cc: 32522715.19,
          cd: 7131303.28,
          fs: 3569498.45,
          qd: 1734731.91,
          tj: 1031389.13,
          dl: 517056.05,
          allCost: 46506694.01,
          ccColor: 0,
          cdColor: 0,
          fsColor: 0,
          qdColor: 0,
          tjColor: 0,
          dlColor: 0,
          allCostColor: 0
        },
        {
          type: "优化成本",
          programme: "原始成本+退火算法",
          cc: 32060803.76,
          cd: 7107174.94,
          fs: 3567430.59,
          qd: 1819815.87,
          tj: 931668.19,
          dl: 568825.34,
          allCost: 46055718.71,
          ccColor: 0,
          cdColor: 0,
          fsColor: 0,
          qdColor: 0,
          tjColor: 0,
          dlColor: 0,
          allCostColor: 0
        }
      ],
      tableData: [],
      saveData: [],
      optimizeData: [
        {
          type: "优化成本",
          programme: "贪心优化算法+原始方法",
          cc: 31629401.68,
          cd: 7294723.51,
          fs: 3539910.23,
          qd: 2134716.26,
          tj: 1131299.02,
          dl: 580510.39,
          allCost: 46310561.11,
          ccColor: 0,
          cdColor: 0,
          fsColor: 0,
          qdColor: 0,
          tjColor: 0,
          dlColor: 0,
          allCostColor: 0
        },
        {
          type: "优化成本",
          programme: "城市因子(开7次方)+原始方法",
          cc: 32281954.62,
          cd: 7576596.89,
          fs: 3410528.86,
          qd: 1532793.45,
          tj: 839594.46,
          dl: 612837.59,
          allCost: 46254305.89,
          ccColor: 0,
          cdColor: 0,
          fsColor: 0,
          qdColor: 0,
          tjColor: 0,
          dlColor: 0,
          allCostColor: 0
        },
        {
          type: "优化成本",
          programme: "城市因子(sigmoid)+原始方法",
          cc: 32189208.52,
          cd: 7684903.41,
          fs: 3390620.56,
          qd: 1529034.93,
          tj: 839594.46,
          dl: 604279.35,
          allCost: 46237641.23,
          ccColor: 0,
          cdColor: 0,
          fsColor: 0,
          qdColor: 0,
          tjColor: 0,
          dlColor: 0,
          allCostColor: 0
        },
        {
          type: "优化成本",
          programme: "贪心优化算法+遗传算法",
          cc: 31774453.11,
          cd: 7219201.0,
          fs: 3571807.74,
          qd: 2033336.78,
          tj: 1080193.39,
          dl: 506976.31,
          allCost: 46185968.32,
          ccColor: 0,
          cdColor: 0,
          fsColor: 0,
          qdColor: 0,
          tjColor: 0,
          dlColor: 0,
          allCostColor: 0
        },
        {
          type: "优化成本",
          programme: "城市因子(开7次方)+遗传算法",
          cc: 31803216.99,
          cd: 7231108.28,
          fs: 3573103.81,
          qd: 2075676.86,
          tj: 989699.4,
          dl: 507658.46,
          allCost: 46180463.8,
          ccColor: 0,
          cdColor: 0,
          fsColor: 0,
          qdColor: 0,
          tjColor: 0,
          dlColor: 0,
          allCostColor: 0
        },
        {
          type: "优化成本",
          programme: "城市因子(sigmoid)+遗传算法",
          cc: 31872063.12,
          cd: 7163642.75,
          fs: 3568826.25,
          qd: 2080568.54,
          tj: 906116.91,
          dl: 525301.06,
          allCost: 46116518.62,
          ccColor: 0,
          cdColor: 0,
          fsColor: 0,
          qdColor: 0,
          tjColor: 0,
          dlColor: 0,
          allCostColor: 0
        },
        {
          type: "优化成本",
          programme: "贪心优化算法+退火算法",
          cc: 31940054.23,
          cd: 7057544.26,
          fs: 3514515.83,
          qd: 2064651.77,
          tj: 899374.9,
          dl: 562998.24,
          allCost: 46039139.24,
          ccColor: 0,
          cdColor: 0,
          fsColor: 0,
          qdColor: 0,
          tjColor: 0,
          dlColor: 0,
          allCostColor: 0
        },
        {
          type: "优化成本",
          programme: "城市因子(开7次方)+退火算法",
          cc: 32066584.25,
          cd: 7054508.25,
          fs: 3570853.75,
          qd: 1935052.53,
          tj: 899374.9,
          dl: 510895.01,
          allCost: 46037268.7,
          ccColor: 0,
          cdColor: 0,
          fsColor: 0,
          qdColor: 0,
          tjColor: 0,
          dlColor: 0,
          allCostColor: 0
        },
        {
          type: "优化成本",
          programme: "城市因子(sigmoid)+退火算法",
          cc: 31883444.22,
          cd: 7110499.65,
          fs: 3535203.64,
          qd: 1996851.55,
          tj: 946571.09,
          dl: 492473.95,
          allCost: 45965044.09,
          ccColor: 0,
          cdColor: 0,
          fsColor: 0,
          qdColor: 0,
          tjColor: 0,
          dlColor: 0,
          allCostColor: 0
        }
      ],
      originalCost: [],
      optimizeCost: [],
      TableHeight: 2,
      tableRadio: {},
      currentPage: 1,
      pagesize: 10,
      pagesizes: [10, 20, 50, 100, 200],
      total: 0,
      title: "",
      loading: false,
      comprehensive: true,
      progOptions: [
        { value: "综合优化概览", label: "综合优化概览" },
        { value: "贪心优化算法", label: "贪心优化算法" },
        { value: "城市因子(开7次方)", label: "城市因子(开7次方)" },
        { value: "城市因子(sigmoid)", label: "城市因子(sigmoid)" }
      ],
      methodOptions: [
        { value: "原始方法", label: "原始方法" },
        { value: "遗传算法", label: "遗传算法" },
        { value: "退火算法", label: "退火算法" }
      ],
      originalTitle: "原始方案零件优化成本",
      optimizeTitle: ""
    };
  },
  //监听属性 类似于data概念
  computed: {},
  //监控data中的数据变化
  watch: {},
  //方法集合
  methods: {
    transData(tData) {
      return [
        { value: tData.cc, name: "长春" },
        { value: tData.cd, name: "成都" },
        { value: tData.fs, name: "佛山" },
        { value: tData.qd, name: "青岛" },
        { value: tData.tj, name: "天津" },
        { value: tData.dl, name: "大连" }
      ];
    },
    // 表单查询
    getData() {
      // 综合优化概览模块
      if (this.form.programme == "综合优化概览") {
        this.comprehensive = true;
        this.saveData = [...this.allTableData];
        this.saveData.push(...this.optimizeData);
        this.saveData.forEach(obj => {
          // 创建新的对象并复制原对象的属性
          obj["ccColor"] = obj.cc - this.saveData[0].cc;
          obj["cdColor"] = obj.cd - this.saveData[0].cd;
          obj["fsColor"] = obj.fs - this.saveData[0].fs;
          obj["qdColor"] = obj.qd - this.saveData[0].qd;
          obj["tjColor"] = obj.tj - this.saveData[0].tj;
          obj["dlColor"] = obj.dl - this.saveData[0].dl;
          obj["costColor"] = obj.allCost - this.saveData[0].allCost;
        });
        setTimeout(() => {
          this.initCharts();
        }, 500);
        return; // 结束函数
      }

      // 下面是优化模块
      this.comprehensive = false;
      const params = { ...this.form };
      axios
        .post(this.baseurl + "/part/optimize", params)
        .then(res => {
          const data = res.data.data;
          this.tableData = data;
          // 获取表格数据总数量
          this.total = data.length;
        })
        .catch(error => console.log(error));
      // 当优化方法修改时，同时也更改echart数据和表格数据
      if (this.form.method == "原始方法") {
        this.saveData = [this.allTableData[0]];
      } else if (this.form.method == "遗传算法") {
        this.saveData = [this.allTableData[1]];
      } else {
        this.saveData = [this.allTableData[2]];
      }
      this.originalTitle = this.form.programme + "成本";
      this.optimizeTitle = this.form.programme + this.form.method + "优化成本";
      // console.log(this.saveData)

      this.saveData.push(
        this.optimizeData.filter(
          item =>
            item.programme === `${this.form.programme}+${this.form.method}`
        )[0]
      );
      this.originalCost = this.transData(this.saveData[0]);
      this.optimizeCost = this.transData(this.saveData[1]);
      //进行比较
      this.saveData[0]["ccColor"] =
        this.saveData[0]["cc"] - this.saveData[1]["cc"];
      this.saveData[1]["ccColor"] =
        this.saveData[1]["cc"] - this.saveData[0]["cc"];
      this.saveData[0]["cdColor"] =
        this.saveData[0]["cd"] - this.saveData[1]["cd"];
      this.saveData[1]["cdColor"] =
        this.saveData[1]["cd"] - this.saveData[0]["cd"];
      this.saveData[0]["fsColor"] =
        this.saveData[0]["fs"] - this.saveData[1]["fs"];
      this.saveData[1]["fsColor"] =
        this.saveData[1]["fs"] - this.saveData[0]["fs"];
      this.saveData[0]["qdColor"] =
        this.saveData[0]["qd"] - this.saveData[1]["qd"];
      this.saveData[1]["qdColor"] =
        this.saveData[1]["qd"] - this.saveData[0]["qd"];
      this.saveData[0]["tjColor"] =
        this.saveData[0]["tj"] - this.saveData[1]["tj"];
      this.saveData[1]["tjColor"] =
        this.saveData[1]["tj"] - this.saveData[0]["tj"];
      this.saveData[0]["dlColor"] =
        this.saveData[0]["dl"] - this.saveData[1]["dl"];
      this.saveData[1]["dlColor"] =
        this.saveData[1]["dl"] - this.saveData[0]["dl"];
      this.saveData[1]["costColor"] =
        this.saveData[1]["allCost"] - this.saveData[0]["allCost"];
    },
    onSearch() {
      if (this.form.programme == "" && this.form.method == "") {
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
          this.initCharts1();
          this.initCharts2();
        }, 1000);
      }
    },
    downloadExcel() {
      if (this.form.programme == "" && this.form.method == "") {
        this.$message({
          message: "优化方法不能为空",
          type: "error"
        });
      } else {
        let filename =
          this.form.programme + "+" + this.form.method + "优化结果.xlsx";
        if (this.form.programme == "综合优化概览") {
          filename = "各方案优化结果统计汇总表.xlsx";
        }
        axios({
          url: this.baseurl + "/part/download", // 替换为实际的后端接口
          method: "POST",
          responseType: "blob", // 设置响应类型为 blob
          data: {
            programme: this.form.programme,
            method: this.form.method
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
    initCharts1() {
      let option = {
        tooltip: {
          trigger: "item"
        },
        legend: {
          top: "5%",
          left: "center",
          textStyle: {
            fontSize: 17, //字体大小
            color: "rgb(125, 180, 173)" //字体颜色
          }
        },
        series: [
          {
            name: "Access From",
            type: "pie",
            radius: ["45%", "95%"],
            avoidLabelOverlap: false,
            top: "20%",
            itemStyle: {
              borderRadius: 8,
              borderColor: "#fff",
              borderWidth: 2
            },
            label: {
              show: false,
              position: "center"
            },
            emphasis: {
              label: {
                show: true,
                fontSize: 20,
                fontWeight: "bold",
                formatter: params => {
                  const percentage = (params.value / 48985600.74).toFixed(4); // 将比例保留三位小数
                  return `${params.name}\n${percentage}%`;
                }
              }
            },
            labelLine: {
              show: false
            },
            data: this.originalCost
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
          trigger: "item"
        },
        legend: {
          top: "5%",
          left: "center",
          textStyle: {
            fontSize: 17, //字体大小
            color: "rgb(125, 180, 173)" //字体颜色
          }
        },
        series: [
          {
            name: "Access From",
            type: "pie",
            radius: ["45%", "95%"],
            avoidLabelOverlap: false,
            top: "20%",
            itemStyle: {
              borderRadius: 8,
              borderColor: "#fff",
              borderWidth: 2
            },
            label: {
              show: false,
              position: "center"
            },
            emphasis: {
              label: {
                show: true,
                fontSize: 20,
                fontWeight: "bold",
                formatter: params => {
                  const percentage = (params.value / 46310561.11).toFixed(4); // 将比例保留三位小数
                  return `${params.name}\n${percentage}%`;
                }
              }
            },
            labelLine: {
              show: false
            },
            data: this.optimizeCost
          }
        ]
      };
      const myChart = this.$echarts.init(this.$refs.partChart2);
      myChart.setOption(option);
      window.addEventListener("resize", () => {
        myChart.resize();
      });
    },
    initCharts() {
      let option = {
        tooltip: {
          trigger: "axis",
          axisPointer: {
            // Use axis to trigger tooltip
            type: "shadow" // 'shadow' as default; can also be 'line' or 'shadow'
          }
        },
        legend: {
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
        xAxis: {
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
        },
        yAxis: {
          type: "category",
          data: [
            "城市因子(sigmoid)+退火算法",
            "城市因子(开7次方)+退火算法",
            "贪心算法+退火算法",
            "原始方案+退火算法",
            "城市因子(sigmoid)+遗传算法",
            "城市因子(开7次方)+遗传算法",
            "贪心算法+遗传算法",
            "原始方案+遗传算法",
            "城市因子(开七次方)",
            "城市因子(sigmoid)",
            "贪心优化算法",
            "原始方法"
          ],
          axisLabel: {
            color: "rgb(125, 180, 173)" // 设置 y 轴字体颜色为蓝色
          }
        },
        series: [
          {
            name: "长春",
            type: "bar",
            stack: "total",
            label: {
              show: true
            },
            emphasis: {
              focus: "series"
            },
            data: [
              31883444,
              32066584,
              31940054,
              32060804,
              31872063,
              31803217,
              31774453,
              32522715,
              32281954,
              32189208,
              31629401,
              33442900
            ]
          },
          {
            name: "成都",
            type: "bar",
            stack: "total",
            label: {
              show: true
            },
            emphasis: {
              focus: "series"
            },
            data: [
              7110500,
              7054508,
              7057544,
              7107175,
              7163643,
              7231108,
              7219201,
              7131303,
              7576596,
              7684903,
              7294723,
              7920157
            ]
          },
          {
            name: "佛山",
            type: "bar",
            stack: "total",
            label: {
              show: true
            },
            emphasis: {
              focus: "series"
            },
            data: [
              3535204,
              3570854,
              3514516,
              3567431,
              3568826,
              3573104,
              3571808,
              3569498,
              3410528,
              3390620,
              3539910,
              3943806
            ]
          },
          {
            name: "青岛",
            type: "bar",
            stack: "total",
            label: {
              show: false // 设置为 false，使标签数字不显示
            },
            emphasis: {
              focus: "series"
            },
            data: [
              1996852,
              1935053,
              2064652,
              1819816,
              2080568,
              2075676,
              2033337,
              1734732,
              1532793,
              1529034,
              2134716,
              2044375
            ]
          },
          {
            name: "天津",
            type: "bar",
            stack: "total",
            label: {
              show: false // 设置为 false，使标签数字不显示
            },
            emphasis: {
              focus: "series"
            },
            data: [
              946571,
              899375,
              899375,
              931668,
              906117,
              989699,
              1080193,
              1031389,
              839594,
              839594,
              1131299,
              1045296
            ]
          },
          {
            name: "大连",
            type: "bar",
            stack: "total",
            label: {
              show: true
            },
            emphasis: {
              focus: "series"
            },
            data: [
              492474,
              510895,
              562998,
              568825,
              525301,
              507658,
              506976,
              517056,
              612837,
              604279,
              580510,
              589063
            ]
          }
        ]
      };
      const myChart = this.$echarts.init(this.$refs.partChart);
      myChart.setOption(option);
      window.addEventListener("resize", () => {
        myChart.resize();
      });
    }
  },
  //生命周期 - 挂载完成（可以访问DOM元素）
  mounted() {
    //动态计算表格高度
    this.getData();
    let windowHeight =
      document.documentElement.clientHeight || document.bodyclientHeight;
    this.$nextTick(() => {
      this.TableHeight = windowHeight - this.$refs.formDiv.offsetHeight - 175; //数值"140"根据需要调整
    });
    setTimeout(() => {
      // this.initCharts1();
      // this.initCharts2();
      this.initCharts();
    }, 500);
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
      padding-top: 10px;
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
      padding-top: 10px;
      height: 12%;
    }

    .partChart2 {
      height: 85%;
    }
  }
}

.chart {
  text-align: center;
  color: rgb(125, 180, 173);
  font-size: 19px;
  width: 80%;
  height: 360px;
  margin: 0 auto;
  background-color: #0623208c;
  border-radius: 5px;

  .chartTitle {
    padding-top: 10px;
    height: 12%;
  }

  .partChart {
    height: 85%;
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

// .el-table tr {
//   color: green !important;
// }
</style>
