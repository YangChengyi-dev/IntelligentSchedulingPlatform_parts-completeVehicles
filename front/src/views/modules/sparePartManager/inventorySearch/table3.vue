<!--  -->
<template>
  <div class="">
    <el-table
      :data="table3Data"
      id="table"
      stripe
      style="width: 100%"
      :header-row-style="{ height: '35px' }"
      :row-style="{ height: '35px' }"
      :height="height"
    >
    
      <el-table-column prop="UNIT_NAME" label="城市" align="center" min-width="32%">
      </el-table-column>
      <el-table-column prop="MARKET_NAME" label="区县" align="center" min-width="32%">
      </el-table-column>
      <el-table-column prop="TYPE_NAME" label="场站" align="center" min-width="32%">
      </el-table-column>
      <el-table-column prop="CAPACITY" label="桩编号" align="center" min-width="32%">
      </el-table-column>

      <el-table-column prop="START_TIME" label="备件类型" align="center" min-width="32%">
      </el-table-column>
      <el-table-column prop="END_TIME" label="厂商" align="center" min-width="32%">
      </el-table-column>
      <el-table-column prop="FILE_NAME" label="型号" align="center" min-width="32%">
      </el-table-column>
      <el-table-column prop="YEAR" label="时间" align="center" min-width="32%">
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
//这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）
//例如：import 《组件名称》 from '《组件路径》';

export default {
  //import引入的组件需要注入到对象中才能使用
  components: {},
  props: ["height", "table3Data"],
  data() {
    //这里存放数据
    return {
      tableData: [],
      searchTableData: [],
      TableHeight: 0,
    };
  },
  //监听属性 类似于data概念
  computed: {},
  //监控data中的数据变化
  watch: {},
  //方法集合
  methods: {},
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
<style lang="scss" scoped>
//@import url(); 引入公共css类
</style>
