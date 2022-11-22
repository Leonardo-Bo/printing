<template>
    <div>
        <h4 class="inline-h mb-4">Add Carousel Item</h4>

        <form @submit.prevent="createCarouselItem">
            <div class="row g-3">
                <div class="form-group mb-3">
                    <label class="mb-1">Related Research Fields or News</label>
                    <Multiselect
                        v-model="relatedFieldsOrNewsSelector.value"
                        v-bind="relatedFieldsOrNewsSelector"
                        placeholder="Select"
                        class="multiselect-blue"
                    />
                </div>
            </div>

            <div class="float-md-end mt-4 mb-4">
                <router-link type="button" class="btn btn-sm btn-outline-secondary ms-1" to="/settings/carousel">Cancel</router-link>
                <button 
                    type="submit" 
                    class="btn btn-sm btn-outline-primary ms-1">Add
                </button>
            </div>
        </form>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'
import Multiselect from '@vueform/multiselect'

import { createToast } from "mosha-vue-toastify"
import { useParamStore } from '@/stores/ParamStore'
import { useUserStore } from '@/stores/UserStore'
import { useRouter } from 'vue-router';

const paramStore = useParamStore()
const userStore = useUserStore()
const router = useRouter()

const errors = ref([])
const isReady = ref(false)
const research_fields = ref([])
const news = ref([])
const selected_field = ref('')
const selected_news = ref('')
const relatedFieldsOrNewsSelector = ref({
    mode: 'single',
    hideSelected: false, 
    closeOnSelect: false,
    groups: true,
    value: [],
    options: [
        {
            label: 'Research Fields',
            options: {},
        }, 
        {
            label: 'News',
            options: {},
        },
    ]
})

const getRelated = async () => {
    paramStore.isLoading = true
    await axios
        .get('/api/v1/research/')
        .then(response => {
            research_fields.value = response.data
        })
        .catch(error =>{
            console.log(error)
        })

    let fields_title = research_fields.value.map(field => field.title)
    let keys_fields = research_fields.value.map(key => key.slug)

    for (let i = 0; i < keys_fields.length; i++) {
        relatedFieldsOrNewsSelector.value.options[0].options[keys_fields[i]] = fields_title[i]
    }

    await axios
        .get('/api/v1/news/')
        .then(response => {
            news.value = response.data
        })
        .catch(error =>{
            console.log(error)
        })

    let news_title = news.value.map(news => news.title)
    let keys_news = news.value.map(key => key.slug)


    for (let i = 0; i < keys_news.length; i++) {
        relatedFieldsOrNewsSelector.value.options[1].options[keys_news[i]] = news_title[i]
    }

    isReady.value = true;
    // console.log(relatedFieldsOrNewsSelector.value)
    paramStore.isLoading = false
}

onMounted(() => {
    getRelated()
})

const createCarouselItem = async () => {
    paramStore.isLoading = true
    errors.value = []

    const slugsFields = research_fields.value.map(f => f.slug)
    const slugsNews = news.value.map(n => n.slug)

    if (slugsFields.includes(relatedFieldsOrNewsSelector.value.value)) {
        selected_field.value = research_fields.value.filter(f => f.slug == relatedFieldsOrNewsSelector.value.value)[0].id
    } else {
        selected_field.value = null
    }

    if (slugsNews.includes(relatedFieldsOrNewsSelector.value.value)) {
        selected_news.value = news.value.filter(n => n.slug == relatedFieldsOrNewsSelector.value.value)[0].id
    } else {
        selected_news.value = null
    } 

    const carousel = {
        author: userStore.user.id,
        author_update: userStore.user.id,
        field: selected_field.value,
        news: selected_news.value
    }
    
    if (!errors.value.length) {

        if (carousel.field != null | carousel.news != null) {

            await axios
                .post('/api/v1/carousel/', carousel)
                .then(response => {
                    // console.log(response)
                    router.push(`/settings/carousel/edit/${response.data.id}`)
                    createToast(
                        'Carousel item added successfully', 
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
        }

    }

    selected_field.value = ''
    selected_news.value = ''
    paramStore.isLoading = false
}
</script>

<style src="@vueform/multiselect/themes/default.css"></style>

<style scoped>
.multiselect-blue {
    --ms-tag-bg: #DBEAFE;
    --ms-tag-color: #2563EB;
    --ms-option-bg-selected: #2563EB;
    --ms-option-bg-selected-pointed: #2563EB;
    --ms-font-size: 14px;
    --ms-line-height: 1.50;
    --ms-option-line-height: 0.8;
    --ms-option-font-size: 14px;
    z-index: 99;
}
</style>
