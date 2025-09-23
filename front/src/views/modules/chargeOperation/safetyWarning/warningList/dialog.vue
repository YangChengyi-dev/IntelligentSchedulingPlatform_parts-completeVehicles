<!--  -->
<template>
  <div class="dialogDiv">
    <el-dialog
      class="dialog"
      :visible.sync="open"
      :width="width"
      :close-on-click-modal="false"
      append-to-body
      :lock-scroll="false"
      @destroy-on-close="true"
    >
    <div id="container"></div>
      <div slot="footer" class="dialog-footer">
        <el-button class="" type="primary" @click="open = false">取消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
//这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）
//例如：import 《组件名称》 from '《组件路径》';
import AMapLoader from '@amap/amap-jsapi-loader';
export default {
  //import引入的组件需要注入到对象中才能使用
  components: {},
  props: ["title", "width"],
  data() {
    //这里存放数据
    return {
      // 是否显示弹出层
      open: false,
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
      });
    },
    initMap() {
      this.open = true;
      AMapLoader.load({
        key: 'b039c6c138fa652d28abf0e62e665b32',  //设置您的key
        version: "2.0", // 高德地图版本
        plugins: ['AMap.ToolBar', 'AMap.Driving'], // 插件
        AMapUI: { // 高德地图UI组件库，可不写，内部提供了覆盖物标注点，以及部分模块的封装
          version: "1.1",
          plugins: [],
        },
        Loca: { // Loca版本(高性能地图数据可视化库) 可不写
          version: "2.0"
        },
      }).then((AMap) => {
        // container渲染的id
        this.map = new AMap.Map("container", {
          zoom: 9, // 当前缩放级别
          zooms: [2, 22], // 缩放级别范围
          center: [118.997428, 31.90923], // 中心点
        });
        // 点标记显示内容，HTML要素字符串
        var markerContent =
          "" +
          '<div class="custom-content-marker" v-if="www" style="position: relative;width: 40px;height: 50px;">' +
          '   <img src="//a.amap.com/jsapi_demos/static/demo-center/icons/poi-marker-default.png" style="width: 100%;height: 100%;">' +
          '   <div class="close-btn" style="position: absolute;top: 4px;right: 8px;width: 30px;height: 30px;font-size: 16px;color: #fff;text-align: center;line-height: 30px;">19</div>' +
          "</div>";
        var position1 = new AMap.LngLat(118.997428, 31.90923);
        this.marker1 = new AMap.Marker({
          position: position1,
          // 将 html 传给 content
          content: markerContent,
          // 以 icon 的 [center bottom] 为原点
          offset: new AMap.Pixel(-13, -30),
        });
        this.map.add( this.marker1);
      }).catch(e => {
        console.log(e);
      })
    },
  },
  //生命周期 - 创建完成（可以访问当前this实例）
  created() {},
  //生命周期 - 挂载完成（可以访问DOM元素）
  mounted() {
  },
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
#container {
        margin-left: 2%;
        width: 98%;
        height: 40vh;
      }
</style>
