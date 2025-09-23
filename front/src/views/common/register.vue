<template>
  <div id="login">
    <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
      <h3 class="title">注册:</h3>
      <el-form-item prop="userName">
        <el-input v-model="ruleForm.userName" auto-complete="off" placeholder="账户" suffix-icon="el-icon-user"
          class="el-input" @keyup.enter.native="submitForm('ruleForm')"></el-input>
      </el-form-item>
      <el-form-item prop="password">
        <el-input type="password" v-model="ruleForm.password" auto-complete="off" placeholder="密码"
          suffix-icon="el-icon-lock" @keyup.enter.native="submitForm('ruleForm')"></el-input>
      </el-form-item>
      <el-form-item prop="confirmPassword">
        <el-input type="password" v-model="ruleForm.confirmPassword" auto-complete="off" placeholder="确认密码"
          suffix-icon="el-icon-lock" @keyup.enter.native="submitForm('ruleForm')"></el-input>
      </el-form-item>
      <el-form-item prop="code">
        <el-row :span="24" :gutter="10">
          <el-col :span="12">
            <el-input v-model="ruleForm.validateCode" auto-complete="off" placeholder="请输入验证码" size=""
              @keyup.enter.native="submitForm('ruleForm')"></el-input>
          </el-col>
          <el-col :span="12">
            <div class="login-code">
              <img :src="img" alt="" class="codeImg" @click="changeCode">
            </div>
          </el-col>
        </el-row>
      </el-form-item>
      <el-row class="register">
        <el-checkbox v-model="ruleForm.rememberMe" class="register">我已阅读并同意 </el-checkbox>
        <span @click="md">使用条款</span>
      </el-row>
      <el-row class="btn">
        <el-button type="primary" @click="submitForm('ruleForm')" @keyup.enter.native="submitForm('ruleForm')">注册
        </el-button>
      </el-row>
      <el-row class="register">
        已经注册过? <span @click="loginFun">直接登录</span>
      </el-row>
    </el-form>

  </div>
</template>

<script>
export default {
  data() {
    var validateConfirmPassword = (rule, value, callback) => {
      if (this.ruleForm.password !== value) {
        callback(new Error("确认密码与新密码不一致"));
      } else {
        callback();
      }
    };
    return {
      ruleForm: {
        userName: "",
        password: "",
        confirmPassword: "",
        validateCode: "",
        rememberMe: false,
      },
      rules: {
        userName: [
          { required: true, message: "用户名不能为空", trigger: "blur" },
        ],
        password: [{ required: true, message: "密码不能为空", trigger: "blur" }, {
          min: 5, message: "密码不能小于5个字符", trigger: "blur"
        }],
        confirmPassword: [
          { required: true, message: "确认密码不能为空", trigger: "blur" },
          { validator: validateConfirmPassword, trigger: "blur" },
        ]
      },

      img: 'http://10.160.24.112:8080/captcha/captchaImage?type=math',
    };
  },
  mounted() {

  },
  computed: {},
  methods: {

    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          if (!this.ruleForm.rememberMe) {
            this.$message({
              message: "请勾选使用条款",
              type: 'error'
            })
            return;
          }
          let params = {
            loginName: this.ruleForm.userName,
            password: this.ruleForm.password,
            rememberMe: this.ruleForm.rememberMe,
            validateCode: this.ruleForm.validateCode
          }
          this.$http({
            url: this.$http.adornUrl(`/register`),
            method: "post",
            params: this.$http.adornParams(params)
          }).then(async ({ data }) => {
            if (data && data.code === 0) {
              this.$message({
                message: '注册成功！',
                type: 'success'
              });
              setTimeout(() => {
                this.$router.replace({ name: "login" });
              }, 2000);
            } else {
              this.$message.error({ message: data.msg, type: 'error' });

            }
          });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },

    changeCode() {
      this.img = "http://10.160.24.112:8080/captcha/captchaImage?type=" + 'math' + "&s=" + Math.random();
    },

    // 登录
    loginFun() {
      this.$router.push({ path: '/login' })
    },

    md() {
      location.href = 'https://gitee.com/y_project/RuoYi/blob/master/README.md'
    }
  },
};
</script>

<style lang="scss" scoped>
#login {
  margin: 0;
  padding: 0;
  background-image: url("~@/assets/img/bgc.png");
  background-repeat: no-repeat;
  background-size: 100% 100%;
  width: 100%;
  height: 100vh;
  overflow: hidden;

  .demo-ruleForm {
    width: 15%;
    background: rgba(255, 255, 255, .2);
    box-shadow: 0 3px 0 rgba(12, 12, 12, .03);
    margin-left: 64%;
    margin-top: 14%;
    padding: 20px;

    .title {
      color: #fff;
      padding-bottom: 10px;
    }

    .el-form-item__label {
      color: #ffffff;
    }

    .btn {
      text-align: center;
      margin-top: 8px;

      .el-button {
        width: 100%;
        background: #1c7168 !important;
      }
    }

    .el-input input {
      height: 37px;
      background: #0b4842;
      border: 1px solid #0a3c36;
      color: #bcc3d1;
    }
  }

  .register {
    color: #fff;
    margin-top: 10px;

    span {
      color: #35bfb1;
      cursor: pointer;
    }
  }
}
</style>

<style scoped>
#login>>>.el-form-item__content {
  margin-left: 0px !important;
}

.el-form-item {
  margin-bottom: 15px !important;
}

.login-code {
  height: 36px;
}

.codeImg {
  cursor: pointer;
}
</style>
