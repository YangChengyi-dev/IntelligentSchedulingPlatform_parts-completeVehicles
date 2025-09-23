<!--  -->
<template>
  <div class="healthOverview">
    <div class="topDiv">
      <div class="top1">
        <div class="pic" id="pic1"></div>
        <div class="num">28个</div>
        <div class="text">总中转站点数</div>
      </div>
      <div class="top2">
        <div class="pic" id="pic2"></div>
        <div class="num">15</div>
        <div class="text">品牌车铁路站点数</div>
      </div>
      <div class="top3">
        <div class="pic" id="pic3"></div>
        <div class="num">9个(>品牌车数)</div>
        <div class="text">合资车铁路站点数</div>
      </div>
      <div class="top4">
        <div class="pic" id="pic4"></div>
        <div class="num">3个</div>
        <div class="text">品牌车水运站点数</div>
      </div>
      <div class="top5">
        <div class="pic" id="pic5"></div>
        <div class="num">1个(>品牌车数)</div>
        <div class="text">合资车水运站点数</div>
      </div>
    </div>
    <div id="container"></div>
  </div>
</template>

<script>
//这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）
//例如：import 《组件名称》 from '《组件路径》';
import AMapLoader from "@amap/amap-jsapi-loader";

export default {
  //import引入的组件需要注入到对象中才能使用
  components: {},
  data() {
    //这里存放数据
    return {};
  },
  //监听属性 类似于data概念
  computed: {},
  //监控data中的数据变化
  watch: {},
  //方法集合
  methods: {
    initMap() {
      AMapLoader.load({
        key: "b039c6c138fa652d28abf0e62e665b32", //设置您的key
        version: "2.0", // 高德地图版本
        plugins: ["AMap.ToolBar", "AMap.Driving"], // 插件
        AMapUI: {
          // 高德地图UI组件库，可不写，内部提供了覆盖物标注点，以及部分模块的封装
          version: "1.1",
          plugins: [],
        },
        Loca: {
          // Loca版本(高性能地图数据可视化库) 可不写
          version: "2.0",
        },
      })
        .then((AMap) => {
          // container渲染的id
          this.map = new AMap.Map("container", {
            zoom: 4, // 设置一个较小的缩放级别，以便整个中国可以在视野中
            zooms: [4, 18], // 根据需要设置缩放级别范围
            center: [105.97, 35.46], // 设置地图中心点为中国的大致中心位置
          });
          // 点标记显示内容，HTML要素字符串
          var markerContent =
            "" +
            '<div class="custom-content-marker" style="position: relative;width: 44px;height: 60px;">' +
            '   <img src="../../../../../../static/img/poi-marker-light.png" style="width: 100%;height: 100%;opacity:0.7">' +
            '   <div class="close-btn" style="position: absolute;top: 4px;right: 8px;width: 30px;height: 30px;font-size: 16px;color: #fff;text-align: center;line-height: 30px;">3</div>' +
            "</div>";
          var markerContent_1 =
            "" +
            '<div class="custom-content-marker" style="position: relative;width: 44px;height: 60px;">' +
            '   <img src="../../../../../../static/img/poi-marker-light.png" style="width: 100%;height: 100%;opacity:0.7">' +
            '   <div class="close-btn" style="position: absolute;top: 4px;right: 8px;width: 30px;height: 30px;font-size: 16px;color: #fff;text-align: center;line-height: 30px;">1</div>' +
            "</div>";
          var markerContent_2 =
            "" +
            '<div class="custom-content-marker" style="position: relative;width: 44px;height: 60px;">' +
            '   <img src="../../../../../../static/img/poi-marker-blue.png"  style="width: 100%;height: 100%;opacity:0.7">' +
            '   <div class="close-btn" style="position: absolute;top: 4px;right: 8px;width: 30px;height: 30px;font-size: 16px;color: #fff;text-align: center;line-height: 30px;">2</div>' +
            "</div>";
          var markerContent_4 =
            "" +
            '<div class="custom-content-marker" style="position: relative;width: 44px;height: 60px;">' +
            '   <img src="../../../../../../static/img/poi-marker-light.png" style="width: 100%;height: 100%;opacity:0.7">' +
            '   <div class="close-btn" style="position: absolute;top: 4px;right: 8px;width: 30px;height: 30px;font-size: 16px;color: #fff;text-align: center;line-height: 30px;">4</div>' +
            "</div>";
          var markerContent_5 =
            "" +
            '<div class="custom-content-marker" style="position: relative;width: 44px;height: 60px;">' +
            '   <img src="../../../../../../static/img/poi-marker-light.png" style="width: 100%;height: 100%;opacity:0.7">' +
            '   <div class="close-btn" style="position: absolute;top: 4px;right: 8px;width: 30px;height: 30px;font-size: 16px;color: #fff;text-align: center;line-height: 30px;">5</div>' +
            "</div>";
          var markerContent_6 =
            "" +
            '<div class="custom-content-marker" style="position: relative;width: 44px;height: 60px;">' +
            '   <img src="../../../../../../static/img/poi-marker-light.png" style="width: 100%;height: 100%;opacity:0.7">' +
            '   <div class="close-btn" style="position: absolute;top: 4px;right: 8px;width: 30px;height: 30px;font-size: 16px;color: #fff;text-align: center;line-height: 30px;">6</div>' +
            "</div>";
          var markerContent_7 =
            "" +
            '<div class="custom-content-marker" style="position: relative;width: 44px;height: 60px;">' +
            '   <img src="../../../../../../static/img/poi-marker-blue.png"  style="width: 100%;height: 100%;opacity:0.7">' +
            '   <div class="close-btn" style="position: absolute;top: 4px;right: 8px;width: 30px;height: 30px;font-size: 16px;color: #fff;text-align: center;line-height: 30px;">7</div>' +
            "</div>";
          var markerContent_8 =
            "" +
            '<div class="custom-content-marker" style="position: relative;width: 44px;height: 60px;">' +
            '   <img src="../../../../../../static/img/poi-marker-light.png" style="width: 100%;height: 100%;opacity:0.7">' +
            '   <div class="close-btn" style="position: absolute;top: 4px;right: 8px;width: 30px;height: 30px;font-size: 16px;color: #fff;text-align: center;line-height: 30px;">8</div>' +
            "</div>";
          var markerContent_9 =
            "" +
            '<div class="custom-content-marker" style="position: relative;width: 44px;height: 60px;">' +
            '   <img src="../../../../../../static/img/poi-marker-light.png" style="width: 100%;height: 100%;opacity:0.7">' +
            '   <div class="close-btn" style="position: absolute;top: 4px;right: 8px;width: 30px;height: 30px;font-size: 16px;color: #fff;text-align: center;line-height: 30px;">9</div>' +
            "</div>";
          var markerContent_10 =
            "" +
            '<div class="custom-content-marker" style="position: relative;width: 44px;height: 60px;">' +
            '   <img src="../../../../../../static/img/poi-marker-light.png" style="width: 100%;height: 100%;opacity:0.7">' +
            '   <div class="close-btn" style="position: absolute;top: 4px;right: 8px;width: 30px;height: 30px;font-size: 16px;color: #fff;text-align: center;line-height: 30px;">10</div>' +
            "</div>";
          var markerContent_11 =
            "" +
            '<div class="custom-content-marker" style="position: relative;width: 44px;height: 60px;">' +
            '   <img src="../../../../../../static/img/poi-marker-light.png" style="width: 100%;height: 100%;opacity:0.7">' +
            '   <div class="close-btn" style="position: absolute;top: 4px;right: 8px;width: 30px;height: 30px;font-size: 16px;color: #fff;text-align: center;line-height: 30px;">11</div>' +
            "</div>";
          var markerContent_12 =
            "" +
            '<div class="custom-content-marker" style="position: relative;width: 44px;height: 60px;">' +
            '   <img src="../../../../../../static/img/poi-marker-light.png" style="width: 100%;height: 100%;opacity:0.7">' +
            '   <div class="close-btn" style="position: absolute;top: 4px;right: 8px;width: 30px;height: 30px;font-size: 16px;color: #fff;text-align: center;line-height: 30px;">12</div>' +
            "</div>";
          var markerContent_13 =
            "" +
            '<div class="custom-content-marker" style="position: relative;width: 44px;height: 60px;">' +
            '   <img src="../../../../../../static/img/poi-marker-blue.png"  style="width: 100%;height: 100%;opacity:0.7">' +
            '   <div class="close-btn" style="position: absolute;top: 4px;right: 8px;width: 30px;height: 30px;font-size: 16px;color: #fff;text-align: center;line-height: 30px;">13</div>' +
            "</div>";
          var markerContent_14 =
            "" +
            '<div class="custom-content-marker" style="position: relative;width: 44px;height: 60px;">' +
            '   <img src="../../../../../../static/img/poi-marker-light.png" style="width: 100%;height: 100%;opacity:0.7">' +
            '   <div class="close-btn" style="position: absolute;top: 4px;right: 8px;width: 30px;height: 30px;font-size: 16px;color: #fff;text-align: center;line-height: 30px;">14</div>' +
            "</div>";
          var markerContent_15 =
            "" +
            '<div class="custom-content-marker" style="position: relative;width: 44px;height: 60px;">' +
            '   <img src="../../../../../../static/img/poi-marker-light.png" style="width: 100%;height: 100%;opacity:0.7">' +
            '   <div class="close-btn" style="position: absolute;top: 4px;right: 8px;width: 30px;height: 30px;font-size: 16px;color: #fff;text-align: center;line-height: 30px;">15</div>' +
            "</div>";
          var markerContent_16 =
            "" +
            '<div class="custom-content-marker" style="position: relative;width: 44px;height: 60px;">' +
            '   <img src="../../../../../../static/img/poi-marker-light.png" style="width: 100%;height: 100%;opacity:0.7">' +
            '   <div class="close-btn" style="position: absolute;top: 4px;right: 8px;width: 30px;height: 30px;font-size: 16px;color: #fff;text-align: center;line-height: 30px;">16</div>' +
            "</div>";
          var markerContent_17 =
            "" +
            '<div class="custom-content-marker" style="position: relative;width: 44px;height: 60px;">' +
            '   <img src="../../../../../../static/img/poi-marker-light.png" style="width: 100%;height: 100%;opacity:0.7">' +
            '   <div class="close-btn" style="position: absolute;top: 4px;right: 8px;width: 30px;height: 30px;font-size: 16px;color: #fff;text-align: center;line-height: 30px;">17</div>' +
            "</div>";
          var markerContent_18 =
            "" +
            '<div class="custom-content-marker" style="position: relative;width: 44px;height: 60px;">' +
            '   <img src="../../../../../../static/img/poi-marker-light.png" style="width: 100%;height: 100%;opacity:0.7">' +
            '   <div class="close-btn" style="position: absolute;top: 4px;right: 8px;width: 30px;height: 30px;font-size: 16px;color: #fff;text-align: center;line-height: 30px;">18</div>' +
            "</div>";
          var markerContent_19 =
            "" +
            '<div class="custom-content-marker" style="position: relative;width: 44px;height: 60px;">' +
            '   <img src="../../../../../../static/img/poi-marker-red.png" style="width: 100%;height: 100%;opacity:0.7">' +
            '   <div class="close-btn" style="position: absolute;top: 4px;right: 8px;width: 30px;height: 30px;font-size: 16px;color: #fff;text-align: center;line-height: 30px;">19</div>' +
            "</div>";
          var markerContent_20 =
            "" +
            '<div class="custom-content-marker" style="position: relative;width: 44px;height: 60px;">' +
            '   <img src="../../../../../../static/img/poi-marker-red.png" style="width: 100%;height: 100%;opacity:0.7">' +
            '   <div class="close-btn" style="position: absolute;top: 4px;right: 8px;width: 30px;height: 30px;font-size: 16px;color: #fff;text-align: center;line-height: 30px;">20</div>' +
            "</div>";
          var markerContent_21 =
            "" +
            '<div class="custom-content-marker" style="position: relative;width: 44px;height: 60px;">' +
            '   <img src="../../../../../../static/img/poi-marker-red.png" style="width: 100%;height: 100%;opacity:0.7">' +
            '   <div class="close-btn" style="position: absolute;top: 4px;right: 8px;width: 30px;height: 30px;font-size: 16px;color: #fff;text-align: center;line-height: 30px;">21</div>' +
            "</div>";
          var markerContent_22 =
            "" +
            '<div class="custom-content-marker" style="position: relative;width: 44px;height: 60px;">' +
            '   <img src="../../../../../../static/img/poi-marker-red.png" style="width: 100%;height: 100%;opacity:0.7">' +
            '   <div class="close-btn" style="position: absolute;top: 4px;right: 8px;width: 30px;height: 30px;font-size: 16px;color: #fff;text-align: center;line-height: 30px;">22</div>' +
            "</div>";
          var markerContent_23 =
            "" +
            '<div class="custom-content-marker" style="position: relative;width: 44px;height: 60px;">' +
            '   <img src="../../../../../../static/img/poi-marker-red.png" style="width: 100%;height: 100%;opacity:0.7">' +
            '   <div class="close-btn" style="position: absolute;top: 4px;right: 8px;width: 30px;height: 30px;font-size: 16px;color: #fff;text-align: center;line-height: 30px;">23</div>' +
            "</div>";
          var markerContent_24 =
            "" +
            '<div class="custom-content-marker" style="position: relative;width: 44px;height: 60px;">' +
            '   <img src="../../../../../../static/img/poi-marker-red.png" style="width: 90%;height: 90%;opacity:0.7">' +
            '   <div class="close-btn" style="position: absolute;top: 4px;right: 8px;width: 30px;height: 30px;font-size: 16px;color: #fff;text-align: center;line-height: 30px;">24</div>' +
            "</div>";
          var markerContent_25 =
            "" +
            '<div class="custom-content-marker" style="position: relative;width: 44px;height: 60px;">' +
            '   <img src="../../../../../../static/img/poi-marker-red.png" style="width: 90%;height: 90%;opacity:0.7">' +
            '   <div class="close-btn" style="position: absolute;top: 4px;right: 8px;width: 30px;height: 30px;font-size: 16px;color: #fff;text-align: center;line-height: 30px;">25</div>' +
            "</div>";
          var markerContent_26 =
            "" +
            '<div class="custom-content-marker" style="position: relative;width: 44px;height: 60px;">' +
            '   <img src="../../../../../../static/img/poi-marker-red.png" style="width: 100%;height: 100%;opacity:0.7">' +
            '   <div class="close-btn" style="position: absolute;top: 4px;right: 8px;width: 30px;height: 30px;font-size: 16px;color: #fff;text-align: center;line-height: 30px;">26</div>' +
            "</div>";
          var markerContent_27 =
            "" +
            '<div class="custom-content-marker" style="position: relative;width: 44px;height: 60px;">' +
            '   <img src="../../../../../../static/img/poi-marker-red.png" style="width: 100%;height: 100%;opacity:0.7">' +
            '   <div class="close-btn" style="position: absolute;top: 4px;right: 8px;width: 30px;height: 30px;font-size: 16px;color: #fff;text-align: center;line-height: 30px;">27</div>' +
            "</div>";
          var markerContent_28 =
            "" +
            '<div class="custom-content-marker" style="position: relative;width: 44px;height: 60px;">' +
            '   <img src="../../../../../../static/img/poi-marker-purple.png" style="width: 100%;height: 100%;opacity:0.7">' +
            '   <div class="close-btn" style="position: absolute;top: 4px;right: 8px;width: 30px;height: 30px;font-size: 16px;color: #fff;text-align: center;line-height: 30px;">28</div>' +
            "</div>";
          var position1 = new AMap.LngLat(114.30525, 30.59276); //武汉
          var marker1 = new AMap.Marker({
            position: position1,
            // 将 html 传给 content
            content: markerContent,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "武汉"
          });
          this.map.add(marker1);

          var position5 = new AMap.LngLat(104.0668, 30.5728); //成都
          var marker5 = new AMap.Marker({
            position: position5,
            // 将 html 传给 content
            content: markerContent_8,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "成都"
          });
          this.map.add(marker5);

          var position6 = new AMap.LngLat(121.5440, 29.8683);  //宁波
          var marker6 = new AMap.Marker({
            position: position6,
            // 将 html 传给 content
            content: markerContent_7,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "宁波"
          });
          this.map.add(marker6);

          var position9 = new AMap.LngLat(113.6254, 34.7466); //郑州
          var marker9 = new AMap.Marker({
            position: position9,
            // 将 html 传给 content
            content: markerContent_9,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "郑州"
          });
          this.map.add(marker9);


          var position7 = new AMap.LngLat(117.1201, 36.6512);  //济南
          var marker7 = new AMap.Marker({
            position: position7,
            // 将 html 传给 content
            content: markerContent_1,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "济南"
          });
          this.map.add(marker7);

          var position8 = new AMap.LngLat(121.4737, 31.23037);//上海
          var marker8 = new AMap.Marker({
            position: position8,
            // 将 html 传给 content
            content: markerContent_2,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "上海"
          });
          this.map.add(marker8);

          var position9 = new AMap.LngLat(120.20, 30.24); //杭州
          var marker9 = new AMap.Marker({
            position: position9,
            // 将 html 传给 content
            content: markerContent_4,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "杭州"
          });
          this.map.add(marker9);

          var position10 = new AMap.LngLat(102.7183, 25.0389); //昆明
          var marker10 = new AMap.Marker({
            position: position10,
            // 将 html 传给 content
            content: markerContent_5,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "昆明"
          });
          this.map.add(marker10);

          var position11 = new AMap.LngLat(113.1216, 23.0219); //佛山
          var marker11 = new AMap.Marker({
            position: position11,
            // 将 html 传给 content
            content: markerContent_6,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "佛山"
          });
          this.map.add(marker11);

          var position12 = new AMap.LngLat(108.9398, 34.3416);//西安
          var marker12 = new AMap.Marker({
            position: position12,
            // 将 html 传给 content
            content: markerContent_10,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "西安"
          });
          this.map.add(marker12);

          var position13 = new AMap.LngLat(117.30983, 39.71755);//天津
          var marker13 = new AMap.Marker({
            position: position13,
            // 将 html 传给 content
            content: markerContent_11,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "天津"
          });
          this.map.add(marker13);

          var position14 = new AMap.LngLat(116.3912757, 39.906217);//北京
          var marker14 = new AMap.Marker({
            position: position14,
            // 将 html 传给 content
            content: markerContent_12,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "北京"
          });
          this.map.add(marker14);

          var position15 = new AMap.LngLat(113.2644, 23.1291);//广州
          var marker15 = new AMap.Marker({
            position: position15,
            // 将 html 传给 content
            content: markerContent_13,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "广州"
          });
          this.map.add(marker15);

          var position16 = new AMap.LngLat(112.9388, 28.2282);//长沙
          var marker16 = new AMap.Marker({
            position: position16,
            // 将 html 传给 content
            content: markerContent_14,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "长沙"
          });
          this.map.add(marker16);

          var position17 = new AMap.LngLat(107.2903, 26.8447);//贵州
          var marker17 = new AMap.Marker({
            position: position17,
            // 将 html 传给 content
            content: markerContent_15,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "贵州"
          });
          this.map.add(marker17);

          var position18 = new AMap.LngLat(87.6168, 43.8256); //乌鲁木齐
          var marker18 = new AMap.Marker({
            position: position18,
            // 将 html 传给 content
            content: markerContent_16,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "乌鲁木齐"
          });
          this.map.add(marker18);

          var position19 = new AMap.LngLat(119.2965, 26.0745);//福州
          var marker19 = new AMap.Marker({
            position: position19,
            // 将 html 传给 content
            content: markerContent_17,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "福州"
          });
          this.map.add(marker19);

          var position20 = new AMap.LngLat(118.4277477, 31.3536127);//芜湖
          var marker20 = new AMap.Marker({
            position: position20,
            // 将 html 传给 content
            content: markerContent_18,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "芜湖"
          });
          this.map.add(marker20);


          // 合资车
          var position19 = new AMap.LngLat(121.6282945, 38.9181714);//大连
          var marker19 = new AMap.Marker({
            position: position19,
            // 将 html 传给 content
            content: markerContent_19,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "大连"
          });
          this.map.add(marker19);

          var position20 = new AMap.LngLat(126.911, 45.7545);//哈尔滨
          var marker20 = new AMap.Marker({
            position: position20,
            // 将 html 传给 content
            content: markerContent_20,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "哈尔滨"
          });
          this.map.add(marker20);

          var position21 = new AMap.LngLat(111.1950469, 40.2758774);//呼和浩特
          var marker21 = new AMap.Marker({
            position: position21,
            // 将 html 传给 content    
            content: markerContent_21,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "呼和浩特"
          });
          this.map.add(marker21);

          var position22 = new AMap.LngLat(103.8318566, 36.0620781);//兰州
          var marker22 = new AMap.Marker({
            position: position22,
            // 将 html 传给 content    
            content: markerContent_22,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "兰州"
          });
          this.map.add(marker22);

          var position23 = new AMap.LngLat(109.4239676, 24.3284746);//柳州
          var marker23 = new AMap.Marker({
            position: position23,
            // 将 html 传给 content    
            content: markerContent_23,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "柳州"
          });
          this.map.add(marker23);

          var position24 = new AMap.LngLat(121.5722179, 29.8040075);//宁波
          var marker24 = new AMap.Marker({
            position: position24,
            // 将 html 传给 content    
            content: markerContent_24,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "宁波"
          });
          this.map.add(marker24);

          var position25 = new AMap.LngLat(121.3912291, 31.2513263);//上海
          var marker25 = new AMap.Marker({
            position: position25,
            // 将 html 传给 content    
            content: markerContent_25,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "上海"
          });
          this.map.add(marker25);

          var position26 = new AMap.LngLat(123.3502179, 41.7989084);//沈阳
          var marker26 = new AMap.Marker({
            position: position26,
            // 将 html 传给 content    
            content: markerContent_26,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "沈阳"
          });
          this.map.add(marker26);

          var position27 = new AMap.LngLat(114.5245739, 38.0061728);//石家庄
          var marker27 = new AMap.Marker({
            position: position27,
            // 将 html 传给 content    
            content: markerContent_27,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "石家庄"
          });
          this.map.add(marker27);

          var position28 = new AMap.LngLat(121.3943367, 37.533762);//烟台
          var marker28 = new AMap.Marker({
            position: position28,
            // 将 html 传给 content    
            content: markerContent_28,
            // 以 icon 的 [center bottom] 为原点
            offset: new AMap.Pixel(-13, -30),
            title: "烟台"
          });
          this.map.add(marker28);

          var that = this;
          AMap.Event.addListener(marker1, "click", function (e) {
            var selected = "0";
            that.$router.replace({ path: '/index/chargeOperation/healthEvaluation/stationHealth/stationHealth', query: { selected: selected } })
          });
          AMap.Event.addListener(marker2, "click", function (e) {
            var selected = "1";
            that.$router.replace({ path: '/index/chargeOperation/healthEvaluation/stationHealth/stationHealth', query: { selected: selected } })
          });
          AMap.Event.addListener(marker3, "click", function (e) {
            var selected = "2";
            that.$router.replace({ path: '/index/chargeOperation/healthEvaluation/stationHealth/stationHealth', query: { selected: selected } })
          });
          AMap.Event.addListener(marker4, "click", function (e) {
            var selected = "3";
            that.$router.replace({ path: '/index/chargeOperation/healthEvaluation/stationHealth/stationHealth', query: { selected: selected } })
          });
          AMap.Event.addListener(marker5, "click", function (e) {
            var selected = "4";
            that.$router.replace({ path: '/index/chargeOperation/healthEvaluation/stationHealth/stationHealth', query: { selected: selected } })
          });
          AMap.Event.addListener(marker6, "click", function (e) {
            var selected = "5";
            that.$router.replace({ path: '/index/chargeOperation/healthEvaluation/stationHealth/stationHealth', query: { selected: selected } })
          });
          AMap.Event.addListener(marker7, "click", function (e) {
            var selected = "6";
            that.$router.replace({ path: '/index/chargeOperation/healthEvaluation/stationHealth/stationHealth', query: { selected: selected } })
          });
          AMap.Event.addListener(marker8, "click", function (e) {
            var selected = "7";
            that.$router.replace({ path: '/index/chargeOperation/healthEvaluation/stationHealth/stationHealth', query: { selected: selected } })
          });
          AMap.Event.addListener(marker9, "click", function (e) {
            var selected = "8";
            that.$router.replace({ path: '/index/chargeOperation/healthEvaluation/stationHealth/stationHealth', query: { selected: selected } })
          });
          AMap.Event.addListener(marker10, "click", function (e) {
            var selected = "9";
            that.$router.replace({ path: '/index/chargeOperation/healthEvaluation/stationHealth/stationHealth', query: { selected: selected } })
          });
          AMap.Event.addListener(marker11, "click", function (e) {
            var selected = "10";
            that.$router.replace({ path: '/index/chargeOperation/healthEvaluation/stationHealth/stationHealth', query: { selected: selected } })
          });

        })
        .catch((e) => {
          console.log(e);
        });
    },
  },
  //生命周期 - 创建完成（可以访问当前this实例）
  created() { },
  //生命周期 - 挂载完成（可以访问DOM元素）
  mounted() {
    setTimeout(() => {
      this.initMap();
    }, 1000);
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
<style lang="scss" scoped>
//@import url(); 引入公共css类
.healthOverview {
  #container {
    position: absolute;
    top: 12%;
    left: 0;
    height: 88%;
    width: 100%;
  }

  .topDiv {
    position: absolute;
    top: 0;
    left: 0;
    height: 12%;
    width: 100%;
    background-color: #fff;

    .top1 {
      position: absolute;
      top: 0;
      left: 0;
      height: 100%;
      width: 20%;
      color: #00bbee;

      #pic1 {
        background-image: url("../../../../../../static/img/chargeOperation/cdzhan.png");
        background-repeat: no-repeat;
        background-size: cover;
      }
    }

    .top2 {
      position: absolute;
      top: 0;
      left: 20%;
      height: 100%;
      width: 20%;
      color: #00bbee;

      #pic2 {
        background-image: url("../../../../../../static/img/chargeOperation/cdzhuang.png");
        background-repeat: no-repeat;
        background-size: cover;
      }
    }

    .top3 {
      position: absolute;
      top: 0;
      left: 40%;
      height: 100%;
      width: 20%;
      color: #00bbee;

      #pic3 {
        background-image: url("../../../../../../static/img/chargeOperation/jiankang.png");
        background-repeat: no-repeat;
        background-size: cover;
      }
    }

    .top4 {
      position: absolute;
      top: 0;
      left: 60%;
      height: 100%;
      width: 20%;
      color: #00bbee;

      #pic4 {
        background-image: url("../../../../../../static/img/chargeOperation/yajiankang.png");
        background-repeat: no-repeat;
        background-size: cover;
      }
    }

    .top5 {
      position: absolute;
      top: 0;
      left: 80%;
      height: 100%;
      width: 20%;
      color: #00bbee;

      #pic5 {
        background-image: url("../../../../../../static/img/chargeOperation/guzhang.png");
        background-repeat: no-repeat;
        background-size: cover;
      }
    }

    .pic {
      position: absolute;
      top: 22%;
      left: 25%;
      height: 65%;
      width: 20%;
    }

    .num {
      position: absolute;
      top: 25%;
      left: 50%;
      height: 50%;
      width: 50%;
    }

    .text {
      position: absolute;
      top: 55%;
      left: 50%;
      height: 50%;
      width: 50%;
    }
  }
}
</style>
