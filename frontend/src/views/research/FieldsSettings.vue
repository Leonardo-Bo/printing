<template>

    <div class="mb-5">
        <h4 class="inline-h">Research Fields</h4>

        <router-link 
            class="btn btn-sm btn-outline-primary px-4" 
            style="text-align:right; float:right;" 
            to="/settings/research-fields/add"
            >Add research field
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
        <t-research-fields 
            :research_fields="research_fields" 
            @fieldSlugEdit="editField"
            @fieldSlugDelete="deleteField"
        ></t-research-fields>
    </template>

    <delete-modal
        :model="'research field'"
        :title="selectedField.title"
        :warning="'Warning! A deleted news item cannot be recovered'"
        :identifier="selectedField.slug"
        :callback="getResearchFields"
        :openDeleteModal="showDeleteModal"
        :endpoint="'research'"
        @closeModal="showDeleteModal = false"
    >
    </delete-modal>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

import { useParamStore } from '@/stores/ParamStore'
import { useUserStore } from '@/stores/UserStore'
import { useRouter } from 'vue-router';

import "@hennge/vue3-pagination/dist/vue3-pagination.css";

import TResearchFields from '@/components/tables/TResearchFields.vue'
import DeleteModal from '@/components/DeleteModal.vue'

const paramStore = useParamStore()
const userStore = useUserStore()
const router = useRouter()

const loading = ref(false) 
const research_fields = ref([])
const selectedField = ref([])
const showDeleteModal = ref(false)


const getResearchFields = async () => {
    paramStore.isLoading = true
    loading.value = true

    await axios
        .get('/api/v1/research/')
        .then(response => {
            loading.value = false
            research_fields.value = response.data 
            // console.log(research_fields.value)
        })
        .catch(error =>{
            console.log(error)
        })
    paramStore.isLoading = false
}

onMounted(() => {
    getResearchFields()
})

const deleteField = (value) => {
    selectedField.value = value
    showDeleteModal.value = true
}

const editField = (value) => {
    router.push(`/settings/research-fields/edit/${value}`)
}
</script>
