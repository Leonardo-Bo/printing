<template>

    <div class="mb-5">
        <h4 class="inline-h">People</h4>
        <router-link 
            class="btn btn-sm btn-outline-primary px-4" 
            style="text-align:right; float:right;" 
            to="/settings/people/add"
            >Add person
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
        <t-people 
            :people="people" 
            @personSlugEdit="editPerson"
            @personSlugDelete="deletePerson"
        ></t-people>
    </template>

    <delete-modal
        :model="'person'"
        :title="selectedPerson.name"
        :warning="'Warning! A deleted person item cannot be recovered'"
        :identifier="selectedPerson.slug"
        :callback="getPeople"
        :openDeleteModal="showDeleteModal"
        :endpoint="'people'"
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

import TPeople from '../../components/tables/TPeople.vue'
import DeleteModal from '@/components/DeleteModal.vue';

const paramStore = useParamStore()
const router = useRouter()

const loading = ref(false) 
const people = ref([])

const selectedPerson = ref([])
const showDeleteModal = ref(false)

const getPeople = async () => {
    paramStore.isLoading = true
    loading.value = true

    await axios
        .get('/api/v1/people/')
        .then(response => {
            loading.value = false
            people.value = response.data 
            // console.log(people.value)
        })
        .catch(error =>{
            console.log(error)
        })
    paramStore.isLoading = false
}

onMounted(() => {
    getPeople()
})

const deletePerson = (value) => {
    selectedPerson.value = value
    showDeleteModal.value = true
}

const editPerson = (value) => {
    router.push(`/settings/people/edit/${value}`)
}
</script>
