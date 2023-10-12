<template>
  <div class="book-container">
    <div class="add-book">
      <b-form-input class="flex-2" v-model="search" id="search" type="search" placeholder="Search Books..."></b-form-input>
      <b-button @click="retrieveBooks" class="flex-1" variant="primary">Search</b-button>
      <b-button v-b-modal.book class="flex-1" block variant="outline-primary">Add Book</b-button>
    </div>
    <b-table 
      id="book-table"
      striped
      hover
      :items="getBookTableItems()"
      @row-clicked="openModal">
    </b-table>
    <b-pagination
      v-model="currentPage"
      :total-rows="total"
      :per-page="perPage"
      aria-controls="book-table"
    ></b-pagination>
    <b-modal 
      id="book"
      :title="modalTitle"
      size="lg" 
      ok-title="Save"
      @hidden="resetModal"
      @ok="saveBook">
      <form ref="form">
        <b-row class="my-1" key="book-name">
          <b-col sm="3">
            <label for="book-name">Book Name:</label>
          </b-col>
          <b-col sm="9">
            <b-form-input id="book-name" required :state="displayError ? selectedItem.name !== '' : null" v-model="selectedItem.name" type="text"></b-form-input>
            <b-form-invalid-feedback :state="!displayError || selectedItem.name !== ''">
              the Book name cannot be empty
            </b-form-invalid-feedback>
          </b-col>
        </b-row>
        <b-row class="my-1" key="page-number">
          <b-col sm="3">
            <label for="page-number">Number of pages:</label>
          </b-col>
          <b-col sm="9">
            <b-form-input 
              id="page-number"
              required
              type="number" 
              min=1
              :state="displayError ? selectedItem.number_page > 0 : null"
              v-model="selectedItem.number_page"></b-form-input>
            <b-form-invalid-feedback :state="!displayError || selectedItem.number_page > 0">
              the number of pages should be greater than zero
            </b-form-invalid-feedback>
          </b-col>
        </b-row>
        <b-row class="my-1" key="author">
          <b-col sm="3">
            <label for="page-number">Author:</label>
          </b-col>
          <b-col sm="9">
            <treeselect 
              v-model="selectedItem.author.id" 
              :multiple="false"
              :searchable="true"
              :options="options"
              />
            <b-form-invalid-feedback :state="!displayError || selectedItem.author.id !== null">
              Select the author of the book
            </b-form-invalid-feedback>
          </b-col>
        </b-row>
      </form>
    </b-modal>
  </div>
</template>
<script>
import cloneDeep from 'lodash/cloneDeep';
import Treeselect from '@riophae/vue-treeselect'
import '@riophae/vue-treeselect/dist/vue-treeselect.css'
import { getRequest, postRequest, putRequest } from '../request.js'
import { API } from '../constants'

const CREATE_BOOK = 'Create Book';
const UPDATE_BOOK = 'Update Book';

export default {
  name: 'Book',
  components: { Treeselect },
  created() {
    this.retrieveBooks();
    this.retrieveAuthorOptions();
  },
  data() {
    return {
      total: 0,
      items: [],
      selectedItem: {
        name: '',
        number_page: 0,
        author: {
          name: '',
          id: null
        }
      },
      modalTitle: CREATE_BOOK,
      search: '',
      currentPage: 1,
      perPage: 7,
      displayError: false,
      options: [],
      value: null
    }
  },
  watch: {
    currentPage() {
      this.retrieveBooks();
    }
  },
  methods: {
    openModal(item, index) {
      this.modalTitle = UPDATE_BOOK;
      this.selectedItem = cloneDeep(this.items[index]);
      this.$root.$emit('bv::show::modal', 'book')
    },
    retrieveBooks() {
      getRequest(this.$axios, this.$auth, API.BOOKS, {q: this.search, limit: this.perPage, skip: this.perPage * (this.currentPage-1)}).then(response => {
        const { items, total } = response.data;
        this.items = items;
        this.total = total;
      });
    },
    retrieveAuthorOptions() {
      getRequest(this.$axios, this.$auth, API.AUTHORS).then(response => {
        const { items, total } = response.data;
        this.options = items.map(item => ({
          id: item.id,
          label: item.name
        }));
      });
    },
    getBookTableItems() {
      return this.items.map(item => ({name: item.name, number_page: item.number_page, author: item.author.name}))
    },
    resetModal() {
      this.selectedItem = {
        name: '',
        number_page: 0,
        author: {
          name: '',
          id: null
        }
      },
      this.modalTitle = CREATE_BOOK;
    },
    saveBook(bvModalEvent) {
      if (!this.$refs.form.checkValidity() || !this.selectedItem.author.id) {
        this.displayError = true;
        bvModalEvent.preventDefault()
        return
      }
      if (!this.selectedItem.id) {
        postRequest(this.$axios, this.$auth, API.BOOKS, {
          name: this.selectedItem.name,
          number_page: this.selectedItem.number_page,
          author_id: this.selectedItem.author.id
        }).then(_ => this.retrieveBooks());
      } else {
        putRequest(this.$axios, this.$auth, `${API.BOOKS}/${this.selectedItem.id}`, {
          name: this.selectedItem.name,
          number_page: this.selectedItem.number_page,
          author_id: this.selectedItem.author.id
        }).then(_ => this.retrieveBooks());
      }
    }
  }
}
</script>

<style scoped>
.book-container {
 background: #eee;
 padding:2rem;
 border-radius: 8px;
}
.book-container .add-book {
  display: flex;
  width: 60%;
  gap: 10px;
  padding-block-end: 2rem;
}
.flex-2 {
  flex: 2;
}
.flex-1 {
  flex: 1;
}
</style>
