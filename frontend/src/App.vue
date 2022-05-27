<template>
  <div class="main">
    <div class="search-bar items-center">
      <q-field borderless class="search-input">
        <div class="col">
          <q-input v-model="query" outlined clearable clear-icon="close" placeholder="search" ref="query_input"
                   @keydown.enter="search" @focus="file = null">
            <template v-slot:prepend>
              <q-file filled class="file-input" v-model="file" v-show="file"/>
            </template>
            <template v-slot:append>
              <q-btn flat icon="image_search" @click="this.$refs.query_image.pickFiles()">
                <q-tooltip>search by image</q-tooltip>
              </q-btn>
              <q-btn flat icon="add">
                <q-tooltip>add filters</q-tooltip>
                <q-menu>
                  <q-list bordered separator>
                    <q-item clickable v-ripple @click="tag_filter_show = true">
                      <q-item-section>Tag Filter {{ tag_filter_desc }}</q-item-section>
                    </q-item>

                    <q-item clickable v-ripple>
                      <q-item-section>Color Filter</q-item-section>
                      <q-menu anchor="top left" self="top right">
                        <q-color v-model="color_hex" no-header-tabs no-footer default-view="palette"
                                 :palette="['#f44336', '#ff9800', '#ffeb3b', '#4caf50',
                                 '#00bcd4', '#2196f3', '#9c27b0', '#e91e63',
                                 '#ffffff', '#9e9e9e', '#000000', '#5d4037']"/>
                        <q-item clickable @click="color_hex = ''">
                          <q-item-section>Disable Color Filter</q-item-section>
                        </q-item>
                      </q-menu>
                    </q-item>

                    <q-item clickable v-ripple>
                      <q-item-section>Size Filter</q-item-section>
                      <q-menu anchor="top left" self="top right">
                        <q-list bordered separator>
                          <q-item>
                            <q-checkbox v-model="pixels" val="xs" label="extra small" size="xs"/>
                          </q-item>
                          <q-item>
                            <q-checkbox v-model="pixels" val="s" label="small" size="xs"/>
                          </q-item>
                          <q-item>
                            <q-checkbox v-model="pixels" val="m" label="medium" size="xs"/>
                          </q-item>
                          <q-item>
                            <q-checkbox v-model="pixels" val="l" label="large" size="xs"/>
                          </q-item>
                          <q-item>
                            <q-checkbox v-model="pixels" val="xl" label="extra large" size="xs"/>
                          </q-item>
                        </q-list>
                      </q-menu>
                    </q-item>
                  </q-list>
                </q-menu>
              </q-btn>
              <q-btn flat icon="search" @click="search">
                <q-tooltip>search</q-tooltip>
              </q-btn>
            </template>
          </q-input>
        </div>
      </q-field>
    </div>

    <q-infinite-scroll @load="loadMore" :disable="continue_from === -1">
      <div class="row items-start justify-around q-gutter-y-xl search-result">
        <q-card v-for="(g, k) in gallery" :key="k" class="image-card">
          <img :src="parseImgUrl(g.image_id)" alt="">

          <q-card-section class="q-pa-s q-gutter-xs image-tag">
            <q-badge outline color="primary" v-for="t in g.tags" :key="t" :label="t" @click="searchByTag(t)"/>
          </q-card-section>

          <q-card-actions>
            <q-space/>
            <q-btn flat dense icon="saved_search" color="grey" @click="searchByImage(g.image_id)">
              <q-tooltip>search similar</q-tooltip>
            </q-btn>
            <q-btn flat dense :icon="g.expanded ? 'keyboard_arrow_up' : 'keyboard_arrow_down'" color="grey"
                   @click="g.expanded = !g.expanded">
              <q-tooltip> {{ g.expanded ? "hide description" : "show description" }}</q-tooltip>
            </q-btn>
          </q-card-actions>

          <q-slide-transition>
            <div v-show="g.expanded">
              <q-separator/>
              <q-card-section class="image-desc">{{ g.desc }}</q-card-section>
            </div>
          </q-slide-transition>
        </q-card>
      </div>
      <template v-slot:loading>
        <div class="row justify-center q-my-md">
          <q-spinner-dots color="primary" size="40px"/>
        </div>
      </template>
    </q-infinite-scroll>

    <q-dialog v-model="tag_filter_show">
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

    <!-- this q-file is bounded to the one in search-input, used to evoke pickFiles() method -->
    <q-file accept=".jpg,image/" ref="query_image" v-model="file" v-show="false"/>
  </div>
