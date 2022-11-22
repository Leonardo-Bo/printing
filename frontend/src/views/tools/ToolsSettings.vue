<template>

    <div class="mb-5">
        <h4 class="inline-h">Tools</h4>

        <router-link 
            class="btn btn-sm btn-outline-primary px-4" 
            style="text-align:right; float:right;" 
            to="/settings/tools/add"
            >Add tool
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
        <t-tools
            :tools="tools" 
            @toolSlugEdit="editTool"
            @toolSlugDelete="deleteTool"
        ></t-tools>
    </template>

    <delete-modal
        :model="'tool'"
        :title="selectedTool.name"
        :warning="'Warning! A deleted tool item cannot be recovered'"
        :identifier="selectedTool.slug"
        :callback="getTools"
        :openDeleteModal="showDeleteModal"
        :endpoint="'tools'"
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

import TTools from '../../components/tables/TTools.vue';
import DeleteModal from '@/components/DeleteModal.vue'

const paramStore = useParamStore()
const userStore = useUserStore()
const router = useRouter()

const loading = ref(false) 
const tools = ref([])
const selectedTool = ref([])
const showDeleteModal = ref(false)

const getTools = async () => {
    paramStore.isLoading = true
    loading.value = true

    await axios
        .get('/api/v1/tools/')
        .then(response => {
            loading.value = false
            tools.value = response.data 
            // console.log(tools.value)
        })
        .catch(error =>{
            console.log(error)
        })
    paramStore.isLoading = false
}

onMounted(() => {
    getTools()
})

const deleteTool = (value) => {
    selectedTool.value = value
    showDeleteModal.value = true
}

const editTool = (value) => {
    router.push(`/settings/tools/edit/${value}`)
}
</script>
