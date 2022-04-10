<template>
  <div class="mt-5 d-flex justify-content-center">
    <b-card class="card">
      <template #header>
        <h6 class="mb-0">Создание аккаунта</h6>
      </template>
      <register-form @successfulRegister="successfulRegister" />
    </b-card>
  </div>
</template>

<script>
import RegisterForm from '../components/RegisterForm.vue';
export default {
  components: { RegisterForm },
  methods: {
    successfulRegister() {
      this.$router.push('/login');
    },
  },
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
