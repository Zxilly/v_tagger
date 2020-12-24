<template>
  <v-row>
    <v-col cols="8">
      
    </v-col>
    <v-col cols="8">

    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "addtag",
  data: () => ({
    saved: false
  }),
  computed: {
    hash: function () {
      return this.$route.params.hash
    }
  },
  beforeRouteLeave(to, from, next) {
    if (!this.saved) {
      const answer = window.confirm('Do you really want to leave? You have unsaved changes!')
      if (answer) {
        next()
      } else {
        next(false)
      }
    }
  }
}
</script>

<style scoped>

</style>