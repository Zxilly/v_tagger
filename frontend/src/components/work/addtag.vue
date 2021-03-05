<template>
  <v-row
      justify="center"
      v-if="!fileinited"
      class="mt-12"
  >
    <v-col
        cols="8"
        class="d-flex justify-center pa-6"
    >
      <v-card
          width="100%"
      >
        <v-card-title>
          请选择视频文件
        </v-card-title>
        <v-card-text>
          <v-file-input
              :label="'MD5: '+hash"
              accept="video/mp4"
              outlined
              ref="file"
              @change="videohash"
              :rules="rules2"
          ></v-file-input>
        </v-card-text>

      </v-card>
    </v-col>
  </v-row>
  <v-row
      justify="center"
      v-else
  >
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
            @loadeddata="onPlayerLoadeddata"
            @timeupdate="onTimeUpdate"
        />
      </v-card>
    </v-col>
    <v-col
        cols="4"
        v-if="isAddtag"
    >
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
          <v-data-table
              :headers="tablecfg.headers"
              :items="clips"
              :items-per-page="5"
          >
            <template
                v-slot:body="{ items }"
            >
              <tbody>
              <template v-for="(item,i) in items">
                <tr
                    :key="i+200"
                    v-if="i!==0"
                    @click.stop="updateclip(2,item.start,item.end,item.tag,item.tagsentence,item.start===0?'':item.conjunction)"
                >
                  <td
                      colspan="2"
                      style="text-align: center"
                  >
                    Conjunction:
                  </td>
                  <td
                      colspan="2"
                      style="text-align: center"
                  >
                    {{ item.conjunction }}
                  </td>
                </tr>
                <tr
                    :key="i"
                    @click.stop="updateclip(0,item.start,item.end,item.tag,item.tagsentence,'')"
                >
                  <td>{{ item.start }}</td>
                  <td>{{ item.end }}</td>
                  <td>{{ item.tag }}</td>
                  <td>{{ item.tagsentence ? "√" : "×" }}</td>
                </tr>
              </template>
              </tbody>
            </template>
          </v-data-table>
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
    <v-col
        cols="4"
        v-if="isMarkSentence"
    >
      <v-card
          v-if="markdisplay"
      >
        <v-card-title>Sentence Mark</v-card-title>
        <v-card-text>
          <div
              style="width: 100%"
          >
            <div>
              <v-btn
                  v-for="(item,i) in clips"
                  :key="i"
                  depressed
                  tile
                  :color="btnColor[i]"
                  :width="1/clips.length*100+'%'"
                  @click="goTime(item.start)"
              >
                {{ item.start.toFixed(1) }}-{{ item.end.toFixed(1) }}
              </v-btn>
            </div>
          </div>
          <v-simple-table>
            <tbody>
            <tr>
              <td>Clip time:</td>
              <td>
                <span>{{ clips[switchCase].start.toFixed(1) }}</span>
                <span>s</span>
                <span> - </span>
                <span>{{ clips[switchCase].end.toFixed(1) }}</span>
                <span>s</span>
              </td>
            </tr>
            <tr>
              <td>Tag:</td>
              <td>
                {{ clips[switchCase].tag }}
              </td>
            </tr>
            <tr>
              <td>Sentence:</td>
              <td></td>
            </tr>
            <tr>
              <td colspan="2">
                {{ clips[switchCase].tagsentence }}
              </td>
            </tr>
            <tr>
              <td colspan="2" class="text-center">Mark Sentence</td>
            </tr>
            <tr>
              <td>Accuracy</td>
              <td>
                <v-rating
                    v-model="clips[switchCase].mark.accuracy"
                    @input="checkColor(clips[switchCase],switchCase)"
                />
              </td>
            </tr>
            <tr>
              <td>Conherent</td>
              <td>
                <v-rating
                    v-model="clips[switchCase].mark.conherent"
                    @input="checkColor(clips[switchCase],switchCase)"
                />
              </td>
            </tr>
            <tr>
              <td>Relevance</td>
              <td>
                <v-rating
                    v-model="clips[switchCase].mark.relevance"
                    @input="checkColor(clips[switchCase],switchCase)"
                />
              </td>
            </tr>
            <tr>
              <td>Usability</td>
              <td>
                <v-rating
                    v-model="clips[switchCase].mark.usability"
                    @input="checkColor(clips[switchCase],switchCase)"
                />
              </td>
            </tr>
            </tbody>
          </v-simple-table>
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
        v-model="dialog0"
        persistent
        max-width="600px"
    >
      <v-card>
        <v-card-title>
          <span class="headline">Add Tag</span>
        </v-card-title>
        <v-card-text>
          <v-autocomplete
              label="Video Tag"
              :items="tags"
              :rules="rules1"
              v-model="clip_tag_tmp"
          />
          <v-textarea
              label="Video Description"
              hint="A short sentence to describe the video."
              rows="2"
              :rules="rules1"
              v-model="clip_tag_sentence_tmp"
          ></v-textarea>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
              text
              @click="dialog0 = false"
          >
            Cancel
          </v-btn>
          <v-btn
              color="blue darken-1"
              text
              @click="saveclip"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog
        v-model="dialog1"
        persistent
        max-width="400px"
    >
      <v-card>
        <v-card-title class="mb-4">
          You have submitted the clips.
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
              v-if="isAddtag"
              text
              color="blue darken-1"
              @click="gotag"
          >
            Tag another video
          </v-btn>
          <v-btn
              v-if="isMarkSentence"
              text
              color="blue darken-1"
              @click="gotag"
          >
            Mark another video
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog
        v-model="dialog2"
        persistent
        max-width="600px"
    >
      <v-card>
        <v-card-title>
          <span class="headline">Add Conjunction</span>
        </v-card-title>
        <v-card-text>
          <v-text-field
              label="Conjunction"
              hint="A word to connect the sentence."
              v-model="clip_conjunction_tmp"
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
              text
              @click="dialog2 = false"
          >
            Cancel
          </v-btn>
          <v-btn
              color="blue darken-1"
              text
              @click="saveconjunction"
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
import md5c from 'js-md5'

