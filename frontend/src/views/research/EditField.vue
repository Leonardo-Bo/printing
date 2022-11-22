<template>

    <h4 class="inline-h mb-4">Edit Research Field</h4>

    <div class="container-upload">
        <form @submit.prevent="editResearchField">
            
            <div class="row">
                <div class="col-md-11">
                    <div class="form-group mb-3">
                        <label class="mb-1">Title*</label>
                        <input
                            type="text"
                            class="form-control"
                            id="name"
                            v-model="field_copy.title">
                    </div>
                </div>

                <div class="col-md-1">
                    <div class="form-group mb-3">
                        <label class="mb-1">Position*</label>
                        <input
                            type="text"
                            class="form-control"
                            id="email"
                            v-model="field_copy.position">
                    </div>
                </div>
            </div>

            <div class="form-group">
                <label class="mb-1">Content (at least 15 words)</label>
                <vue-simplemde v-model="field_copy.content" ref="markdownEditor" />
            </div>

            <div class="form-group mb-3">
                <label class="me-3">Show in research fields page</label>
                    <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" value="Yes" v-model="show_in_page">
                        <label class="form-check-label">Yes</label>
                    </div>
                    <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" value="No" v-model="show_in_page">
                        <label class="form-check-label">No</label>
                    </div>
            </div>

            <div class="mt-4" align="right">
                <router-link 
                    type="button" 
                    class="btn btn-sm btn-outline-secondary ms-1" 
                    to="/settings/research-fields"
                >Cancel
                </router-link>
                <button 
                    type="submit" 
                    class="btn btn-sm btn-outline-primary ms-1">Edit Research Field
                </button>
            </div>
        </form>
    </div>

    <hr style="margin-top: 40px;">

    <!-- <images-field
        :field="field"
        :callback="getResearchField"
    /> -->
    <images-component
        :model="field"
        :callback="getResearchField"
        :endpoint="'research-images'"
        :base_ref="'images_research'"
    >
    </images-component>

    <hr style="margin-top: 40px;">

    <cover-component
        :model="field"
        :callback="getResearchField"
        :endpoint="'research-cover'"
        :base-ref="'cover_research'"
        :width="300"
        :height="450"
        :aspect-ratio="2/3"
    >
    </cover-component>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

import { createToast } from "mosha-vue-toastify"
import VueSimplemde from 'vue-simplemde'

import ImagesComponent from '@/components/images/ImagesComponent.vue'
import CoverComponent from '@/components/images/CoverComponent.vue'

import { useParamStore } from '@/stores/ParamStore'
import { useUserStore } from '@/stores/UserStore'
import { useRoute, useRouter } from 'vue-router';

const paramStore = useParamStore()
const userStore = useUserStore()
const router = useRouter()
const route = useRoute()

const field = ref([]) 
const field_copy = ref([])
const show_in_page = ref("No")

const errors = ref([])

const getResearchField = async () => {
    paramStore.isLoading = true

    errors.value = []
    
    const fieldSlug = route.params.slug
    
    await axios
        .get(`/api/v1/research/${fieldSlug}`)
        .then(response => {
            // console.log(response.data)
            field.value = response.data
        })
        .catch(error =>{
            console.log(error)
        })

    if (field_copy.value.length == 0) {
        field_copy.value = field.value
    }

    if (field_copy.value.images_research != field.value.images_research) {
        field_copy.value.images_research = field.value.images_research
    }

    if (field_copy.value.cover_research != field.value.cover_research) {
        field_copy.value.cover_research = field.value.cover_research
    }

    if (field_copy.value.show_in_page == false) {
    show_in_page.value = "No"
    }

    if (field_copy.value.show_in_page == true) {
        show_in_page.value = "Yes"
    }
    
    // console.log(field_copy.value.author[0].id)
    paramStore.isLoading = false
}

onMounted(() => {
    getResearchField()
})

const editResearchField = async () => {

    paramStore.isLoading = true

    const fieldSlug = route.params.slug

    field_copy.value.author = field_copy.value.author[0].id
    field_copy.value.author_update = userStore.user.id

    if (show_in_page.value == "Yes") {
        field_copy.value.show_in_page = true
    }

    if (show_in_page.value == "No") {
        field_copy.value.show_in_page = false
    }
                
    errors.value = []

    await axios
        .patch(`/api/v1/research/${fieldSlug}/`, field_copy.value)
        .then(response => {
            router.push('/settings/research-fields')

            createToast(
                'research field edited successfully', 
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

    paramStore.isLoading = false
}
</script>

<style scoped>
@import '~simplemde/dist/simplemde.min.css';
</style>