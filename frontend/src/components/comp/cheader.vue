<template>
  <v-app-bar
      app
      dark
      color="primary"
  >
    <v-btn icon class="ml-1"
           @click="this.$router.push('/')"
    >
      <v-icon>
        mdi-tag-multiple
      </v-icon>
    </v-btn>
    <v-toolbar-title>
      {{ title }}
    </v-toolbar-title>
    <v-spacer/>
    <v-btn
        text
        class="float-right"
        v-if="loginstatus"
        @click="logout"
    >
      <v-icon left>
        mdi-logout
      </v-icon>
      Logout
    </v-btn>
    <v-btn
        v-if="this.$route.path === '/user/add'||this.$route.path.indexOf('/work/addtag/') !== -1||this.$route.path.indexOf('/work/marksentence/') !== -1"
        text
        @click="goback"
    >
      Go Back
    </v-btn>
  </v-app-bar>
</template>

<script>
export default {
  name: "user",
  props: {
    title: String,
    loginstatus: Boolean,
  },
  methods: {
    logout: function () {
      this.$bus.$emit("logout")
    },
    goback: function () {
      this.$bus.$emit('goany', '/')
    }
  }
}
</script>

<style scoped>

</style>
