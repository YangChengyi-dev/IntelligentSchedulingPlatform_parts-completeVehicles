<!--  -->
<template>
  <div>
    <div class="table">
      <!-- 工具栏 -->
      <div ref="toolbar" class="toolbar">
        <el-row class="btnGroup">
          <el-button type="primary" size="mini" icon="el-icon-plus" @click="add"
            >返修件入库登记
          </el-button>
        </el-row>
      </div>
      <!-- 表格 -->
      <el-table
        :data="table1Data.slice((currentPage - 1) * pagesize, currentPage * pagesize)"
        id="table"
        stripe
        style="width: 100%"
        :header-row-style="{ height: '35px' }"
        :row-style="{ height: '35px' }"
        :height="tableHeight"
        @current-change="clickChange"
      >
        <!-- <el-table-column type="selection"  align="center" min-width="4%"> </el-table-column>
        <el-table-column type="index" label="序号" align="center" min-width="4%"> 
        </el-table-column>-->
        <el-table-column prop="NUMBER" label="返修件类型" align="center" min-width="10%">
        </el-table-column>
        <el-table-column
          prop="UNIT_NAME"
          label="返修件名称"
          align="center"
          min-width="10%"
        >
        </el-table-column>
        <el-table-column
          prop="MARKET_NAME"
          label="状态"
          :formatter="matterStatus"
          align="center"
          min-width="10%"
        >
        </el-table-column>
        <el-table-column prop="TYPE_NAME" label="厂商" align="center" min-width="10%">
        </el-table-column>
        <el-table-column prop="CAPACITY" label="型号" align="center" min-width="10%">
        </el-table-column>
        <el-table-column prop="YEAR" label="场站" align="center" min-width="10%">
        </el-table-column>
        <el-table-column prop="ORDER" label="充电桩编号" align="center" min-width="10%">
        </el-table-column>
        <el-table-column prop="TIME" label="入库时间" align="center" min-width="10%">
        </el-table-column>
        <el-table-column prop="PROBLEM" label="入库人" align="center" min-width="10%">
        </el-table-column>
        <el-table-column label="操作" align="center" min-width="16%">
          <template slot-scope="scope">
            <div class="opr">
              <template v-if="scope.row.MARKET_NAME == 3">
                <div class="operate" @click="back(scope.row)">回库</div>
                <div class="operate" @click="scrap(scope.row)">报废</div>
              </template>
            </div>
          </template>
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
        :total="total"
      >
      </el-pagination>
    </div>
    <!-- 新增，编辑弹框 -->
    <div class="dialog">
      <Dialog
        :title="title"
        width="70%"
        height="80%"
        :isDetail="isDetail"
        v-if="openDialog"
        ref="testDialog"
      ></Dialog>
    </div>
  </div>
</template>

<script>
//这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）
//例如：import 《组件名称》 from '《组件路径》';
import Dialog from "./dialog";
export default {
  //import引入的组件需要注入到对象中才能使用
  components: { Dialog },
  props: ["table1Data", "height"],
  data() {
    //这里存放数据
    return {
      tableRadio: "",
      currentPage: 1,
      pagesize: 10,
      pagesizes: [2, 5, 10, 20, 50, 100],

      title: "",
      isDetail: false,
      openDialog: false,
      tableHeight: 0,
    };
  },
  //监听属性 类似于data概念
  computed: {
    total: {
      get() {
        return this.table1Data.length;
      },
    },
  },
  //监控data中的数据变化
  watch: {
    table1Data(newVal, oldVal) {
      this.currentPage = 1;
    },
    height(newVal, oldVal) {
      this.tableHeight = newVal - this.$refs.toolbar.offsetHeight;
    },
  },
  //方法集合
  methods: {
    // 单选获取整行数据
    clickChange(item) {
      this.tableRadio = item;
    },

    // 表格选择当前显示行数
    handleSizeChange(val) {
      this.pagesize = val;
    },
    // 切换表格页面
    handleCurrentChange(val) {
      this.currentPage = val;
    },
    // 新增
    add() {
      this.openDialog = true;
      this.isDetail = false;
      this.title = "新增";
      this.$nextTick(() => {
        this.$refs.testDialog.init(null);
      });
    },
    // 回库
    back() {
      this.$confirm("确认回库?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          setTimeout(() => {
            this.$message({
              type: "success",
              message: "回库成功!",
            });
          }, 1000);
        })
        .catch(() => {
          setTimeout(() => {
            this.$message({
              type: "error",
              message: "回库失败!",
            });
          }, 1000);
        });
    },
    // 报废
    scrap() {
      this.$confirm("确认报废?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          setTimeout(() => {
            this.$message({
              type: "success",
              message: "报废成功!",
            });
          }, 1000);
        })
        .catch(() => {
          setTimeout(() => {
            this.$message({
              type: "error",
              message: "报废失败!",
            });
          }, 1000);
        });
    },
    matterStatus(row, column, cellValue, index) {
      switch (cellValue) {
        case "1":
          return "检修再入库";
          break;
        case "2":
          return "报废";
          break;
        case "3":
          return "正常";
          break;
        default:
          return "";
      }
    },
  },
  //生命周期 - 创建完成（可以访问当前this实例）
  created() {},
  //生命周期 - 挂载完成（可以访问DOM元素）
  mounted() {},
  beforeCreate() {}, //生命周期 - 创建之前
  beforeMount() {}, //生命周期 - 挂载之前
  beforeUpdate() {}, //生命周期 - 更新之前
  updated() {}, //生命周期 - 更新之后
  beforeDestroy() {}, //生命周期 - 销毁之前
  destroyed() {}, //生命周期 - 销毁完成
  activated() {}, //如果页面有keep-alive缓存功能，这个函数会触发
};
</script>
<style lang="scss" scoped>
//@import url(); 引入公共css类
.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-evenly;
  padding-bottom: 15px;

  .btnGroup {
    width: 100%;
  }
}
.opr {
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  .operate {
    color: #1ba799;
    cursor: pointer;
  }
}
</style>
