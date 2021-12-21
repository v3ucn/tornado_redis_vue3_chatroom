<template>
  <div>


            <h1>聊天窗口</h1>


            <van-tabs v-model:active="active" @click="change_channel">

              <van-tab title="客服1号">


                <table>
              
              <tr v-for="item,index in msglist" :key="index">
                
                {{ item }}

              </tr>

            </table>
                


              </van-tab>


              <van-tab title="客服2号">
                

                <table>
              
              <tr v-for="item,index in msglist" :key="index">
                
                {{ item }}

              </tr>

            </table>


              </van-tab>

            </van-tabs>


            


            <van-field label="聊天信息" v-model="msg" />

            <van-button color="gray" @click="commit">发送</van-button>

   
  </div>
</template>

<script>

export default {
 data() {
    return {
      auditlist:[],

      //聊天记录
      msglist:[],
      msg:"",
       websock: null, //建立的连接
      lockReconnect: false, //是否真正建立连接
      timeout: 3 * 1000, //30秒一次心跳
      timeoutObj: null, //外层心跳倒计时
      serverTimeoutObj: null, //内层心跳检测
      timeoutnum: null, //断开 重连倒计时
      active:0,
      channel:"channel_1"
     
    }
  },
  methods:{


    //切换频道
    change_channel:function(){


          if(this.active === 0){


                this.channel = "channel_1";

                var name = "channel";
          var value = "channel_1";

          

          }else{


              this.channel = "channel_2";

                var name = "channel";
          var value = "channel_2";


          }


          //清空聊天记录
          this.msglist = [];


          var d = new Date();
          d.setTime(d.getTime() + (24 * 60 * 60 * 1000));
          var expires = "expires=" + d.toGMTString();
          document.cookie = name + "=" + value + "; " + expires;


          this.reconnect();


    },
     initWebSocket() {
      //初始化weosocket
      const wsuri = "ws://localhost:8000/wb/";
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
         // self.websock.close();
        }, self.timeout);
      }, self.timeout);
      // 3s一次
    },

    websocketonopen(e) {
      //连接建立之后执行send方法发送数据
      console.log("成功");

     // this.websock.send("123");
      // this.websocketsend(JSON.stringify(actions));
    },
    websocketonerror() {
      //连接建立失败重连
      console.log("失败");
      this.initWebSocket();
    },
    websocketonmessage(e) {

      console.log(e);
      //数据接收
      //const redata = JSON.parse(e.data);
      const redata = e.data;

      //累加
      this.msglist.push(redata);

      console.log(redata);

     
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

    //提交表单
    commit:function(){


        //发送请求

        this.myaxios("http://localhost:8000/send/","post",{"data":this.msg,channel:this.channel}).then(data =>{

          console.log(data);

        });



    },
  

  },

  mounted(){


      //连接后端websocket服务
      this.initWebSocket();



      var d = new Date();
          d.setTime(d.getTime() + (24 * 60 * 60 * 1000));
          var expires = "expires=" + d.toGMTString();
          document.cookie = "channel" + "=" + "channel_1" + "; " + expires;

    

  }

}
</script>


<style scoped>
  @import url("../assets/style.css");

  .chatbox{

      color:black;

  }

  .mymsg{

      background-color:green;

  }


</style>

