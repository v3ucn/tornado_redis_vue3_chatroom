<template>
  <div>


                <h1>您需要审核{{ num }}位用户</h1>

                <van-button color="wheat" @click="openchat">咨询客服</van-button>


                <van-popup  v-model:show="show" :before-close="close" >


                  <table class="chatbox">
                    
                      <tr v-for="item,index in msglist" :key="index" >


                        <td> {{ item.username }} </td>


                        <td v-html="change_bg(item.msg,item.uid)"> </td>
                        

                      </tr>



                  </table>


                  <van-field label="信息" v-model="message" placeholder="请输入聊天内容" />

                  <van-uploader :after-read="afterread" />

                  <van-button size="small" color="green" @click="send">点击发送</van-button>


                </van-popup>



                <van-tabs v-model="active">
                  

                  <van-tab title="审核中">审核中</van-tab>


                  <van-tab title="审核通过">审核通过</van-tab>


                  <van-tab title="审核拒绝">审核拒绝</van-tab>



                </van-tabs>
              

              <table>
                
                <tr>
                  
                  <td>用户id</td><td>用户名</td><td>用户类型</td><td>表单</td><td>操作</td>

                </tr>


                <tr v-for="item,index in auditlist" :key="index">


                  <td>{{ item.id}}</td>

                  <td>{{ item.username}}</td>

                  <td>{{ item.type}}</td>

                  <td>

                    <div v-for="val,key in item.audit" :key="key">

                      {{ val["text"] }}:

                      <van-image :src="upload_dir+val['val']" />
                      

                    </div>


                  </td>


                  <td>
                      
                      <van-button color="green">通过</van-button>

                      /

                      <van-button color="red">拒绝</van-button>

                  </td>
                  

                </tr>


              </table>

                

   
  </div>
</template>

<script>

