<!--  -->
<template>
  <div class="dialogDiv">
    <el-dialog class="dialog" :title="title" :visible.sync="open" :width="width" :close-on-click-modal="false"
      append-to-body :lock-scroll="false" @destroy-on-close="true">
      <el-form :model="form" :rules="rules" ref="form" class="demo-form" id="form">
        <el-form-item class="form-item" label="公告标题:" prop="noticeTitle">
          <el-input v-model="form.noticeTitle"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="公告类型:" prop="noticeType">
          <el-select v-model="form.noticeType" placeholder="请选择">
            <el-option v-for="(item,index) in options" :key="index" :label="item.dictLabel" :value="item.dictValue">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item class="form-item" label="公告内容:" prop="noticeContent">
          <editor ref="editors" :value="form.noticeContent"></editor>
        </el-form-item>
        <el-form-item class="form-item" label="公告状态:" prop="status">
          <el-radio v-for="(item,index) in configTypeArr" :key="index" v-model="form.status"
            :label="item.dictValue">{{item.dictLabel}}</el-radio>
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
import editor from "@/views/common/editor";
export default {
  //import引入的组件需要注入到对象中才能使用
  components: {
    editor,
  },
  props: ["title", "width", "isDetail"],
  inject: ['getData'],
  data() {
    //这里存放数据
    return {
      // 是否显示弹出层
      open: false,
      form: {
        noticeTitle: "",
        noticeType: "1",
        status: "0",
        noticeContent: "",
      },
      rules: {
        noticeTitle: [{ required: true, message: "公告标题不能为空", trigger: "blur" }],
      },

      options: [],

      configTypeArr:[],

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
    addFun(tableRadio, status) {
      this.open = true;
      this.status = status;
      // 编辑器赋值为空
      this.$nextTick(() => {
        // this.$refs.editors.editor.txt.html()="";
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
            url: this.$http.adornUrl(`/system/notice/edit/${data.noticeId}`),
            method: "get",
            params: this.$http.adornParams({})
          }).then((res) => {
            if (res.data.notice) {
              let menu = res.data.notice,
              form=this.form;
              form.noticeId=menu.noticeId;
              form.noticeTitle= menu.noticeTitle,
              form.noticeType= menu.noticeType,
              form.noticeContent= menu.noticeContent,
              form.status= menu.status
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
          form.noticeContent=this.$refs.editors.editor.txt.html();
          let params = {
            noticeTitle: form.noticeTitle,
            noticeType: form.noticeType,
            noticeContent: form.noticeContent,
            status: form.status,
          }
          if (this.status == 'edit') {
            params.noticeId = this.form.noticeId;
          }
          this.$http({
            url: this.$http.adornUrl(`/system/notice/${this.status}`),
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

     // 公告类型接口
     dictTypeFun() {
      this.$http({
                url: this.$http.adornUrl("/tool/dict/getType"),
                method: "get",
                params: this.$http.adornParams(
                    {
                        "type": "sys_notice_type"
                    }
                ),
            }).then((res) => {
                if (res.data.length) {
                    const data = res.data;
                    this.options = data;
                }
            });
        },

        // 公告状态接口
    isDefaultFun() {
      this.$http({
        url: this.$http.adornUrl("/tool/dict/getType"),
        method: "GET",
        params: this.$http.adornParams({
          type: "sys_notice_status"
        }),
      }).then((res) => {
        this.configTypeArr = res.data;
      });
    },
  },
  //生命周期 - 创建完成（可以访问当前this实例）
  created() { },
  //生命周期 - 挂载完成（可以访问DOM元素）
  mounted() {
    this.dictTypeFun();
    this.isDefaultFun();
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
  /* display: flex;
  justify-content: space-between;
  flex-wrap: wrap; */
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
  width: 90% !important;
}
</style>
