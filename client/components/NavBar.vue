<template>
  <b-navbar toggleable sticky variant="light" type="light" class="shadow-sm">
    <b-container>
      <b-navbar-brand to="/">Блог</b-navbar-brand>
      <b-nav class="mr-auto">
        <b-nav-item to="/">Главная</b-nav-item>
        <b-nav-item v-if="$auth.loggedIn" to="/posts/create"
          >Создать пост</b-nav-item
        >
      </b-nav>

      <b-nav v-if="$auth.loggedIn">
        <b-nav-text class="align-self-center mx-2">{{ $auth.user }}</b-nav-text>
        <b-button class="text-decoration-none" variant="link" @click="logout"
          >Выйти</b-button
        >
      </b-nav>

      <b-nav v-else>
        <b-nav-item to="/register">Регистрация</b-nav-item>
        <b-nav-item to="/login">Войти</b-nav-item>
      </b-nav>
    </b-container>
  </b-navbar>
</template>

<script>
export default {
  methods: {
    logout() {
      this.$auth.logout();
    },
  },
};
</script>
