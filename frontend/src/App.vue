<template>
  <v-app>
    <cheader
        :title="title"
        :loginstatus="logined"
        @logout="logout"
    />
    <v-main>
      <v-container>
        <router-view/>
      </v-container>

      <v-snackbar
          v-model="snackbarBool"
          :color="snackbarColor"
          top
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
import Cheader from "@/components/comp/cheader";

export default {
  name: 'App',
  components: {Cheader},
  created() {
    if(this.$route.path!=='/')
    {
      this.$router.push('/')
    }
    if (this.checkLocalUserStatus()) {
      this.auth()
    } else {
      this.$router.push('/user/login')
    }
  },
  data: () => ({
    user: "",
    authCode: "",
    session: "",
    waiting: true,
    logined: false,
    // loginAttempt: false,
    authedAxios: null,
    snackbarBool: false,
    snackbarMessage: '',
    snackbarColor: '',
    title: "",
    video:null
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
          localStorage.setItem("user", this.user)
          localStorage.setItem("session", data[2])
          this.session = data[2]
        }
      })
    },
    auth: function () {
      this.$axios.post(
          apiurl + "/user/auth",
          null, {
            params: {
              'username': this.user
            },
            headers: {
              'session': this.session
            }
          }
      ).then((resp) => {
        let data = resp.data
        if (data[0] === 4) {
          // session有效,跳转到 /work/tag
          this.showSnackbar([data[1], 'success'])
          this.authedAxios = this.$axios.create({
            baseURL:apiurl,
            params: {
              'username': this.user
            },
            headers: {
              'session': this.session
            }
          })
          this.getInfo().then(()=>{
            this.$router.push('/work/addtag/'+this.video.hash)
          })
        } else {
          //session 无效，跳转到 /user/login
        }
      })
    },
    logout: function () {
      localStorage.removeItem('session')
      localStorage.removeItem('user')
      localStorage.removeItem('exist')
    },
    getInfo: function () {
      return new Promise((resolve) =>{
        this.authedAxios.get('/video/getinfo').then((resp)=>{
          let data = resp.data
          console.log(data)
          this.showSnackbar([data[1],'success'])
          this.video = data[2]
          // console.log(this.video)
          resolve()
        })
      })


    }
  }
};
</script>
