import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import VueRouter from 'vue-router'

import reg from '@/components/user/reg'
import login from '@/components/user/login'

import addtag from "@/components/work/addtag";
import notfound from "@/components/page/notfound";
import welcome from "@/components/page/welcome";

import axios from 'axios'
import md5 from 'js-md5'
import VueVideoPlayer from 'vue-video-player'

import 'video.js/dist/video-js.css'

Vue.use(VueRouter)
Vue.use(VueVideoPlayer)

Vue.config.productionTip = false

Vue.prototype.$axios = axios;
Vue.prototype.$md5 = md5
Vue.prototype.$bus = new Vue()
Vue.prototype.$authedAxios = null

Vue.prototype.$bus.authed = false


const router = new VueRouter({
    routes: [
        {
            path: '/',
            component: welcome
        },
        {
            path: '/user/reg',
            component: reg
        },
        {
            path: '/user/login',
            component: login
        },
        {
            path: '/work/addtag/:hash',
            component: addtag
        },
        {
            path: '*',
            component: notfound
        }
    ]
})

new Vue({
    vuetify,
    router,
    render: h => h(App)
}).$mount('#app')
