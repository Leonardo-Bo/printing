<template>

    <h4 class="inline-h mb-4">Edit News</h4>

    <div class="container-upload">
        <form @submit.prevent="editNews">

            <div class="form-group mb-3">
                <label class="mb-1">Title*</label>
                <input
                    type="text"
                    class="form-control"
                    id="title"
                    v-model="news_copy.title">
                <template v-if="isReady">
                    <char-count
                        :input="news_copy.title"
                        :inputLen="100"
                        :inputWarn="25"
                    />
                </template>
            </div>

            <div class="form-group">
                <label class="mb-1">Content</label>
                <vue-simplemde v-model="news_copy.content" ref="markdownEditor" />
            </div>

            <div class="row">
                <div class="col-md-6">
                    <label class="mb-1">Publication date*</label>
                    <input 
                        type="date" 
                        class="form-control" 
                        v-model="news_copy.publicated_at"
                    >
                </div>
                <div class="col-md-6">
                    <label class="mb-1">Show author</label>
                    <br>
                    <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" value="Yes" v-model="showAuthor">
                        <label class="form-check-label">Yes</label>
                    </div>
                    <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" value="No" v-model="showAuthor">
                        <label class="form-check-label">No</label>
                    </div>

                </div>
            </div>

            <div class="mt-4" align="right">
                <router-link 
                    type="button" 
                    class="btn btn-sm btn-outline-secondary ms-1" 
                    to="/settings/news"
                >Cancel
                </router-link>
                <button 
                    type="submit" 
                    class="btn btn-sm btn-outline-primary ms-1">Edit News
                </button>
            </div>
        </form>
    </div>

    <hr style="margin-top: 40px;">

    <images-component
        :model="news"
        :callback="getNews"
        :endpoint="'news-images'"
        :base_ref="'images_news'"
    >
    </images-component>

    <hr style="margin-top: 40px;">

    <cover-component
        :model="news"
        :callback="getNews"
        :endpoint="'news-cover'"
        :base-ref="'cover_news'"
        :width="300"
        :height="300"
        :aspect-ratio="1/1"
    >
    </cover-component>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

import { createToast } from "mosha-vue-toastify"
import VueSimplemde from 'vue-simplemde'

import ImagesComponent from '@/components/images/ImagesComponent.vue'
import CoverComponent from '@/components/images/CoverComponent.vue'
import CharCount from '@/components/CharCount.vue'

import { useParamStore } from '@/stores/ParamStore'
import { useUserStore } from '@/stores/UserStore'
import { useRoute, useRouter } from 'vue-router';

const paramStore = useParamStore()
const userStore = useUserStore()
const router = useRouter()
const route = useRoute()

const news = ref([]) 
const news_copy = ref([])

const errors = ref([])
const showAuthor = ref("Yes")
const isReady = ref(false)


const getNews = async () => {
            
    paramStore.isLoading = true
    errors.value = []
    
    const newsSlug = route.params.slug
    
    await axios
        .get(`/api/v1/news/${newsSlug}`)
        .then(response => {
            news.value = response.data
            // console.log(news.value)
        })
        .catch(error =>{
            console.log(error)
        })

        if (news_copy.value.length == 0) {
            news_copy.value = news.value
        }

        if (news_copy.value.images_news != news.value.images_news) {
            news_copy.value.images_news = news.value.images_news
        }

        if (news_copy.value.cover_news != news.value.cover_news) {
            news_copy.value.cover_news = news.value.cover_news
        }

        if (news_copy.value.show_author == false) {
            showAuthor.value = "No"
        }

    isReady.value = true
    paramStore.isLoading = false
}

onMounted(() => {
    getNews()
})

const editNews = async () => {
            
    paramStore.isLoading = true    
    const newsSlug = route.params.slug

    news_copy.value.author = news_copy.value.author[0].id
    news_copy.value.author_update = userStore.user.id

    if (showAuthor.value == "Yes") {
        news_copy.value.show_author = true
    }

    if (showAuthor.value == "No") {
        news_copy.value.show_author = false
    }
                
    errors.value = []

    await axios
        .patch(`/api/v1/news/${newsSlug}/`, news_copy.value)
        .then(response => {
            router.push('/settings/news')

            createToast(
                'news edited successfully', 
                paramStore.toastSuccess
            )
        })
        .catch(error => {
            if (error.response) {
                for (const property in error.response.data) {
                    errors.value.push(`${property}: ${error.response.data[property]}`)
                    createToast(
                        `${property}: ${error.response.data[property]}`, 
                        paramStore.toastDanger
                    )
                }
                console.log(JSON.stringify(error.response.data))
            } else if (error.message) {
                console.log(JSON.stringify(error.message))
            } else {
                console.log(JSON.stringify(error))
            }
        })
    paramStore.isLoading = false
}
</script>

<style>
@import '~simplemde/dist/simplemde.min.css';
</style>