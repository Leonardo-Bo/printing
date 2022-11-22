<template>
    <div class="mb-5">
        <h4 class="inline-h">Publications</h4>

        <router-link 
            class="btn btn-sm btn-outline-primary px-4" 
            style="text-align:right; float:right;" 
            to="/settings/publications/add"
            >Add publication
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
        <t-publications 
            :publications="publications" 
            @publicationIdEdit="editPublication"
            @publicationIdDelete="deletePublication"
        ></t-publications>
    </template>

    <delete-modal
        :model="'publication'"
        :title="selectedPublication.title"
        :warning="'Warning! A deleted publication item cannot be recovered'"
        :identifier="selectedPublication.id"
        :callback="getPublications"
        :openDeleteModal="showDeleteModal"
        :endpoint="'publications'"
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

import TPublications from '@/components/tables/TPublications.vue'
import DeleteModal from '@/components/DeleteModal.vue';

const paramStore = useParamStore()
const router = useRouter()

const loading = ref(false) 
const publications = ref([])

const selectedPublication = ref([])
const showDeleteModal = ref(false)

const getPublications = async () => {
    paramStore.isLoading = true
    loading.value = true

    await axios
        .get('/api/v1/publications/')
        .then(response => {
            loading.value = false
            publications.value = response.data 
            // console.log(publications.value)            
        })
        .catch(error =>{
            console.log(error)
        })
    paramStore.isLoading = false
}

onMounted(() => {
    getPublications()
})

const deletePublication = (value) => {
    selectedPublication.value = value
    showDeleteModal.value = true
}

const editPublication = (value) => {
    router.push(`/settings/publications/edit/${value}`)
}
</script>
