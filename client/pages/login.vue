<template>
  <div class="mt-5 d-flex justify-content-center">
    <b-card class="card">
      <template #header>
        <h6 class="mb-0">Вход в аккаунт</h6>
      </template>
      <login-form />
    </b-card>
  </div>
</template>

<script>
import LoginForm from '../components/LoginForm.vue';
export default {
  components: { LoginForm },
  mounted() {
    if (this.$auth.loggedIn) this.$router.push('/');
  },
};
</script>

<style scoped>
.card {
  max-width: 32rem;
  width: 100%;
}
</style>
