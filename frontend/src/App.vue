<template>
  <div class="search-bar">
    <q-field borderless class="search-input">
      <q-input v-model="this.query" rounded outlined clearable clear-icon="close" placeholder="search"/>
      <q-btn rounded flat icon="search" @click="search"/>
    </q-field>
  </div>
  <div class="search-result q-pa-md row items-start q-gutter-md">
    <q-card v-for="(g, k) in gallery" :key="k" class="image-card">
      <img :src="parseImgUrl(g.image_id)" alt="">
      <q-card-section>
        <div class="image-desc">
          {{ g.desc }}
        </div>
      </q-card-section>
    </q-card>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LayoutDefault',

  components: {
    // HelloWorld
  },

  methods: {
    search() {
      const path = process.env.VUE_APP_BACKEND_URL + "/search";
      axios.get(path, {params: {query: this.query}})
          .then(resp => {
            if (resp.status === 200) {
              this.gallery = resp.data.data;
            } else {
              console.log(resp.status);
            }
          })
          .catch(err => {
            console.log(err);
          });
    },
    parseImgUrl(image_id) {
      return process.env.VUE_APP_BACKEND_URL + "/image/" + image_id;
    }
  },

  data() {
    return {
      query: '',
      gallery: [],
    }
  },

}
</script>

<style lang="scss">
@import "./styles/app.scss";
</style>