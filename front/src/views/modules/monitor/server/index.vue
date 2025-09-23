<!--  -->
<template>
  <div class="container">
    <div class="collapseGroup first">
      <el-collapse v-model="activeNames1" class="collapse children">
        <el-collapse-item title="CPU" name="1">
          <ul>
            <li>
              <span>属性</span>
              <span>值</span>
            </li>
            <template>
              <li v-for="item in cpuArr" :key="item.label">
                <span>{{ item.label }}</span>
                <span>{{ item.value }}</span>
              </li>
            </template>
          </ul>
        </el-collapse-item>
      </el-collapse>
      <el-collapse v-model="activeNames2" class="collapse children">
        <el-collapse-item title="内存" name="1">
          <ul>
            <li>
              <span>属性</span>
              <span>内存</span>
              <span>JVM</span>
            </li>
            <template>
              <li v-for="item in storageArr" :key="item.label">
                <span>{{ item.label }}</span>
                <span>{{ item.value1 }}</span>
                <span>{{ item.value2 }}</span>
              </li>
            </template>
          </ul>
        </el-collapse-item>
      </el-collapse>
    </div>
    <div class="collapseGroup second">
      <el-collapse v-model="activeNames3" class="collapse children">
        <el-collapse-item title="服务器信息" name="1">
          <ul>
            <li>
              <span>服务器名称</span>
              <span>zhny</span>
              <span>操作系统</span>
              <span>Windows 10</span>
            </li>
            <template>
              <li v-for="item in serverArr" :key="item.label">
                <span>{{ item.label }}</span>
                <span>{{ item.value1 }}</span>
                <span>{{ item.value2 }}</span>
                <span>{{ item.value3 }}</span>
              </li>
            </template>
          </ul>
        </el-collapse-item>
      </el-collapse>
    </div>
    <div class="collapseGroup third">
      <el-collapse v-model="activeNames4" class="collapse children">
        <el-collapse-item title="服务器信息" name="1">
          <ul>
            <li>
              <span>Java名称</span>
              <span>Java HotSpot(TM) 64-Bit Server VM</span>
              <span>Java版本</span>
              <span>1.8.0_181</span>
            </li>
            <template>
              <li v-for="item in javaArr" :key="item.label">
                <span>{{ item.label }}</span>
                <span>{{ item.value1 }}</span>
                <span>{{ item.value2 }}</span>
                <span>{{ item.value3 }}</span>
              </li>
            </template>
          </ul>
        </el-collapse-item>
      </el-collapse>
    </div>
    <div class="collapseGroup four">
      <el-collapse v-model="activeNames5" class="collapse children">
        <el-collapse-item title="磁盘状态" name="1">
          <ul>
            <li>
              <span>盘符路径</span>
              <span>文件系统</span>
              <span>盘符类型</span>
              <span>总大小</span>
              <span>可用大小</span>
              <span>已用大小</span>
              <span>已用百分比</span>
            </li>
            <template>
              <li v-for="item in statusArr" :key="item.label">
                <span>{{ item.label }}</span>
                <span>{{ item.value1 }}</span>
                <span>{{ item.value2 }}</span>
                <span>{{ item.value3 }}</span>
                <span>{{ item.value4 }}</span>
                <span>{{ item.value5 }}</span>
                <span>{{ item.value6 }}</span>
              </li>
            </template>
          </ul>
        </el-collapse-item>
      </el-collapse>
    </div>
  </div>
</template>

<script>
//这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）
//例如：import 《组件名称》 from '《组件路径》';

