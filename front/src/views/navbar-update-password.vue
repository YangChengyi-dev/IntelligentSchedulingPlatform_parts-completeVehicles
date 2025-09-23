<template>

  <el-dialog title="修改密码" class="dialog" id="updatePwd" :visible.sync="visible" :append-to-body="true">
    <el-form id="form" :model="dataForm" :rules="dataRule" ref="dataForm" @keyup.enter.native="dataFormSubmit()">
      <el-form-item label="账号：">
        <span style="color:#fff">{{ userName }}</span>
      </el-form-item>
      <el-form-item label="原密码：" prop="oldPassword">
        <el-input type="password" v-model="dataForm.oldPassword"></el-input>
      </el-form-item>
      <el-form-item label="新密码：" prop="newPassword">
        <el-input type="password" v-model="dataForm.newPassword"></el-input>
      </el-form-item>
      <el-form-item label="确认密码：" prop="confirmPassword">
        <el-input type="password" v-model="dataForm.confirmPassword"></el-input>
      </el-form-item>
    </el-form>
    <span slot="footer" class="dialog-footer">
      <el-button @click="visible = false">取消</el-button>
      <el-button type="primary" @click="dataFormSubmit()">确定</el-button>
    </span>
  </el-dialog>
</template>

<script>
import { clearLoginInfo } from "@/utils";
export default {
  data() {
    var validateConfirmPassword = (rule, value, callback) => {
      if (this.dataForm.newPassword !== value) {
        callback(new Error("确认密码与新密码不一致"));
      } else {
        callback();
      }
    };
    return {
      visible: false,
      dataForm: {
        oldPassword: "",
        newPassword: "",
        confirmPassword: "",
      },
      dataRule: {
        oldPassword: [{ required: true, message: "原密码不能为空", trigger: "blur" }],
        newPassword: [{ required: true, message: "新密码不能为空", trigger: "blur" }],
        confirmPassword: [
          { required: true, message: "确认密码不能为空", trigger: "blur" },
          { validator: validateConfirmPassword, trigger: "blur" },
        ],
      },
    };
  },
  computed: {
    userName: {
      get() {
        return this.$store.state.user.user.loginName;
      },
    },
    mainTabs: {
      get() {
        return this.$store.state.common.mainTabs;
      },
      set(val) {
        this.$store.commit("common/updateMainTabs", val);
      },
    },
  },
  methods: {
    // 初始化
    init() {
      this.visible = true;
      this.$nextTick(() => {
        this.$refs["dataForm"].resetFields();
      });
    },
    // 表单提交
    dataFormSubmit() {
      this.$refs["dataForm"].validate((valid) => {
        if (valid) {
          let data = {
            loginName: this.userName,
            oldPassword: this.dataForm.oldPassword,
            newPassword: this.dataForm.newPassword,
            confirmPassword: this.dataForm.confirmPassword,
            userId: this.$store.state.user.user.userId
          }
          this.$http({
            url: this.$http.adornUrl("/system/user/profile/resetPwd"),
            method: "post",
            params: this.$http.adornParams(data),
          }).then(({ data }) => {
            if (data && data.code === 0) {
              this.$message({
                message: "操作成功",
                type: "success",
                duration: 1500,
                onClose: () => {
                  this.visible = false;
                  this.$nextTick(() => {
                    this.mainTabs = [];
                    clearLoginInfo();
                    this.$router.replace({ name: "login" });
                  });
                },
              });
            } else {
              this.$message.error(data.msg);
            }
          });
        }
      });
    },
  },
};
</script>

<style lang="scss">
#updatePwd {
  #form {
    width: 70%;
    margin: 0 auto;

    .el-form-item__label {
      width: 20%;
    }
  }
}
</style>
