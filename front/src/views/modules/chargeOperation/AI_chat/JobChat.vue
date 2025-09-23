<template>
  <div class="ui_guide">
    <el-tooltip
      class="item"
      effect="dark"
      content="智能助手“小邮”"
      placement="top-start"
    >
      <img
        src="../../../../../static/img/AI2.png"
        @mousedown="startImgDrag"
        alt="机器人"
        class="robot"
        v-show="!change"
        @click="changeL"
        :style="{ top: `${imageY}px` }"
      />
    </el-tooltip>
    <div
      class="chat"
      :style="{ left: `${chatX}px`, top: `${chatY}px` }"
      v-show="change"
      :key="change"
    >
      <div class="title" @mousedown="startChatDrag">
        <span
          ><i class="iconfont el-icon-s-unfold" @click="openPersonalCenter"></i
        ></span>
        <span
          >智能助手"小邮"
          <el-dropdown style="color:#fff">
            <i class="iconfont el-icon-arrow-down"></i>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item icon="el-icon-plus" @click.native="createChat"
                >新建对话</el-dropdown-item
              >
              <el-dropdown-item icon="el-icon-delete" @click.native="clearChat"
                >清空对话</el-dropdown-item
              >
            </el-dropdown-menu>
          </el-dropdown>
        </span>
        <span><i class="iconfont el-icon-minus" @click="changeL"></i></span>
      </div>
      <!-- 个人中心设置 -->
      <el-drawer
        class="drawer"
        :visible.sync="drawer"
        direction="ltr"
        style="position: absolute;"
        size="50%"
        :modal-append-to-body="false"
      >
        <span class="drawer-title" slot="title">
          <img
            class="circle-image"
            src="../../../../../static/img/customer.png"/>个人中心<i
            class="el-icon-arrow-right"
          ></i
        ></span>
        <div class="drawer-content">
          <div class="history-title">
            对话历史<i class="el-icon-pie-chart"></i>
          </div>
          <div v-if="!historyList.length" class="no-history">
            <img src="../../../../../static/img/empty.jpg" />暂无历史对话
          </div>
          <div
            v-else
            v-for="(item, index) in historyList"
            :key="index"
            class="content-list"
          >
            <div class="content-body">
              <div class="content-item" @click="changeChat(index)">
                <div class="content-text">{{ item.content[1].content }}</div>
                <div
                  style="font-size: 12px;display: flex;justify-content: space-between;padding: 0 4%;color:#bbbebb;"
                >
                  <span>{{ item.name }}</span>
                  <span>{{ item.time }}</span>
                </div>
              </div>
              <i class="el-icon-delete" @click="deleteChat(index)"></i>
            </div>
          </div>
        </div>
      </el-drawer>

      <div style="height: calc(100% - 100px);width: 100%;">
        <ul id="chat-box" class="text" ref="messageList">
          <li
            v-for="(messageItem, index) in messageList"
            :key="index"
            :class="[messageItem.type === 'sent' ? 't2' : 't1']"
          >
            <img
              src="../../../../../static/img/AI2-li.png"
              alt=""
              v-show="messageItem.type !== 'sent'"
            />
            <div class="txt" v-if="messageItem.isImage">
              <img
                :src="messageItem.content"
                alt="Image"
                class="image-message"
                style="width: 70px;height: 70px;"
              />
            </div>
            <div class="txt" v-else v-html="messageItem.content"></div>
            <img
              src="../../../../../static/img/customer.png"
              alt=""
              v-show="messageItem.type === 'sent'"
            />
          </li>
        </ul>
      </div>
      <div class="cont">
        <input
          type="text"
          placeholder="在这里输入文字"
          class="inp"
          v-model="message"
          @keydown.enter="sendMessage"
          :disabled="loading"
        />
        <input
          type="button"
          value="发送"
          @click="sendMessage"
          class="send"
          :disabled="loading"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
// 导入json文件

