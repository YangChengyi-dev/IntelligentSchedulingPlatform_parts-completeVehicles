<template>
  <div id="login">
    <div class="mainTitle">基于多式联运的零件与整车智能调度平台</div>
    <el-form
      :model="ruleForm"
      :rules="rules"
      ref="ruleForm"
      label-width="100px"
      class="demo-ruleForm"
    >
      <h3 class="title">登录:</h3>
      <el-form-item prop="userName">
        <el-input
          v-model="ruleForm.userName"
          auto-complete="off"
          placeholder="账户"
          suffix-icon="el-icon-user"
          class="el-input"
          @keyup.enter.native="submitForm('ruleForm')"
        ></el-input>
      </el-form-item>
      <el-form-item prop="password">
        <el-input
          type="password"
          v-model="ruleForm.password"
          auto-complete="off"
          placeholder="密码"
          suffix-icon="el-icon-lock"
          @keyup.enter.native="submitForm('ruleForm')"
        ></el-input>
      </el-form-item>
      <el-form-item prop="code">
        <el-row :span="24" :gutter="10">
          <el-col :span="12">
            <el-input
              v-model="ruleForm.validateCode"
              auto-complete="off"
              placeholder="请输入验证码"
              size=""
              @keyup.enter.native="submitForm('ruleForm')"
            ></el-input>
          </el-col>
          <el-col :span="12">
            <div class="login-code">
              <img :src="img" alt="" class="codeImg" @click="changeCode" />
            </div>
          </el-col>
        </el-row>
      </el-form-item>
      <el-row>
        <el-checkbox v-model="ruleForm.rememberMe">记住我</el-checkbox>
      </el-row>
      <el-row class="btn">
        <el-button
          type="primary"
          @click="submitForm('ruleForm')"
          @keyup.enter.native="submitForm('ruleForm')"
          >登录
        </el-button>
      </el-row>
      <el-row class="register">
        还没有账号? <span @click="registerFun">立即注册</span>
      </el-row>
    </el-form>
  </div>
</template>

<script>
// import { getUUID } from '@/utils'
import axios from "axios";
export default {
  data() {
    return {
      data: "",
      ruleForm: {
        userName: "",
        password: "",
        validateCode: "",
        rememberMe: true
      },
      rules: {
        userName: [
          { required: true, message: "用户名不能为空", trigger: "blur" }
        ],
        password: [{ required: true, message: "密码不能为空", trigger: "blur" }]
      },

      img: "http://10.160.24.112:7000/captcha/captchaImage?type=math"
    };
  },
  mounted() {},
  computed: {},
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          let params = {
            username: this.ruleForm.userName,
            password: this.ruleForm.password,
            rememberMe: this.ruleForm.rememberMe,
            validateCode: this.ruleForm.validateCode
          };
          // this.$http({
          //   url: this.$http.adornUrl(`/login`),
          //   method: "post",
          //   params: this.$http.adornParams(params)
          // }).then(async ({ data }) => {
          //   if (data && data.code === 0) {
          //     this.$message({
          //       message: '登录成功！',
          //       type: 'success'
          //     });
          //     setTimeout(() => {
          //       this.$router.replace({ name: "index" });
          //       // this.$router.push("/peakIntranet/protocolManagerment/index");
          //     }, 2000);
          //   } else {
          //     this.$message.error(data.msg);
          //   }
          // });
          axios({
            url: this.baseurl + "/user/login", // 替换为实际的后端接口
            method: "POST",
            data: {
              username: params.username,
              password: params.password
            }
          }).then(res => {
            const data = res.data.data;
            console.log(data);
            if (data.isSuccess === true) {
              this.$message({
                message: "登录成功！",
                type: "success"
              });
              setTimeout(() => {
                this.$router.replace({ name: "index" });
                console.log(this.$route);
                // this.$router.push("/peakIntranet/protocolManagerment/index");
              }, 2000);
            } else {
              this.$message.error("账号或者密码输入错误！！！");
            }
          });

          // 模拟登录成功后的跳转
          //if (params.username === "admin" && params.password === "123456") {
          //  this.$message({
          //    message: "登录成功！",
          //    type: "success"
          //  });
          //  setTimeout(() => {
          //    this.$router.replace({ name: "index" });
          //    console.log(this.$route);
          //    // this.$router.push("/peakIntranet/protocolManagerment/index");
          //  }, 2000);
          //} else {
          //  this.$message.error("账号或者密码输入错误！！！");
          //}
          // this.$message({
          //        message: '登录成功！',
          //        type: 'success'
          //      });
          // setTimeout(() => {
          //        this.$router.replace({ name: "index" });
          //        // this.$router.push("/peakIntranet/protocolManagerment/index");
          //      }, 2000);
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },

    changeCode() {
      this.img =
        "http://10.160.24.112:7000/captcha/captchaImage?type=" +
        "math" +
        "&s=" +
        Math.random();
    },

    // 注册
    registerFun() {
      this.$router.push({ path: "/register" });
    }
  }
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

  .mainTitle {
    position: absolute;
    text-align: center;
    top: 17%;
    left: 54%;
    font-size: 30px;
    color: rgb(28, 113, 104);
    font-weight: 600;
    font-family: "思源黑体";
  }

  .demo-ruleForm {
    width: 16%;
    background: rgba(255, 255, 255, 0.2);
    box-shadow: 0 3px 0 rgba(12, 12, 12, 0.03);
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
#login >>> .el-form-item__content {
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
