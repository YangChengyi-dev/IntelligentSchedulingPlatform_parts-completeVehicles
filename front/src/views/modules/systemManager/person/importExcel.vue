<!--  -->
<template>
  <div class="dialogDiv">
    <el-dialog class="dialog" title="导入excel文件" :visible.sync="open" width="40%" :close-on-click-modal="false"
      append-to-body :lock-scroll="false" @destroy-on-close="true">
      <el-upload ref="upload" name="file" :limit="limit" :auto-upload="false" action="接口地址" :on-exceed="handleExceed"
        :file-list="filelist" :on-change="handleChansge">
        <el-button slot="trigger" size="small" type="primary">选取excel文件</el-button>
        <div slot="tip" class="el-upload__tip tip">上传文件只能为excel文件，且为xlsx,xls格式</div>
      </el-upload>
      <div slot="footer" class="dialog-footer">
        <el-button class="" @click="open = false">取消</el-button>
        <el-button class="" type="primary" @click="submitForm('form')">导入</el-button>
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
      //文件
      file: "",
      filename: "",
      limit: 1,
      filelist: [],
      errmesg: [],
      button: {
        disable: false,
        message: "上传到服务器",
      },
    };
  },
  //监听属性 类似于data概念
  computed: {},
  //监控data中的数据变化
  watch: {},
  //方法集合
  methods: {
    resetPwd() {
      this.open = true;
    },
    //选择文件方法
    handleExceed(e) {
      // 判断是否只能上传一个文件，超过提示报错
      this.$notify.error({
        title: "错误",
        message: "只能上传一个文件",
      });
    },

    handleChansge(file, fileList) {
      let name = file.name;
      //判断是否是excel文件
      if (!/\.(xlsx|xls|XLSX|XLS)$/.test(name)) {
        this.$notify.error({
          title: "错误",
          message: "上传文件只能为excel文件，且为xlsx,xls格式",
        });
        this.filelist = [];
        this.file = "";
        return false;
      }
      this.file = file.raw;
      this.filename = name;
    },

    //上传文件方法
    submitForm() {
      //判断是否有上传的文件，不能传空值
      if (this.file == "") {
        this.$notify.error({
          title: "错误",
          message: "上传文件不能为空",
        });
        return false;
      } else {
        // 文件形式的需要用 formData形式
        let formData = new FormData();
        formData.append('file', this.file);
        const loading = this.$loading({
          lock: true,
          text: "导入中...",
          spinner: "el-icon-loading",
          background: "rgba(0, 0, 0, 0.7)",
        });
        this.$http({
          url: this.$http.adornUrl(`/system/user/importData`),
          method: "POST",
          data: formData,
          headers: {
            "Content-Type": "multipart/form-data;boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW"
          }
        }).then(res => {
          loading.close();
          if (res.data.code == 0) {
            this.$message({
              type: "success",
              message: res.data.msg,
            });
            setTimeout(() => {
              that.open = false;
              this.getData();
            }, 1000);
          } else {
            this.$notify.error({
              title: "错误",
              message: res.data.msg,
            });
          }
        }).catch(err => {
          loading.close();
        })
      }
    },
  },
  //生命周期 - 创建完成（可以访问当前this实例）
  created() { },
  //生命周期 - 挂载完成（可以访问DOM元素）
  mounted() {
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
  /* display: flex;
    justify-content: space-between;
    flex-wrap: wrap; */
  padding: 0 70px;
}

.form-item>>>.el-form-item__label {
  width: 30% !important;
}

.el-form-item {
  width: 100%;
  align-items: flex-start;
}

.form-item>>>.el-form-item__content {
  margin-left: 10px !important;
  width: 70% !important;
}

.tip {
  color: rgb(226, 66, 66);
}
</style>
