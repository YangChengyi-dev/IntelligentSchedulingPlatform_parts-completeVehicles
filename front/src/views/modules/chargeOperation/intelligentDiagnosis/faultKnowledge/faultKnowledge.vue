<!--  -->
<template>
    <div class="faultKnowledge">
      <div class="title">故障说明</div>
      <div class="top">
        <input type="text" class="search" />
      </div>
      <div class="box1">
        <div class="text1">动力电池</div>
        <div class="text2">0.5C倍率下,温升初期速率约1.7℃/min。</div>
        <div class="text3">1C倍率下,电池过充至约130%后,电池温度超过700℃。</div>
        <!-- <div class="text4">交流输入接触器粘连故障</div> -->
        <el-button icon="el-icon-search" size="small" class="button1" @click="more_one"
            >更多</el-button>
      </div>
      <div class="box2">
        <div class="text1">动力电池</div>
        <div class="text2">T1在SOC变化过程在50℃-100℃范围内波动</div>
        <div class="text3">T2随SOC的增加而降低,容易进入热失控</div>
        <div class="text4">T3随SOC的增加而增加</div>
        <el-button icon="el-icon-search" size="small" class="button1" @click="more_two"
            >更多</el-button>
      </div>
      <div class="box3">
        <div class="text1">动力电池</div>
        <div class="text2">过充电到110-130%的电池容量没有明显衰减</div>
        <div class="text3">过充电到140-160%的电池容量均发生了衰减。</div>
        <div class="text4">电池的放电容量衰减情况比充电容量衰减情况严重</div>
        <el-button icon="el-icon-search" size="small" class="button1" @click="more_three"
            >更多</el-button>
      </div>
      <!-- <div class="box4">
        <div class="text1">电气原件</div>
        <div class="text2">交流输入断路器跳闸故障</div>
        <div class="text3">避雷器动作预警</div>
        <div class="text4">交流输入接触器粘连故障</div>
        <el-button icon="el-icon-search" size="small" class="button1"
            >更多</el-button>
      </div> -->
      <div class="box5">
        <div class="text1">充电设备（充电电流）</div>
        <div class="text2">当线路正常工作时，系统的剩余电流约等于零</div>
        <div class="text3">发生漏电时，零序电流互感器可测量出剩余电流</div>
        <div class="text4">交流侧输入电流超动作电流,比较环节KA有输出</div>
        <el-button icon="el-icon-search" size="small" class="button1" @click="more_five"
            >更多</el-button>
      </div>
      <div class="box6">
        <div class="text1">充电设备（充电电压）</div>
        <div class="text2">当充电桩输出过压后</div>
        <div class="text3">接触器断开时间为1.153s</div>
        <div class="text4">超过标准规定的1s</div>
        <el-button icon="el-icon-search" size="small" class="button1" @click="more_six"
            >更多</el-button>
      </div>
      <!--结果展示-->
          <el-dialog :visible.sync="firstShow" customClass="customWidth">
              <el-row :gutter="20" class="result-list">
                  <el-col :span="24">
            <div>
              <h1>动力电池</h1>
            </div>
            <div class="first_one">
              <img src="../../../../../assets/faultKnowledge/Power battery First One.jpg" style="width:100%"/>
              <sapn style="margin-left:25%;">三元锂电池以0.5C倍率过充</sapn>
            </div>
                      
                      <div class="first_second">
              <img src="../../../../../assets/faultKnowledge/Power battery First Two.jpg" style="width:95%"/>
            
              <span style="margin-left:25%">三元锂电池以1C倍率过充</span>
            </div>
  
            <div class="text">
              <span style="float:right;margin-right: 18.8%;margin-top: 5%;">0.5C倍率下，电池SOC超过100%后即出现明显温升，温升初期速率约1.7℃/min。</span>
              <span style="float:right;margin-right: 10%;">1C倍率下，电池过充至约130%后，出现温度骤升并发生剧烈热失控，电池温度超过700℃。</span>
  
            </div>
            
                  </el-col>
              </el-row>
          </el-dialog>
  
      <!--结果展示-->
          <el-dialog :visible.sync="secondShow" customClass="customWidth">
              <el-row :gutter="20" class="result-list">
                  <el-col :span="24">
            <div>
              <h1>动力电池</h1>
            </div>
                      <img src="../../../../../assets/faultKnowledge/Power battery Second.jpg" style="margin-left:10%;width:600px"/>
            <span style="margin-left:30%">三元锂电池在不同SOC下的热耐受性研究</span>
            <div>
              <span style="float:left;margin-left: 7%;margin-top: 3%;">T1（自加热温度）在SOC变化过程中基本保持不变，在50℃-100℃范围内波动；</span>
              <span style="float:left;margin-left: 7%;">T2（热失控起始温度）随SOC的增加而降低，表征电池随着内部电量的累积，更容易进入热失控开始阶段；</span>      
              <span style="float:left;margin-left: 7%;">T3随SOC的增加而增加；</span> 
              <span style="float:left;margin-left: 7%;">T2 - T3过程中的最大温升速率随SOC的增加而增加，表征电池内部电量的累积，热失控释能的速度更快。</span>
              
            </div>
                  </el-col>
              </el-row>
          </el-dialog>
  
      <!--结果展示-->
          <el-dialog :visible.sync="thirdShow" customClass="customWidth">
              <el-row :gutter="20" class="result-list">
                  <el-col :span="24">
            <div>
              <h1>动力电池</h1>
            </div>
            <div class="first_one">
              <img src="../../../../../assets/faultKnowledge/Power battery Third One.jpg" style="width:100%"/>
              <span style="margin-left:20%">不同程度过充电电池充电容量变化情况</span>
            </div>
            <div class="first_second">
              <img src="../../../../../assets/faultKnowledge/Power battery Third Two.jpg" style="width:90%"/>
              <span style="margin-left:20%">不同程度过充电电池放电容量变化情况</span>
            </div>
                      <div class="text">
              <span style="float:left;margin-left: 5%;margin-top: 5%;">从不同程度过充电电池充放电容量变化情况图来看，过充电到SOC=110%，120%，130%的电池充放电容量并没有发生明显衰减，过充电到SOC=140%，150%，160%的电池充放电容量均发生了衰减。</span>
              <span style="float:left;margin-left: 5%;">同时还发现，电池的放电容量衰减情况比充电容量衰减情况严重。</span>
            </div>
                      
                  </el-col>
              </el-row>
          </el-dialog>
  
      <!--结果展示-->
          <el-dialog :visible.sync="fifthShow" customClass="customWidth">
              <el-row :gutter="20" class="result-list">
                  <el-col :span="24">
            <div>
              <h1>充电设备</h1>
            </div>
                      <img src="../../../../../assets/faultKnowledge/Charging equipment First One.jpg" style="width:60%;margin-left: 20%;"/>
                      <span style="margin-left:40%">过载保护电流特性曲线</span>
            <div>
              <span style="float:left;margin-top:3%">当线路正常工作时，系统的剩余电流约等于零；当线路中发生漏电时，从零序电流互感器中可以测量出剩余电流。</span>
            </div>
                  </el-col>
              </el-row>
          </el-dialog>
  
      <!--结果展示-->
          <el-dialog :visible.sync="sixthShow" customClass="customWidth">
              <el-row :gutter="20" class="result-list">
                  <el-col :span="24">
            <div>
              <h1>充电设备</h1>
            </div>
            <div class="last">
              <img src="../../../../../assets/faultKnowledge/Charging equipment Second One.jpg" />
              <span style="margin-left:25%;margin-top: 5%;">输入过压保护</span>
            </div>
            <div class="last">
              <img src="../../../../../assets/faultKnowledge/Charging equipment Second Three.jpg"/>
              <span style="margin-left:25%;margin-top: 5%;">输出过压保护</span>
            </div>
            <div class="last" style="margin-top:5%">
              <img src="../../../../../assets/faultKnowledge/Charging equipment Second Two.jpg"/>
              <span style="margin-left:25%;margin-top: 5%;">输出过压时接触器断开</span>
            </div>			
            <div>
              <span style="float:left;width:40%;margin-top:7%;margin-left:2%">
                充电桩在检测到电压故障后，充电控制器向BMS发送CST报文，并延时判定未收到BST报文后才进入结束充电阶段，因此导致下发充电功率模块关机指令延长，造成过压后充电桩未立即停机。当充电桩输出过压后，接触器断开时间为1.153s，超过标准规定的1s。
              </span>
            </div>		           
                  </el-col>
              </el-row>
          </el-dialog>
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
        firstShow:false,
        secondShow:false,
        thirdShow:false,
        fifthShow:false,
        sixthShow:false
      };
    },
    //监听属性 类似于data概念
    computed: {},
    //监控data中的数据变化
    watch: {},
    //方法集合
    methods: {
      more_one(){
        this.firstShow = !this.firstShow;
      },
      more_two(){
        this.secondShow = !this.secondShow;
      },
      more_three(){
        this.thirdShow = !this.thirdShow;
      },
      more_five(){
        this.fifthShow = !this.fifthShow ;
      },
      more_six(){
        this.sixthShow = !this.sixthShow;
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
  <style lang="scss" scoped>
  //@import url(); 引入公共css类
  .faultKnowledge {
    .title {
      position: absolute;
      top: 5%;
      left: 0%;
      width: 100%;
      height: 10%;
      color: #00bbee;
      font-size: 20px;
      font-weight: bold;
      text-align: center;
    }
    .top {
      position: absolute;
      top: 10%;
      left: 20%;
      width: 60%;
      .search {
        background: url("/static/img/chargeOperation/searchbox_button.png")
          no-repeat 5px center;
        padding-left: 40px;
        color: #00bbee;
        display: block;
        width: 100%;
        height: 38px;
        line-height: 1.3;
        border-width: 1px;
        border-style: solid;
        border-radius: 2px;
      }
    }
    .first_one {
      width: 50%;
      float: left;
    }
    .first_second {
      width: 50%;
      float: left;
    }
    .last {
      width: 50%;
      float: left;
    }
    .box1 {
      position: absolute;
      top: 40%;
      left: 1%;
      width: 24%;
      height: 20%;
      background-color: #323c41;
    }
    .box2 {
      position: absolute;
      top: 40%;
      left: 35%;
      width: 24%;
      height: 20%;
      background-color: #323c41;
    }
    .box3 {
      position: absolute;
      top: 40%;
      left: 71%;
      width: 24%;
      height: 20%;
      background-color: #323c41;
    }
    .box4 {
      position: absolute;
      top: 40%;
      left: 76%;
      width: 23%;
      height: 20%;
      background-color: #323c41;
    }
    .box5 {
      position: absolute;
      top: 62%;
      left: 14%;
      width: 24%;
      height: 20%;
      background-color: #323c41;
    }
    .box6 {
      position: absolute;
      top: 62%;
      left: 54%;
      width: 24%;
      height: 20%;
      background-color: #323c41;
    }
    .text1 {
      position: absolute;
      top: 5%;
      left: 2%;
      color: #00bbee;
      font-size: 16px;
    }
    .text2 {
      position: absolute;
      top: 25%;
      left: 15%;
      color: #00bbee;
      font-size: 12px;
    }
    .text3 {
      position: absolute;
      top: 40%;
      left: 15%;
      color: #00bbee;
      font-size: 12px;
    }
    .text4 {
      position: absolute;
      top: 55%;
      left: 15%;
      color: #00bbee;
      font-size: 12px;
    }
    .button1 {
      position: absolute;
      top: 70%;
      left: 3%;
      background-color: #00bbee;
      border: 1px solid #00bbee;
    }
  }
  </style>
  