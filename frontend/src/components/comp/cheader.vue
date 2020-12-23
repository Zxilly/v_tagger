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
        v-if="loginstatus"
        @click="this.$emit('logout')"
    >
      <v-icon left>
        mdi-logout
      </v-icon>
      Logout
    </v-btn>
<!--    <v-btn text v-else>
      <v-icon left>
        mdi-login
      </v-icon>
      &nbsp;Log in
    </v-btn>-->
  </v-app-bar>
</template>

<script>
export default {
  name: "user",
  props: {
    title: String,
    loginstatus: Boolean,
  },
}
</script>

<style scoped>

</style>