<!-- Vue SFC -->
<template>
  <div id="app">
    <header>
      <b-navbar type="dark" variant="dark">
        <b-navbar-brand>PORTAL</b-navbar-brand>
        <b-navbar-nav>
          <b-nav-item v-for="item in items" :key="item.key"><NuxtLink :to="{ path: ROUTES.HOME, query: { page: item.path }}">{{ item.label }}</NuxtLink></b-nav-item>
        </b-navbar-nav>
        <b-navbar-nav>
          <b-nav-item @click="logout">logout</b-nav-item>
        </b-navbar-nav>
      </b-navbar>
    </header>
    <component class="page-container" :is="items[selected].component" />
  </div>
</template>

<script>
  import { ROUTES } from './../constants'
  import Author from '../components/Author.vue'
  import Book from '../components/Book.vue'

  const items = [{
    key: 'authors',
    path: ROUTES.AUTHORS,
    label: 'Authors',
    component: Author
  }, {
    key: 'books',
    path: ROUTES.BOOKS,
    label: 'Books',
    component: Book
  }];

  export default {
    auth: true,
    data() {
      return {
        ROUTES,
        items,
      }
    },
    methods: {
      async logout() {
        await this.$auth.setUserToken('', '');
        location.reload();
      }
    },
    computed: {
      selected() {
        const index = this.items.findIndex((item) => item.path === this.$route.query.page)
        if (index === -1) {
          return 0
        }
        return index
      }
    }
  }
</script>
<style scoped>
.page-container {
  margin-inline: 10rem;
  margin-block: 3rem;
}
</style>