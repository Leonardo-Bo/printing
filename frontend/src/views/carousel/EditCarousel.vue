<template>
    <h4 class="inline-h mb-4">Edit Carousel Item</h4>

    <div class="container-upload" v-if="isReady">
        <form @submit.prevent="editCarouselItem">

            <div class="form-group mb-3">
                <label class="mb-1">Content*</label>
                <input
                    type="text"
                    class="form-control"
                    id="title"
                    v-model="carousel_copy.content">
                <char-count
                    :input="carousel_copy.content"
                    :inputLen="100"
                    :inputWarn="25"
                />
            </div>

            <div class="form-group mb-3">
                <label class="mb-1">Related Research Fields or News</label>

                <Multiselect
                    v-model="relatedFieldsOrNewsSelector.value"
                    v-bind="relatedFieldsOrNewsSelector"
                    placeholder="Select"
                    class="multiselect-blue"
                />
            </div>

            <div class="form-group mb-3">
                <label class="me-3">Show in home carousel</label>
                    <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" value="Yes" v-model="show_in_home">
                        <label class="form-check-label">Yes</label>
                    </div>
                    <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" value="No" v-model="show_in_home">
                        <label class="form-check-label">No</label>
                    </div>
            </div>

            <div class="mt-4" align="right">
                <router-link 
                    type="button" 
                    class="btn btn-sm btn-outline-secondary ms-1" 
                    to="/settings/carousel"
                >Cancel
                </router-link>
                <button 
                    type="submit" 
                    class="btn btn-sm btn-outline-primary ms-1">Edit Carousel Item
                </button>
            </div>
        </form>
    </div>

    <hr style="margin-top: 40px;">

    <cover-component
        :model="carousel"
        :callback="getCarousel"
        :endpoint="'carousel-cover'"
        :base-ref="'cover_carousel'"
        :width="1680"
        :height="400"
        :aspect-ratio="21/5"
    >
    </cover-component>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Multiselect from '@vueform/multiselect'

import { createToast } from "mosha-vue-toastify"

import CoverComponent from '@/components/images/CoverComponent.vue'
import CharCount from '@/components/CharCount.vue'

import { useParamStore } from '@/stores/ParamStore'
import { useUserStore } from '@/stores/UserStore'
import { useRoute, useRouter } from 'vue-router';

const paramStore = useParamStore()
const userStore = useUserStore()
const router = useRouter()
const route = useRoute()

const carousel = ref([]) 
const carousel_copy = ref([])
const errors = ref([])
const isReady = ref(false)
const show_in_home = ref("No") 
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

const getCarousel = async () => {
    paramStore.isLoading = true
    errors.value = []

    const itemID = route.params.id

    await axios
        .get(`/api/v1/carousel/${itemID}`)
        .then(response => {
            carousel.value = response.data
            // console.log(carousel.value)
        })
        .catch(error =>{
            console.log(error)
        })

        if (carousel.value.field != null) {
            relatedFieldsOrNewsSelector.value.value = carousel.value.field.slug
        }

        if (carousel.value.news != null) {
            relatedFieldsOrNewsSelector.value.value = carousel.value.news.slug
        }

        if (carousel.value.content == null) {
            carousel.value.content = ''
        }

        if (carousel_copy.value.length == 0) {
            carousel_copy.value = carousel.value
        }

        if (carousel_copy.value.cover_carousel != carousel.value.cover_carousel) {
            carousel_copy.value.cover_carousel = carousel.value.cover_carousel
        }

        if (carousel_copy.value.show_in_home == false) {
            show_in_home.value = "No"
        }

        if (carousel_copy.value.show_in_home == true) {
            show_in_home.value = "Yes"
        }

    paramStore.isLoading = false
}

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
    getCarousel()
    getRelated()
})

const editCarouselItem = async () => {
    paramStore.isLoading = true
    errors.value = []
    
    const itemID = route.params.id

    carousel_copy.value.author = carousel_copy.value.author[0].id
    carousel_copy.value.author_update = userStore.user.id
    
    if (carousel_copy.value.content == null) {
        carousel_copy.value.content = ''
    }
    
    if (show_in_home.value == "Yes") {
        carousel_copy.value.show_in_home = true
    }

    if (show_in_home.value == "No") {
        carousel_copy.value.show_in_home = false
    }

    const slugsFields = research_fields.value.map(f => f.slug)
    const slugsNews = news.value.map(n => n.slug)

    if (slugsFields.includes(relatedFieldsOrNewsSelector.value.value)) {
        carousel_copy.value.field  = research_fields.value.filter(f => f.slug == relatedFieldsOrNewsSelector.value.value)[0].id
    } else {
        carousel_copy.value.field = null
    }

    if (slugsNews.includes(relatedFieldsOrNewsSelector.value.value)) {
        carousel_copy.value.news = news.value.filter(n => n.slug == relatedFieldsOrNewsSelector.value.value)[0].id
    } else {
        carousel_copy.value.news = null
    }

            
    if (carousel_copy.value.field != null | carousel_copy.value.news != null) {
        await axios
            .patch(`/api/v1/carousel/${itemID}/`, carousel_copy.value)
            .then(response => {
                router.push('/settings/carousel')
                createToast(
                    'carousel item edited successfully', 
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
    } else {
        createToast(
            'Carousel item must have related field or news', 
            paramStore.toastDanger
        )
    } 
    paramStore.isLoading = false
}
</script>

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
    z-index: 7;
}
</style>