export default {
 data() {
    return {
      auditlist:[],
      num:0,
      active:0,
       websock: null, //建立的连接
      lockReconnect: false, //是否真正建立连接
      timeout: 3 * 1000, //30秒一次心跳
      timeoutObj: null, //外层心跳倒计时
      serverTimeoutObj: null, //内层心跳检测
      timeoutnum: null, //断开 重连倒计时
      //聊天窗口
      show:false,
      //实时消息
      message:"",
      //聊天记录
      msglist:[],
      //分配客服id
      chatid:3,
      //当前用户身份
      clientid:0,
      //队列计数器
      count:0,
      //出队的uid
      uid:0
    }
  },
  methods:{

    //图片上传
    afterread(file){

          let data = new FormData();

          data.append("file",file.file);

          data.append("type","chat");

          const axiosInstance = this.axios.create({withCredentials:false});

          axiosInstance({

            method:"post",
            url:"https://localhost/upload/",
            data:data

          }).then(data =>{


            console.log(data);

            var filename = data.data.filename;

            //拼接消息
            var msg = "<img src='https://localhost/static/"+filename+"' width=200 height=300  />";

            this.message = msg;


            //调用发送消息接口
            this.send();


          })

    },
    //判断信息是否为当前登陆用户所发
    change_bg:function(msg,uid){


      if(localStorage.getItem("id") === uid){


            return "<div  style='background-color:green'>"+ msg + "</div>";

      }else{


            return msg;

      }


    },
    //发送聊天信息
    send:function(){


      //计数器累加
      this.count++;



  if(this.clientid === 0){

      var key = "chat"+localStorage.getItem("id") + this.chatid;


      // 发起出队请求

      this.myaxios("https://localhost/outserver/","get",{id:localStorage.getItem("id")}).then(data =>{


            this.uid = data.uid;
            console.log(data);


        });




    }else{


       //获取聊天记录
        var key = "chat"+this.clientid + localStorage.getItem("id");


    }

      console.log("计数器:"+this.count);

      console.log("出队uid"+this.uid);



      if(this.clientid === 0){



      // 判断是否首次聊天，并且出队uid是否和当前用户的id是否一致
      if(this.count == 1 && this.uid == 0){

            //提示用户
            this.$toast.fail("对不起，客服正在忙，请稍后");

            //关闭聊天框
            this.show = false;

            // 计数器归零
            this.count = 0;

            return false;

      }


    }


      //发送聊天请求

          this.myaxios("http://localhost:8000/send/","post",{data:this.message}).then(data =>{


            console.log(data);

            this.message = "";


        });

    },

    //关闭聊天框
    close:function(){

      console.log("退出聊天");


      //同步状态

     this.myaxios("https://localhost/client/","post",{id:localStorage.getItem("id"),state:0}).then(data =>{


     console.log(data);


});


      return true;


    },
    //聊天窗口
    openchat:function(){

          var mydata = {};


          console.log(this.clientid);

          this.show = true;

          if(this.clientid === 0){



          //获取聊天记录
           var key = "chat"+localStorage.getItem("id") + this.chatid;

           mydata = {key:key,id:localStorage.getItem("id")}

          //设置该用户客服


            this.myaxios("https://localhost/client/","put",{id:this.chatid,clientid:localStorage.getItem("id")}).then(data =>{


            console.log(data);

            


        });


          }else{


            //出队

            // 发起出队请求

      // this.myaxios("https://localhost/outserver/","get",{id:localStorage.getItem("id"),type:"client"}).then(data =>{


      //       console.log(data);


      //   });


             //获取聊天记录
              var key = "chat"+this.clientid + localStorage.getItem("id");


              mydata = {key:key};


              //同步状态

               this.myaxios("https://localhost/client/","post",{id:localStorage.getItem("id"),state:1}).then(data =>{


               console.log(data);


        });


          }



      //发送聊天请求

          this.myaxios("https://localhost/chatlist/","get",mydata).then(data =>{


            console.log(data);

            var mylist = [];

            //遍历后强转
            for (var i = 0; i < data.length; i++) {

                  var msg = JSON.parse(data[i]);

                  console.log(msg);

                  mylist.push(msg);
            
            }

            //排序
            mylist = mylist.reverse()

            //赋值
            this.msglist = mylist;


        });


    },
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
         // self.websock.close();
        }, self.timeout);
      }, self.timeout);
      // 3s一次
    },

    websocketonopen(e) {
      //连接建立之后执行send方法发送数据
      console.log("成功");
      let actions = { test: "12345" };

     // this.websock.send("123");
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

      //强转数据类型
      var data = JSON.parse(redata);

      console.log(data);

      //聊天入队
      this.msglist.push(data);

      //this.$toast.success(redata);



      this.num = this.num + 1;
   
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

    //审核列表
    get_data:function(){


        this.myaxios("https://localhost/oc/","get",{"id":localStorage.getItem("id")}).then(data =>{

          var datalist = [];

          //遍历数据
          for (var i = 0; i < data.length; i++) {
                
                //转换
                var audit = JSON.parse(data[i]["audit"]);

                datalist.push({"username":data[i]["username"],"id":data[i]["id"],"type":data[i]["type"],"audit":audit})
          }

          console.log(datalist);

          this.auditlist = datalist;

          this.num = this.auditlist.length;


        });


    },
    //替换方法
    change_state(val){

       return this.state_dict[val];

    },
    //获取用户信息
    get_info:function(){


      this.myaxios("https://localhost/auditupdate/","get",{"id":localStorage.getItem("id"),"token":localStorage.getItem("token")}).then(data =>{


          console.log(data);

          //审核状态赋值
          this.state = data.state;

          //强转数据类型

          try {
             var audit = JSON.parse(data.audit);

          //遍历存储好的表单数据

          var num = 0;

          for(var key in audit){

                //回填表单数据
                this.info[key] = audit[key].val;
                //回填图片
                this.info["img"+num] = this.upload_dir + audit[key].val;

                num++;
          }

          } catch(e) {
            // statements
     
          }

         


        });



    },
    set_click:function(index,key){

        console.log(index);
        this.index = index;
        this.key = key;

    },
    getclient:function(){


           this.myaxios("https://localhost/client/","get",{id:localStorage.getItem("id")}).then(data =>{

                this.clientid = data.clientid;


        });


    },
    //提交表单
    commit:function(){

        //遍历取值
        let data  = {};


        var num = 0;
        for(var key in this.info.data){

              console.log(key);
              console.log(this.info.data[key]);
              data[key] = {"text":this.info.data[key],"val":this.info[key]}

              num++;

              console.log(num);
        }

        console.log(data);


        //发送请求

        this.myaxios("https://localhost/auditupdate/","put",{"id":localStorage.getItem("id"),"audit":JSON.stringify(data)}).then(data =>{


          console.log(data);

          if(data.code===200){

            this.$toast.success("提交审核资料成功");

          }


        });



    },
  

  },

  mounted(){

      //获取审核列表
      this.get_data();

      //获取用户身份
      this.getclient();

      //连接后端websocket服务
      this.initWebSocket();



      // //连接后端websocket服务

      // var ws = new WebSocket("wss://localhost/ws/");

      // //建立连接
      // ws.onopen = function(){

      //       ws.send("你好，这里是前端");

      // }

      // //接收消息
      // ws.onmessage = function(res){

      //   console.log(res.data);

      // }

    

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

