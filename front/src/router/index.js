import { createRouter, createWebHistory } from 'vue-router'
import HelloWorld from '../components/HelloWorld'
import reg from '../components/reg'
import login from '../components/login'
import userinfo from '../components/userinfo'
import chat from '../components/chat'
import chat_client from '../components/chat_client'


//import myindex from '@/components/myindex'
// import test from '@/components/test'
// import mylogin from '@/components/mylogin'
// import user from '@/components/user'
// import addcate from '@/components/addcate'
// import addcourse from '@/components/addcourse'
// import mycourse from '@/components/mycourse'
// import editcourse from '@/components/editcourse'

// import reg from '@/components/reg'
// import login from '@/components/login'
// import mystation from '@/components/mystation'

// import userinfo from '@/components/userinfo'


// Vue.use(Router)

var routes = [
        {
          path:'/',
          name:'HelloWorld',
          component:HelloWorld
        },
        {
          path:'/reg',
          name:'reg',
          component:reg
        },
        {
          path:'/login',
          name:'login',
          component:login
        },
        {
          path:'/userinfo',
          name:'userinfo',
          component:userinfo
        },
        {
          path:'/chat_client',
          name:'chat_client',
          component:chat_client
        },
        {
          path:'/chat',
          name:'chat',
          component:chat
        },
        // {
        //   path:'/reg',
        //   name:'reg',
        //   component:reg
        // },
        
        //  {
        //   path:'/test',
        //   name:'test',
        //   component:test
        // },
        // {
        //   path:'/addcourse',
        //   name:'addcourse',
        //   component:addcourse
        // },
        // {
        //   path:'/addcate',
        //   name:'addcate',
        //   component:addcate
        // },
        // {
        //   path:'/editcourse',
        //   name:'editcourse',
        //   component:editcourse
        // },
        // {
        //   path:'/login',
        //   name:'login',
        //   component:login
        // },
        // {
        //   path:'/mycourse',
        //   name:'mycourse',
        //   component:mycourse
        // },
        // {
        //   path:'/mystation',
        //   name:'mystation',
        //   component:mystation
        // },
        // {
        //   path:'/userinfo',
        //   name:'userinfo',
        //   component:userinfo
        // },
    
        
    
        
]


const router = new createRouter({
  history: createWebHistory(), // history为必填项
  routes,
})

export {
    router
}
