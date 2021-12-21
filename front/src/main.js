import { createApp } from 'vue'
import App from './App.vue'
import { router } from './router/index'


import axios from 'axios'
import qs from 'qs'


import Vant from 'vant';
import 'vant/lib/index.css';

//封装请求
const myaxios = function(url,type,data={}){

	return new

	Promise((resolve) => {


		//判断
		if(type==="get" || type === "delete"){


			axios({

				method:type,
				url:url,
				params:data
			}).then((result) => {

					resolve(result.data);

			});


		}else{


			axios({

				method:type,
				url:url,
				data:qs.stringify(data)
			}).then((result) => {

					resolve(result.data);

			});



		}


	});



}

const app = createApp(App)


app.config.globalProperties.myaxios = myaxios;
app.config.globalProperties.axios = axios;
app.config.globalProperties.upload_dir = "https://localhost/static/";

app.use(router);
app.use(Vant);

app.mount('#app')