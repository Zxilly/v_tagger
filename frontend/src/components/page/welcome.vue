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
      <v-btn
          class="mx-auto mt-4"
          text
          style="display:block"
          @click="goSentence"
      >
        Go Sentence Mark
      </v-btn>
      <v-btn
          class="mx-auto mt-4"
          text
          style="display:block"
          @click="goadd"
      >
        Add videos
      </v-btn>
<!--      <v-text-field-->
<!--          style="max-width: 40%"-->
<!--          class="mx-auto mt-4"-->
<!--          v-model="hash"-->
<!--          :rules="[v => v.length === 32 || 'Hash should be 32 characters.']"-->
<!--          hint="Please input hash you want to review tag."-->
<!--          label="Review hash"-->
<!--      >-->
<!--        <template v-slot:append-outer>-->
<!--          <v-btn-->
<!--              text-->
<!--              style="display:block"-->
<!--              @click="goReviewTag"-->
<!--          >-->
<!--            Submit-->
<!--          </v-btn>-->
<!--        </template>-->
<!--      </v-text-field>-->
<!--      Cannot support because of complicated data structure. -->
    </div>
  </div>
</template>

<script>
export default {
  name: "welcome",
  data:()=>({
    hash:''
  }),
  methods: {
    gotag: function () {
      this.$bus.$emit('gotag')
    },
    goadd: function () {
      this.$bus.$emit('goadd')
    },
    goSentence: function () {
      this.$bus.$emit('gosentence')
    },
    goReviewTag: function () {
      this.$bus.$emit('goreviewtag',this.hash)
    }
  }
}
</script>

<style scoped>

</style>
