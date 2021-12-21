<template>
  <div>
 

      <div v-if="username==''">


        <router-link to="/login">登录</router-link>

        /

        <router-link to="/reg">注册</router-link>
        

      </div>


      <div>
        
          欢迎您，尊贵的{{ change_type(type) }} 用户:  {{ username }}


          <van-button @click="logout">登出</van-button>


          <ul>
              
              <li v-for="item,index in menulist" :key="index" @click="get_nodeid(item.id)">
                
                {{ item.name }}

              </li>


          </ul>


      </div>



   
  </div>
</template>

<script>

export default {
 data() {
    return {

      username:"",
      type:0,

      //菜单列表
      menulist:[]
     
    }
  },
  //预加载方法
  setup(props,{emit}){


      function get_nodeid(nodeid){


            emit("val",nodeid);

      }

      return {

        get_nodeid

      }


  },
  methods:{

    //获取菜单数据
    get_data:function(){

      this.myaxios("https://localhost/menu/","get",{id:localStorage.getItem("id")}).then(data =>{


               console.log(data);


               this.menulist = data;


        });


    },
    logout:function(){


          localStorage.removeItem("username");
          localStorage.removeItem("id");
          localStorage.removeItem("token");
          localStorage.removeItem("type");


          this.$router.push("/login");


    },
    //替换类别
    change_type:function(val){


        if(val === "1"){

            return "商户后台";

        }else if(val === "2"){

            return "运营后台";

        }else{

            return "流量后台";
        }



    }

    

  },
  mounted(){

      //判断是否登录
      if(localStorage.getItem("username") === null){

            this.username = "";

      }else{


          this.username = localStorage.getItem("username");

          this.type = localStorage.getItem("type");

      }

      this.get_data();





       // this.myaxios("https://localhost/","get").then(data =>{

       //    console.log(data);



       //  });

    

  }

}
</script>


<style scoped>
  @import url("../assets/style.css");

  li {

    margin-top:15px;
    margin-bottom:15px;
    cursor:pointer;

  }


</style>

