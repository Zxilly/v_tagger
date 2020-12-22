import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import VueRouter from 'vue-router'

import reg from '@/components/user/reg'
import login from '@/components/user/login'

import addtag from "@/components/work/addtag";
import notfound from "@/components/page/notfound";

import axios from 'axios'

Vue.use(VueRouter)


Vue.config.productionTip = false

Vue.prototype.$axios = axios;


const router = new VueRouter({
  routes: [
    {
      path:'/',
      component: App
    },
    {
      path:'/user/reg',
      component: reg
    },
    {
      path:'/user/login',
      component: login
    },
    {
      path:'/work/addtag/:hash',
      component: addtag
    },
    {
      path:'*',
      component: notfound
    }
  ]
})

new Vue({
  vuetify,
  router,
  render: h => h(App)
}).$mount('#app')
