<!--  -->
<template>
  <div class="dialogDiv">
    <el-dialog class="dialog" :title="title" :visible.sync="open" :width="width" :close-on-click-modal="false"
      append-to-body :lock-scroll="false" @destroy-on-close="true">
      <el-form :model="form" :rules="rules" ref="form" class="demo-form" id="form">
        <el-form-item class="form-item" label="登录名称:" prop="userName">
          <el-input v-model="form.userName" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="登录密码:" prop="password">
          <el-input show-password v-model="form.password"></el-input>
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
  components: {  },
  props: ["title", "width", "isDetail"],
  inject: ['getData'],
  data() {
    //这里存放数据
    return {
      // 是否显示弹出层
      open: false,
      form: {
        userId:"",
        userName: "",
        password: "",
      },
      rules: {
        userName: [{ required: true, message: "登录名称不能为空", trigger: "blur" }],
        password: [{ required: true, message: "登录密码不能为空", trigger: "blur" }],
      },
    };
  },
  //监听属性 类似于data概念
  computed: {},
  //监控data中的数据变化
  watch: {},
  //方法集合
  methods: {
    resetPwd(data){
      this.open = true;
      this.form.userId=data.userId;
      this.$http({
        url: this.$http.adornUrl(`/system/user/edit/${data.userId}`),
        method: "GET",
        params: this.$http.adornParams({
          
        }),
      }).then((res) => {
        this.form.userName=res.data.user.loginName;
      });

      this.$http({
        url: this.$http.adornUrl(`/tool/config/getKey`),
        method: "GET",
        params: this.$http.adornParams({
          configKey:"sys.user.initPassword"
        }),
      }).then((res) => {
        this.form.password=res.data.key;
      });
    },
    // 保存
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          var that = this;
          let params = {
            userId: this.form.userId,
            loginName: this.form.userName,
            password: this.form.password,
          }
          this.$http({
            url: this.$http.adornUrl(`/system/user/resetPwd`),
            method: "post",
            params: this.$http.adornParams(params)
          }).then((res) => {
            if (res.data.code == 0) {
              this.$message({
                message: res.data.msg,
                type: "success"
              })
              setTimeout(() => {
                that.open = false;
                that.getData();
              }, 1000);
            } else {
              this.$message({
                message: res.data.msg,
                type: "error"
              })
            }
          });

        } else {
        //   console.log("error submit!!");
        //   return false;
        }
      });
    },
  },
  //生命周期 - 创建完成（可以访问当前this实例）
  created() { },
  //生命周期 - 挂载完成（可以访问DOM元素）
  mounted() {
  },
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
  max-height: 76%;
}
  #form {
    /* display: flex;
    justify-content: space-between;
    flex-wrap: wrap; */
    padding: 0 70px;
  }
  
  .form-item>>>.el-form-item__label {
    width: 30% !important;
  }
  
  .el-form-item {
    width: 100%;
    align-items: flex-start;
  }
  
  .form-item>>>.el-form-item__content {
    margin-left: 10px !important;
    width: 70% !important;
  }
  </style>
