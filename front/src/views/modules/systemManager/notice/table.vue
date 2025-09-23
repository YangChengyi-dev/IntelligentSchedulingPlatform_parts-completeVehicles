<!--  -->
<template>
  <div>
    <div class="table">
      <!-- 工具栏 -->
      <div ref="toolbar" class="toolbar">
        <el-row class="btnGroup">
          <el-button type="primary" size="mini" @click="addRow(null)">新增 </el-button>
          <el-button type="primary" size="mini" @click="editRow(muticalSelectData)"> 修改 </el-button>
          <el-button type="primary" size="mini" @click="deleteRow(muticalSelectData)"> 删除 </el-button>
        </el-row>
      </div>
      <!-- 表格 -->
      <el-table :data="table1Data.slice((currentPage - 1) * pagesize, currentPage * pagesize)" id="table" stripe
        style="width: 100%" :header-row-style="{ height: '35px' }" :row-style="{ height: '35px' }" :height="tableHeight"
        @current-change="clickChange" @selection-change="handleSelectionChange">
        <el-table-column type="selection" align="center" min-width="4%"> </el-table-column>
        <el-table-column prop="noticeId" label="序号" align="center" min-width="4%">
        </el-table-column>
        <el-table-column prop="noticeTitle" label="公告标题" align="center" min-width="10%">
        </el-table-column>
        <el-table-column prop="noticeType" label="公告类型" align="center" min-width="10%">
          <template slot-scope="scope">
            <div v-if="scope.row.noticeType == '2'">
              <el-tag effect="dark" type="">公告</el-tag>
            </div>
            <div v-if="scope.row.noticeType == '1'">
              <el-tag effect="dark" type="">通知</el-tag>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="status" label="状态" align="center" min-width="10%">
          <template slot-scope="scope">
            <div v-if="scope.row.status == '0'">
              <el-tag effect="dark" type="">正常</el-tag>
            </div>
            <div v-if="scope.row.status == '1'">
              <el-tag effect="dark" type="">关闭</el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="createBy" label="创建者" align="center" min-width="10%">
        </el-table-column>

        <el-table-column prop="createTime" label="创建时间" align="center" min-width="10%">
        </el-table-column>
        <el-table-column label="操作" align="center" min-width="10%">
          <template slot-scope="scope">
            <div class="opr">
              <el-button type="primary" icon="el-icon-edit" size="mini" @click="editRow(scope.row)">编辑</el-button>
              <el-button type="primary" icon="el-icon-delete" size="mini" @click="deleteRow(scope.row)">删除</el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
      <!-- 分页 -->
      <el-pagination background @size-change="handleSizeChange" @current-change="handleCurrentChange"
        :current-page="currentPage" :page-sizes="pagesizes" :page-size="pagesize"
        layout=" prev, pager, next, jumper, sizes,total" :total="total">
      </el-pagination>
    </div>
    <!-- 新增，编辑弹框 -->
    <div class="dialog">
      <Dialog :title="title" width="70%" :isDetail="isDetail" v-if="openDialog" ref="testDialog"></Dialog>
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

      muticalSelectData: [],

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
    // 复选框选中的数组
    handleSelectionChange(val) {
      this.muticalSelectData = val;
    },
    // 新增
    addRow(data) {
      this.openDialog = true;
      this.isDetail = false;
      this.title = "添加公告";
      this.$nextTick(() => {
        this.$refs.testDialog.addFun(data, 'add');
      });
    },
    // 编辑
    editRow(data) {
      var that = this;
      let arr = [];
      if (Array.isArray(data)) {//是数组
        arr = data;
      } else {//obj
        arr.push(data);
      }
      if (arr.length == 1) {
        that.openDialog = true;
        that.isDetail = false;
        that.title = "修改公告";
        that.$nextTick(() => {
          that.$refs.testDialog.editFun(arr[0], 'edit');
        });
      } else {
        this.$message({
          message: '请选择一条数据',
          type: 'warning'
        })
      }
    },
    // 删除复选框选中的数据
    deleteRow(data) {
      if (data) {
        let arr = [];
        var length='该';
        if (Array.isArray(data)) {//是数组
          arr = data;
          length = arr.length;
        } else {//obj
          arr.push(data);
        }

        var ids = [];
        for (const key of arr) {
          ids.push(key.noticeId)
        }

        this.$confirm("确认删除" + length + "行数据?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        })
          .then(() => {
            this.$http({
              url: this.$http.adornUrl(`/system/notice/remove`),
              method: "POST",
              params: this.$http.adornParams({
                "ids": ids.join(',')
              })
            }).then(res => {
              if (res.data.code == 0) {
                this.$message({
                  type: "success",
                  message: res.data.msg,
                });
                setTimeout(() => {
                  this.$parent.getData();
                }, 1000);
              } else {
                this.$message({
                  message: res.data.msg,
                  type: "error"
                })
              }
            }).catch(err => {

            })

          })
          .catch(() => { });
      } else {
        this.$message({
          message: "请选择行！",
          type: "warning",
        });
      }
    },
  },
  //生命周期 - 创建完成（可以访问当前this实例）
  created() { },
  //生命周期 - 挂载完成（可以访问DOM元素）
  mounted() { },
  beforeCreate() { }, //生命周期 - 创建之前
  beforeMount() { }, //生命周期 - 挂载之前
  beforeUpdate() { }, //生命周期 - 更新之前
  updated() { }, //生命周期 - 更新之后
  beforeDestroy() { }, //生命周期 - 销毁之前
  destroyed() { }, //生命周期 - 销毁完成
  activated() { }, //如果页面有keep-alive缓存功能，这个函数会触发
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
