<template>
  <div class="author-container">
    <div class="add-author">
      <b-form-input class="flex-2" v-model="search" id="search" type="search" placeholder="Search Author..."></b-form-input>
      <b-button @click="retrieveAuthors" class="flex-1" variant="primary">Search</b-button>
      <b-button v-b-modal.author class="flex-1" block variant="outline-primary">Add Author</b-button>
    </div>
    <b-table 
      id="author-table"
      striped
      hover
      :items="getAuthorTableItems()"
      @row-clicked="openModal">
    </b-table>
    <b-pagination
      v-model="currentPage"
      :total-rows="total"
      :per-page="perPage"
      aria-controls="author-table"
    ></b-pagination>
    <b-modal 
      id="author"
      :title="modalTitle"
      size="lg" 
      ok-title="Save"
      @hidden="resetModal"
      @ok="saveAuthor">
      <form ref="form">
        <b-row class="my-1" key="author-name">
          <b-col sm="2">
            <label for="author-name">Author Name:</label>
          </b-col>
          <b-col sm="10">
            <b-form-input id="author-name" required :state="displayError ? selectedItem.name !== '' : null" v-model="selectedItem.name" type="text"></b-form-input>
            <b-form-invalid-feedback :state="!displayError || selectedItem.name !== ''">
              the Author name cannot be empty
            </b-form-invalid-feedback>
          </b-col>
        </b-row>
        <b-button variant="outline-primary" size="sm" class="mb-2" @click="addBook()">
          Add Book
        </b-button>
        <b-table striped hover :items="getBooksTableItems(selectedItem?.books)">
          <template #cell(name)="row">
            <b-input 
              v-if="selectedItem.books[row.index]"
              required
              v-model="selectedItem.books[row.index].name"
              :state="displayError ? selectedItem.books[row.index]?.name !== '' : null"
              ></b-input>
            <b-form-invalid-feedback 
              :state="!displayError ||selectedItem.books[row.index]?.name !== ''">
              the book name cannot be empty
            </b-form-invalid-feedback>
          </template>
          <template #cell(number_page)="row">
            <b-input 
              v-if="selectedItem.books[row.index]"
              required
              type="number" 
              min=1
              v-model="selectedItem.books[row.index].number_page"
              :state="displayError ? selectedItem.books[row.index]?.number_page > 0 : null"
              ></b-input>
            <b-form-invalid-feedback 
              :state="!displayError || selectedItem.books[row.index]?.number_page > 0">
              the number of pages should be greater than zero
            </b-form-invalid-feedback>
          </template>
          <template #cell(actions)="row">
            <b-button size="sm" class="mr-1" @click="deleteBookFromAuthor(row)">
              Delete
            </b-button>
          </template>
        </b-table>
      </form>
    </b-modal>
  </div>
</template>
<script>
import cloneDeep from 'lodash/cloneDeep';
import { getRequest, postRequest, putRequest } from '../request.js'
import { API } from '../constants'

const CREATE_AUTHOR = 'Create Author';
const UPDATE_AUTHOR = 'Update Author';
const BOOK_ITEM = {
  name: '',
  number_page: 0
}

export default {
  name: 'Author',
  created() {
    this.retrieveAuthors();
  },
  data() {
    return {
      total: 0,
      items: [],
      selectedItem: {
        name: '',
        books: [{...BOOK_ITEM}]
      },
      modalTitle: CREATE_AUTHOR,
      search: '',
      currentPage: 1,
      perPage: 7,
      displayError: false,
    }
  },
  watch: {
    currentPage() {
      this.retrieveAuthors();
    }
  },
  methods: {
    openModal(item, index) {
      this.modalTitle = UPDATE_AUTHOR;
      this.selectedItem = cloneDeep(this.items[index]);
      this.$root.$emit('bv::show::modal', 'author')
    },
    retrieveAuthors() {
      getRequest(this.$axios, this.$auth, API.AUTHORS, {q: this.search, limit: this.perPage, skip: this.perPage * (this.currentPage-1)}).then(response => {
        const { items, total } = response.data;
        this.items = items;
        this.total = total;
      });
    },
    getAuthorTableItems() {
      return this.items.map(item => ({name: item.name, number_of_books: item.books.length}))
    },
    getBooksTableItems(books) {
      if (books){
        return books.map(item => ({ name: item.name, number_page: item.number_page, actions: {} }))
      }
    },
    deleteBookFromAuthor(row) {
      this.selectedItem.books.splice(row.index, 1);
    },
    resetModal() {
      this.selectedItem = {
        name: '',
        books: [{...BOOK_ITEM}]
      },
      this.modalTitle = CREATE_AUTHOR;
    },
    addBook() {
      this.selectedItem.books.push({...BOOK_ITEM})
    },
    saveAuthor(bvModalEvent) {
      if (!this.$refs.form.checkValidity()) {
        this.displayError = true;
        bvModalEvent.preventDefault()
        return
      }
      if (!this.selectedItem.id) {
        postRequest(this.$axios, this.$auth, API.AUTHORS, {name: this.selectedItem.name}).then(response => {
          postRequest(this.$axios, this.$auth, API.BULK_BOOKS, {
            author_id: response.data.id,
            books: this.selectedItem.books
          }).then(_ => this.retrieveAuthors())
        });
      } else {
        putRequest(this.$axios, this.$auth, `${API.AUTHORS}/${this.selectedItem.id}`, {name: this.selectedItem.name}).then(response => {
          postRequest(this.$axios, this.$auth, API.BULK_BOOKS, {
            author_id: this.selectedItem.id,
            books: this.selectedItem.books
          }).then(_ => this.retrieveAuthors())
        });
      }
    }
  }
}
</script>

<style scoped>
.author-container {
 background: #eee;
 padding:2rem;
 border-radius: 8px;
}
.author-container .add-author {
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
