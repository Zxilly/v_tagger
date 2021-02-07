<template>
  <div>
    <v-row
        justify="center"
        class="mt-12"
    >
      <v-col
          cols="8"
          class="d-flex justify-center pa-6"
      >
        <v-card
            width="50%"
        >
          <v-card-title>
            请选择视频文件
          </v-card-title>
          <v-card-text>
            <v-file-input
                accept="video/mp4"
                :label="this.filetip"
                outlined
                multiple
                @change="videoTraverse"
                ref="file"
                messages="请一次性多选选中所有视频文件"
            ></v-file-input>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row
        justify="center"
    >
      <v-col
          cols="8"
          class="d-flex justify-center pa-6"
      >
        <v-card
            width="50%"
            v-show="filelist.length>0"
        >
          <v-card-actions
              class="px-8 pt-4"
          >
            <v-btn
                elevation="0"
                :loading="btn_pending"
                @click="upload"
            >
              UPLOAD
            </v-btn>
          </v-card-actions>
          <v-card-text>
            <v-simple-table>
              <template v-slot:default>
                <thead>
                <tr>
                  <th class="text-left">
                    MD5
                  </th>
                  <th class="text-left">
                    Length
                  </th>
                </tr>
                </thead>
                <tbody>
                <tr
                    v-for="item in filelist"
                    :key="item.hash"
                >
                  <td>{{ item.hash }}</td>
                  <td>{{ item.length }}</td>
                </tr>
                </tbody>
                <tfoot>
                <tr>
                  <td>{{ tfoot }}</td>
                </tr>
                </tfoot>
              </template>
            </v-simple-table>
          </v-card-text>
        </v-card>
      </v-col>

    </v-row>
    <video
        :src="bloburl"
        ref="lengthplayer"
        style="display: none"
        id="vid"
    >
    </video>
  </div>

</template>

<script>
import md5c from "js-md5";
import {apiurl} from "@/config";

export default {
  name: "add",
  data: () => ({
    filetip: "视频",
    filelist: [],
    bloburl: null,
    tfoot: '',
    btn_pending: false
  }),
  methods: {
    videoTraverse: async function (files) {
      if (this.filelist.length !== 0) {
        this.filelist = []
      }
      let success = 0
      let errorcount = 0
      let all = files.length
      for (const file of files) {
        this.tfoot = `已处理 ${success} / ${all} 个，忽略 ${errorcount} 个`
        if (file.type !== 'video/mp4') {
          errorcount++
          continue
        }
        await this.oneVideoHandle(file)
        success++
      }
      this.tfoot = `已处理 ${success} / ${all} 个，忽略 ${errorcount} 个`
    },
    oneVideoHandle: async function (file) {
      const md5 = await this.md5Compute(file)
      const length = await this.videoDuration(file)
      console.log('md5:' + md5)
      console.log('length:' + length)
      this.filelist.push({
        'hash': md5,
        'length': length
      })
      return true
    },
    md5Compute: function (file) {
      return new Promise(resolve => {
        let fileReader = new FileReader()
        let blobSlice = File.prototype.slice
        fileReader.readAsArrayBuffer(blobSlice.call(file, 0, 200 * 1024))
        fileReader.onload = (e) => {
          const md5 = md5c.hex(e.target.result)
          resolve(md5)
        }
      })
    },
    videoDuration: function (file) {
      return new Promise((resolve => {
        this.bloburl = window.URL.createObjectURL(file)
        let videoDOM = document.getElementById('vid')
        videoDOM.onloadedmetadata = () => {
          let length = videoDOM.duration.toFixed(1)
          resolve(length)
        }
      }))
    },
    upload: function () {
      this.btn_pending = true
      this.$bus.$authedAxios.post(apiurl + '/video/add',
          {videos: this.filelist}
      ).then((resp) => {
        this.btn_pending = false
        let data = resp.data
        if (data[0] === 11) {
          this.$bus.$emit('snackbar', [data[1], 'success'])
        } else {
          this.$bus.$emit('snackbar', ['Internal Error.', 'error'])
        }
      }).catch((e) => {
        console.log(e)
      })
    }
  }
}
</script>

<style scoped>

</style>