export default {
  //import引入的组件需要注入到对象中才能使用
  components: {},
  data() {
    //这里存放数据
    return {
      activeNames1: "1",
      activeNames2: "1",
      activeNames3: "1",
      activeNames4: "1",
      activeNames5: "1",
      cpuArr: [],
      storageArr: [],
      serverArr: [],
      javaArr: [
        {
          label: "启动时间",
          value1: "2022-09-07 09:32:45",
          value2: "运行时长",
          value3: "0天4小时36分钟",
        },
        {
          label: "安装路径",
          value1: "C:\Program Files\Java\jdk1.8.0_181\jre",
          value2: "",
        },
        {
          label: "项目路径",
          value1: "D:\IDEA_WORKSPACE\pec-Sepa\pec-Sepa",
          value2: "",
        },
      ],
      statusArr: [
        {
          label: "'C:'",
          value1: "NTFS",
          value2: "本地固定磁盘 (C:)",
          value3: "400.0 GB",
          value4: "340.4 GB",
          value5: "59.6 GB",
          value6: "14.89%",
        },
        {
          label: "'D:'",
          value1: "NTFS",
          value2: "本地固定磁盘 (D:)",
          value3: "400.0 GB",
          value4: "340.4 GB",
          value5: "59.6 GB",
          value6: "14.89%",
        },
      ],
    };
  },
  //监听属性 类似于data概念
  computed: {},
  //监控data中的数据变化
  watch: {},
  //方法集合
  methods: {
    // 获取数据
    getData() {

      this.$http({
        url: this.$http.adornUrl("/monitor/server"),
        method: "GET",
        params: this.$http.adornParams({}),
      }).then((res) => {
        const server = res.data;
        const cpu = server.cpu;
        this.cpuArr = [
          {
            label: "核心数",
            value: cpu.cpuNum,
          },
          {
            label: "用户使用率",
            value: cpu.used + '%',
          },
          {
            label: "系统使用率",
            value: cpu.sys + '%',
          },
          {
            label: "当前空闲率",
            value: cpu.free + '%',
          },
        ];
        this.storageArr = [
          {
            label: "总内存",
            value1: server.mem.total ? (server.mem.total + 'G') : '0GB',
            value2: server.jvm.total ? (server.jvm.total + 'M') : '0MB',
          },
          {
            label: "已用内存",
            value1: server.mem.used ? (server.mem.used + 'G') : '0GB',
            value2: server.jvm.used ? (server.jvm.used + 'M') : '0MB',
          },
          {
            label: "剩余内存",
            value1: server.mem.free ? (server.mem.free + 'G') : '0GB',
            value2: server.jvm.free ? (server.jvm.free + 'M') : '0MB',
          },
          {
            label: "使用率",
            value1: server.mem.usage + '%',
            value2: server.jvm.usage + "%"
          }
        ];
        this.serverArr = [
          {
            label: server.sys.computerName ? server.sys.computerName : 'pec',
            value1: server.sys.osName ? server.sys.osName : 'Linux',
            value2: server.sys.computerIp ? server.sys.computerIp : '127.0.0.1',
            value3: server.sys.osArch ? server.sys.osArch : 'amd64',
          }
        ]
      });
    },
  },
  //生命周期 - 创建完成（可以访问当前this实例）
  created() { },
  //生命周期 - 挂载完成（可以访问DOM元素）
  mounted() {
    this.getData();
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
.collapseGroup {
  margin-bottom: 20px;
}

.first {
  display: flex;
  justify-content: space-between;

  .children {
    width: 49%;
  }
}

.collapse {
  border-top: #0c082e;
  border-bottom: none;

  .el-collapse-item {
    background: #000;

    ul>li {
      display: flex;
      justify-content: space-between;
      padding: 10px 20px;
      border-bottom: 1px solid #12665d;

      span {
        width: 50%;
      }
    }

    ul>li:hover {
      cursor: pointer;
      background: #167672;
    }
  }
}
</style>
<style scoped>
.collapse>>>.el-collapse-item__header {
  background: #123c38;
  color: #fff;
  padding-left: 13px;
  font-weight: 700;
  font-size: 16px;
}

.collapse>>>.el-collapse-item__wrap {
  background: #153533;
  /* color: #fff; */
  border-bottom: 1px solid #0f4e54;
}

.collapse>>>.el-collapse-item__content {
  color: #fff;
  padding-bottom: 0px;
}
</style>
