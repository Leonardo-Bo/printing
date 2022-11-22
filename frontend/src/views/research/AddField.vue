<template>
    <div>
        <h4 class="inline-h mb-4">Add Research Field</h4>

        <form @submit.prevent="createResearcField">
        
            <div class="row g-3">

                <div class="col-md-12">
                    <label>Title*</label>
                    <input
                        type="text"
                        class="form-control"
                        id="title"
                        v-model="title">
                </div>

            </div>

            <div class="float-md-end mt-4 mb-4">
                <router-link type="button" class="btn btn-sm btn-outline-secondary ms-1" to="/settings/research-fields">Cancel</router-link>
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

import { createToast } from "mosha-vue-toastify"
import { useParamStore } from '@/stores/ParamStore'
import { useUserStore } from '@/stores/UserStore'
import { useRouter } from 'vue-router';

const paramStore = useParamStore()
const userStore = useUserStore()
const router = useRouter()

const title = ref('')
const errors = ref([])

const createResearcField = async () => {
    paramStore.isLoading = true

    errors.value = []

    const research_field = {
        title: title.value,
        content: '',
        author: userStore.user.id,
        author_update: userStore.user.id
    }
    
    if (!errors.value.length) {

        await axios
            .post('/api/v1/research/', research_field)
            .then(response => {
                console.log(response)

                router.push(`/settings/research-fields/edit/${response.data.slug}`)
                
                createToast(
                    'Research Field added successfully', 
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
