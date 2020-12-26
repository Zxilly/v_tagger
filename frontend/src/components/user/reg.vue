<template>
  <v-row justify="center" align="center" style="height: 70vh">
    <v-col
        cols="12"
        sm="8"
        md="6"
        lg="4"
        class="my-12"
    >
      <v-card class="pa-3">
        <v-card-title>注册</v-card-title>
        <v-card-text
            class="d-flex flex-column"
        >
          <v-form
              ref="form"
              v-model="valid"
              lazy-validation
          >
            <v-text-field
                label="学号"
                v-model="sn_value"
                :rules="[rules.required,rules.length]"
            ></v-text-field>
            <v-text-field
                label="密码"
                v-model="password"
                :rules="[rules.required]"
            ></v-text-field>
            <v-text-field
                label="重复密码"
                v-model="password2"
                :rules="[rules.required]"
            ></v-text-field>
          </v-form>
          <v-btn
              @click="reg"
              text
          >
            Register
          </v-btn>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "reg",
  data: () => ({
    valid: true,
    sn_value: '',
    password: '',
    password2: '',
    rules: {
      required: value => !!value || 'Required.',
      length: value => value.length === 10 || 'Student number should be 10 characters.',
    }
  }),
  methods: {
    reg: function () {
      if (this.$refs.form.validate()) {
        if (this.password === this.password2) {
          let authcode = this.$md5(this.password2)
          this.$bus.$emit('reg', [this.sn_value, authcode])
        }
      }
    }
  }
}
</script>

<style scoped>

</style>