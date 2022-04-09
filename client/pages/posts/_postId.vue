<template>
  <b-container>
    <div v-if="!loading" class="post-section my-4">
      <h3>{{ post.title }}</h3>
      <p class="subtitle">
        {{ post.author + ', ' + new Date(post.date_added).toLocaleString() }}
      </p>
      <p class="body">
        {{ post.body }}
      </p>
    </div>

    <div v-if="!loading" class="comments-section">
      <div class="title-wrapper d-flex justify-content-between mb-3">
        <p class="m-0 align-self-center">Комментарии</p>
        <b-button
          variant="link"
          class="text-decoration-none comment-toggle-button"
          @click="() => (commentInputShown = !commentInputShown)"
          >{{
            commentInputShown ? 'Закрыть поле ввода' : 'Написать комментарий'
          }}</b-button
        >
      </div>

      <div v-if="commentInputShown">
        <b-form
          v-if="$auth.loggedIn"
          class="mt-3 mb-5"
          @submit.stop.prevent="onComment"
        >
          <b-form-textarea
            v-model="currentComment"
            class="mb-3"
            placeholder="Пишите здесь..."
            required
            autofocus
          />
          <b-button type="submit" variant="primary">Отправить</b-button>
        </b-form>

        <p v-else class="mb-5">
          Пожалуйста,
          <nuxt-link to="/login" class="text-decoration-none"
            >войдите</nuxt-link
          >
          или
          <nuxt-link to="/register" class="text-decoration-none"
            >зарегистрируйтесь</nuxt-link
          >
          прежде чем оставлять комментарии
        </p>
      </div>

      <p v-if="comments.length === 0 && !commentInputShown" class="mb-5">
        Здесь пока нет комментариев. Будьте первым!
      </p>

      <div v-for="(comment, index) in comments" :key="index" class="my-3">
        <b-card
          :sub-title="
            comment.author +
            ', ' +
            new Date(comment.date_added).toLocaleString()
          "
        >
          <b-card-text class="comment-body">
            {{ comment.body }}
          </b-card-text>
        </b-card>
      </div>

      <infinite-loading
        v-if="!loading"
        :identifier="infiniteId"
        spinner="circles"
        class="my-3 text-muted"
        @infinite="infiniteHandler"
      >
        <div slot="no-more">Все комментарии загружены</div>
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
    </div>
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
      post: {
        id: Number,
        title: String,
        body: String,
        date_added: String,
        author: String,
      },
      comments: [],
      loading: true,
      commentInputShown: false,
      currentComment: '',
      currentCommentsOffset: 0,
      infiniteId: +new Date(),
    };
  },
  async mounted() {
    this.$nextTick(() => {
      this.$nuxt.$loading.start();
    });
    this.post = await this.$axios.$get(
      `/api/posts/${this.$route.params.postId}/`
    );
    const commentsResponse = await this.$axios.$get(
      `/api/comments/${this.$route.params.postId}/`
    );
    this.comments = commentsResponse.results;
    this.loading = false;
    this.$nuxt.$loading.finish();
  },
  methods: {
    async onComment() {
      try {
        await this.$axios.$post(`/api/comments/${this.$route.params.postId}/`, {
          body: this.currentComment,
        });
        const commentsResponse = await this.$axios.$get(
          `/api/comments/${this.$route.params.postId}/`
        );
        this.comments = commentsResponse.results;
        this.commentInputShown = false;
        this.currentComment = '';
        this.refreshInfiniteLoading();
      } catch (error) {
        if (error.response.status === 401) {
          this.$auth.reset();
          this.$router.push('/login');
        }
      }
    },
    async infiniteHandler($state) {
      this.currentCommentsOffset += 10;

      try {
        const response = await this.$axios.$get(
          `/api/comments/${this.$route.params.postId}/?limit=10&offset=${this.currentCommentsOffset}`
        );

        const newComments = response.results;

        if (!newComments.length) {
          $state.complete();
          return;
        }

        this.comments.push(...newComments);
        $state.loaded();
      } catch {
        $state.error();
      }
    },
    refreshInfiniteLoading() {
      this.currentCommentsOffset = 0;
      this.infiniteId += 1;
    },
  },
};
</script>

<style scoped>
.comments-section .title-wrapper {
  border-bottom: 1px solid lightgray;
}

.comments-section .title-wrapper > p {
  font-weight: bold;
  font-size: 15px;
}

.comment-toggle-button:focus,
.retry-button:focus {
  outline: none !important;
  box-shadow: none !important;
}

.post-section .body {
  white-space: pre-line;
}

.post-section .subtitle {
  font-weight: 500;
  color: #6c757d;
}
</style>
