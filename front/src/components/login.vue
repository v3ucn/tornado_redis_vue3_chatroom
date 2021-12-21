<template>
  <div>
 

    <h1>登录页面</h1>


    <van-cell-group>
      
        <van-field label="用户名" v-model="username" />

        <van-field label="密码" v-model="password" type="password"  />

        用户类型: 

        <select v-model="type">
          

          <option v-for="item,index in types"  :value="item.id" :key="index" >
            
            {{ item.text }}

          </option>


        </select>


        <van-button color="gray" @click="reg"> 点击登录 </van-button>



    </van-cell-group>



   
  </div>
</template>

<script>

export default {
 data() {
    return {
      username:"",
      password:"",
      password1:"",
      type:1,
      types:[{"id":1,"text":"商户后台"},{"id":2,"text":"运营后台"},{"id":3,"text":"流量后台"}]
    }
  },
  methods:{

    reg:function(){


          this.myaxios("https://localhost/user/","get",{"username":this.username,"password":this.password,"type":this.type}).then(data =>{

          console.log(data);

          if(data.code == 200){

              this.$toast.success("登录成功");

              localStorage.setItem("id",data.id)
              localStorage.setItem("type",data.type)
              localStorage.setItem("username",data.username)
              localStorage.setItem("token",data.token)

              this.$router.push("/userinfo")

          }else{

              this.$toast.fail(data.msg);

          }



        });


    }

  },

  mounted(){


       this.myaxios("https://localhost/","get").then(data =>{

          console.log(data);



        });

    

  }

}
</script>


<style scoped>
  @import url("../assets/style.css");




</style>