export default {
  //import引入的组件需要注入到对象中才能使用
  components: {},
  data() {
    return {
      loading: false,
      change: false,
      frist: 0,
      message: "",
      messageList: [
        {
          type: "received",
          content: "您好，我是智能助手小邮，有任何问题可以向我提问哦!",
          isImage: false
        }
      ],
      ContextMessage: [],
      imageY: 380,
      dragging: false,

      chatX: 800, // 文本框的初始位置
      chatY: 175,

      drawer: false,
      historyList: []
    };
  },
  //监听属性 类似于data概念
  computed: {},
  //监控data中的数据变化
  watch: {
    //messageList() {
    // 每当 messageList 更新时，滚动到最底部
    //  this.$nextTick(() => {
    //    const messageList = this.$refs.messageList;
    //    messageList.scrollTop = messageList.scrollHeight;
    //  });
    //}
  },
  //方法集合
  methods: {
    changeL() {
      this.change = !this.change;
      this.$nextTick(() => {
        const messageList = this.$refs.messageList;
        messageList.scrollTop = messageList.scrollHeight;
      });
    },
    sendMessage() {
      if (this.message.value === "") {
        this.$message({
          message: "输入内容不能为空!!!",
          type: "error"
        });
        return;
      }
      const sentMessage = {
        type: "sent",
        content: this.message,
        isImage: false
      };
      this.messageList.push(sentMessage);
      this.generateContext();
      this.$nextTick(() => {
        const messageList = this.$refs.messageList;
        messageList.scrollTop = messageList.scrollHeight;
      });
      this.loading = !this.loading;
      if (this.message.includes("图")) {
        this.submitPhoto();
      } else {
        this.sendChat();
      }
      //this.submitChat();
      this.message = "";
    },
    //将聊天内容传到后端
    submitChat() {
      let params = {
        chat: this.message
      };
      axios({
        url: this.baseurl + "/part/ai_chat", // 替换为实际的后端接口
        method: "POST",
        data: {
          chat: params.chat
        }
      }).then(res => {
        const data = res.data.data;
        // 判断返回的 data 是否为图片 URL（简单根据后缀判断）
        let messageContent = data;
        let isImage = false;
        const imageExtensions = [
          ".jpg",
          ".jpeg",
          ".png",
          ".gif",
          ".bmp",
          ".webp"
        ];
        if (imageExtensions.some(ext => data.endsWith(ext))) {
          isImage = true;
          messageContent = data; // 图片 URL
        }
        console.log(isImage);
        const receivedMessage = {
          type: "received",
          content: messageContent,
          isImage: isImage
        }; // 添加一个字段标识该消息是否为图片
        this.messageList.push(receivedMessage);
        this.$nextTick(() => {
          const messageList = this.$refs.messageList;
          messageList.scrollTop = messageList.scrollTop + 80;
        });
        this.loading = !this.loading;
      });
    },
    submitPhoto() {
      let params = {
        chat: this.message
      };
      axios({
        url: this.baseurl + "/part/ai_photo", // 替换为实际的后端接口
        method: "POST",
        data: {
          chat: params.chat
        }
      }).then(res => {
        const data = res.data.data;
        // 判断返回的 data 是否为图片 URL（简单根据后缀判断）
        let messageContent = data;
        let isImage = false;
        const imageExtensions = [
          ".jpg",
          ".jpeg",
          ".png",
          ".gif",
          ".bmp",
          ".webp"
        ];
        if (imageExtensions.some(ext => data.endsWith(ext))) {
          isImage = true;
          messageContent = data; // 图片 URL
        }
        const receivedMessage = {
          type: "received",
          content: messageContent,
          isImage: isImage
        }; // 添加一个字段标识该消息是否为图片
        this.messageList.push(receivedMessage);
        this.$nextTick(() => {
          const messageList = this.$refs.messageList;
          messageList.scrollTop = messageList.scrollTop + 80;
        });
        this.loading = !this.loading;
      });
    },
    async sendChat() {
      // 给后端发送POST请求
      const response = await fetch(
        "https://open.bigmodel.cn/api/paas/v4/chat/completions",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization:
              "Bearer d568090a61c7da8a7f4b1f668cbee364.iPnj21ZxZ6C7SFIq"
          },
          body: JSON.stringify({
            model: "glm-4",
            messages: this.ContextMessage,
            stream: true
          })
        }
      );
      // 检查是否返回内容
      if (!response.ok || !response.body) {
        console.error("网络错误");
        this.messageList.push({
          type: "received",
          content: "网络出现问题，抱歉！",
          isImage: false
        });
        return;
      }
      // 创建一个读取器来读取流
      const reader = response.body.getReader();
      let decoder = new TextDecoder("utf-8");
      this.messageList.push({
        type: "received",
        content: "  ",
        isImage: false
      });

      while (true) {
        // 读取流中的下一个数据块
        const { value, done } = await reader.read();
        if (done) {
          break; // 流结束，可以在这里处理最后的消息
        }
        // 将读取到的数据块解码为字符串
        let receivedMessage = decoder.decode(value, { stream: true });
        // 尝试解析JSON对象
        const messages = receivedMessage.split("\n\n");
        // receivedMessage = messages.pop(); // 保存最后一个可能不完整的消息
        messages.forEach(message => {
          if (message.startsWith("data: ") && message !== "data: [DONE]") {
            message = message.replace("data: ", "");
            message = JSON.parse(message);
            let answer = message.choices[0].delta.content;
            this.messageList[this.messageList.length - 1].content += answer;
          }
          this.$nextTick(() => {
            // 确保DOM更新后滚动到底部
            this.scrollToBottom();
          });
        });
      }
      this.messageList[
        this.messageList.length - 1
      ].content = this.parseMarkdown(
        this.messageList[this.messageList.length - 1].content
      );
      this.loading = !this.loading;
    },

    scrollToBottom() {
      const chatBox = document.getElementById("chat-box");
      chatBox.scrollTop = chatBox.scrollHeight;
    },

    // 生成上下文消息
    generateContext() {
      // 跳过第一个消息（系统消息）
      const messages = this.messageList.slice(0);
      // 如果消息数量超过4条，只保留最后4条
      if (messages.length > 4) {
        messages.splice(0, messages.length - 4);
      }
      const newMessage = {
        type: "received", // 根据需求调整角色
        content:
          "你是智能助手小邮，负责为客户提供邮政方面的帮助，要热情回复用户的提问"
      };
      messages.unshift(newMessage); // 将新消息添加到数组的前面
      messages.forEach(message => {
        if (message.type === "received")
          this.ContextMessage.push({
            role: "assistant",
            content: message.content
          });
        else
          this.ContextMessage.push({ role: "user", content: message.content });
      });
    },

    // 拖拽机器人图片（将X周注销了，只能上下移动）
    startImgDrag(event) {
      event.preventDefault();
      this.dragging = true;
      const startY = event.pageY - this.imageY;

      const moveAt = pageY => {
        this.imageY = pageY - startY;
      };

      const onMouseMove = event => {
        if (this.dragging) {
          moveAt(event.pageY);
        }
      };

      const stopDrag = () => {
        this.dragging = false;
        document.removeEventListener("mousemove", onMouseMove);
        document.removeEventListener("mouseup", stopDrag);
      };

      document.addEventListener("mousemove", onMouseMove);
      document.addEventListener("mouseup", stopDrag);
    },

    // 拖拽聊天框
    startChatDrag(event) {
      event.preventDefault();
      this.dragging = true;
      const startX = event.pageX - this.chatX;
      const startY = event.pageY - this.chatY;

      const moveAt = (pageX, pageY) => {
        this.chatX = pageX - startX;
        this.chatY = pageY - startY;
      };

      const onMouseMove = event => {
        if (this.dragging) {
          moveAt(event.pageX, event.pageY);
        }
      };

      const stopDrag = () => {
        this.dragging = false;
        document.removeEventListener("mousemove", onMouseMove);
        document.removeEventListener("mouseup", stopDrag);
      };

      document.addEventListener("mousemove", onMouseMove);
      document.addEventListener("mouseup", stopDrag);
    },

    parseMarkdown(text) {
      // 简单的Markdown解析逻辑
      return (
        text
          // 转换标题
          .replace(/^# (.*?)$/gm, "<h1>$1</h1>")
          .replace(/^## (.*?)$/gm, "<h2>$1</h2>")
          .replace(/^### (.*?)$/gm, "<h3>$1</h3>")
          // 转换加粗
          .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
          // 转换斜体
          .replace(/__(.*?)__/g, "<em>$1</em>")
          .replace(/\*(.*?)\*/g, "<em>$1</em>")
          // 转换链接
          .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2">$1</a>')
          // 转换无序列表
          .replace(/^\*(.*?)$/gm, "<li>$1</li>")
          .replace(/<li>(.*?)<\/li>/g, "<ul><li>$1</li></ul>")
      );
      // 转换有序列表
      // .replace(/^(\d+)\. (.*?)$/gm, '<li>$2</li>')
      // .replace(/<li>(.*?)<\/li>/g, '<ol><li>$1</li></ol>');
    },

    // 创建新对话
    createChat() {
      this.saveChat();
      this.messageList = [
        {
          type: "received",
          content: "您好，我是智能助手小邮，有任何问题可以向我提问哦!"
        }
      ];
      this.$message.success("对话已创建");
    },

    // 清空对话
    clearChat() {
      this.messageList = [
        {
          type: "received",
          content: "您好，我是智能助手小邮，有任何问题可以向我提问哦!"
        }
      ];
      this.$message.success("对话已清空");
    },

    // 切换对话
    changeChat(index) {
      this.messageList = this.historyList[index].content;
      // console.log(index);
      this.drawer = false;
    },

    // 加载历史对话
    // async loadChat() {
    //   try {
    //     // 假设 data.json 文件位于 public 目录下
    //     const response = await fetch('/static/json/AiHistory.json');
    //     if (!response.ok) {
    //       throw new Error(`HTTP error! status: ${response.status}`);
    //     }
    //     const AiIHistory = await response.json();
    //     // 查找里面userInfo为"admin"的对象
    //     const adminHistory = AiIHistory.find(item => item.userInfo === "admin");
    //     if (this.historyList.length == 0) {
    //       // 如果存在这样的对象，则获取其history属性
    //       this.historyList = adminHistory ? adminHistory.history : [];
    //     }
    //   } catch (error) {
    //     console.error('Error fetching data:', error);
    //   }
    // },

    loadChat() {
      const AiIHistory = require("../../../../../static/json/AiHistory.json"); // 引入json文件
      // 查找里面userInfo为"admin"的对象
      const adminHistory = AiIHistory.find(item => item.userInfo === "admin");
      // 如果存在这样的对象，则获取其history属性
      this.historyList = adminHistory ? adminHistory.history : [];
    },

    // 将当前对话保存到历史记录中
    saveChat() {
      if (this.messageList.length == 1) return;
      let isSave = -1;
      // 通过比较historyList中每条记录中content的前三条是否一样来查看当前对话有没有保存过
      this.historyList.forEach((item, index) => {
        if (
          JSON.stringify(item.content.slice(0, 3)) ===
          JSON.stringify(this.messageList.slice(0, 3))
        ) {
          isSave = index;
        }
      });
      console.log(isSave == -1);
      if (isSave == -1) {
        console.log(this.historyList);
        // 如果没有保存过，则将当前对话保存到历史记录中
        this.historyList.push({
          name: "小邮",
          time: new Date().toLocaleString(),
          content: this.messageList
        });
        console.log(this.historyList);
      } else {
        // 如果保存过，则更新历史记录中的对应对话
        this.historyList[isSave].content = this.messageList;
      }
      this.historyList.sort((a, b) => new Date(b.time) - new Date(a.time));
    },

    deleteChat(index) {
      this.historyList.splice(index, 1);
      this.$message.success("对话已删除");
    },

    //TODO  将修改后的数据写回json文件,这边需要重写
    writeChat() {
      // 检查有没有数据没保存
      this.saveChat();
      const fs = require("fs");

      const AiIHistory = require("../../../../../static/json/AiHistory.json"); // 引入json文件
      // 查找里面userInfo为"admin"的对象
      const adminHistory = AiIHistory.find(item => item.userInfo === "admin");

      // 如果存在这样的对象，则获取其history属性
      if (adminHistory) {
        adminHistory.history = this.historyList;
      } else {
        console.log("No history found for admin.");
      }
      // 使用promises来处理异步写入操作
      fs.promises
        .writeFile(
          "../../../../../static/json/AiHistory.json",
          JSON.stringify(AiIHistory, null, 2)
        )
        .then(() => {
          console.log("The file has been saved!");
        })
        .catch(err => {
          console.error("Error writing file:", err);
        });
    },

    // 打开个人中心
    openPersonalCenter() {
      this.drawer = true;
      this.saveChat();
    }
  },

  mounted() {
    this.loadChat();
    // window.addEventListener('beforeunload', this.writeChat);
  },
  beforeDestroy() {
    // 在组件销毁前移除事件监听器
    // window.removeEventListener('beforeunload', this.writeChat);
  }
};
</script>

<style lang="scss" scoped>
.ui_guide {
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB",
    "Microsoft YaHei", "微软雅黑", Arial, sans-serif;

  .robot {
    /* font-size: 34px; */
    width: 55px;
    height: 90px;
    /* color: rgb(43, 126, 154); */
    position: fixed;
    /* left: 1390px; */
    right: 9px;
    cursor: pointer;
    transition: all 0.5s ease;
    top: 380px;
  }

  .chat {
    width: 600px;
    height: 500px;
    background-color: #f5f5f5;
    box-sizing: border-box;
    background-size: cover;
    border-radius: 10px;
    resize: both;
    overflow: hidden;
    position: fixed;
    user-select: text;
  }

  .title {
    width: 100%;
    height: 50px;
    line-height: 56px;
    text-align: center;
    font-size: 18px;
    background-color: #26a02af0;
    color: #f9f9f9;
    display: flex;
    justify-content: space-between;
    padding: 0px 20px 0px 20px;

    .iconfont {
      font-size: 20px;
      cursor: pointer;
    }
  }

  .title:hover {
    cursor: move;
  }

  .drawer {
    .drawer-title {
      display: flex;
      justify-content: left;
      align-items: center;
      font-size: 18px;

      .circle-image {
        border-radius: 50%;
        /* 50% 的半径使图片成为圆形 */
        width: 50px;
        /* 设置图片的宽度 */
        height: 50px;
        /* 设置图片的高度 */
        overflow: hidden;
        /* 防止图片溢出圆形区域 */
        margin-right: 5%;
      }
    }

    .drawer-content {
      height: 100%;
      color: black;
      background-color: #f5f5f5;
      padding-top: 15px;
      /* 上边距 */

      .history-title {
        display: flex;
        justify-content: space-between;
        padding: 0 10px 0 10px;
        font-size: 18px;
      }

      .no-history {
        margin-top: 15%;
        display: flex;
        align-items: center;
        flex-direction: column;

        img {
          width: 80%;
          height: 60%;
          margin-bottom: 10%;
        }
      }

      .content-list {
        border-radius: 8px;
        background-color: #fff;
        margin: 10px auto;
        width: 90%;
        height: 16%;

        .content-body {
          height: 100%;
          display: flex;
          justify-content: space-between;

          .content-item {
            width: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            cursor: pointer;
            padding-top: 4%;

            .content-text {
              width: 90%;
              text-indent: 6px;
              overflow: hidden;
              text-overflow: ellipsis;
              white-space: nowrap;
            }
          }

          .el-icon-delete {
            margin: auto 0;
            color: red;
            padding-right: 4px;
            visibility: hidden;
          }
        }

        .content-body:hover {
          background-color: rgb(246, 247, 249);
          color: #02cb0b;
          border: 1px solid #02cb0b;
          border-radius: 8px;
          cursor: pointer;
        }

        /* 当.content-body悬停时，显示删除图标 */
        .content-body:hover .el-icon-delete {
          visibility: visible;
          /* 显示删除图标 */
        }
      }
    }
  }

  .text {
    width: 100%;
    height: 100%;
    padding: 0 12px 10px;
    box-sizing: border-box;
    overflow-x: hidden;
    overflow-y: auto;
    margin-top: 0px;

    li {
      /* width: 90%; */
      margin-top: 15px;
      box-sizing: border-box;
      list-style-type: none;

      img:not(.image-message) {
        width: 40px;
        height: 40px;
        border-radius: 80%;
      }

      .txt {
        .image-message {
          img {
            max-width: 60% !important;
            max-height: 100px !important;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            border-radius: 100% !important;
          }
        }
      }
    }

    .txt {
      min-height: 40px;
      font-size: 13px;
      line-height: 24px;
      padding: 8px;
      box-sizing: border-box;
      border-radius: 6px;
      border: 1px solid #d8d8d8;
      color: #333;
      white-space: pre-wrap;
      /* 保持Markdown中的换行 */
    }

    .t1 {
      display: flex;
      justify-content: left;

      img {
        margin-right: 10px;
      }

      .txt {
        margin-right: 20px;
        background-color: #fff;
      }
    }

    .t2 {
      display: flex;
      justify-content: right;

      img {
        margin-left: 10px;
      }

      img:hover {
        transform: rotate(1turn);
        /* 1turn 等于 360度 */
        transition-duration: 3s;
        /* 旋转一圈的时间为5秒 */
        transition-property: transform;
        transition-timing-function: cubic-bezier(0.34, 0, 0.84, 1);
        transition-delay: 1s;
      }

      .txt {
        margin-left: 20px;
        background-color: #98e855;
      }
    }

    /* 新增的图片消息展示样式 */
    .image-message {
      display: flex;
      justify-content: center;
      align-items: center;
      margin-top: 10px;
      min-height: 250px;
      min-width: 250px;

      img {
        max-width: 60% !important;
        max-height: 100px !important;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        border-radius: 100% !important;
      }
    }
  }

  .text::-webkit-scrollbar {
    /*滚动条整体样式*/
    width: 6px;
    /*高宽分别对应横竖滚动条的尺寸*/
    height: 1px;
  }

  .text::-webkit-scrollbar-thumb {
    /*滚动条里面小方块*/
    border-radius: 5px;
    background: #7b889c;
  }

  .text::-webkit-scrollbar-track {
    /*滚动条里面轨道*/
    /*-webkit-box-shadow: inset 0 0 5px rgba(0,0,0,0.2);*/
    border-radius: 5px;
    background: #d9dde4;
  }

  .cont {
    width: 100%;
    height: 52px;
    z-index: 10;
    background-color: #ebebeb;
    box-sizing: border-box;
    box-shadow: 0 -2px 5px #d8d8d8;
    margin-top: 3px;

    .inp {
      width: 80%;
      height: 36px;
      margin: 0;
      padding: 5px 10px;
      padding-left: 15px;
      border: 1px solid #d8d8d8;
      color: #333;
      box-sizing: border-box;
      background-color: #fff;
      border-radius: 10px;
      margin-left: 5px;
      margin-top: 1%;
    }

    .inp::-webkit-input-placeholder {
      color: #999;
    }

    .inp::-moz-placeholder {
      color: #999;
    }

    .inp::-ms-input-placeholder {
      color: #999;
    }

    .send {
      width: 15%;
      height: 33px;
      line-height: 3px;
      text-align: center;
      color: #3b3a3f;
      background-color: #cccccc;
      border: 0;
      border-radius: 8px;
      font-weight: bold;
      margin-left: 3px;
      cursor: pointer;
    }

    .send:hover {
      background-color: #02cb0b;
    }
  }
}

.el-card__body {
  padding: 0px;
}
</style>
