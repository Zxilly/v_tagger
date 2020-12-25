<template>
  <v-row justify="center">
    <v-col
        cols="8"
        class="d-flex"
    >
      <v-card
          style="display:block"
          class="mx-auto"
      >
        <video-player
            class="video-player-box ma-2"
            ref="videoPlayer"
            :options="playerOptions"
        />
      </v-card>
    </v-col>
    <v-col cols="4">
      <v-card>
        <v-card-title>Tag List</v-card-title>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import {apiurl} from "@/config";


export default {
  name: "addtag",
  data: () => ({
    saved: false,
  }),
  computed: {
    hash: function () {
      return this.$route.params.hash
    },
    player() {
      return this.$refs.videoPlayer.player
    },
    vh2pxheight: function () {
      return window.innerHeight*0.7
    },
    playerOptions: function () {
      return {
        // videojs options
        muted: false,
        //width: "100%",
        height: this.vh2pxheight,
        playbackRates: [0.7, 1.0, 1.5, 2.0],
        language: 'zh-cmn-Hans',
        fluid: false,
        sources: [{
          type: "video/mp4",
          src: apiurl + '/video/data/' + this.$route.params.hash + '.mp4'
        }],
      }
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