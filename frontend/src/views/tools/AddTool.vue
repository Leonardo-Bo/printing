<template>
    <div>
        <h4 class="inline-h mb-4">Add Tool</h4>

        <form @submit.prevent="createTool">
        
            <div class="row g-3">
                <div class="col-md-12">
                    <label>Name*</label>
                    <input
                        type="text"
                        class="form-control"
                        id="name"
                        v-model="name">
                    <char-count
                        :input="name"
                        :inputLen="150"
                        :inputWarn="25"
                    />
                </div>
            </div>

            <div class="float-md-end mt-4 mb-4">
                <router-link type="button" class="btn btn-sm btn-outline-secondary ms-1" to="/settings/tools">Cancel</router-link>
                <button 
                    type="submit" 
                    class="btn btn-sm btn-outline-primary ms-1">Add
                </button>
            </div>
        </form>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

import CharCount from '@/components/CharCount.vue'
import { createToast } from "mosha-vue-toastify"
import { useParamStore } from '@/stores/ParamStore'
import { useUserStore } from '@/stores/UserStore'
import { useRouter } from 'vue-router';

const paramStore = useParamStore()
const userStore = useUserStore()
const router = useRouter()

const name = ref('')
const errors = ref([])

const createTool = async () => {
    paramStore.isLoading = true
    errors.value = []

    const tool = {
        name: name.value,
        content: '',
        link: '#',
        author: userStore.user.id,
        author_update: userStore.user.id
    }
    
    if (!errors.value.length) {

        await axios
            .post('/api/v1/tools/', tool)
            .then(response => {
                // console.log(response)
                router.push(`/settings/tools/edit/${response.data.slug}`)
                createToast(
                    'Tool added successfully', 
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
    paramStore.isLoading = false
}
</script>
