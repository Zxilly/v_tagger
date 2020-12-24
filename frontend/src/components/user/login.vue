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
        <v-card-title>登录</v-card-title>
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
                type="password"
                :rules="[rules.required]"
            ></v-text-field>
          </v-form>
          <div>
            <v-btn
                @click="login"
                text
            >
              Log in
            </v-btn>
            <v-btn
                @click="jump"
                text
                class="float-right"
            >
              Sign up
            </v-btn>
          </div>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "login",
  data: () => ({
    valid: true,
    sn_value: '',
    password: '',
    rules: {
      required: value => !!value || 'Required.',
      length: value => value.length === 10 || 'Student number should be 10 characters.'
    }
  }),
  methods: {
    login: function () {
      if (this.$refs.form.validate()) {
        let authcode = this.$md5(this.password)
        this.$bus.$emit('login', [this.sn_value, authcode])
      }
    },
    jump:  function () {
      this.$router.push('/user/reg')
    }
  }
}
</script>

<style scoped>

</style>