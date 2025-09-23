<!--  -->
<template>
  <div class="dialogDiv">
    <el-dialog class="dialog" title="菜单选择" :visible.sync="open" :width="width" :close-on-click-modal="false"
      append-to-body :lock-scroll="false" @destroy-on-close="true">
      <div class="filter">
        <div id="form">
          <el-input placeholder="请输入" v-model="filterText"> </el-input>
        </div>
        <el-button type="primary" size="small" plain @click="expandTree">展开/折叠</el-button>
      </div>
      <el-tree class="tree" ref="treeNode" :data="treeData" :props="defaultProps" node-key="title"
        :default-expand-all="isExpand" accordion @node-click="handleNodeClick" :filter-node-method="filterNode">
      </el-tree>
      <div slot="footer" class="dialog-footer">
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
  props: ["width"],
  data() {
    //这里存放数据
    return {
      // 是否显示弹出层
      open: false,
      filterText: "",
      treeData: [

      ],
      defaultProps: {
        children: "children",
        label: "title",
      },
      isExpand: false,

      parentId: "",
    };
  },
  //监听属性 类似于data概念
  computed: {},
  //监控data中的数据变化
  watch: {
    filterText(val) {
      this.$refs.treeNode.filter(val);
    },
  },
  //方法集合
  methods: {
    // 窗口初始化方法，nextTick方法可以添加逻辑，如打开窗口时查询数据填充
    init(tableRadio) {
      this.open = true;
      this.getTree();
    },

    // 树接口
    getTree() {
      this.treeData = [];
      this.$http({
        url: this.$http.adornUrl(`/system/dept/treeData`),
        method: "get",
        data: {},
      }).then((res) => {
        // this.treeData = res.data.treeData;
        if (res.data.length) {
          const data = res.data;
          for (let i = 0; i < data.length; i++) {
            data[i].children = [];
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
    // 保存
    submitForm(formName) {
      this.$parent.form.deptId = this.parentId;
      this.$parent.form.deptName = this.parentMenu;
      this.open = false;
    },

    handleNodeClick(data) {
      this.parentId = data.id;
      this.parentMenu = data.title;
    },
    filterNode(value, data) {
      if (!value) return true;
      return data.title.indexOf(value) !== -1;
    },
    // 展开/折叠树
    expandTree() {
      this.isExpand = !this.isExpand;
      this.$nextTick(() => {
        this.buildData();
      })
    },
    //遍历树的所有子节点，展开的时候给子节点展开状态赋值true，折叠时候赋值false
    buildData() {
      for (let i = 0; i < this.$refs.treeNode.store._getAllNodes().length; i++) {
        this.$refs.treeNode.store._getAllNodes()[i].expanded = this.isExpand;
      }
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

.dialog>>>.el-dialog {
  max-height: 76%;
}

#form {
  margin: 0 20px 0px 0;
}

#form>>>.el-form-item__label {
  width: 30%!important;
}

.el-form-item {
  width: 100%;
  align-items: flex-start !important;
}

#form>>>.el-form-item__content {
  margin-left: 10px !important;
  width: 90% !important;
}

.filter {
  display: flex;
  align-items: center;
}

.tree {
  height: 50vh;
  overflow: auto;
}
</style>
