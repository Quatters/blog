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
        placeholder="Придумайте имя пользователя"
        required
        @input="() => (errors.username = [])"
      ></b-form-input>

      <b-form-invalid-feedback
        v-for="(error, index) in errors.username"
        :key="index"
        :state="!errors"
      >
        {{ error }}
      </b-form-invalid-feedback>
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
        placeholder="Придумайте пароль"
        required
        @input="() => (errors.password = [])"
      ></b-form-input>

      <b-form-invalid-feedback
        v-for="(error, index) in errors.password"
        :key="index"
        :state="!errors"
      >
        {{ error }}
      </b-form-invalid-feedback>
    </b-form-group>

    <b-form-group>
      <b-form-input
        id="repeat-password-input"
        v-model="repeatPassword"
        type="password"
        placeholder="Введите пароль еще раз"
        required
        @input="() => (errors.repeat_password = [])"
      ></b-form-input>

      <b-form-invalid-feedback
        v-for="(error, index) in errors.repeat_password"
        :key="index"
        :state="!errors"
      >
        {{ error }}
      </b-form-invalid-feedback>
    </b-form-group>

    <b-button type="submit" variant="primary" class="mt-3"
      >Зарегистрироваться</b-button
    >
  </b-form>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
      repeatPassword: '',
      errors: [],
    };
  },
  methods: {
    async onSubmit(event) {
      const username = this.username.trim();
      const password = this.password.trim();
      const repeatPassword = this.repeatPassword.trim();

      try {
        await this.$axios.post('/api/auth/register/', {
          username,
          password,
          repeat_password: repeatPassword,
        });
        this.$emit('successfulRegister');
      } catch (error) {
        if (error.response.status === 400) {
          this.errors = error.response.data;
        }
      }
    },
  },
};
</script>
