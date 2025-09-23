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
        <el-form-item class="form-item" label="备件名称:" prop="UNIT_NAME">
          <el-input v-model="form.UNIT_NAME"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="类别:" prop="MARKET_NAME">
          <el-input v-model="form.MARKET_NAME"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="库房:" prop="TYPE_NAME">
          <el-input v-model="form.TYPE_NAME"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="入库数:" prop="CAPACITY">
          <el-input v-model="form.CAPACITY"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="入库人:" prop="START_TIME">
          <el-input v-model="form.START_TIME"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="入库时间:" prop="END_TIME">
          <el-date-picker
            v-model="form.END_TIME"
            type="datetime"
            placeholder="请选择"
          ></el-date-picker>
        </el-form-item>

        <el-form-item class="form-item" label="生产厂商:" prop="YEAR">
          <el-input v-model="form.YEAR"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="型号:" prop="perform">
          <el-input v-model="form.perform"></el-input>
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
        END_TIME: "",
        YEAR: "",
        perform: "",
      },
      rules: {
        UNIT_NAME: [{ required: true, message: "备件名称不能为空", trigger: "blur" }],
        MARKET_NAME: [{ required: true, message: "类别不能为空", trigger: "blur" }],
        TYPE_NAME: [{ required: true, message: "库房不能为空", trigger: "blur" }],
        CAPACITY: [{ required: true, message: "入库数不能为空", trigger: "blur" }],
        START_TIME: [{ required: true, message: "入库人不能为空", trigger: "blur" }],
        YEAR: [{ required: true, message: "生产厂商不能为空", trigger: "blur" }],
        perform: [{ required: true, message: "型号不能为空", trigger: "blur" }],
        END_TIME: [
          {
            required: true,
            message: "入库时间不能为空",
            trigger: "change",
          },
        ],
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
          this.form.END_TIME = tableRadio.END_TIME;
          this.form.YEAR = tableRadio.YEAR;
          this.form.perform = tableRadio.perform;
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
