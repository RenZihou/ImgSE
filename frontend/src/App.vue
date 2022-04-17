<template>
  <div class="main">
    <div class="search-bar items-center">
      <q-field borderless class="search-input">
        <div class="col">
          <q-input v-model="query" outlined clearable clear-icon="close" placeholder="search"
                   @keydown.enter.prevent="search">
            <q-btn flat icon="add">
              <q-menu>
                <q-list bordered separator>
                  <q-item clickable v-ripple @click="add_tag = true">
                    <q-item-section>Tag Filter {{ tag_filter_desc }}</q-item-section>
                  </q-item>

                  <q-item clickable v-ripple>
                    <q-item-section>Color Filter</q-item-section>
                  </q-item>

                  <q-item clickable v-ripple>
                    <q-item-section>size Filter</q-item-section>
                  </q-item>
                </q-list>
              </q-menu>
            </q-btn>
            <q-btn flat icon="search" @click="search"/>
          </q-input>
        </div>
      </q-field>
    </div>

    <div class="row items-start justify-around q-gutter-y-xl search-result">
      <q-card v-for="(g, k) in gallery" :key="k" class="image-card">
        <img :src="parseImgUrl(g.image_id)" alt="">

        <q-card-section class="q-pa-s q-gutter-xs image-tag">
          <q-badge outline color="primary" v-for="t in g.tags" :key="t" :label="t"/>
        </q-card-section>

        <q-card-actions>
          <q-space/>
          <q-btn flat dense :icon="g.expanded ? 'keyboard_arrow_up' : 'keyboard_arrow_down'" color="grey"
                 @click="g.expanded = !g.expanded"/>
        </q-card-actions>

        <q-slide-transition>
          <div v-show="g.expanded">
            <q-separator/>
            <q-card-section class="image-desc">{{ g.desc }}</q-card-section>
          </div>
        </q-slide-transition>
      </q-card>
    </div>

    <q-dialog v-model="add_tag">
      <q-card class="tag-card">
        <q-card-section>
          <div class="text-h6">Tag Filter</div>
        </q-card-section>
        <q-card-section class="row q-pa-s q-gutter-xs image-tag">
          <q-badge flat v-for="(t, k) in tags" :key="k">
            {{ t }}
            <q-btn flat dense icon="close" size="xs" @click="removeTag(k)"/>
          </q-badge>
        </q-card-section>
        <q-card-section class="q-pt-none">
          <q-input dense v-model="new_tag" autofocus clearable @keyup.enter="addTag"/>
        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn flat label="cancel" v-close-popup @click="new_tag = ''"/>
          <q-btn flat label="ok" v-close-popup @click="addTag"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'MainLayout',

  methods: {
    search() {
      const path = process.env.VUE_APP_BACKEND_URL + "/search";
      axios.get(path, {params: {query: this.query, tags: this.tags.join(",")}})
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
    },
    addTag() {
      if (this.new_tag.length > 0) {
        this.tags.push(this.new_tag);
      }
      this.new_tag = "";
      if (this.tags.length === 0) {
        this.tag_filter_desc = "";
      } else {
        this.tag_filter_desc = "(" + this.tags.length + " tags applied)";
      }
    },
    removeTag(key) {
      this.tags.splice(key, 1);
      if (this.tags.length === 0) {
        this.tag_filter_desc = "";
      } else {
        this.tag_filter_desc = "(" + this.tags.length + " tags applied)";
      }
    }
  },

  data() {
    return {
      query: "",
      new_tag: "",
      tags: [],
      gallery: [],
      add_tag: false,
      tag_filter_desc: "",
    }
  },

}
</script>

<style lang="scss">
@import "./styles/app.scss";
</style>