<template>

    <h4 class="inline-h mb-4">Edit Person</h4>

    <div class="container-upload">
        <form @submit.prevent="editPerson">

            <div class="row">
                <div class="col-md-6">
                    <div class="form-group mb-3">
                        <label class="mb-1">Name*</label>
                        <input
                            type="text"
                            class="form-control"
                            id="name"
                            v-model="person_copy.name">
                    </div>
                </div>

                <div class="col-md-6">
                    <div class="form-group mb-3">
                        <label class="mb-1">Email*</label>
                        <input
                            type="text"
                            class="form-control"
                            id="email"
                            v-model="person_copy.email">
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col-md-3">
                    <div class="form-group mb-3">
                        <label class="mb-1">Role*</label>
                        <input
                            type="text"
                            class="form-control"
                            id="role"
                            v-model="role">
                    </div>
                </div>

                <div class="col-md-8">
                    <div class="form-group mb-3">
                        <label class="mb-1">Affiliation</label>
                        <input
                            type="text"
                            class="form-control"
                            id="role"
                            v-model="affiliation">
                    </div>
                </div>

                <div class="col-md-1">
                    <div class="form-group mb-3">
                        <label class="mb-1">Position*</label>
                        <input
                            type="text"
                            class="form-control"
                            id="role"
                            v-model="person_copy.position">
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col-md-4">
                    <div class="form-group mb-3">
                        <label class="mb-1">Scholar</label>
                        <input
                            type="text"
                            class="form-control"
                            id="scholar"
                            v-model="person_copy.link_scholar">
                    </div>
                </div>

                <div class="col-md-4">
                    <div class="form-group mb-3">
                        <label class="mb-1">Linkedin</label>
                        <input
                            type="text"
                            class="form-control"
                            id="linkedin"
                            v-model="person_copy.linkedin">
                    </div>
                </div>

                <div class="col-md-4">
                    <div class="form-group mb-3">
                        <label class="mb-1">Github</label>
                        <input
                            type="text"
                            class="form-control"
                            id="role"
                            v-model="person_copy.github">
                    </div>
                </div>
            </div>

            <div class="form-group">
                <label class="mb-1">Content</label>
                <vue-simplemde v-model="person_copy.content" ref="markdownEditor" />
            </div>

            <div class="form-group mb-3">
                <label class="me-3">Show in people page</label>
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
                    to="/settings/people"
                >Cancel
                </router-link>
                <button 
                    type="submit" 
                    class="btn btn-sm btn-outline-primary ms-1">Edit Person
                </button>
            </div>
        </form>
    </div>

    <hr style="margin-top: 40px;">

    <images-component
        :model="person"
        :callback="getPerson"
        :endpoint="'person-images'"
        :base_ref="'images_person'"
    >
    </images-component>

    <hr style="margin-top: 40px;">

    <pic-person 
        :person="person"
        :callback="getPerson"
    />

    <hr style="margin-top: 40px;">

    <cover-component
        :model="person"
        :callback="getPerson"
        :endpoint="'person-cover'"
        :base-ref="'cover_person'"
        :width="1200"
        :height="300"
        :aspect-ratio="4/1"
    >
    </cover-component>

    <hr style="margin-top: 40px;">

    <c-v-person 
        :person="person"
        :callback="getPerson"
    />
    
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

import { createToast } from "mosha-vue-toastify"
import VueSimplemde from 'vue-simplemde'

import ImagesComponent from '@/components/images/ImagesComponent.vue'
import CoverComponent from '@/components/images/CoverComponent.vue'
import PicPerson from '@/components/images/PicPerson.vue'
import CVPerson from '@/components/files/CVPerson.vue'

import { useParamStore } from '@/stores/ParamStore'
import { useUserStore } from '@/stores/UserStore'
import { useRoute, useRouter } from 'vue-router';

const paramStore = useParamStore()
const userStore = useUserStore()
const router = useRouter()
const route = useRoute()

const person = ref([]) 
const person_copy = ref([])
const show_in_page = ref("No")

const role = ref('')
const affiliation = ref('')

const errors = ref([])


const getPerson = async () => {
    paramStore.isLoading = true
    errors.value = []
    
    const personSlug = route.params.slug
    
    await axios
        .get(`/api/v1/people/${personSlug}`)
        .then(response => {
            person.value = response.data
            const role_affiliation = person.value.role.split('<br><small><em>')
            role.value = role_affiliation[0]
            affiliation.value = role_affiliation[1].slice(0, -13)
        })
        .catch(error =>{
            console.log(error)
        })

    if (person.value.content == null) {
        person.value.content = ''
    }

    if (person.value.role == '#') {
        person.value.role = ''
    }

    if (person.value.email == '#') {
        person.value.email = ''
    }


    if (person_copy.value.length == 0) {
        person_copy.value = person.value
    }

    if (person_copy.value.images_person != person.value.images_person) {
        person_copy.value.images_person = person.value.images_person
    }

    if (person_copy.value.cover_person != person.value.cover_person) {
        person_copy.value.cover_person = person.value.cover_person
    }

    if (person_copy.value.show_in_page == false) {
        show_in_page.value = "No"
    }

    if (person_copy.value.show_in_page == true) {
        show_in_page.value = "Yes"
    }

    paramStore.isLoading = false
}

onMounted(() => {
    getPerson()
})

const editPerson = async () => {
    paramStore.isLoading = true    
    
    const personSlug = route.params.slug

    person_copy.value.author = person_copy.value.author[0].id
    person_copy.value.author_update = userStore.user.id
    
    if (show_in_page.value == "Yes") {
        person_copy.value.show_in_page = true
    }

    if (show_in_page.value == "No") {
        person_copy.value.show_in_page = false
    }

    person_copy.value.role = `${role.value}<br><small><em>${affiliation.value}</em></small>`

    errors.value = []

    await axios
        .patch(`/api/v1/people/${personSlug}/`, person_copy.value)
        .then(response => {
            // console.log(person_copy.value)
            router.push('/settings/people')

            createToast(
                'person field edited successfully', 
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

<style>
@import '~simplemde/dist/simplemde.min.css';
</style>