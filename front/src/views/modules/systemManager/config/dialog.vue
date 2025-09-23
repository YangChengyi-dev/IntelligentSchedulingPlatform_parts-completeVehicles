<!--  -->
<template>
  <div class="dialogDiv">
     <el-dialog class="dialog" :title="title" :visible.sync="open" :width="width" :close-on-click-modal="false"
      append-to-body :lock-scroll="false" @destroy-on-close="true">
      <el-form :model="form" :rules="rules" ref="form" class="demo-form" id="form">

        <el-form-item class="form-item" label="参数名称:" prop="configName">
          <el-input v-model="form.configName"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="参数键名:" prop="configKey">
          <el-input v-model="form.configKey"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="参数键值:" prop="configValue">
          <el-input v-model="form.configValue"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="系统内置:" prop="configType">
          <el-radio v-for="(item,index) in configTypeArr" :key="index" v-model="form.configType"
            :label="item.dictValue">{{item.dictLabel}}</el-radio>
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
        configName: "",
        configKey: "",
        configType: "Y",
        remark: "",
        configValue: "",
      },
      rules: {
        configName: [{ required: true, message: "参数名称不能为空", trigger: "blur" }],
        configKey: [{ required: true, message: "参数键名不能为空", trigger: "blur" }],
        configValue: [{ required: true, message: "参数键值不能为空", trigger: "blur" }],
      },
      status: "",

      configTypeArr: [],
    };
  },
  //监听属性 类似于data概念
  computed: {},
  //监控data中的数据变化
  watch: {},
  //方法集合
  methods: {
    addFun(tableRadio, status) {
      this.open = true;
      this.status = status;
      this.$nextTick(() => {
        // 表单重置
        this.$refs["form"].resetFields();
      });
    },

     // 修改
     editFun(data,status){
      this.open = true;
      this.status = status;
      this.$nextTick(() => {
        // 表单重置
        this.$refs["form"].resetFields();

        if (data) {
          this.$http({
            url: this.$http.adornUrl(`/system/config/edit/${data.configId}`),
            method: "get",
            params: this.$http.adornParams({})
          }).then((res) => {
            if (res.data.config) {
              let menu = res.data.config,
              form=this.form;
              form.configId=menu.configId;
              form.configName= menu.configName,
              form.configKey = menu.configKey,
              form.configValue= menu.configValue,
              form.configType= menu.configType,
              form.remark= menu.remark
            }
          });
        }
      });
    },
    // 保存
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          let form = this.form;
          let params = {
            configName: form.configName,
            configKey: form.configKey,
            configValue: form.configValue,
            configType: form.configType,
            remark: form.remark
          }
          if (this.status == 'edit') {
            params.configId = this.form.configId;
          }
          this.$http({
            url: this.$http.adornUrl(`/system/config/${this.status}`),
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

    // 字典名称接口
    isDefaultFun() {
      this.$http({
        url: this.$http.adornUrl("/tool/dict/getType"),
        method: "GET",
        params: this.$http.adornParams({
          type: "sys_yes_no"
        }),
      }).then((res) => {
        this.configTypeArr = res.data;
      });
    },
  },
  //生命周期 - 创建完成（可以访问当前this实例）
  created() {
    this.isDefaultFun();

  },
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
