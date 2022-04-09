<template>
  <div>
    <b-container class="my-4">
      <div v-if="error.statusCode === 404">
        <h2>404</h2>
        <h4>Страница не найдена</h4>
        <div class="my-4">
          <NuxtLink class="text-decoration-none" to="/">На главную</NuxtLink>
        </div>
      </div>

      <div v-else-if="error.statusCode === 500">
        <h2>500</h2>
        <h4>Ошибка сервера</h4>
      </div>

      <div v-else>
        <h4>Неизвестная ошибка</h4>
        <div class="my-4">
          <NuxtLink class="text-decoration-none" to="/">На главную</NuxtLink>
        </div>
      </div>
    </b-container>
  </div>
</template>

<script>
export default {
  layout: 'error',
  props: {
    error: {
      type: Object,
      default: () => {},
    },
  },
};
</script>
