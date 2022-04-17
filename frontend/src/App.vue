<template>
  <div class="main">
    <div class="search-bar items-center">
      <q-field borderless class="search-input">
        <div class="col">
          <q-input v-model="this.query" outlined clearable clear-icon="close" placeholder="search"
                   @keydown.enter.prevent="search">
            <q-btn flat icon="search" @click="search"/>
          </q-input>
        </div>
      </q-field>
    </div>
    <div class="row items-start justify-around q-gutter-y-xl search-result">
      <q-card v-for="(g, k) in gallery" :key="k" class="image-card">
        <img :src="parseImgUrl(g.image_id)" alt="">
        <q-card-section class="q-pa-md q-gutter-md image-tag">
          <q-badge outline color="primary" v-for="t in g.tags" :key="t" :label="t"/>
        </q-card-section>
        <q-card-actions>
          <q-space/>
          <q-btn flat :icon="g.expanded ? 'keyboard_arrow_up' : 'keyboard_arrow_down'" color="grey"
                 @click="g.expanded = !g.expanded"/>
        </q-card-actions>
        <q-slide-transition>
          <div v-show="g.expanded">
            <q-separator/>
            <q-card-section class="image-desc">
              {{ g.desc }}
            </q-card-section>
          </div>
        </q-slide-transition>
      </q-card>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'MainLayout',

  methods: {
    search() {
      const path = process.env.VUE_APP_BACKEND_URL + "/search";
      axios.get(path, {params: {query: this.query}})
          .then(resp => {
            if (resp.status === 200) {
              Array.from(resp.data.data).forEach(each => {
                each.expanded = false;
              });
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