</template>

<script>
import axios from "axios";
import {useQuasar} from "quasar"

function sleep(ms) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  })
}

export default {
  name: "MainLayout",

  methods: {
    search() {
      this.continue_from = -1;
      const path = process.env.VUE_APP_BACKEND_URL + "/search";
      axios.get(path, {
        params: {query: this.query, tags: this.tags.join(","), pixels: this.pixels.join(","), color: this.color}
      })
          .then(async resp => {
            if (resp.status === 200) {
              Array.from(resp.data.data).forEach(each => {
                each.expanded = false;
              });
              this.gallery = resp.data.data;
              window.scrollTo(0, 0);
              if (this.gallery.length === 0) {
                this.noResultAlert();
              } else {
                await sleep(2000);  // wait for render to avoid immediate "load more"
                this.continue_from = resp.data.continue_from;
              }
            }
          })
    },
    searchByTag(query) {
      this.query = "";
      this.tags = [query];
      this.file = null;
      this.search();
    },
    searchByImage(query) {
      this.query = "";
      this.continue_from = -1;
      const path = process.env.VUE_APP_BACKEND_URL + "/search";
      const form_data = new FormData();
      form_data.append("query", query);
      axios.post(path, form_data)
          .then(resp => {
            if (resp.status === 200) {
              Array.from(resp.data.data).forEach(each => {
                each.expanded = false;
              });
              this.gallery = resp.data.data;
              window.scrollTo(0, 0);
            }
          })
    },
    loadMore(index, done) {
      if (this.continue_from === -1) {
        done();
        return;
      }
      const continue_from = this.continue_from;
      this.continue_from = -1;
      const path = process.env.VUE_APP_BACKEND_URL + "/search";
      axios.get(path, {
        params: {
          query: this.query, tags: this.tags.join(","), pixels: this.pixels.join(","), color: this.color,
          continue_from: continue_from
        }
      })
          .then(async resp => {
            if (resp.status === 200) {
              Array.from(resp.data.data).forEach(each => {
                each.expanded = false;
              });
              this.gallery.push(...resp.data.data);
              await sleep(2000);  // wait for render to avoid immediate "load more"
              if (resp.data.data.length >= 0) {
                this.continue_from = resp.data.continue_from;
              }
            }
            done();
          })
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

  watch: {
    "color_hex": {
      handler() {
        this.color = {
          "#f44336": "red", "#ff9800": "orange", "#ffeb3b": "yellow", "#4caf50": "green",
          "#00bcd4": "teal", "#2196f3": "blue", "#9c27b0": "purple", "#e91e63": "pink",
          "#ffffff": "white", "#9e9e9e": "grey", "#000000": "black", "#5d4037": "brown"
        }[this.color_hex];
      }
    },
    "file": {
      handler() {
        if (this.file === null) return;
        this.$refs.query_input.blur();
        this.searchByImage(this.file);
      }
    }
  },

  data() {
    return {
      query: "",
      file: null,
      new_tag: "",
      tags: [],
      pixels: [],
      color_hex: "",
      color: "",
      gallery: [],
      tag_filter_show: false,
      tag_filter_desc: "",
      size_filter_desc: "",
      continue_from: -1,
    }
  },

  setup() {
    const $q = useQuasar();
    return {
      noResultAlert() {
        $q.notify({message: "No Image Found", position: "center", color: "negative", icon: "error", timeout: 2000});
      }
    }
  },

  created() {
    document.title = "ImgSE | Search Images";
  }
}
</script>

<style lang="scss">
@import "./styles/app.scss";
</style>