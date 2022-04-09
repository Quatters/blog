<template>
  <b-form @submit.stop.prevent="$emit('submit', { title, body })">
    <b-form-group>
      <b-form-input
        v-model="title"
        placeholder="Заголовок"
        required
      ></b-form-input>
    </b-form-group>

    <b-form-group>
      <b-form-textarea
        v-model="body"
        placeholder="Пишите здесь"
        rows="8"
        max-rows="20"
        required
      ></b-form-textarea>
    </b-form-group>

    <b-button type="submit" variant="primary">Создать</b-button>
  </b-form>
</template>

<script>
export default {
  data() {
    return {
      title: '',
      body: '',
    };
  },
  methods: {
    onSubmit() {},
  },
};
</script>

<style></style>
