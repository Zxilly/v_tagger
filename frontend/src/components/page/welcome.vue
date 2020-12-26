<template>
  <div class="mt-16">
    <h1 class="mx-auto text-center">Welcome to v_tagger</h1>
    <div style="width: 100%">
      <v-btn
          class="mx-auto mt-12"
          text
          style="display:block"
          @click="gotag"
      >
        Go Tagging
      </v-btn>
    </div>
  </div>
</template>

<script>
export default {
  name: "welcome",
  methods: {
    gotag: function () {
      this.$bus.$emit('gotag')
    }
  }
}
</script>

<style scoped>

</style>