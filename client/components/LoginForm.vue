<template>
  <b-form @submit.stop.prevent="onSubmit">
    <b-form-group
      id="username-input-group"
      label="Имя пользователя:"
      label-for="username-input"
    >
      <b-form-input
        id="username-input"
        v-model="username"
        placeholder="Введите имя пользователя"
        required
        @input="() => (wrongCredentials = false)"
      ></b-form-input>
    </b-form-group>

    <b-form-group
      id="password-input-group"
      label="Пароль:"
      label-for="password-input"
    >
      <b-form-input
        id="password-input"
        v-model="password"
        type="password"
        placeholder="Введите пароль"
        required
        @input="() => (wrongCredentials = false)"
      ></b-form-input>
    </b-form-group>

    <b-form-invalid-feedback class="my-3" :state="!wrongCredentials">
      Неверное имя пользователя или пароль
    </b-form-invalid-feedback>

    <b-button type="submit" variant="primary" class="mt-3">Войти</b-button>
  </b-form>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
      wrongCredentials: false,
    };
  },
  methods: {
    async onSubmit(event) {
      const username = this.username.trim();
      const password = this.password.trim();

      try {
        await this.$auth.loginWith('local', {
          data: { username, password },
        });
      } catch (error) {
        if (error.response.status === 400) {
          this.wrongCredentials = true;
        }
      }
    },
  },
};
</script>
