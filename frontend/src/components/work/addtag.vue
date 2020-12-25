<template>
  <v-row>
    <v-col cols="8">
      <video-player class="video-player-box"
                    ref="videoPlayer"
                    :options="playerOptions"
      >
      </video-player>
    </v-col>
    <v-col cols="4">

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
    playerOptions:function (){
      return {
        // videojs options
        muted: false,
        playbackRates: [0.7, 1.0, 1.5, 2.0],
        sources: [{
          type: "video/mp4",
          src: apiurl+'/video/data/'+this.$route.params.hash+'.mp4'
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