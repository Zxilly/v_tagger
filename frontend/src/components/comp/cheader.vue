<template>
  <v-app-bar
      app
      dark
      color="primary"
  >
    <v-btn icon class="ml-1">
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
  </v-app-bar>
</template>

<script>
export default {
  name: "user",
  props: {
    title: String,
    loginstatus: Boolean,
  },
  methods:{
    logout:function () {
      this.$bus.$emit("logout")
    }
  }
}
</script>

<style scoped>

</style>