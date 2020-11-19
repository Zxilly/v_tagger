import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import VueRouter from 'vue-router'

import axios from 'axios'

Vue.use(VueRouter)


Vue.config.productionTip = false

Vue.prototype.$axios = axios;

new Vue({
  vuetify,
  render: h => h(App)
}).$mount('#app')
