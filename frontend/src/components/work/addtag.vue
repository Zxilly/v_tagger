<template>
  <v-row justify="center">
    <v-col
        cols="8"
    >
      <v-card
          class="pa-2"
          :max-height="vh2pxheight"
      >
        <video-player
            class="video-player-box ma-2"
            ref="videoPlayer"
            :options="playerOptions"
            @canplay="finit"
        />
      </v-card>
    </v-col>
    <v-col cols="4">
      <v-card class="mb-6 pa-4">
        <v-btn
            class="mx-auto"
            style="display: block"
            text
            x-large
            @click="addbreakpoint"
        >
          Add Breakpoint
        </v-btn>
      </v-card>
      <v-card>
        <v-card-title>Clip List</v-card-title>
        <v-card-text>
          <v-simple-table>
            <template v-slot:default>
              <thead>
              <tr>
                <th class="text-left">
                  Start
                </th>
                <th class="text-left">
                  End
                </th>
                <th class="text-left">
                  Tag
                </th>
              </tr>
              </thead>
              <tbody>
              <tr
                  v-for="clip in clips"
                  :key="clip.start"
                  @click.stop="updatechip(clip.start)"
              >
                <td>{{ clip.start }}</td>
                <td>{{ clip.end }}</td>
                <td>{{ clip.tag }}</td>
              </tr>
              </tbody>
            </template>
          </v-simple-table>
          <div
              class="mt-2"
          >Click the clip to add or change the tag.
          </div>
        </v-card-text>
      </v-card>
    </v-col>
    <v-dialog
        v-model="dialog"
        persistent
        max-width="600px"
    >
      <v-card>
        <v-card-title>
          <span class="headline">Add Tag</span>
        </v-card-title>
        <v-card-text>
          <v-autocomplete
              :items="tags"
              v-model="clip_tag_tmp"
          />
        </v-card-text>
        <v-card-actions>
          <v-btn
              color="red darken-1"
              text
              @click="deletechip"
          >
            Delete Chip
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn
              color="red darken-1"
              text
              @click="dialog = false"
          >
            Cancal
          </v-btn>
          <v-btn
              color="green darken-1"
              text
              @click="savechip"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import {apiurl} from "@/config";


export default {
  name: "addtag",
  data: () => ({
    saved: false,
    clips: [],
    init: false,
    dialog: false,
    clip_start_tmp: Number,
    clip_tag_tmp: String,
    tags: null,
  }),
  mounted() {
    this.$axios.get(apiurl + '/video/gettags').then((resp) => {
      this.tags = resp.data
    })
  },
  computed: {
    hash: function () {
      return this.$route.params.hash
    },
    duartion: function () {
      return Number(this.player.cache_.duration.toFixed(1))
    },
    player() {
      return this.$refs.videoPlayer.player
    },
    vh2pxheight: function () {
      // console.log(window.innerHeight*0.7)
      return window.innerHeight * 0.7
    },
    playerOptions: function () {
      return {
        // videojs options
        preload: 'auto',
        muted: false,
        playbackRates: [0.7, 1.0, 1.5, 2.0],
        language: 'zh-cmn-Hans',
        fluid: true,
        aspectRatio: '16:9',
        sources: [{
          type: "video/mp4",
          src: apiurl + '/video/data/' + this.$route.params.hash + '.mp4'
        }],
      }
    },
  },
  methods: {
    updatechip: function (start) {
      this.dialog = true
      this.clip_start_tmp = start
    },
    savechip: function () {
      for (let clip of this.clips) {
        if (clip.start===this.clip_start_tmp){
          clip.tag=this.clip_tag_tmp
          this.dialog=false
          this.clip_tag_tmp=''
          break
        }
      }
    },
    deletechip: function () {
      // TODO
      window.alert("还没写，别急")
    },
    finit: function () {
      if (!this.init) {
        this.clips.push({
          start: 0,
          end: this.duartion,
          tag: ''
        })
        this.init = true
      }
    },
    addbreakpoint: function () {
      this.finit()
      if ("currentTime" in this.player.cache_) {
        let time = this.player.cache_.currentTime
        time = Number(time.toFixed(1))
        for (let clip of this.clips) {
          if (time > clip.start && time <= clip.end) {
            this.clips.push({
              start: time,
              end: clip.end,
              tag: ''
            })
            clip.end = time
            clip.tag = ''
            this.clips.sort((a, b) => {
              return a.start - b.start
            })
            break
          }
        }
      } else {
        this.$bus.$emit('snackbar', ['You should play the video before this.', 'info'])
      }
      //console.log(this.clips)
    },
    submit: function () {

    }
  },
  beforeRouteLeave(to, from, next) {
    if (!this.saved) {
      const answer = window.confirm('Do you really want to leave? You have unsaved changes!')
      if (answer) {
        this.player.dispose()
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