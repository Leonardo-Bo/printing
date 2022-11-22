<template>
    <h4 class="inline-h mb-4">Edit Tool</h4>

    <div class="container-upload">
        <form @submit.prevent="editTool">

            <div class="form-group mb-3">
                <label class="mb-1">Name*</label>
                <input
                    type="text"
                    class="form-control"
                    id="title"
                    v-model="tool_copy.name">
                <template v-if="isReady">
                    <char-count
                        :input="tool_copy.name"
                        :inputLen="100"
                        :inputWarn="25"
                    />
                </template>
            </div>

            <div class="form-group">
                <label class="mb-1">Content</label>
                <template v-if="isReady">
                    <char-count
                        :input="tool_copy.content"
                        :inputLen="150"
                        :inputWarn="25"
                    />
                </template>
                <vue-simplemde v-model="tool_copy.content" ref="markdownEditor" />
            </div>

            <div class="row">
                <div class="col-md-6">
                    <label class="mb-1">Link*</label>
                    <input 
                        type="text" 
                        class="form-control" 
                        v-model="tool_copy.link"
                    >
                </div>
                <div class="col-md-6">
                    <label class="mb-1">Show tool</label>
                    <br>
                    <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" value="Yes" v-model="showTool">
                        <label class="form-check-label">Yes</label>
                    </div>
                    <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" value="No" v-model="showTool">
                        <label class="form-check-label">No</label>
                    </div>

                </div>
            </div>

            <div class="mt-4" align="right">
                <router-link 
                    type="button" 
                    class="btn btn-sm btn-outline-secondary ms-1" 
                    to="/settings/tools"
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

    <cover-component
        :model="tool"
        :callback="getTool"
        :endpoint="'tool-cover'"
        :base-ref="'cover_tool'"
        :width="300"
        :height="300"
        :aspect-ratio="1/1"
    >
    </cover-component>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

import { createToast } from "mosha-vue-toastify"
import VueSimplemde from 'vue-simplemde'

import CharCount from '@/components/CharCount.vue'
import ImagesComponent from '@/components/images/ImagesComponent.vue'
import CoverComponent from '@/components/images/CoverComponent.vue'

import { useParamStore } from '@/stores/ParamStore'
import { useUserStore } from '@/stores/UserStore'
import { useRoute, useRouter } from 'vue-router';

const paramStore = useParamStore()
const userStore = useUserStore()
const router = useRouter()
const route = useRoute()

const tool = ref([]) 
const tool_copy = ref([])

const errors = ref([])
const showTool = ref("Yes")
const isReady = ref(false)

const getTool = async () => {
    paramStore.isLoading = true
    errors.value = []
    
    const toolSlug = route.params.slug
    
    await axios
        .get(`/api/v1/tools/${toolSlug}`)
        .then(response => {
            tool.value = response.data
            // console.log(tool.value)
        })
        .catch(error =>{
            console.log(error)
        })

        if (tool.value.link == '#') {
            tool.value.link = ''
        }

        if (tool_copy.value.length == 0) {
            tool_copy.value = tool.value
        }

        if (tool_copy.value.cover_tool != tool.value.cover_tool) {
            tool_copy.value.cover_tool = tool.value.cover_tool
        }

        if (tool_copy.value.show_tool == false) {
            showTool.value = "No"
        }

    isReady.value = true
    paramStore.isLoading = false
}

onMounted(() => {
    getTool()
})

const editTool = async () => {
    paramStore.isLoading = true 

    const toolSlug = route.params.slug

    tool_copy.value.author = tool_copy.value.author[0].id
    tool_copy.value.author_update = userStore.user.id

    if (showTool.value == "Yes") {
        tool_copy.value.show_tool = true
    }
    if (showTool.value == "No") {
        tool_copy.value.show_tool = false
    }
                
    errors.value = []

    if (tool_copy.value.link != '') {

        await axios
            .patch(`/api/v1/tools/${toolSlug}/`, tool_copy.value)
            .then(response => {
                router.push('/settings/tools')
                createToast(
                    'tool edited successfully', 
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
    } else {
        createToast(
            'link is mandatory', 
            paramStore.toastDanger
        )
    }
    paramStore.isLoading = false
}
</script>

<style>
@import '~simplemde/dist/simplemde.min.css';
</style>