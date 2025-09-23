<!--  -->
<template>
  <div>
    <div class="table">
      <!-- 工具栏 -->
      <div ref="toolbar" class="toolbar">
        <el-row class="btnGroup">
          <el-button type="primary" size="mini" @click="deleteSelect(muticalSelectData)"> 删除 </el-button>
          <el-button type="primary" size="mini" @click="cleanFun"> 清空 </el-button>
          <el-button type="primary" size="mini" @click="unlock(muticalSelectData)"> 解锁 </el-button>
          <el-button type="primary" size="mini" @click="exportExcel"> 导出 </el-button>
        </el-row>
      </div>
      <!-- 表格 -->
      <el-table :data="table1Data.slice((currentPage - 1) * pagesize, currentPage * pagesize)" id="table" stripe
        style="width: 100%" :header-row-style="{ height: '35px' }" :row-style="{ height: '35px' }" :height="tableHeight"
        @current-change="clickChange" @selection-change="handleSelectionChange">
        <el-table-column type="selection"  align="center" min-width="4%"> </el-table-column>
        <el-table-column prop="infoId" label="访问编号" align="center" min-width="4%">
        </el-table-column>
        <el-table-column prop="loginName" label="登录名称" align="center" min-width="10%">
        </el-table-column>
        <el-table-column prop="ipaddr" label="登录地址" align="center" min-width="10%">
        </el-table-column>

        <el-table-column prop="loginLocation" label="登录地点" align="center" min-width="10%">
        </el-table-column>
        <el-table-column prop="browser" label="浏览器" align="center" min-width="10%">
        </el-table-column>
        <el-table-column prop="os" label="操作系统" align="center" min-width="10%">
        </el-table-column>
        <el-table-column prop="msg" label="操作信息" align="center" min-width="10%">
        </el-table-column>
        <el-table-column prop="status" label="登录状态" align="center" min-width="10%">
          <template slot-scope="scope">
            <div v-if="scope.row.status==0">
              <el-tag effect="dark" type="">成功</el-tag>
            </div>
            <div v-if="scope.row.status==1">
              <el-tag effect="dark" type="danger">失败</el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="loginTime" label="登录时间" sortable align="center" min-width="10%">
        </el-table-column>
      </el-table>
      <!-- 分页 -->
      <el-pagination background @size-change="handleSizeChange" @current-change="handleCurrentChange"
        :current-page="currentPage" :page-sizes="pagesizes" :page-size="pagesize"
        layout=" prev, pager, next, jumper, sizes,total" :total="total">
      </el-pagination>
    </div>
  </div>
</template>

<script>
//这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）
//例如：import 《组件名称》 from '《组件路径》';
import FileSaver from 'file-saver';
import * as XLSX from 'xlsx';
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

    // 删除复选框选中的数据
    deleteSelect(data) {
      if (data) {
        let length = data.length;
        var ids = [];
        for (const key of data) {
          ids.push(key.infoId)
        }

        this.$confirm("确认删除" + length + "行数据?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        })
          .then(() => {
            this.$http({
              url: this.$http.adornUrl(`/monitor/logininfor/remove`),
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
    // 解锁
    unlock(data) {
      var that = this;
      if (data.length == 1) {
        this.$http({
          url: this.$http.adornUrl(`/monitor/logininfor/unlock`),
          method: "POST",
          params: this.$http.adornParams({
            "loginName": data[0].loginName
          })
        }).then(res => {
          if (res.data.code == 0) {
            this.$message({
              type: "success",
              message: res.data.msg,
            });
            setTimeout(() => {
              this.getData();
            }, 1000);
          } else {
            this.$message({
              message: res.data.msg,
              type: "error"
            })
          }
        }).catch(err => {

        })
      } else {
        this.$message({
          message: '请选择一条数据',
          type: 'warning'
        })
      }
    },

     // 清空
     cleanFun() {
      this.$confirm("确认清空所有登录日志?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.$http({
            url: this.$http.adornUrl(`/monitor/logininfor/clean`),
            method: "POST",
            params: this.$http.adornParams({})
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
    },
    // 导出
    exportExcel() {
      const loading = this.$loading({
        lock: true,
        text: "导出中...",
        spinner: "el-icon-loading",
        background: "rgba(0, 0, 0, 0.7)",
      });
      setTimeout(() => {
        loading.close();
        /* generate workbook object from table */
        var xlsxParam = { raw: true };
        var wb = XLSX.utils.table_to_book(document.querySelector("#table"), xlsxParam);
        /* get binary string as output */
        var wbout = XLSX.write(wb, { bookType: "xlsx", bookSST: true, type: "array" });
        try {
          FileSaver.saveAs(
            new Blob([wbout], { type: "application/octet-stream" }),
            this.$route.meta.title + ".xlsx"
          );
        } catch (e) {
          if (typeof console !== "undefined") console.log(e, wbout);
        }
        return wbout;
      }, 2000);
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
