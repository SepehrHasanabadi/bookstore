<template>
  <div>
    <b-alert v-if="wrongpass" show variant="danger">Your username or password is incorrect!</b-alert>
    <b-form @submit="onSubmit">
      <b-form-group
        id="username-group"
        label="Username:"
        label-for="username"
        prepend="@"
        description="Please enter your username."
      >
        <b-form-input
          id="username"
          v-model="form.username"
          placeholder="Username"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group id="password-group" label="Your Password" label-for="password">
        <b-form-input
          id="password"
          v-model="form.password"
          placeholder="Password"
          type="password"
          required
        ></b-form-input>
      </b-form-group>

      <b-button block type="submit" variant="primary">Submit</b-button>
    </b-form>
  </div>
</template>
<script>
  import { API, ROUTES } from '../constants'
  export default {
    name: 'Login',
    data() {
      return {
        form: {
          username: '',
          password: ''
        },
        wrongpass: false
      }
    },
    methods: {
      async onSubmit(event) {
        event.preventDefault()
        const bodyFormData = new FormData();
        bodyFormData.append('username', this.form.username);
        bodyFormData.append('password', this.form.password);
        this.$auth.loginWith('local', { data: bodyFormData }).then(response => {
          this.$auth.setUserToken(response.data.access_token, '');
          this.$router.push({ path: `/${ROUTES.HOME}` });
        }).catch(error => {
          if (error.response.status === 401) {
            this.wrongpass = true;
          }
        });
      }
    }
  }

</script>