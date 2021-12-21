<template>
  <div>


                <h1>广告物料页面</h1>


                 <van-uploader :after-read="afterread">
  <van-button icon="plus" type="primary" >上传文件</van-button>
</van-uploader>


              <div v-for="item,index in filelist" :key="index">


                <div v-if="item.type === 'png' || item.type === 'jpg' || item.type === 'jpeg' || item.type === 'gif' || item.type === 'webp' ">
                  
                    <van-image :src="item.filename" />

                </div>

                <div v-if="item.type === 'mp4' ">
                  
                    <video :src="item.filename" width="320" height="240" controls="controls" muted autoplay="autoplay" ></video>

                </div>


                <div v-if="item.type === 'mp3' ">
                  
                    <audio controls>

                      <source :src="item.filename" type="audio/mpeg">


                      </audio>

                </div>
                

              </div>
              

    



   
  </div>
</template>

<script>

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

      //物料展示
      filelist:[]

    }
  },
  methods:{

    afterread:function(file){


        //设置表单
        let data = new FormData();

        data.append("file",file.file);
        data.append("id",localStorage.getItem("id"));
        data.append("nodeid",localStorage.getItem("nodeid"));
        //data.append("token",localStorage.getItem("token"));

        const axiosInstance = this.axios.create({withCredentials:false});


        //添加拦截器

        axiosInstance.interceptors.request.use(

            config => {

                const token = localStorage.getItem("token");

                if(token){

                  console.log(config.data);

                  config.data.append("token",token);


                }else{

                    alert("token不存在");
                    return false;

                }


                return config;

            }

          )




        //发送请求
        axiosInstance({

          method:"post",
          url:"https://localhost/adupload/",
          data:data

        }).then( data => {

          console.log(data)

          if(data.data.code == 200){

          var thing = this.upload_dir + data.data.filename;

          //获取文件类型
          
          var type = thing.substring(thing.lastIndexOf(".")+1);

          this.filelist.push( {"filename":thing,"type":type} );

          console.log(this.filelist);

        }else{


            this.$toast.fail(data.data.msg);


        }
          

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

      //调用配置字段
      this.get_role();

      //调用用户信息
      this.get_info();

    

  }

}
</script>


<style scoped>
  @import url("../assets/style.css");

</style>

