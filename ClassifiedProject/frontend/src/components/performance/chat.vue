<template>
  <div class="performance">
    <div style="margin-bottom: 10px">
      <el-input
        type="textarea"
        :rows="10"
        placeholder="请输入内容"
        v-model="textarea"
      >
      </el-input>
    </div>
    <div style="margin-bottom: 10px">
      <el-input v-model="input" placeholder="请输入内容"></el-input>
    </div>
    <div style="margin-bottom: 10px; text-align: left">
      <el-button type="primary" @click="onSubmit">发送</el-button>
    </div>
  </div>
</template>

<script>
export default {
  components: {},
  data() {
    return {
      socket: "",
      textarea: "",
      input: "",
    };
  },
  created() {
    this.initConn();
  },
  methods: {
    //初始化连接
    initConn() {
      const wss_protocol =
        window.location.protocol == "https" ? "wss://" : "ws://"; //创建协议开头wss,ws的常量
      this.socket = new WebSocket(
        wss_protocol + "127.0.0.1:8000/ws/performance/chat/room/"
      ); //创建socket实例
      this.socket.onmessage = this.OnMessage;
      this.socket.onopen = this.OnOpen;
      this.socket.onclose = this.onClose;
    },
    // 建立websocket连接时触发此方法，展示欢迎提示
    OnOpen() {
      this.textarea += this.textarea + "[公告]欢迎来到讨论群。请文明发言!";
    },
    //接收到后台数据后对其解析，并加入到聊天记录chat-log
    OnMessage(e) {
      const data = JSON.parse(e.data);
      console.log(data);
      this.textarea += "\n" + data.message;
    },
    //websocket关闭
    onClose(e) {
      console.error("e-->", e);
    },
    //发送消息
    onSubmit() {
      this.textarea += "\n" + "Me：" + this.input;
      this.socket.send(
        JSON.stringify({
          message: this.input,
        })
      );
      console.log("发送格式：", JSON.stringify({ message: this.input }));
    },
  },
};
</script>
