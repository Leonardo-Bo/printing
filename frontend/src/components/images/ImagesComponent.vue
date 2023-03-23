<template>
    <div class="mt-4">
        <h5 class="inline-h mb-4">Content images</h5>
        <div class="container-upload">
            <form @submit.prevent="uploadImages">
                <input class="form-control" type="file" ref="inputImages" multiple>
                <button class="btn btn-primary btn-sm mt-3" type="submit">Submit <i class="bi bi-upload ms-3"></i></button>
            </form>
        </div>
    </div>

    <div class="mt-4 container-upload">
        <table class="table table-striped table-hover table-sm">
            <thead>
                <tr>
                    <th style="width: 72%">Image</th>
                    <th class="pe-5" style="width: 20%; text-align: right;">Size</th>
                    <th style="width: 8%; text-align: right;">Actions</th>
                </tr>
            </thead>
            <tbody style="font-size: 13px;">
                <tr v-for="image in model[props.base_ref]" :key="image.id">
                    <td><a class="table-image-link" :href="image.image" target="_blank">{{ getFileName(image.image) }}</a></td>
                    <td class="pe-5" style="text-align: right;">
                        {{ getFileSize(image.size) }}
                    </td>
                    <td>
                        <abbr style="cursor: pointer;" title="Delete">
                            <i 
                                @click="deleteImage(image)" 
                                class="bi bi-trash text-danger float-end">
                            </i>
                        </abbr>
                        <abbr style="cursor: pointer;" title="Copy link">
                            <i 
                                @click="copyImage(image.image)" 
                                class="bi bi-files text-primary float-end me-4">
                            </i>
                        </abbr>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

import { useParamStore } from '@/stores/ParamStore'
import { createToast } from "mosha-vue-toastify"

import { getFileName, getFileSize, getCopyImage } from '@/composables/handleFiles'

const paramStore = useParamStore()

const props = defineProps([
    'model',
    'callback',
    'endpoint',
    'base_ref'
])

const inputImages = ref(null)

const errors = []

const uploadImages = async () => {
            
    for (let i = 0; i < inputImages.value.files.length; i++) {

        const formData = new FormData()

        formData.append('reffield', props.model.id)
        formData.append('image', inputImages.value.files[i])

        await axios 
            .post(`/api/v1/${props.endpoint}/`, formData, { 
                headers: {
                    "Content-Type": "multipart/form-data",
                }
            })
            .then(response => {
                props.callback()
                createToast(
                    `${ getFileName(response.data.image) } uploaded`, 
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

    inputImages.value.value = ''
}

const copyImage = (str) => {
    getCopyImage(str)
    createToast(
        'image copied to clipboard', 
        paramStore.toastSuccess
    )
}

const deleteImage = async (image) => {
    await axios 
        .delete(`/api/v1/${props.endpoint}/${image.id}`)
        .then(response => {
            props.callback()
            createToast(
                `${getFileName(image.image)} deleted successfully`, 
                paramStore.toastSuccess
            )
        })
}
</script>
