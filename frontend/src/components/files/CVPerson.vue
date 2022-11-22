<template>
    <div class="mt-4">
        <h5 class="inline-h mb-4">Curriculum PDF</h5>
        <div class="container-upload">
            <form @submit.prevent="uploadCurriculumPDF">
                <input class="form-control" type="file" ref="inputFiles">
                <button class="btn btn-primary btn-sm mt-3" type="submit">Submit <i class="bi bi-upload ms-3"></i></button>
            </form>
        </div>
    </div>

    <div class="mt-4 container-upload">
        <table class="table table-striped table-hover table-sm">
            <thead>
                <tr>
                    <th style="width: 72%">File</th>
                    <th class="pe-5" style="width: 20%; text-align: right;">Size</th>
                    <th style="width: 8%; text-align: right;">Actions</th>
                </tr>
            </thead>
            <tbody style="font-size: 13px;">
                <tr v-for="file in person.pdf_personCV" :key="file.id">
                    <td><a class="table-image-link" :href="file.file" target="_blank">{{ getFileName(file.file) }}</a></td>
                    <td class="pe-5" style="text-align: right;">
                        {{ getFileSize(file.size) }}
                    </td>
                    <td>
                        <abbr style="cursor: pointer;" title="Delete">
                            <i 
                                @click="deletePDF(file)" 
                                class="bi bi-trash text-danger float-end">
                            </i>
                        </abbr>
                        <abbr style="cursor: pointer;" title="Set as CV">
                            <i 
                                @click="setPDF(file)" 
                                class="bi bi-arrow-up-square text-primary float-end me-4">
                            </i>
                        </abbr>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import axios from 'axios'

import { useParamStore } from '@/stores/ParamStore'
import { createToast } from "mosha-vue-toastify"

import { getFileName, getFileSize } from '@/composables/handleFiles'

const paramStore = useParamStore()

const props = defineProps([
    'person',
    'callback'
])

const errors = ref([])

const inputFiles = ref(null)


const uploadCurriculumPDF = async () => {
                        
    if (inputFiles.value.files.length > 0) {

        // fnu file name upload
        const fnu = inputFiles.value.files[0].name

        if(fnu.split('.').pop().toLowerCase() != "pdf") {
            createToast(
                `${ fnu } is not a pdf`, 
                paramStore.toastDanger
            )
        } else {
            const formData = new FormData()

            formData.append('reffield', props.person.id)
            formData.append('file', inputFiles.value.files[0])

            if (props.person.pef_personCV.length == 0) {
                formData.append('isPDF', true)
            }

            await axios 
                .post('/api/v1/perople-files/', formData, { 
                    headers: {
                        "Content-Type": "multipart/form-data",
                    }
                })
                .then(response => {
                    console.log(response)
                    props.callback()
                    createToast(
                        `${ getFileName(response.data.file) } uploaded`, 
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

            inputFiles.value.value = ''
        }
    }
}

const setPDF = async (file) => {

    const formFalse = new FormData()
    formFalse.append('isPDF', false)

    for (let i = 0; i < props.person.pef_personCV.length; i ++) {

        const fileID = props.person.pef_personCV[i].id

        await axios
            .patch(`/api/v1/people-files/${fileID}/`, formFalse, { 
                headers: {
                    "Content-Type": "multipart/form-data",
                }
            })
            .then(response => {
                // console.log(response)
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

    const formTrue = new FormData()
    formTrue.append('isPDF', true)

    await axios
        .patch(`/api/v1/people-files/${file.id}/`, formTrue, { 
            headers: {
                "Content-Type": "multipart/form-data",
            }
        })
        .then(response => {
            // console.log(response)
            createToast(
                'PDF changed successfully', 
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

    props.callback()
}

const deletePDF = async (file) => {
    await axios 
        .delete(`/api/v1/people-files/${file.id}`)
        .then(response => {
            console.log(response)
            props.callback()
            createToast(
                `${getFileName(file.file)} deleted successfully`, 
                paramStore.toastSuccess
            )
        })
}
</script>
