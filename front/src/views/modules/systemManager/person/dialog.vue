<!--  -->
<template>
  <div class="dialogDiv">
    <el-dialog class="dialog" :title="title" :visible.sync="open" :width="width" :close-on-click-modal="false"
      append-to-body :lock-scroll="false" @destroy-on-close="true">
      <el-form :model="form" :rules="rules" ref="form" class="demo-form" id="form">
        <el-form-item class="form-item" label="用户名称:" prop="userName">
          <el-input v-model="form.userName"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="归属部门:" prop="deptName">
          <el-input v-model="form.deptName" @focus="treeDialogFun"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="手机号码:" prop="phonenumber">
          <el-input v-model="form.phonenumber"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="邮箱:" prop="email">
          <el-input v-model="form.email"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="登录账号:" prop="loginName">
          <el-input v-model="form.loginName"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="登录密码:" prop="password" v-if="status!='edit'">
          <el-input show-password v-model="form.password"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="用户性别:" prop="sex">
          <el-select v-model="form.sex">
            <el-option v-for="item in sexArr" :key="item.dictCode" :label="item.dictLabel" :value="item.dictValue">

            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item class="form-item" label="用户状态:" prop="status">
          <el-switch v-model="form.status" active-color="#13ce66" inactive-color="#ff4949" active-value="0"
            inactive-value="1">
          </el-switch>
        </el-form-item>
        <el-form-item class="form-item" label="岗位:" prop="postIds">
          <el-select v-model="form.postIds" multiple>
            <el-option v-for="item in postArr" :key="item.postId" :label="item.postName" :value="item.postId">

            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item class="form-item" label="角色:" prop="roleIds">
          <el-radio-group v-model="form.roleIds">
            <el-radio v-for="item in roleArr" :key="item.roleId" :label="item.roleId">{{item.roleName}}</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item class="form-item" label="备注:" prop="remark">
          <el-input type="textarea" v-model="form.remark"></el-input>
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
        userId: "",
        deptId: "",
        userName: "",
        deptName: "",
        phonenumber: "",
        email: "",
        password: "",
        loginName: "",
        status: "0",
        postIds: [],
        sex: "0",
        roleIds: "",
        remark: ""
      },
      rules: {
        userName: [{ required: true, message: "用户名称不能为空", trigger: "blur" }],
        deptName: [{ required: true, message: "归属部门不能为空", trigger: "blur" }],
        phonenumber: [{ required: true, message: "手机号码不能为空", trigger: "blur" }],
        email: [{ required: true, message: "邮箱不能为空", trigger: "blur" }],
        loginName: [{ required: true, message: "用户账户不能为空", trigger: "blur" }],
        password: [{ required: true, message: "登录密码不能为空", trigger: "blur" }],
      },

      postArr: [],
      roleArr: [],
      sexArr: [],

      editData: {},

      status: "",

      openTree: false,

    };
  },
  //监听属性 类似于data概念
  computed: {},
  //监控data中的数据变化
  watch: {},
  //方法集合
  methods: {
    // 窗口初始化方法，nextTick方法可以添加逻辑，如打开窗口时查询数据填充
    addFun(data, status) {
      this.open = true;
      this.status = status;
      this.$nextTick(() => {
        // 表单重置
        this.$refs["form"].resetFields();
      });
    },

    // 修改
    editFun(data, status) {
      this.open = true;
      this.status = status;
      this.$nextTick(() => {
        // 表单重置
        this.$refs["form"].resetFields();

        if (data) {
          this.$http({
            url: this.$http.adornUrl(`/system/user/edit/${data.userId}`),
            method: "get",
            params: this.$http.adornParams({})
          }).then((res) => {
            if (res.data.user) {
              let user = res.data.user;
              this.form.userId = user.userId,
                this.form.deptId = user.dept.deptId,
                this.form.userName = user.userName,
                this.form.deptName = user.dept.deptName,
                this.form.phonenumber = user.phonenumber,
                this.form.email = user.email,
                this.form.loginName = user.loginName,
                this.form.password = user.password,
                this.form.sex = user.sex,
                this.form.remark = user.remark,
                this.form.status = user.status,
                this.form.roleIds = user.roleIds;
              if (res.data.posts.length > 0) {
                for (const key of res.data.posts) {
                  if (key.flag) {
                    this.form.postIds.push(key.postId);
                  }
                }
              }

              if (res.data.roles.length > 0) {
                for (const key of res.data.roles) {
                  if (key.flag) {
                    this.form.roleIds = (key.roleId);
                  }
                }
              }
            }
          });
        }
      });
    },
    // 保存
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          var that = this;
          let params = {
            userId: this.form.userId,
            deptId: this.form.deptId,
            userName: this.form.userName,
            deptName: this.form.deptName,
            phonenumber: this.form.phonenumber,
            // email: sm2Encrypt(new AesUtil().encrypt({ data: this.form.email })),
            email: this.form.email,
            loginName: this.form.loginName,
            password: this.form.password,
            sex: this.form.sex,
            remark: this.form.remark,
            status: this.form.status,
            roleIds: this.form.roleIds,
            postIds: this.form.postIds.join(','),
          }
          this.$http({
            url: this.$http.adornUrl(`/system/user/${this.status}`),
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
    },
    sexFun() {
      this.$http({
        url: this.$http.adornUrl(`/tool/dict/getType`),
        method: "get",
        params: this.$http.adornParams({
          "type": "sys_user_sex"
        }),
      }).then((res) => {
        this.sexArr = res.data;

      });

      this.$http({
        url: this.$http.adornUrl(`/system/user/add`),
        method: "get",
        params: {},
      }).then((res) => {
        const data = res.data;
        this.postArr = data.posts;
        this.roleArr = data.roles;
      });
    }
  },
  //生命周期 - 创建完成（可以访问当前this实例）
  created() { },
  //生命周期 - 挂载完成（可以访问DOM元素）
  mounted() {
    this.sexFun();
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
#form {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  padding: 0 70px;
}

#form>>>.el-form-item__label {
  width: 40% !important;
}

#form>>>.el-form-item {
  width: 45%;
}

.el-form-item__content {
  margin-left: 10px !important;
  width: 60%;
}

.form-item>>>.el-form-item__content {
  margin-left: 15px !important;
}
</style>
