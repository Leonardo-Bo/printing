<template>

    <div class="mb-5">
        <h4 class="inline-h">Carousel</h4>

        <router-link 
            class="btn btn-sm btn-outline-primary px-4" 
            style="text-align:right; float:right;" 
            to="/settings/carousel/add"
            >Add carousel item
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
        <t-carousel 
            :carousel="carousel" 
            @carouselIdEdit="editCarouselItem"
            @carouselIdDelete="deleteCarouselItem"
        ></t-carousel>
    </template>

    <delete-modal
        :model="'carousel item'"
        :title="selectedCarouselItem.id"
        :warning="'Warning! A deleted carousel item cannot be recovered'"
        :identifier="selectedCarouselItem.id"
        :callback="getCarousel"
        :openDeleteModal="showDeleteModal"
        :endpoint="'carousel'"
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

import TCarousel from '../../components/tables/TCarousel.vue'
import DeleteModal from '@/components/DeleteModal.vue';

const paramStore = useParamStore()
const router = useRouter()

const loading = ref(false) 
const carousel = ref([])

const selectedCarouselItem = ref([])
const showDeleteModal = ref(false)

const getCarousel = async () => {
    paramStore.isLoading = true
    loading.value = true

    await axios
        .get('/api/v1/carousel/')
        .then(response => {
            loading.value = false
            carousel.value = response.data 
            // console.log(carousel.value)
        })
        .catch(error =>{
            console.log(error)
        })
    paramStore.isLoading = false
}

onMounted(() => {
    getCarousel()
})

const deleteCarouselItem = (value) => {
    selectedCarouselItem.value = value
    showDeleteModal.value = true
}

const editCarouselItem = (value) => {
    router.push(`/settings/carousel/edit/${value}`)
}
</script>
