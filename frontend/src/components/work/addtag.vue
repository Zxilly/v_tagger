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
      <v-card class="mt-6 pa-4">
        <v-btn
            class="mx-auto"
            style="display: block"
            text
            x-large
            @click.stop="submit"
        >
          Submit
        </v-btn>
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
            Cancel
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
    <v-dialog
        v-model="dialog2"
        persistent
        max-width="300px"
    >
      <v-card>
        <v-card-title class="mb-4">
          You have submit the clips.
        </v-card-title>
        <v-card-actions>
          <v-btn
              text
              @click="exit"
          >
            Exit
          </v-btn>
          <v-spacer/>
          <v-btn
              text
              @click="gotag"
          >
            Tag another video
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
    dialog2: false,
    clip_start_tmp: Number,
    clip_tag_tmp: String,
    tags: null,
    length: '',
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
    getInfo: function () {
      this.$bus.$authedAxios.get('/video/getinfo', {
        params: {
          'hashv': this.hash
        }
      }).then((resp) => {
        let data = resp.data
        this.length = data[2]['info']['length']
        this.clips = data[2]['info']['clips']
        console.log(this.clips)
        if (this.clips.length !== 0) {
          this.clips.sort((a, b) => {
            return a.start - b.start
          })
        } else {
          this.finit()
        }
      }).catch((resp) => {
        let status = resp.response.status
        if (status === 404) {
          this.$bus.$emit('snackbar', ['Internal Error.', 'error'])
        }
      })
    },
    updatechip: function (start) {
      this.dialog = true
      this.clip_start_tmp = start
    },
    savechip: function () {
      for (let clip of this.clips) {
        if (clip.start === this.clip_start_tmp) {
          clip.tag = this.clip_tag_tmp
          clip.tagger = localStorage.getItem('user')
          this.dialog = false
          this.clip_tag_tmp = ''
          break
        }
      }
    },
    deletechip: function () {
      // TODO:implement
      window.alert("还没写，别急")
    },
    finit: function () {
      if (!this.init || this.clips !== []) {
        this.clips.push({
          start: 0,
          end: this.length,
          tag: '',
          tagger: ''
        })
        this.init = true
      }
    },
    addbreakpoint: function () {
      if ("currentTime" in this.player.cache_) {
        let time = this.player.cache_.currentTime
        time = Number(time.toFixed(1))
        for (let clip of this.clips) {
          if (time > clip.start && time <= clip.end) {
            this.clips.push({
              start: time,
              end: clip.end,
              tag: '',
              tagger: localStorage.getItem('user')
            })
            clip.end = time
            clip.tag = ''
            clip.tagger = localStorage.getItem('user')
            this.clips.sort((a, b) => {
              return a.start - b.start
            })
            break
          }
          console.log(this.clips)
        }
      } else {
        this.$bus.$emit('snackbar', ['You should play the video before this.', 'info'])
      }
      //console.log(this.clips)
    },
    submit: function () {
      for (let clip of this.clips) {
        if (clip.tag === '') {
          this.$bus.$emit('snackbar', ['Exist untagged clip.', 'error'])
          return
        }
      }
      this.$bus.$authedAxios.post('/video/setinfo', {
        'info': {
          'hash': this.hash,
          'length': this.duartion,
          'clips': this.clips
        },
        'tagstatus': 1
      }).then((resp) => {
        let data = resp.data
        if (data[0] === 9) {
          this.saved = true
          this.dialog2 = true
        }
      }).catch((resp) => {
        let status = resp.response.status
        if (status === 404) {
          this.$bus.$emit('snackbar', ['Internal Error.', 'error'])
        }
      })
    },
    gotag: function () {
      this.$bus.$emit('gotag')
    },
    exit: function () {
      this.$router.push('/')
    }
  },
  beforeRouteEnter(to, from, next) {
    next((vm) => {
      vm.$bus.$on('authready', vm.getInfo)
    })
  },
  beforeRouteLeave(to, from, next) {
    if (!this.saved) {
      const answer = window.confirm('Do you really want to leave? You have unsaved changes!')
      if (answer) {
        //this.player.dispose()
        next()
      } else {
        next(false)
      }
    } else {
      //this.player.dispose()
    }
  }
}
</script>

<style scoped>

</style>