<template>
  <div>


                <h1>我的订单</h1>

                <table>
                  
                  <tr> 

                    <td>订单id</td> <td>金额</td> <td>状态</td> <td>操作</td>

                  </tr>


                  <tr v-for="item,index in orderlist" :key="index">
                    
                    <td>
                      
                      {{ item.orderid }}

                    </td>

                    <td>
                      
                      {{ item.price }}

                    </td>

                    <td>
                      
                      {{ item.state }}

                    </td>

                    <td>
                      
                      <van-button>查看详情</van-button>

                      <van-button>删除订单</van-button>

                      <van-button>售后</van-button>

                    </td>

                  </tr>


                </table>
                

                <van-pagination @change="get_order" v-model="page" :total-items="total" :items-per-page="size"  />


   
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

      //订单列表
      orderlist:[],
      //当前页
      page:1,
      //一共多少数据
      total:0,
      //每页多少个
      size:5

    }
  },
  methods:{

    //初始化订单

    get_order:function(){


      this.myaxios("https://localhost/orderlist/","get",{"id":localStorage.getItem("id"),"page":this.page}).then(data =>{


          console.log(data);

          this.total = data.total;
          this.orderlist = data.data;


        });



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

 
    this.get_order();
    

  }

}
</script>


<style scoped>
  @import url("../assets/style.css");

  .radio{

    background-color:white;

  }

</style>

