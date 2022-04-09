<template>
  <b-container>
    <div v-for="(post, index) in posts" :key="index">
      <b-card
        :title="post.title"
        :sub-title="
          post.author + ', ' + new Date(post.date_added).toLocaleString()
        "
        class="my-4 card"
        @click="$router.push(`/posts/${post.id}`)"
      >
        <b-card-text>{{ post.body }}</b-card-text>
      </b-card>
    </div>

    <infinite-loading
      v-if="!loading"
      spinner="circles"
      class="my-3 text-muted"
      @infinite="infiniteHandler"
    >
      <div slot="no-more">Все посты загружены</div>
      <div slot="no-results"></div>
      <div slot="error" slot-scope="{ trigger }">
        <p class="mb-1">Ошибка при загрузке данных</p>
        <b-button
          size="sm"
          variant="link"
          class="text-decoration-none retry-button"
          @click="trigger"
        >
          Попробовать еще раз
        </b-button>
      </div>
    </infinite-loading>
  </b-container>
</template>

<script>
import InfiniteLoading from 'vue-infinite-loading';
export default {
  components: {
    InfiniteLoading,
  },
  data() {
    return {
      posts: [],
      currentPostsOffset: 0,
      loading: true,
    };
  },
  async mounted() {
    this.$nextTick(() => {
      this.$nuxt.$loading.start();
    });
    const response = await this.$axios.$get('/api/posts/');
    this.posts = response.results;
    this.loading = false;
    this.$nuxt.$loading.finish();
  },
  methods: {
    async infiniteHandler($state) {
      this.currentPostsOffset += 10;

      try {
        const response = await this.$axios.$get(
          `/api/posts/?limit=10&offset=${this.currentPostsOffset}`
        );

        const newPosts = response.results;

        if (!newPosts.length) {
          $state.complete();
          return;
        }

        this.posts.push(...newPosts);
        $state.loaded();
      } catch {
        $state.error();
      }
    },
  },
};
</script>

<style scoped>
.card:hover {
  cursor: pointer;
  background-color: rgb(249, 249, 249);
}

.retry-button:focus {
  outline: none !important;
  box-shadow: none !important;
}
</style>
