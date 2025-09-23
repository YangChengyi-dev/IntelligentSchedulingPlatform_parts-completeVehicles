<!--  -->
<template>
  <div class="dialogDiv">
    <el-dialog class="dialog" :title="title" :visible.sync="open" :width="width" :close-on-click-modal="false"
      append-to-body :lock-scroll="false" @destroy-on-close="true">
      <el-form :model="form" :rules="rules" ref="form" class="demo-form" id="form">
        <el-form-item class="form-item" label="任务名称:" prop="jobName">
          <el-input v-model="form.jobName"></el-input>
        </el-form-item>
         <el-form-item class="form-item" label="任务分组:" prop="jobGroup">
          <el-select v-model="form.jobGroup" placeholder="请选择">
            <el-option v-for="item in options" :key="item.value" :label="item.dictLabel" :value="item.dictValue">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item class="form-item" label="调用目标字符串:" prop="invokeTarget">
          <el-input v-model="form.invokeTarget"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="cron表达式:" prop="cronExpression">
          <el-input v-model="form.cronExpression"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="执行策略:" prop="misfirePolicy">
          <el-radio v-model="form.misfirePolicy" label="1">立即执行</el-radio>
          <el-radio v-model="form.misfirePolicy" label="2">执行一次</el-radio>
          <el-radio v-model="form.misfirePolicy" label="3">放弃执行</el-radio>
        </el-form-item>
        <el-form-item class="form-item" label="并发执行:" prop="concurrent">
          <el-radio v-model="form.concurrent" label="0">允许</el-radio>
          <el-radio v-model="form.concurrent" label="1">禁止</el-radio>
        </el-form-item>
        <el-form-item class="form-item" label="状态:" prop="status">
          <el-radio v-model="form.status" label="0">正常</el-radio>
          <el-radio v-model="form.status" label="1">暂停</el-radio>
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
        jobId: "",
        jobName: "",
        jobGroup: "DEFAULT",
        invokeTarget: "",
        cronExpression: "",
        misfirePolicy: '1',
        concurrent: '1',
        status: '0',
        remark: "",
      },
      rules: {
        jobName: [{ required: true, message: "任务名称不能为空", trigger: "blur" }],
        invokeTarget: [
          { required: true, message: "调用目标字符串不能为空", trigger: "blur" },
        ],
        cronExpression: [
          { required: true, message: "cron表达式不能为空", trigger: "blur" },
        ],
      },

      options: [],
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
            url: this.$http.adornUrl(`/monitor/job/edit/${data.jobId}`),
            method: "get",
            params: this.$http.adornParams({})
          }).then((res) => {
            if (res.data.job) {
              let menu = res.data.job;
              this.form.jobId = menu.jobId;
              this.form.jobName = menu.jobName;
              this.form.UNITjobGroup = menu.UNITjobGroup;
              this.form.invokeTarget = menu.invokeTarget;
              this.form.cronExpression = menu.cronExpression;
              this.form.misfirePolicy = menu.misfirePolicy;
              this.form.concurrent = menu.concurrent;
              this.form.status = menu.status;
              this.form.remark = menu.remark;
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
            jobName: this.form.jobName,
            jobGroup: this.form.UNITjobGroup,
            invokeTarget: this.form.invokeTarget,
            cronExpression: this.form.cronExpression,
            misfirePolicy: this.form.misfirePolicy,
            concurrent: this.form.concurrent,
            status: this.form.status,
            remark: this.form.remark
          }
          if (this.status == 'edit') {
            params.jobId = this.form.jobId;
          }
          this.$http({
            url: this.$http.adornUrl(`/monitor/job/${this.status}`),
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
                that.$parent.openDialog = false;
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
    // 用户状态接口
    statusFun() {
      this.$http({
        url: this.$http.adornUrl("/tool/dict/getType"),
        method: "get",
        params: this.$http.adornParams(
          {
            "type": "sys_job_group"
          }
        ),
      }).then((res) => {
        if (res.data.length) {
          const data = res.data;
          this.options = data;
        }
      });
    },
  },
  //生命周期 - 创建完成（可以访问当前this实例）
  created() { },
  //生命周期 - 挂载完成（可以访问DOM元素）
  mounted() {
    this.statusFun();
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
  padding: 0 70px;
}

.form-item>>>.el-form-item__label {
  width: 20% !important;
}

.el-form-item {
  width: 100%;
  align-items: flex-start;
}

.form-item>>>.el-form-item__content {
  margin-left: 10px !important;
  width: 80% !important;
}
</style>
