<!--  -->
<template>
  <div class="dialogDiv">
    <el-dialog
      class="dialog"
      :title="title"
      :visible.sync="open"
      :width="width"
      style="height: 100%"
      :close-on-click-modal="false"
      append-to-body
      :lock-scroll="false"
      @destroy-on-close="true"
    >
      <el-form :model="form" :rules="rules" ref="form" class="demo-form" id="form">
        <el-form-item class="form-item" label="库房名称:" prop="UNIT_NAME">
          <el-input v-model="form.UNIT_NAME"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="联系人:" prop="MARKET_NAME">
          <el-input v-model="form.MARKET_NAME"></el-input>
        </el-form-item>

        <el-form-item class="form-item" label="联系电话:" prop="TYPE_NAME">
          <el-input v-model="form.TYPE_NAME"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="所处区域:" prop="CAPACITY">
          <el-input v-model="form.CAPACITY"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="详细地址:" prop="START_TIME">
          <el-input v-model="form.START_TIME"></el-input>
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
        UNIT_NAME: "",
        MARKET_NAME: "",
        TYPE_NAME: "",
        CAPACITY: "",
        START_TIME: "",
      },
      rules: {
        UNIT_NAME: [{ required: true, message: "库房名称不能为空", trigger: "blur" }],
        MARKET_NAME: [{ required: true, message: "联系人不能为空", trigger: "blur" }],
        TYPE_NAME: [{ required: true, message: "联系电话不能为空", trigger: "blur" }],
        CAPACITY: [{ required: true, message: "所处区域不能为空", trigger: "blur" }],
        START_TIME: [{ required: true, message: "详细地址不能为空", trigger: "blur" }],
      },

      editStartOptions: {
        disabledDate: (time) => {
          if (!this.form.YEAR) {
            return time.getTime() < new Date(1970 - 1 - 1).getTime(); //禁止选择1970年以前的日期
          } else {
            return time.getTime() > new Date(this.form.YEAR);
          }
        },
      },
      editStopOptions: {
        disabledDate: (time) => {
          return (
            time.getTime() < new Date(this.form.startTime) ||
            time.getTime() < new Date(1970 - 1 - 1).getTime() //禁止选择1970年以前的日期
          );
        },
      },
    };
  },
  //监听属性 类似于data概念
  computed: {},
  //监控data中的数据变化
  watch: {},
  //方法集合
  methods: {
    // 窗口初始化方法，nextTick方法可以添加逻辑，如打开窗口时查询数据填充
    init(tableRadio) {
      this.open = true;
      this.$nextTick(() => {
        // 表单重置
        this.$refs["form"].resetFields();
        if (tableRadio) {
          this.form.UNIT_NAME = tableRadio.UNIT_NAME;
          this.form.MARKET_NAME = tableRadio.MARKET_NAME;
          this.form.TYPE_NAME = tableRadio.TYPE_NAME;
          this.form.CAPACITY = tableRadio.CAPACITY;
          this.form.START_TIME = tableRadio.START_TIME;
        }
      });
    },
    // 保存
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          alert("submit!");
          // console.log(this.$parent.searchTableData)
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
  },
  //生命周期 - 创建完成（可以访问当前this实例）
  created() {},
  //生命周期 - 挂载完成（可以访问DOM元素）
  mounted() {},
  beforeCreate() {}, //生命周期 - 创建之前
  beforeMount() {}, //生命周期 - 挂载之前
  beforeUpdate() {}, //生命周期 - 更新之前
  updated() {}, //生命周期 - 更新之后
  beforeDestroy() {}, //生命周期 - 销毁之前
  destroyed() {}, //生命周期 - 销毁完成
  activated() {}, //如果页面有keep-alive缓存功能，这个函数会触发
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
.el-form-item__label {
  width: 40%;
}
.el-form-item {
  width: 45%;
}
.el-form-item__content {
  margin-left: 10px !important;
  width: 60%;
}
.form-item >>> .el-form-item__content {
  margin-left: 15px !important;
}
</style>
