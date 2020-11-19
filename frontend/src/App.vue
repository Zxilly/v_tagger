<template>
<v-app>
  <cheader

  />
</v-app>
</template>

<script>

import Cheader from "@/components/cheader";
export default {
  name: 'App',
  components: {
    Cheader
  },
  created() {
    if(this.checkLocalUserStatus()){
      this.loginAttempt = true;
    }
  },
  data: () => ({
    "user":"",
    "authCode":"",
    "waiting":true,
    "logined":false,
    "loginAttempt":false,
    "authedAxios":null,
  }),
  methods:{
    checkLocalUserStatus:function () {
      if(localStorage.getItem("exist")){
        this.user = localStorage.getItem("user");
        this.authCode = localStorage.getItem("authCode");
        return true;
      } else {
        return false;
      }
    },
    login:function (){
      this.$axios({

      })
    }
  }
};
</script>
