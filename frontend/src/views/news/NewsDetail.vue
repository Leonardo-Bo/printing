<template>
    <div class="news-container">
        <template v-if="isReady">
            <template v-if="isNews">
                <h2 class="mb-3">{{ news.title }}</h2>
                <div class="mb-3">

                    {{ formatDate(news.publicated_at) }} |
                    
                    <!-- <span v-if="isReady"> -->
                        <span v-if="news.show_author && news.author.full_name">
                            {{ news.author.full_name }}
                        </span>
                        <span v-else>Team</span>
                    <!-- </span> -->
                </div>

                <div class="md-content" v-html="news.contentMD"></div>
            </template>
            <template v-else>
                <span style="font-size: 20px;">
                    404: Page does not exist
                </span>
            </template>
        </template>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { marked } from 'marked'

import { useParamStore } from '@/stores/ParamStore'
import { useRoute } from 'vue-router'

const paramStore = useParamStore()
const route = useRoute()

const dayjs = require('dayjs')

const news = ref({})
const isReady = ref(false)
const isNews = ref(false)

const getNews = async () => {
    paramStore.isLoading = true

    const newsSlug = route.params.slug

    await axios
        .get(`/api/v1/news/${newsSlug}`)
        .then(response => {
            news.value = response.data
            // console.log(news.value)
            news.value.contentMD = marked(news.value.content)
            isNews.value = true
        })
        .catch(error =>{
            console.log(error)
        })

    isReady.value = true
    paramStore.isLoading = false
}

onMounted(() => {
    getNews()
})

const formatDate = (value) => {
    if (value) {
        return dayjs(String(value)).format('DD MMM YY')
    }
}
</script>

<style lang="scss" scoped>
@media screen and (min-width: 279px) and (max-width: 769px) {
    .news-container {
        margin-top: 60px;
        margin-bottom: 100px;
        margin-left: 20px;
        margin-right: 20px;
        padding-bottom: 5px;
    }

}

@media screen and (min-width: 770px) and (max-width: 1179px) {
    .news-container {
        margin-top: 60px;
        margin-bottom: 100px;
        margin-left: 90px;
        margin-right: 90px;
        padding-bottom: 5px;
    }

}

@media screen and (min-width: 1180px) {
    .news-container {
        margin-top: 60px;
        margin-bottom: 100px;
        margin-left: 180px;
        margin-right: 180px;
        padding-bottom: 5px;
    }

}

.md-content {
	text-align: justify;
	&:deep(p) {
		hyphens: auto;
        -ms-hyphens: auto;
        -webkit-hyphens: auto;
	}
}
</style>