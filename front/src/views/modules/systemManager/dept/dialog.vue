<!--  -->
<template>
  <div class="dialogDiv">
    <el-dialog class="dialog" :title="title" :visible.sync="open" :width="width" :close-on-click-modal="false"
      append-to-body :lock-scroll="false" @destroy-on-close="true">
      <el-form :model="form" :rules="rules" ref="form" class="demo-form" id="form">
        <el-form-item class="form-item" label="上级部门:" prop="parentdept">
          <el-input v-model="form.parentdept" @focus="treeDialogFun"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="部门名称:" prop="deptName">
          <el-input v-model="form.deptName"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="显示排序:" prop="orderNum">
          <el-input v-model="form.orderNum"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="负责人:" prop="leader">
          <el-input v-model="form.leader"></el-input>
        </el-form-item>

        <el-form-item class="form-item" label="联系电话:" prop="phone">
          <el-input v-model="form.phone"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="邮箱:" prop="email">
          <el-input v-model="form.email"></el-input>
        </el-form-item>

        <el-form-item label="部门状态:" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio label="0">正常</el-radio>
            <el-radio label="1">隐藏</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer" v-if="!isDetail">
        <el-button class="" @click="open = false">取消</el-button>
        <el-button class="" type="primary" @click="submitForm('form')">保存</el-button>
      </div>
    </el-dialog>

    <!-- 新增，编辑弹框 -->
    <div class="dialog">
      <Tree width="40%" v-if="openTree" ref="treeDialog"></Tree>
    </div>
  </div>
</template>

<script>
//这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）
//例如：import 《组件名称》 from '《组件路径》';
import Tree from "./tree";
export default {
  //import引入的组件需要注入到对象中才能使用
  components: { Tree },
  props: ["title", "width", "isDetail"],
  inject: ['getData'],
  data() {
    //这里存放数据
    return {
      // 是否显示弹出层
      open: false,
      form: {
        parentId: "0",
        parentdept: "",
        deptName: "",
        orderNum: "",
        leader: "",
        phone: "",
        email: "",
        status: "0",
        deptId: "",
      },
      rules: {
        deptName: [{ required: true, message: "部门名称不能为空", trigger: "blur" }],
        orderNum: [{ required: true, message: "显示排序不能为空", trigger: "blur" }],
      },


      // 是否显示树
      openTree: false,

      // 判断是新增还是编辑
      status: '',
    };
  },
  //监听属性 类似于data概念
  computed: {},
  //监控data中的数据变化
  watch: {},
  //方法集合
  methods: {
    // 窗口初始化方法，nextTick方法可以添加逻辑，如打开窗口时查询数据填充
    init(tableRadio, status) {
      this.open = true;
      this.status = status;
      this.$nextTick(() => {
        // 表单重置
        this.$refs["form"].resetFields();
        if (tableRadio) {
          this.$http({
            url: this.$http.adornUrl(`/system/dept/add/${tableRadio.deptId}`),
            method: "get",
            params: this.$http.adornParams({})
          }).then((res) => {
            if (res.data.dept) {
              let dept = res.data.dept;
              this.form.parentdept = dept.deptName;
              this.form.parentId = dept.deptId;
            }
          });
        }
      });
    },

    edit(data, status) {
      this.open = true;
      this.status = status;
      this.$nextTick(() => {
        // 表单重置
        this.$refs["form"].resetFields();
        if (data) {
          this.$http({
            url: this.$http.adornUrl(`/system/dept/edit/${data.deptId}`),
            method: "get",
            params: this.$http.adornParams({})
          }).then((res) => {
            if (res.data.dept) {
              let dept = res.data.dept;
              this.form.parentdept = dept.parentName ? dept.parentName : '无';
              this.form.parentId = dept.parentId;
              this.form.deptId = dept.deptId;
              this.form.deptName = dept.deptName;
              this.form.leader = dept.leader;
              this.form.phone = dept.phone;
              this.form.orderNum = dept.orderNum;
              this.form.email = dept.email;
              this.form.status = dept.status;

            }
          });
        }
      });
    },
    // 保存
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          let params = {
            parentId: this.form.parentId,
            parentName: this.form.parentdept,
            deptName: this.form.deptName,
            orderNum: this.form.orderNum,
            leader: this.form.leader,
            phone: this.form.phone,
            email: this.form.email,
            status: this.form.status,
          }
          if (this.status == 'edit') {
            params.deptId = this.form.deptId;
          }
          this.$http({
            url: this.$http.adornUrl(`/system/dept/${this.status}`),
            method: "post",
            params: this.$http.adornParams(params)
          }).then((res) => {
            if (res.data.code == 0) {
              this.$message({
                message: res.data.msg,
                type: "success"
              })
              setTimeout(() => {
                this.open = false;
                this.$parent.openDialog = false;
                this.getData();
              }, 1000);
            } else {
              this.$message({
                message: res.data.msg,
                type: "error"
              })
            }
          });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    // 弹出树形框
    treeDialogFun() {
      this.openTree = true;
      this.$nextTick(() => {
        this.$refs.treeDialog.init(null);
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
<style scoped>
/* @import url(); 引入公共css类 */
/* .dialog >>> .el-dialog {
  height: v-bind(height) !important;
} */
.dialog>>>.el-dialog {
  max-height: 77%;
}

#form {
  padding: 0 70px;
}

#form>>>.el-form-item__label {
  width: 30% !important;
}

.el-form-item {
  width: 100%;
  align-items: flex-start !important;
}

#form>>>.el-form-item__content {
  margin-left: 10px !important;
  width: 90% !important;
}

.ico-list .fa {
  margin: 5px;
  padding: 5px;
  cursor: pointer;
  font-size: 18px;
  width: 28px;
  border-radius: 3px;
}

.ico-list .fa:hover {
  background-color: #1d9d74;
  color: #ffffff;
}
</style>
