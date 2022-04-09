<template>
  <b-container class="mb-5 mt-4">
    <p class="header-text">Создание поста</p>
    <create-post-form @submit="onCreate" />
  </b-container>
</template>

<script>
import CreatePostForm from '../../components/CreatePostForm.vue';
export default {
  components: { CreatePostForm },
  mounted() {
    if (!this.$auth.loggedIn) {
      this.$router.push('/login');
    }
  },
  methods: {
    async onCreate(post) {
      const response = await this.$axios.post('/api/posts/', post);
      if (response.status === 201) {
        this.$router.push('/posts');
      }
    },
  },
};
</script>

<style scope>
.header-text {
  border-bottom: 1px solid lightgray;
  font-weight: bold;
  font-size: 16px;
  line-height: 2rem;
}
</style>