export default {
  name: "addtag",
  data: () => ({
    saved: false,
    markdisplay: false,
    clips: [],
    conjunctions: [],
    rules1: [value => !!value || 'Required.'],
    filetip: true,
    fileinited: false,
    init: false,
    dialog0: false,
    dialog1: false,
    dialog2: false,
    clip_start_tmp: Number,
    clip_end_tmp: Number,
    clip_tag_tmp: '',
    clip_tag_sentence_tmp: '',
    clip_conjunction_tmp: '',
    tags: null,
    length: '',
    videodata: undefined,
    playerel: undefined,
    switchCase: 0,
    btnColor: [],
    tablecfg: {
      headers: [
        {
          text: 'Start',
          align: 'start',
          sortable: false,
          value: 'start',
        },
        {text: 'End', value: 'end', sortable: false},
        {text: 'Tag', value: 'tag', sortable: false},
        {text: 'Sentence', value: 'tagsentence', sortable: false},
      ],
    }
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
      //return Number(this.player["cache_"].duration.toFixed(1))
      return Number(this.playerel.duration.toFixed(1))
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
          src: this.videodata
        }],
      }
    },
    rules2: function () {
      return [this.filetip]
    },
    isAddtag: function () {
      return this.$route.path.indexOf('/work/addtag/') !== -1
    },
    isMarkSentence: function () {
      return this.$route.path.indexOf('/work/marksentence/') !== -1
    }
  },
  methods: {
    checkColor: function (item, i) {
      if (item.mark.accuracy && item.mark.conherent && item.mark.relevance && item.mark.usability) {
        //this.btnColor[i] = 'blue lighten-4'
        this.$set(this.btnColor, i, 'blue lighten-4')
      }
    },
    videohash: function (value) {
      // console.log(value)
      if (value === undefined) {
        this.filetip = 'Please select a file.'
      }
      let fileReader = new FileReader()
      let blobSlice = File.prototype.slice
      fileReader.readAsArrayBuffer(blobSlice.call(value, 0, 200 * 1024))
      fileReader.onload = (e) => {
        let md5 = md5c.hex(e.target.result)
        if (md5.toString() === this.hash) {
          this.filetip = true
          this.fileinited = true
          this.videodata = window.URL.createObjectURL(value)
        } else {
          console.log(md5)
          this.filetip = 'Please select correct video.'
        }
      }
    },
    getInfo: function () {
      this.$bus.$authedAxios.get('/video/getinfo', {
        params: {
          'hashv': this.hash
        }
      }).then((resp) => {
        let data = resp.data
        this.length = data[2]['info']['length']
        this.clips = data[2]['info']['clips']
        this.conjunctions = data[2]['info']['conjunctions']
        // console.log(this.clips)
        if (this.clips.length !== 0) {
          this.clips.sort((a, b) => {
            return a.start - b.start
          })
        } else {
          this.finit()
        }

        if (this.$route.path.indexOf('/work/marksentence/') !== -1) {
          for (const clip of this.clips) {
            clip['mark'] = {
              'accuracy': 0,
              'conherent': 0,
              'relevance': 0,
              'usability': 0
            }
          }
          this.markdisplay = true
        }

      }).catch((resp) => {
        let status = resp.response.status
        if (status === 404) {
          this.$bus.$emit('snackbar', ['Internal Error.', 'error'])
        }
      })
    },
    updateclip: function (dialogid, start, end, tag, tagsentence, conjunction) {
      this.clip_start_tmp = start
      this.clip_end_tmp = end
      this.clip_tag_tmp = tag
      this.clip_tag_sentence_tmp = tagsentence
      if (start !== 0) {
        this.clip_conjunction_tmp = conjunction
      }
      if (dialogid === 0) {
        this.dialog0 = true
      }

      if (dialogid === 2) {
        this.dialog2 = true
      }

    },
    saveclip: function () {
      for (let clip of this.clips) {
        if (clip.start === this.clip_start_tmp) {
          clip.tag = this.clip_tag_tmp
          clip.tagger = localStorage.getItem('user')
          clip.tagsentence = this.clip_tag_sentence_tmp
          this.dialog0 = false
          this.clip_tag_tmp = ''
          this.clip_tag_sentence_tmp = ''
          break
        }
      }
    },
    deleteclip: function () {
      // TODO:implement
      window.alert("还没写，别急")
    },
    saveconjunction: function () {
      for (let clip of this.clips) {
        if (clip.start === this.clip_start_tmp) {
          clip.conjunction = this.clip_conjunction_tmp
          this.dialog2 = false
          break
        }
      }
    },
    finit: function () {
      if (!this.conjunctions) {
        this.conjunctions = []
      }

      if ((!this.init) || this.clips === []) {
        this.clips.push({
          start: 0,
          end: this.length,
          tag: '',
          tagsentence: '',
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
            if (time === clip.end) {
              this.$bus.$emit('snackbar', ['This breakpoint has been added.', 'error'])
              break
            }
            this.clips.push({
              start: time,
              end: clip.end,
              tag: '',
              tagsentence: '',
              tagger: localStorage.getItem('user'),
              conjunction: ''
            })
            clip.end = time
            clip.tag = ''
            clip.tagsentence = ''
            clip.tagger = localStorage.getItem('user')
            if (clip.start !== 0) {
              clip.conjunction = ''
            }
            this.clips.sort((a, b) => {
              return a.start - b.start
            })
            break
          }
          // console.log(this.clips)
        }
      } else {
        this.$bus.$emit('snackbar', ['You should play the video before this.', 'info'])
      }
    },
    submit: function () {
      if (this.isAddtag) {
        for (let clip of this.clips) {
          if (clip.tag === '' || clip.tagsentence === '') {
            this.$bus.$emit('snackbar', ['Exist untagged or empty sentence clip.', 'error'])
            return
          }
        }
        for (let i = 1; i < this.clips.length; i++) {
          if (this.clips[i].conjunction === '' || this.clips[i].conjunction === undefined) {
            this.$bus.$emit('snackbar', ['Exist empty conjunction.', 'error'])
            return
          }
          this.conjunctions[i - 1] = this.clips[i].conjunction
        }
      }
      // console.log(this.clips)
      let markstatus = false
      if (this.isMarkSentence) {
        for (const item of this.clips) {
          if (!(item.mark.accuracy && item.mark.conherent && item.mark.relevance && item.mark.usability)) {
            this.$bus.$emit('snackbar', ['Exist not mark sentence.', 'error'])
            return
          }
        }
        markstatus = true
      }

      this.$bus.$authedAxios.post('/video/setinfo', {
        'info': {
          'hash': this.hash,
          'length': this.duartion,
          'clips': this.clips,
          'conjunctions': this.conjunctions
        },
        'tagstatus': true,
        'markstatus': markstatus
      }).then((resp) => {
        let data = resp.data
        if (data[0] === 9) {
          this.saved = true
          this.dialog1 = true
        } else {
          this.$bus.$emit('snackbar', ['Internal Error.', 'error'])
        }
      }).catch((resp) => {
        let status = resp.response.status
        if (status === 404) {
          this.$bus.$emit('snackbar', ['Internal Error.', 'error'])
        }
      })
    },
    goTime: function (time) {
      this.playerel.currentTime = time
    },
    onPlayerLoadeddata: function () {
      this.playerel = document.getElementsByTagName('video')[0]
    },
    onTimeUpdate: function () {
      if (this.clips === []) {
        return
      }
      let a = this.playerel.currentTime
      // console.log(a)
      for (const [i, clip] of new Map(this.clips.map((item, i) => [i, item]))) {
        if (a >= clip.start && a <= clip.end) {
          this.switchCase = i
          break
        }
      }
    },
    gotag: function () {
      this.dialog1 = false
      this.fileinited = false
      this.$bus.$emit('gotag')
    },
    gomark: function () {
      this.dialog1 = false
      this.fileinited = false
      this.$bus.$emit('goSentence')
    },
    exit: function () {
      // console.log("exit")
      this.dialog1 = false
      this.$router.push('/')
    }
  },
  beforeRouteEnter(to, from, next) {
    next((vm) => {
      if (vm.$bus.authed) {
        vm.getInfo()
      } else {
        vm.$bus.$on('authready', vm.getInfo)
      }
    })
  },
  beforeRouteLeave(to, from, next) {
    if (!this.saved && this.init) {
      const answer = window.confirm('Do you really want to leave? You have unsaved changes!')
      if (answer) {
        next()
      } else {
        next(false)
      }
    } else {
      next()
    }
  }
}
</script>

<style scoped>
tr:hover {
  background: #FFFFFF !important;
}
</style>