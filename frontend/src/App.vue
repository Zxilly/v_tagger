<template>
  <v-app>
  </v-app>
</template>

<script>
import {apiurl} from "./config"

export default {
  name: 'App',
  components: {},
  created() {
    if (this.checkLocalUserStatus()) {
      this.login()
    }
  },
  data: () => ({
    "user": "",
    "authCode": "",
    "waiting": true,
    "logined": false,
    "loginAttempt": false,
    "authedAxios": null,
  }),
  methods: {
    checkLocalUserStatus: function () {
      if (localStorage.getItem("exist")) {
        this.user = localStorage.getItem("user");
        this.authCode = localStorage.getItem("authCode");
        return true;
      } else {
        return false;
      }
    },
    login: function () {
      this.$axios.post(
          apiurl + "/user/login",
          {
            "authcode": this.authCode
          }, {
            params: {
              'username': this.user
            }
          }
      ).then((resp) => {
        let data = resp.data
        if (data[0]===0){
          
        }
      })
    }
  }
};
</script>
