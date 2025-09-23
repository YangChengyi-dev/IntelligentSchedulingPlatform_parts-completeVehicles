<!--  -->
<template>
  <div class="dialogDiv">
    <el-dialog class="dialog" :title="title" :visible.sync="open" :width="width" :close-on-click-modal="false"
      append-to-body :lock-scroll="false" @destroy-on-close="true">
      <el-form :model="form" :rules="rules" ref="form" class="demo-form" id="form">
        <el-form-item class="form-item" label="角色名称:" prop="roleName">
          <el-input v-model="form.roleName"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="权限字符:" prop="roleKey">
          <el-input v-model="form.roleKey"></el-input>
        </el-form-item>
        <el-form-item class="form-item" label="显示顺序:" prop="roleSort">
          <el-input v-model="form.roleSort"></el-input>
        </el-form-item>
        <el-form-item label="状态:" prop="status">
          <el-switch active-color="#13ce66" inactive-color="#ff4949" v-model="form.status" active-value="0"
            inactive-value="1">
          </el-switch>
        </el-form-item>
        <el-form-item class="form-item" label="备注:" prop="remark">
          <el-input v-model="form.remark"></el-input>
        </el-form-item>

        <el-form-item label="菜单权限:" prop="checkBox">
          <el-checkbox-group v-model="form.checkBox">
            <el-checkbox label="展开/折叠" @change="expandTree"></el-checkbox>
            <el-checkbox label="全选/全不选" v-model="checked" @change="checkedAll"></el-checkbox>
          </el-checkbox-group>

          <el-tree class="tree" ref="treeNode" :data="treeData" :props="defaultProps" show-checkbox node-key="id"
            :default-expand-all="isExpand" @node-click="handleNodeClick"></el-tree>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer" v-if="!isDetail">
        <el-button class="" @click="cancel">取消</el-button>
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
  components: {  },
  props: ["title", "width", "isDetail"],
  inject: ['getData'],
  data() {
    //这里存放数据
    return {
      // 是否显示弹出层
      open: false,
      form: {
        roleName: "",
        roleKey: "",
        roleSort: "",
        status: "0",
        remark: "",
        menuIds: "",
        checkBox: [],
      },
      rules: {
        roleName: [{ required: true, message: "角色名称不能为空", trigger: "blur" }],
        roleKey: [{ required: true, message: "权限字符不能为空", trigger: "blur" }],
        roleSort: [{ required: true, message: "显示顺序不能为空", trigger: "blur" }],
      },

      treeData: [],
      defaultProps: {
        children: "children",
        label: "title",
      },
      isExpand: false,
      checked: false,


      roles: {},
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
      var that = this;
      // this.form.menuIds='';
      this.$nextTick(() => {
        // 表单重置
        that.$refs.form.resetFields();
        // 查看/修改
        if (tableRadio) {
          this.$http({
            url: this.$http.adornUrl(`/system/role/edit/${tableRadio.roleId}`),
            method: "get",
            params: this.$http.adornParams({})
          }).then(res => {
            if (res.data.role) {
              this.roles = res.data.role;
              let roles = res.data.role;

              this.form.roleName = roles.roleName;
              this.form.roleKey = roles.roleKey;
              this.form.roleSort = roles.roleSort;
              this.form.status = roles.status;
              this.form.remark = roles.remark;
            }
          }).catch(err => {

          })

          let p = {
            roleId: tableRadio.roleId
          }
          this.getTree(p);
        } else {//新增
          this.getTree();
        }
      });
    },
    // 保存
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          var that = this;
          if (that.$refs.treeNode.getCheckedKeys().length > 0) {
            for (let i of that.$refs.treeNode.getCheckedKeys()) {
              this.form.menuIds += i + ',';
            }
          }
          let params = {
            roleName: this.form.roleName,
            roleKey: this.form.roleKey,
            roleSort: this.form.roleSort,
            status: this.form.status,
            remark: this.form.remark,
            menuIds: this.form.menuIds.substr(0, this.form.menuIds.length - 1),
          }
          var status = 'add';
          if (JSON.stringify(that.roles)!="{}") {
            status = 'edit';
            params.roleId = this.roles.roleId
          }
          this.$http({
            url: this.$http.adornUrl(`/system/role/${status}`),
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
            }else{
              this.$message({
                message: res.data.msg,
                type: "error"
              })
            }


          });
        } else {
          alert("error submit!!");
          return false;
        }
      });
    },
    // 取消
    cancel() {
      this.open = false;
      this.$parent.openDialog = false;
      this.getData();
    },
    handleNodeClick(data) {
      console.log(data);
    },
    // 获取树列表
    getTree(params) {
      this.treeData=[];
      this.$http({
        url: this.$http.adornUrl(`/system/menu/roleMenuTreeData`),
        method: "get",
        params: this.$http.adornParams(params)
      }).then((res) => {
        // this.treeData = res.data.treeData;
        if (res.data.length) {
          const data = res.data;
          for (let i = 0; i < data.length; i++) {
            data[i].children = [];
            // 默认选中
            if (data[i].checked) {
              this.$nextTick(() => {
                this.$refs.treeNode.setChecked(data[i].id, true);
              })
            }
            if (data[i].pId == 0) {
              this.treeData.push(data[i]);
            }
            for (let j = 1; j < data.length; j++) {
              if (data[j].pId == data[i].id) {
                data[i].children.push(data[j])
              }
            }
          }
        }

      });
    },

    // 展开/折叠树
    expandTree() {
      this.isExpand = !this.isExpand;
      this.buildData();
    },
    //遍历树的所有子节点，展开的时候给子节点展开状态赋值true，折叠时候赋值false
    buildData() {
      for (let i = 0; i < this.$refs.treeNode.store._getAllNodes().length; i++) {
        this.$refs.treeNode.store._getAllNodes()[i].expanded = this.isExpand;
      }
    },

    // 全选/全不选
    checkedAll() {
      this.checked = !this.checked;
      if (this.checked) {
        this.$refs.treeNode.setCheckedNodes(this.treeData);
      } else {
        this.$refs.treeNode.setCheckedNodes([])
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
/* @import roleSort(); 引入公共css类 */
/* .dialog >>> .el-dialog {
  height: v-bind(height) !important;
} */
.dialog>>>.el-dialog {
  max-height: 80%;
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

.ico-list .fa {
  margin: 5px;
  padding: 5px;
  cursor: pointer;
  font-size: 18px;
  width: 28px;
  border-radius: 3px;
}

.ico-list .fa:hover {
  background-color: #1d9d74;
  color: #ffffff;
}
</style>

<style lang="scss" scoped>
.tree {
  height: 20vh;
  overflow: auto;
}
</style>
