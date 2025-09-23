<!--  -->
<template>
  <div class="dialogDiv">
    <el-dialog class="dialog" :title="title" :visible.sync="open" :width="width" :close-on-click-modal="false"
      append-to-body :lock-scroll="false" @destroy-on-close="true">
      <el-form :model="form" :rules="rules" ref="form" class="demo-form" id="form">
        <el-form-item class="form-item" label="岗位名称:" prop="postName">
          <el-input v-model="form.postName"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="岗位编码:" prop="postCode">
          <el-input v-model="form.postCode"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="显示顺序:" prop="postSort">
          <el-input v-model="form.postSort"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="岗位状态:" prop="postStatus">
          <el-radio v-model="form.postStatus" label="0">正常</el-radio>
          <el-radio v-model="form.postStatus" label="1">停用</el-radio>
        </el-form-item>
        <el-form-item class="form-item" label="备注:" prop="postBz">
          <el-input type="textarea" v-model="form.postBz"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer" v-if="!isDetail">
        <el-button class="" @click="open = false">取消</el-button>
        <el-button class="" type="primary" @click="submitForm('form')">保存</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
//这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）
//例如：import 《组件名称》 from '《组件路径》';

export default {
  //import引入的组件需要注入到对象中才能使用
  components: {},
  props: ["title", "width", "isDetail"],
  inject: ['getData'],
  data() {
    //这里存放数据
    return {
      // 是否显示弹出层
      open: false,
      form: {
        postId:"",
        postName: "",
        postCode: "",
        postSort: "",
        postStatus: "0",
        postBz: "",
      },
      rules: {
        postName: [{ required: true, message: "岗位名称不能为空", trigger: "blur" }],
        postCode: [{ required: true, message: "岗位编码不能为空", trigger: "blur" }],
        postSort: [{ required: true, message: "显示顺序不能为空", trigger: "blur" }],
      },

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
     addFun(tableRadio, status) {
      this.open = true;
      this.status = status;
      this.$nextTick(() => {
        // 表单重置
        this.$refs["form"].resetFields();
      });
    },

    editFun(data,status){
      this.open = true;
      this.status = status;
      this.$nextTick(() => {
        // 表单重置
        this.$refs["form"].resetFields();

        if (data) {
          this.$http({
            url: this.$http.adornUrl(`/system/post/edit/${data.postId}`),
            method: "get",
            params: this.$http.adornParams({})
          }).then((res) => {
            if (res.data.post) {
              let menu = res.data.post;
              this.form.postId=menu.postId;
              this.form.postName = menu.postName;
              this.form.postCode = menu.postCode;
              this.form.postSort = menu.postSort;
              this.form.postStatus = menu.status;
              this.form.postBz = menu.remark;
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
            postName: this.form.postName,
            postCode: this.form.postCode,
            postSort: this.form.postSort,
            status: this.form.postStatus,
            remark: this.form.postBz,
          }
          if (this.status == 'edit') {
            params.postId = this.form.postId;
          }
          this.$http({
            url: this.$http.adornUrl(`/system/post/${this.status}`),
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
</style>
