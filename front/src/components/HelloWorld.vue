<template>
  <div>
 

    {{ upload_dir }}



   
  </div>
</template>

<script>

export default {
 data() {
    return {
      message: '欢迎来到广告平台',
      info:{},
      websock: null, //建立的连接
      lockReconnect: false, //是否真正建立连接
      timeout: 3 * 1000, //30秒一次心跳
      timeoutObj: null, //外层心跳倒计时
      serverTimeoutObj: null, //内层心跳检测
      timeoutnum: null //断开 重连倒计时
    }
  },
  methods:{

    initWebSocket() {
      //初始化weosocket
      const wsuri = "wss://localhost/ws/";
      this.websock = new WebSocket(wsuri);
      this.websock.onopen = this.websocketonopen;
      this.websock.onmessage = this.websocketonmessage;
      this.websock.onerror = this.websocketonerror;
      this.websock.onclose = this.websocketclose;
    },

    reconnect() {
      //重新连接
      var that = this;
      if (that.lockReconnect) {
        // 是否真正建立连接
        return;
      }
      that.lockReconnect = true;
      //没连接上会一直重连，设置延迟避免请求过多
      that.timeoutnum && clearTimeout(that.timeoutnum);
      // 如果到了这里断开重连的倒计时还有值的话就清除掉
      that.timeoutnum = setTimeout(function() {
        //然后新连接
        that.initWebSocket();
        that.lockReconnect = false;
      }, 5000);
    },

     reset() {
      //重置心跳
      var that = this;
      //清除时间（清除内外两个心跳计时）
      clearTimeout(that.timeoutObj);
      clearTimeout(that.serverTimeoutObj);
      //重启心跳
      that.start();
    },

    start() {
      //开启心跳
      var self = this;
      self.timeoutObj && clearTimeout(self.timeoutObj);
      // 如果外层心跳倒计时存在的话，清除掉
      self.serverTimeoutObj && clearTimeout(self.serverTimeoutObj);
      // 如果内层心跳检测倒计时存在的话，清除掉
      self.timeoutObj = setTimeout(function() {
        // 重新赋值重新发送 进行心跳检测
        //这里发送一个心跳，后端收到后，返回一个心跳消息，
        if (self.websock.readyState == 1) {
          //如果连接正常
          // self.websock.send("heartCheck");
        } else {
          //否则重连
          self.reconnect();
        }
        self.serverTimeoutObj = setTimeout(function() {
          // 在三秒一次的心跳检测中如果某个值3秒没响应就关掉这次连接
          //超时关闭
          self.websock.close();
        }, self.timeout);
      }, self.timeout);
      // 3s一次
    },

    websocketonopen(e) {
      //连接建立之后执行send方法发送数据
      console.log("成功");
      let actions = { test: "12345" };

      this.websock.send("123");
      // this.websocketsend(JSON.stringify(actions));
    },
    websocketonerror() {
      //连接建立失败重连
      console.log("失败");
      this.initWebSocket();
    },
    websocketonmessage(e) {
      //数据接收
      //const redata = JSON.parse(e.data);
      const redata = e.data;
      console.log(redata);
   
      this.reset();
    },
    websocketsend(Data) {
      //数据发送
      this.websock.send(Data);
    },
    websocketclose(e) {
      //关闭
      this.reconnect()
      console.log("断开连接", e);
    },

    send:function(){


      console.log(this.info)


    }

  },

  mounted(){

    var that = this;


    this.initWebSocket()


    // var ws = new WebSocket("wss://localhost/ws/");
    //         ws.onopen = function() {
    //            ws.send("你好");
    //         };
    //         ws.onmessage = function (evt) {
    //            // alert(evt.data);

    //            that.$toast.success(evt.data)
    //         };


    // var lockReconnect = false;//避免重复连接
    // var wsUrl = "wss://localhost/ws/";
    // var ws;
    // var tt;
    // function createWebSocket() {
    //   try {
    //     ws = new WebSocket("wss://localhost/ws/");
    //     init();
    //   } catch(e) {
    //     console.log('catch');
    //     reconnect(wsUrl);
    //   }
    // }
    // function init() {
    //   ws.onclose = function () {
    //     console.log('链接关闭');
    //     reconnect(wsUrl);
    //   };
    //   ws.onerror = function() {
    //     console.log('发生异常了');
    //     reconnect(wsUrl);
    //   };
    //   ws.onopen = function () {
    //     //心跳检测重置
    //     heartCheck.start();
    //   };
    //   ws.onmessage = function (event) {
    //     //拿到任何消息都说明当前连接是正常的
    //     console.log(event.data);
    //     heartCheck.start();
    //   }
    // }
    // function reconnect(url) {
    //   if(lockReconnect) {
    //     return;
    //   };
    //   lockReconnect = true;
    //   //没连接上会一直重连，设置延迟避免请求过多
    //   tt && clearTimeout(tt);
    //   tt = setTimeout(function () {
    //     createWebSocket(url);
    //     lockReconnect = false;
    //   }, 4000);
    // }
    // //心跳检测
    // var heartCheck = {

    //   timeout: 3000,
    //   timeoutObj: null,
    //   serverTimeoutObj: null,
      
    //   start: function(){
    //     console.log('start');
    //     var self = this;
    //     this.timeoutObj && clearTimeout(this.timeoutObj);
    //     this.serverTimeoutObj && clearTimeout(this.serverTimeoutObj);
    //     this.timeoutObj = setTimeout(function(){
    //       //这里发送一个心跳，后端收到后，返回一个心跳消息，
 
    //       this.ws.send("ping");
    //       this.serverTimeoutObj = setTimeout(function() {
    //         console.log(111);
    //         console.log(this.ws);
    //         this.ws.close();
    //         // createWebSocket();
    //       }, this.timeout);

    //     }, this.timeout)
    //   }
    // }
    // createWebSocket(wsUrl);

    // console.log(123123);


    //    this.myaxios("https://localhost/","get").then(data =>{

    //       console.log(data);



    //     });

    //    this.$toast.success("123");

      

    

  }

}
</script>


<style scoped>
  @import url("../assets/style.css");




</style>

