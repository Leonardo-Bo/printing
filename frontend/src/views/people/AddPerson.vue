<template>
    <div>
        <h4 class="inline-h mb-4">Add Person</h4>

        <form @submit.prevent="createPerson">
        
            <div class="row g-3">
                <div class="col-md-12">
                    <label>Name*</label>
                    <input
                        type="text"
                        class="form-control"
                        id="name"
                        v-model="name">
                </div>
            </div>

            <div class="float-md-end mt-4 mb-4">
                <router-link type="button" class="btn btn-sm btn-outline-secondary ms-1" to="/settings/people">Cancel</router-link>
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

import CharCount from '@/components/CharCount.vue'

const paramStore = useParamStore()
const userStore = useUserStore()
const router = useRouter()

const name = ref('')
const errors = ref([])

const createPerson = async () => {
    paramStore.isLoading = true
    errors.value = []

    const person = {
        name: name.value,
        email: '#',
        role: '#',
        author: userStore.user.id,
        author_update: userStore.user.id,
    }
    
    if (!errors.value.length) {

        await axios
            .post('/api/v1/people/', person)
            .then(response => {
                // console.log(response)
                router.push(`/settings/people/edit/${response.data.slug}`)
                createToast(
                    'Person added successfully', 
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
