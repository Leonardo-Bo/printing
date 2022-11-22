<template>

    <div class="mb-5">
        <h4 class="inline-h">News</h4>

        <router-link 
            class="btn btn-sm btn-outline-primary px-4" 
            style="text-align:right; float:right;" 
            to="/settings/news/add"
            >Add news
        </router-link>
    </div>

    <template v-if="loading">
        <div class="d-flex justify-content-center">
            <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    </template>
    <template v-else>
        <t-news 
            :allNews="allNews" 
            @newsSlugEdit="editNews"
            @newsSlugDelete="deleteNews"
        ></t-news>
    </template>

    <delete-modal
        :model="'news'"
        :title="selectedNews.title"
        :warning="'Warning! A deleted news item cannot be recovered'"
        :identifier="selectedNews.slug"
        :callback="getNews"
        :openDeleteModal="showDeleteModal"
        :endpoint="'news'"
        @closeModal="showDeleteModal = false"
    >
    </delete-modal>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

import { useParamStore } from '@/stores/ParamStore'
import { useRouter } from 'vue-router';

import "@hennge/vue3-pagination/dist/vue3-pagination.css";

import TNews from '../../components/tables/TNews.vue'
import DeleteModal from '@/components/DeleteModal.vue';

const paramStore = useParamStore()
const router = useRouter()

const loading = ref(false) 
const allNews = ref([])

const selectedNews = ref([])
const showDeleteModal = ref(false)

const getNews = async () => {
    paramStore.isLoading = true
    loading.value = true

    await axios
        .get('/api/v1/news/')
        .then(response => {
            loading.value = false
            allNews.value = response.data 
            // console.log(allNews.value)
        })
        .catch(error =>{
            console.log(error)
        })
    paramStore.isLoading = false
}

onMounted(() => {
    getNews()
})

const deleteNews = (value) => {
    selectedNews.value = value
    showDeleteModal.value = true
}

const editNews = (value) => {
    router.push(`/settings/news/edit/${value}`)
}
</script>
