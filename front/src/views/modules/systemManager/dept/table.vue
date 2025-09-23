<!--  -->
<template>
  <div>
    <div class="table">
      <!-- 工具栏 -->
      <div ref="toolbar" class="toolbar">
        <el-row class="btnGroup">
          <el-button type="primary" size="mini" @click="addRow(null)">新增 </el-button>
          <el-button type="primary" size="mini" @click="editMenu"> 修改 </el-button>
          <el-button type="primary" size="mini" @click="isExpandEvent">
            展开/折叠
          </el-button>
        </el-row>
      </div>
      <!-- 表格 -->
      <el-table
        :data="table1Data"
        id="table"
        ref="table"
        stripe
        style="width: 100%"
        :header-row-style="{ height: '35px' }"
        :row-style="{ height: '35px' }"
        :height="tableHeight"
        row-key="deptId"
        :default-expand-all="isExpand"
        :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection"  align="center" min-width="4%"> </el-table-column>
        <el-table-column
          prop="deptName"
          label="部门名称"
          class-name="menuName"
          min-width="14%"
        >
          <template slot-scope="scope">
            <i :class="('iconfont', scope.row.icon)"></i>
            <span style="margin-left: 0px">{{ scope.row.deptName }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="orderNum" label="排序" align="center" min-width="12%">
        </el-table-column>
      
        <el-table-column
          prop="status"
          label="状态"
          sortable
          align="center"
          min-width="14%"
        >
          <template slot-scope="scope">
            <div v-if="scope.row.status == '0'">
              <el-tag effect="dark" type="">正常</el-tag>
            </div>
            <div v-if="scope.row.status == '1'">
              <el-tag effect="dark" type="danger" >停用</el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column
          prop="createTime"
          label="创建时间"
          sortable
          align="center"
          min-width="14%"
        >
        </el-table-column>
        <el-table-column label="操作" align="center" min-width="18%">
          <template slot-scope="scope">
            <div class="opr">
              <el-button
                type="primary"
                size="mini"
                icon="el-icon-edit"
                @click="edit(scope.row)"
                >编辑</el-button
              >
              <el-button
                type="primary"
                icon="el-icon-plus"
                size="mini"
                @click="addRow(scope.row)"
                >新增</el-button
              >
              <el-button
                type="primary"
                icon="el-icon-delete"
                size="mini"
                @click="deleteRow(scope.row)"
                >删除</el-button
              >
            </div>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <!-- 新增，编辑弹框 -->
    <div class="dialog">
      <Dialog
        :title="title"
        width="55%"
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
      title: "",
      isDetail: false,
      openDialog: false,
      tableHeight: 0,

      // 是否展开
      isExpand: false,
       muticalSelectData: [],
    };
  },
  //监听属性 类似于data概念
  computed: {
   
  },
  //监控data中的数据变化
  watch: {
    height(newVal, oldVal) {
      this.tableHeight = newVal - this.$refs.toolbar.offsetHeight;
    },
  },
  //方法集合
  methods: {
    // 多选框选择数据
    handleSelectionChange(val) {
      this.muticalSelectData = val;
    },
    // 新增
    addRow(data) {
      if(data==null) data=this.table1Data[0];
        this.openDialog = true;
        this.isDetail = false;
        this.title = "添加部门";
        this.$nextTick(() => {
          this.$refs.testDialog.init(data,'add');
        });
    },
    // 修改
    edit(data) {
      this.openDialog = true;
      this.isDetail = false;
      this.title = "修改菜单";
      this.$nextTick(() => {
        this.$refs.testDialog.edit(data,'edit');
      });
    },
    editMenu() {
      if (this.muticalSelectData.length != 1) {
        this.$message({
          message: "请选择一条数据！",
          type: "warning",
        });
        return;
      }
      this.openDialog = true;
      this.isDetail = false;
      this.title = "修改菜单";
      this.$nextTick(() => {
        this.$refs.testDialog.edit(this.muticalSelectData[0],'edit');
      });
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
            url: this.$http.adornUrl(`/system/dept/remove/${data.deptId}`),
            method: "get",
            params: this.$http.adornParams({})
          }).then((res) => {
            if (res.data.code == 0) {
              this.$message({
                message: res.data.msg,
                type: "success"
              })
              setTimeout(() => {
                this.$parent.getData();
              }, 1000);
            }else{
              this.$message({
                message: res.data.msg,
                type: "error"
              })
            }
          });
          })
          .catch(() => {});
      } else {
        this.$message({
          message: "请选择行！",
          type: "warning",
        });
      }
    },
    // 展开/折叠
    isExpandEvent() {
      this.isExpand = !this.isExpand;
      this.$nextTick(() => {
        this.forArr(this.table1Data, this.isExpand);
      });
    },
    // 遍历
    forArr(arr, isExpand) {
      arr.forEach((i) => {
        // toggleRowExpansion(i, isExpand)用于多选表格，切换某一行的选中状态，如果使用了第二个参数，则是设置这一行选中与否（selected 为 true 则选中）
        this.$refs.table.toggleRowExpansion(i, isExpand);
        if (i.children) {
          this.forArr(i.children, isExpand);
        }
      });
    },
  },
  //生命周期 - 创建完成（可以访问当前this实例）
  created() {},
  //生命周期 - 挂载完成（可以访问DOM元素）
  mounted() {
  },
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
