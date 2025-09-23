<!--  -->
<template>
  <div class="table">
    <!-- 工具栏 -->
    <!-- <div ref="toolbar" class="toolbar">
      <el-row class="btnGroup">
        <el-button type="primary" size="mini" icon="el-icon-plus" @click="add"
          >新增
        </el-button>
      </el-row>
    </div> -->
    <!-- 表格 -->
    <el-table
      :data="table1Data.slice((currentPage - 1) * pagesize, currentPage * pagesize)"
      id="table"
      stripe
      style="width: 100%"
      :header-row-style="{ height: '35px' }"
      :row-style="{ height: '35px' }"
      :height="height"
      @current-change="clickChange"
    >
      <!-- <el-table-column type="selection"  align="center" min-width="4%"> </el-table-column>
        <el-table-column type="index" label="序号" align="center" min-width="4%"> 
        </el-table-column>-->
      <el-table-column prop="UNIT_NAME" label="地市" align="center" min-width="16%">
      </el-table-column>
      <el-table-column prop="MARKET_NAME" label="备件类别" align="center" min-width="16%">
      </el-table-column>
      <el-table-column prop="TYPE_NAME" label="当前库存数" align="center" min-width="16%">
      </el-table-column>
      <el-table-column
        prop="CAPACITY"
        label="下季度用量预测"
        align="center"
        min-width="18%"
      >
      </el-table-column>
      <el-table-column
        prop="START_TIME"
        label="半年用量预测"
        align="center"
        min-width="18%"
      >
      </el-table-column>
      <el-table-column prop="STATUS" label="状态" align="center" min-width="18%">
      </el-table-column>
      <el-table-column prop="USER" label="推荐厂商" align="center" min-width="18%">
      </el-table-column>
      <el-table-column label="操作" align="center" min-width="14%">
        <template slot-scope="scope">
          <div class="opr">
            <div class="operate" @click="deleteRow(scope.row)">加入采购计划</div>
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
</template>

<script>
//这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）
//例如：import 《组件名称》 from '《组件路径》';

export default {
  //import引入的组件需要注入到对象中才能使用
  components: {},
  props: ["table1Data", "height"],
  data() {
    //这里存放数据
    return {
      tableRadio: "",
      currentPage: 1,
      pagesize: 10,
      pagesizes: [2,5, 10, 20, 50, 100],
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
    table1Data(newVal,oldVal){
      this.currentPage=1;
    }
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

     // 删除
     deleteRow(data) {
      if (data) {
        this.$confirm("确认加入采购计划?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        })
          .then(() => {
           
            setTimeout(() => {
              this.$message({
                type: "success",
                message: "加入成功!",
              });
            }, 1000);
          })
          .catch(() => {});
      } else {
        this.$message({
          message: "请选择行！",
          type: "warning",
        });
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
