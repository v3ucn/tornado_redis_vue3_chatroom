<template>
  <div>


                <h1>充值页面</h1>


                <van-steps :active="active">


                  <van-step>阅读条款</van-step>

                  <van-step>同意条款</van-step>

                  <van-step>选择支付方式</van-step>

                  <van-step>输入充值金额</van-step>
                  

                </van-steps>


                <div v-if="active===0"> 

                阅读条款  

                1.明确责任内容
                2.用户对自己涉及钱款操作负责

                <van-button color="blue" @click="next">下一步</van-button>

                </div>


                <div v-if="active===1">



                    <van-radio-group v-model="checked">
                      

                        <van-radio name="0">不同意该充值条款</van-radio>



                        <van-radio name="1">同意该充值条款</van-radio>


                    </van-radio-group>



                    <van-button @click="last">上一步</van-button>  

                    <van-button v-if="checked == 1" @click="next">下一步</van-button>




                </div>



                <div v-if="active===2" class="radio">



                    <van-radio-group v-model="pay">
                      

                        <van-radio name="0">银行卡</van-radio>

                        <van-radio name="1">支付宝</van-radio>

                        <van-radio name="2">微信</van-radio>


                    </van-radio-group>


                    <van-field v-if="pay == 0" label="银行卡号" v-model="card" placeholder="请输入银行卡号" />



                    <van-button @click="last">上一步</van-button>  

                    <van-button @click="next">下一步</van-button>




                </div>


                <div v-if="active===3" class="radio">



                   
                    <van-field label="充值金额" v-model="price" placeholder="请输入金额" />



                    <van-button @click="last">上一步</van-button>  

                    <van-button @click="createorder" >生成订单</van-button>




                </div>
              



   
  </div>
</template>

<script>

export default {
 data() {
    return {
      checked:0,
      info:{},
      type:1,
      types:[{"id":1,"text":"商户后台"},{"id":2,"text":"运营后台"},{"id":3,"text":"流量后台"}],
      index:0,
      key:"",
      state:0,

      //状态维护字典
      state_dict:{0:"待审核",1:"审核通过",2:"审核拒绝",3:"审核中"},

      //步骤记录
      active:0,

      //支付方式
      pay:0,

      //卡号
      card:"",

      //金额
      price:0,

      //标识位
      mytoken:""
    }
  },
  methods:{

    //创建订单
    createorder:function(){

        this.myaxios("https://localhost/order/","post",{"id":localStorage.getItem("id"),"price":this.price,"mytoken":this.mytoken}).then(data =>{


              this.$toast.success(data.msg);

              this.active = 0 ;

              this.get_step();


        });    


    },
    //获取栈内步骤
    get_step:function(){


      //发起请求

      this.myaxios("https://localhost/stepform/","get",{"id":localStorage.getItem("id")}).then(data =>{


          console.log(data);

          if(data != 0 ){

              this.active = data.index + 1;

          }


          console.log(this.active);

          


        });




    },
    //上一步操作
    last:function(){

        //第二步上一步
        if(this.active===1){

            this.active = 0;

        }

        if(this.active===2){

            this.active = 1;

        }

        if(this.active===3){

            this.active = 2;

        }



        this.myaxios("https://localhost/stepform/","delete",{"id":localStorage.getItem("id")}).then(data =>{


          console.log(data);

          if(this.active==1){

                this.checked = data.value;

          }

          if(this.active==2){

                this.pay = data.value;

                if(data.value==0){

                  this.card = data.card;
                }

          }


        });



    },
    //下一步操作
    next:function(){


      var value = "";

      
      //第一步的下一步
      if(this.active===0){

          this.active = 1;


      }else if(this.active===1){


        this.active = 2;

          value = this.checked;


      }else if(this.active===2){


        this.active = 3;

          value = this.pay;


      }


      this.myaxios("https://localhost/stepform/","post",{"id":localStorage.getItem("id"),"num":this.active-1,"value":value,"card":this.card}).then(data =>{


          console.log(data);


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


        });



    },
    set_click:function(index,key){

        console.log(index);
        this.index = index;
        this.key = key;

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
    //生成标识位
    send_token:function(){

        this.myaxios("https://localhost/order/","put",{"id":localStorage.getItem("id")}).then(data =>{


              //获取时间
              var mytime = new Date().getMinutes();

              console.log(mytime);

              //base64
              this.mytoken = window.btoa("123_"+localStorage.getItem("id")+mytime);


              this.mytoken = this.mytoken.slice(0,this.mytoken.length-3);


              console.log(this.mytoken);


         

        });


    },
    //获取用户角色配置字段
    get_role:function(){


      this.myaxios("https://localhost/role/","get",{"type":localStorage.getItem("type")}).then(data =>{


          console.log(data);

          //强转
          data = JSON.parse(data);

          //遍历初始化

          var num = 0;
   
          for(var key in data){

                this.info[key] = "";

                this.info["img"+num] = "";

                num++;

          }

          this.info.data = data

          console.log(this.info.data);

        });

    },

  },

  mounted(){

      //通知后端生成标识位
      this.send_token();

      //调用配置字段
      this.get_role();

      //调用用户信息
      this.get_info();

      //调用当前步骤
      this.get_step();

    

  }

}
</script>


<style scoped>
  @import url("../assets/style.css");

  .radio{

    background-color:white;

  }

</style>

