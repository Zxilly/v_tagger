<template>
  <v-app>
    <v-main>
      <v-snackbar
          v-model="snackbarBool"
          :color="snackbarColor"
          top
          dark
      >
        {{ snackbarMessage }}
        <template v-slot:action="{ attrs }">
          <v-btn
              dark
              text
              v-bind="attrs"
              @click="snackbarBool = false"
          >
            关闭
          </v-btn>
        </template>
      </v-snackbar>
    </v-main>
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
    user: "",
    authCode: "",
    waiting: true,
    logined: false,
    loginAttempt: false,
    authedAxios: null,
    snackbarBool: false,
    snackbarMessage: '',
    snackbarColor: '',
  }),
  methods: {
    showSnackbar: function (arg) {
      this.snackbarMessage = arg[0]
      this.snackbarColor = arg[1]
      this.snackbarBool = true
    },
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
        if (data[0] === 0) {
          this.showSnackbar([data[1]])
          sessionStorage.setItem("session",data[2])
          // TODO:路由跳转
        }
      })
    }
  }
};
</script>
