<template>
  <v-app>
    <cheader
        :title="titleword"
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
    if (this.checkLocalUserStatus()) {
      this.auth()
    } else {
      if (this.$route.path !== '/user/login') {
        this.$router.push('/user/login')
      }
    }
  },
  mounted() {
    this.$bus.$on('login', this.loginevent)
    this.$bus.$on('reg', this.regevent)
    this.$bus.$on('logout', this.logout)
    this.$bus.$on('gotag', this.getJob)
    this.$bus.$on('goadd', this.addVideo)
    this.$bus.$on('gosentence', this.getMarkJob)
    this.$bus.$on('snackbar', this.showSnackbar)
    this.$bus.$on('goany', this.goAnywhere)
    this.$bus.$on('goreviewtag', this.goReviewTag)
  },
  data: () => ({
    user: "",
    authCode: "",
    session: "",
    // waiting: true,
    logined: false,
    regcode: "",
    // loginAttempt: false,
    // authedAxios: null,
    snackbarBool: false,
    snackbarMessage: '',
    snackbarColor: '',
    title: {
      '/': 'Welcome',
      '/user/reg': 'Register',
      '/user/login': 'Login',
      '/user/add': 'Add Video',
    },
    hash: ''
  }),
  computed: {
    titleword: function () {
      if (this.$route.path.indexOf('/work/addtag/') !== -1) {
        return 'Tagging'
      } else if (this.$route.path.indexOf('/work/marksentence/') !== -1) {
        return 'Marking'
      } else {
        return this.title[this.$route.path]
      }
    }
  },
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
        return true
      } else {
        return false
      }
    },
    regevent: function ([sn_value, authcode, regcode]) {
      this.user = sn_value
      this.authCode = authcode
      this.regcode = regcode
      this.reg()
    },
    reg: function () {
      this.$axios.post(
          apiurl + "/user/reg",
          {
            "authcode": this.authCode,
            'regcode': this.regcode,
          }, {
            params: {
              'username': this.user
            }
          }
      ).then((resp) => {
        let data = resp.data
        if (data[0] === 6) {
          this.showSnackbar([data[1], 'error'])
        } else {
          localStorage.setItem("exist", 1)
          localStorage.setItem("user", this.user)
          localStorage.setItem("session", data[2])
          this.session = data[2]
          this.auth()
        }
      }).catch((resp) => {
        let status = resp.response.status
        if (status === 403) {
          this.showSnackbar(['RegCode Error', 'error'])
        }
      })
    },
    loginevent: function ([sn_value, authcode]) {
      this.user = sn_value
      this.authCode = authcode
      this.login()
    },
    login: function () {
      this.$axios.post(
          apiurl + "/user/login",
          {
            "authcode": this.authCode,
          }, {
            params: {
              'username': this.user
            }
          }
      ).then((resp) => {
        let data = resp.data
        if (data[0] === 0) {
          this.showSnackbar([data[1], 'success'])
          localStorage.setItem("exist", 1)
          localStorage.setItem("user", this.user)
          localStorage.setItem("session", data[2])
          this.session = data[2]
          this.auth()
        } else {
          this.showSnackbar([data[1], 'error'])
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
          this.logined = true
          // session有效,跳转到 /work/tag
          this.showSnackbar([data[1], 'success'])
          this.$bus.$authedAxios = this.$axios.create({
            baseURL: apiurl,
            params: {
              'username': this.user
            },
            headers: {
              'session': this.session
            }
          })
          this.$bus.authed = true
          // console.log("set authed as")
          // console.log(this.$bus.authed)
          this.$bus.$emit('authready')
          if (this.$route.path !== '/') {
            this.$router.push('/')
          } // 跳转逻辑是合理的
        } else {
          if (this.$route.path !== '/user/login') {
            this.$router.push('/user/login')
          }
          //session 无效，跳转到 /user/login
        }
      }).catch(() => {
        if (this.$route.path !== '/error') {
          this.$router.push('/error')
        }

        this.showSnackbar(["Backend Service unavailable.", 'error'])

      })
    },
    logout: function () {
      localStorage.removeItem('session')
      localStorage.removeItem('user')
      localStorage.removeItem('exist')
      this.logined = false
      if (this.$route.path !== '/user/login') {
        this.$router.push("/user/login")
      }
      location.reload();
    },
    getHash: function () {
      return new Promise(((resolve, reject) => {
        this.$bus.$authedAxios.get('/video/gethash').then((resp) => {
          this.hash = resp.data[2]
          resolve()
        }).catch((resp) => {
          let status = resp.response.status
          if (status === 503) {
            this.showSnackbar(['No more video to tag', 'info'])
            reject()
          } else {
            this.showSnackbar(['Unknown error, please contact developer.', 'error'])
          }
        })
      }))
    },
    getJob: function () {
      this.getHash().then(() => {
        // console.log(this.$route.path,'/work/addtag/' + this.hash)
        if (this.$route.path !== '/') {
          this.$router.push('/') // 要触发路由守卫
        }
        this.$router.push('/work/addtag/' + this.hash)
      }).catch(() => {
        if (this.$route.path !== '/') {
          this.$router.push('/')
        }
      })
    },
    getMarkJob: function () {
      this.$bus.$authedAxios.get(apiurl + '/video/getsentencehash').then((resp) => {
        return resp.data[2]
      }).catch((err) => {
        let status = err.response.status
        if (status === 503) {
          this.showSnackbar(['No more sentence to mark', 'info'])
        }
      }).then((hash) => {
        if (hash !== undefined) {
          if (this.$route.path !== '/') {
            this.$router.push('/') // 要触发路由守卫
          }
          this.$router.push('/work/marksentence/' + hash)
        }
      })
    },
    addVideo: function () {
      this.$router.push('/user/add')
    },
    goAnywhere: function (path) {
      if (this.$route.path !== path) {
        this.$router.push(path)
      } else {
        console.log('duplicate lead to ' + path + ',please report this to developer.')
      }
    },
    goReviewTag: function (hash) {
      this.$bus.$authedAxios.get('/video/getinfo', {
        params: {
          'hashv': hash
        }
      }).then(() => {
        this.$router.push('/work/addtag/' + hash)
      }).catch((resp) => {
        let status = resp.response.status
        if (status === 404) {
          this.$bus.$emit('snackbar', ['Target hash not exist.', 'error'])
        }
      })
    }
  }
};
</script>
