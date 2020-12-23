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
      this.auth()
    }
  },
  data: () => ({
    user: "",
    authCode: "",
    session: "",
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
        this.session = localStorage.getItem("session");
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
          localStorage.setItem("user",this.user)
          localStorage.setItem("session",data[2])
          this.session = data[2]
        }
      })
    },
    auth: function () {
      this.$axios.post(
          apiurl+"/user/auth",
          {},{
            params: {
              'username': this.user
            },
            headers: {
              'session': this.session
            }
          }
      ).then((resp)=>{
        let data = resp.data
        if(data[0]===4){
          // session有效,跳转到 /work/tag

        } else {
          //session 无效，跳转到 /user/login
        }
      })
    }
  }
};
</script>
