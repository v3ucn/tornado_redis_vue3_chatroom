<template>
  <div>
 

    <h1>用户信息提交</h1>


    <div class="container">


        <div class="item_column">


            <div class="left">
              
          
              <left  @val=get_val />
           


            </div>


            <div class="right">


                <div v-if="type==='1'">
                

                     <div v-if="nodeid===0">

                     <right_merchant />

                   </div>


                    <div v-if="nodeid===1">

                     <setmoney />

                   </div>

                   <div v-if="nodeid===2">

                     <adthing />

                   </div>

                   <div v-if="nodeid===6">

                     <myorder />

                   </div>


                

                </div>


                <div v-if="type==='2'">


                  <div v-if="nodeid===0">

                     <chat />

                   </div>


                   <div v-if="nodeid===1">

                     <setmoney />

                   </div>

                    <div v-if="nodeid===7">

                     <chat />

                   </div>
                

                


                </div>



            </div>
        




        </div>
      


    </div>


    



   
  </div>
</template>

<script>


import left from './left.vue'

import right_merchant from './right_merchant.vue'

import right_oc from './right_oc.vue'

import setmoney from './setmoney.vue'

import adthing from './adthing.vue'

import myorder from './myorder.vue'

import chat from './chat.vue'

export default {
 data() {
    return {
      info:{},
      type:1,
      types:[{"id":1,"text":"商户后台"},{"id":2,"text":"运营后台"},{"id":3,"text":"流量后台"}],
      index:0,
      key:"",
      state:0,

      //状态维护字典
      state_dict:{0:"待审核",1:"审核通过",2:"审核拒绝",3:"审核中"},

      //默认功能节点id
      nodeid:0,
      //性别
      sex:0
    }
  },
  components:{

    "left":left,
    "right_merchant":right_merchant,
    "right_oc":right_oc,
    "setmoney":setmoney,
    "adthing":adthing,
    "myorder":myorder,
    "chat":chat,

  },
  methods:{

    //获取子组件变量
    get_val:function(val){

      console.log(val);

      // 将节点id进行动态赋值
      this.nodeid = val;

      localStorage.setItem("nodeid",this.nodeid);

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

          this.sex = data.sex
          localStorage.setItem("sex",this.sex);

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
    //上传图片
    afterread:function(file){


        //设置表单
        let data = new FormData();

        data.append("file",file.file);
        data.append("type","audit");

        const axiosInstance = this.axios.create({withCredentials:false});


        //发送请求
        axiosInstance({

          method:"post",
          url:"https://localhost/upload/",
          data:data

        }).then( data => {

          console.log(data)

          this.info["img"+this.index] = this.upload_dir + data.data.filename;
          this.info[this.key] = data.data.filename;

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


      this.type = localStorage.getItem("type");

      this.get_info();

    

  }

}
</script>


<style scoped>
  @import url("../assets/style.css");

</style>

