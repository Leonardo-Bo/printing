<template>
    <div>
        <h4 class="inline-h mb-4">Add News</h4>

        <form @submit.prevent="createNews">
        
            <div class="row g-3">

                <div class="col-md-12">
                    <label class="mb-1">Title*</label>
                    <input
                        type="text"
                        class="form-control"
                        id="title"
                        v-model="title"
                    >
                    <char-count
                        :input="title"
                        :inputLen="100"
                        :inputWarn="25"
                    />
                </div>

            </div>

            <div class="float-md-end mt-4 mb-4">
                <router-link type="button" class="btn btn-sm btn-outline-secondary ms-1" to="/settings/news">Cancel</router-link>
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

const title = ref('')
const errors = ref([])

const createNews = async () => {
    paramStore.isLoading = true
    errors.value = []

    // var date = new Date();
    // var today = date.getFullYear()+'-'+(date.getMonth()+1)+'-'+date.getDate();
    var date = new Date(new Date().setDate(new Date().getDate() + 1))
    var tomorrow = date.getFullYear()+'-'+(date.getMonth()+1)+'-'+date.getDate()

    const news = {
        title: title.value,
        content: '',
        author: userStore.user.id,
        author_update: userStore.user.id,
        publicated_at: tomorrow
    }
    
    if (!errors.value.length) {

        await axios
            .post('/api/v1/news/', news)
            .then(response => {
                // console.log(response)
                router.push(`/settings/news/edit/${response.data.slug}`)
                createToast(
                    'News added successfully', 
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
