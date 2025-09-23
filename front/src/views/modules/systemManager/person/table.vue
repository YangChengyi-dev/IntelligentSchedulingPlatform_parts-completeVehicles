<!--  -->
<template>
  <div>
    <div class="table">
      <!-- 工具栏 -->
      <div ref="toolbar" class="toolbar">
        <el-row class="btnGroup">
          <el-button type="primary" size="mini" @click="addRow">新增 </el-button>
          <el-button type="primary" size="mini" @click="editRow(muticalSelectData)"> 修改 </el-button>
          <el-button type="primary" size="mini" @click="deleteSelect(muticalSelectData)"> 删除 </el-button>
          <el-button type="primary" size="mini" @click="importExcel"> 导入 </el-button>
          <el-button type="primary" size="mini" @click="exportExcel"> 导出 </el-button>
        </el-row>
      </div>
      <!-- 表格 -->
      <el-table :data="table1Data.slice((currentPage - 1) * pagesize, currentPage * pagesize)" id="table" stripe
        style="width: 100%" :header-row-style="{ height: '35px' }" :row-style="{ height: '35px' }" :height="tableHeight"
        @current-change="clickChange" @selection-change="handleSelectionChange">
        <el-table-column type="selection" align="center" min-width="4%"> </el-table-column>
        <!--<el-table-column type="index" label="序号" align="center" min-width="4%"> 
        </el-table-column>-->
        <el-table-column prop="userId" label="用户ID" align="center" min-width="10%">
        </el-table-column>
        <el-table-column prop="loginName" label="登录名称" sortable align="center" min-width="10%">
        </el-table-column>
        <el-table-column prop="userName" label="用户名称" align="center" min-width="12%">
        </el-table-column>
        <el-table-column prop="dept.deptName" label="部门" align="center" min-width="10%">
        </el-table-column>
        <el-table-column prop="phonenumber" label="手机" align="center" min-width="12%">
        </el-table-column>
        <el-table-column prop="status" label="用户状态" align="center" min-width="10%">
          <template slot-scope="scoped">
            <el-switch active-color="#13ce66" inactive-color="#ff4949" v-model="scoped.row.status" active-value="0"
              inactive-value="1" @change="changeStatus($event, scoped.row, scoped.$index)">
            </el-switch>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" sortable align="center" min-width="12%">
        </el-table-column>
        <el-table-column label="操作" align="center" min-width="20%">
          <template slot-scope="scope">
            <div class="opr">
              <el-button type="primary" size="mini" icon="el-icon-edit" @click="editRow(scope.row)">编辑</el-button>
              <el-button type="primary" size="mini" icon="el-icon-delete" @click="deleteRow(scope.row)">删除</el-button>
              <el-dropdown>
                <el-button type="primary" size="mini">
                  更多菜单<i class="el-icon-arrow-down el-icon--right"></i>
                </el-button>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item @click.native="resetPwd(scope.row)">重置密码</el-dropdown-item>
                  <el-dropdown-item @click.native="goUser(scope.row)">分配角色</el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
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
      <resetPwd title="重置密码" width="30%" v-if="openPwd" ref="testPwd"></resetPwd>
      <import-excel title="导入用户数据" width="30%" v-if="openExcel" ref="openExcel"></import-excel>
    </div>
  </div>
</template>

<script>
//这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）
//例如：import 《组件名称》 from '《组件路径》';
import FileSaver from 'file-saver';
import * as XLSX from 'xlsx';
import Dialog from "./dialog";
import resetPwd from "./resetPwd";
import importExcel from "./importExcel";
export default {
  //import引入的组件需要注入到对象中才能使用
  components: { Dialog, resetPwd, importExcel },
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
      openPwd: false,
      openExcel: false,
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
    addRow() {
      this.openDialog = true;
      this.isDetail = false;
      this.title = "新增用户";
      this.$nextTick(() => {
        this.$refs.testDialog.addFun(null, 'add');
      });
    },

    // switch切换
    changeStatus(e, row, index) {
      //e返回状态，row当前行数据，index下标
      // if(e==1){

      this.$confirm("确认要停用/启用用户吗?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.$http({
            url: this.$http.adornUrl(`/system/user/changeStatus`),
            method: "post",
            params: this.$http.adornParams({
              "userId": row.userId,
              "status": row.status
            }),
          }).then((res) => {
            if (res.data.code == 0) {
              this.$message({ message: res.data.msg, type: "success" })
              setTimeout(() => {
                this.$parent.getData();
              }, 1000);
            } else {
              this.$message({ message: res.data.msg, type: "error" });
            }
          });
        })
        .catch(() => {
          this.$message({ message: '操作失败', type: "error" });
          setTimeout(() => {
            this.$parent.getData();
          }, 1000);
        });
      // }
    },

    // 编辑多选数据
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
        that.title = "修改用户";
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
    // 编辑
    // editRow(data) {
    //   this.openDialog = true;
    //   this.isDetail = false;
    //   this.title = "修改用户";
    //   this.$nextTick(() => {
    //     this.$refs.testDialog.editFun(data, 'edit');
    //   });
    // },
    // 删除复选框选中的数据
    deleteSelect(data) {
      if (data) {
        let length = data.length;
        var ids = [];
        for (const key of data) {
          ids.push(key.userId)
        }

        this.$confirm("确认删除" + length + "行数据?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        })
          .then(() => {
            this.$http({
              url: this.$http.adornUrl(`/system/user/remove`),
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
    // 删除
    deleteRow(data) {
      if (data) {
        this.$confirm("确认删除该行数据?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        })
          .then(() => {
            this.$http({
              url: this.$http.adornUrl(`/system/user/remove`),
              method: "POST",
              params: this.$http.adornParams({
                "ids": data.userId
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
                  type: "warning",
                });
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

    // 日志
    goUser(data) {
      this.$router.push(
        {
          name: 'userTag',
          params: {
            userId: data.userId
          }
        }
      )
    },

    // 重置密码
    resetPwd(data) {
      this.openPwd = true;
      this.$nextTick(() => {
        this.$refs.testPwd.resetPwd(data);
      });
    },

    // 导入
    importExcel() {
      this.openExcel = true;
      this.$nextTick(() => {
        this.$refs.openExcel.resetPwd();
      });
    }
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
