<!--  -->
<template>
  <div class="dialogDiv">
    <el-dialog class="dialog" :title="title" :visible.sync="open" :width="width" :close-on-click-modal="false"
      append-to-body :lock-scroll="false" @destroy-on-close="true">
      <el-form :model="form" :rules="rules" ref="form" class="demo-form" id="form">
        <el-form-item class="form-item" label="操作模块:" prop="detailTitle">
          <el-input v-model="form.detailTitle" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="登录信息:" prop="detailOperName">
          <el-input v-model="form.detailOperName" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="请求地址:" prop="detailOperUrl">
          <el-input v-model="form.detailOperUrl" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="请求方式:" prop="detailRequestMethod">
          <el-input v-model="form.detailRequestMethod" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="操作方法:" prop="detailMethod">
          <el-input v-model="form.detailMethod" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="请求参数:" prop="operParam">
          <el-input type="textarea" v-model="form.operParam" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="返回参数:" prop="jsonResult">
          <el-input type="textarea" v-model="form.jsonResult" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="状态:" prop="status">
          <el-tag effect="dark" type="">{{form.statusTag}}</el-tag>
        </el-form-item>
        <el-form-item class="form-item" label="异常信息:" prop="errorMsg" v-show="form.statusTag=='异常'">
          <el-input type="input" v-model="form.errorMsg" :disabled="true"></el-input>
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
  data() {
    //这里存放数据
    return {
      // 是否显示弹出层
      open: false,
      form: {
        detailTitle: "",
        detailOperName: "",
        detailRequestMethod: "",
        detailMethod: "",
        operParam: "",
        detailOperUrl: "",
        jsonResult: "",
        statusTag:'正常',
        errorMsg:'',
      },
      rules: {
        detailTitle: [{ required: true, message: "操作模块不能为空", trigger: "blur" }],
        detailOperName: [
          { required: true, message: "登录信息不能为空", trigger: "blur" },
        ],
        detailOperUrl: [{ required: true, message: "请求地址不能为空", trigger: "blur" }],
      },

      status: '',
      rowData: {},
    };
  },
  //监听属性 类似于data概念
  computed: {},
  //监控data中的数据变化
  watch: {},
  //方法集合
  methods: {
    // 修改
    editFun(data, status) {
      this.open = true;
      this.status = status;
      this.rowData = data;
      this.$nextTick(() => {
        // 表单重置
        this.$refs["form"].resetFields();

        if (data) {
          this.$http({
            url: this.$http.adornUrl(`/monitor/operlog/detail/${data.operId}`),
            method: "get",
            params: this.$http.adornParams({})
          }).then((res) => {
            if (res.data) {
              let operLog = res.data,
                form = this.form;
              form.operId = operLog.operId;
              this.getLabel().then(data => {
                form.detailTitle = operLog.title + '/' + data
              })
              form.detailOperName = `${operLog.operName}/${operLog.deptName}/${operLog.operIp}/${operLog.operLocation}`,
                form.detailOperUrl = operLog.operUrl,
                form.detailRequestMethod = operLog.requestMethod,
                form.detailMethod = operLog.method,
                form.operParam = operLog.operParam,
                form.jsonResult = operLog.jsonResult,
                form.statusTag=(operLog.status == 0 ? '正常' : '异常'),
                form.errorMsg = operLog.errorMsg

            }
          });
        }
      });
    },
    // 保存
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          alert("submit!");
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    async getLabel() {
      var label = "";
      await this.$http({
        url: this.$http.adornUrl(`/tool/dict/getLabel`),
        method: "get",
        params: this.$http.adornParams({
          dictType: "sys_oper_type",
          dictValue: this.rowData.businessType,

        })
      }).then((res) => {
        label = res.data.label;
      });
      return label;
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
