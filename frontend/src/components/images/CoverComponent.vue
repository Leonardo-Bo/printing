<template>

    <div class="mt-4">
        <h5 class="inline-h mb-4">Cover</h5>

        <div class="container-upload">
            <input
                class="form-control"
                ref="inputCover"
                type="file"
                name="image"
                @change="setImage"
            />

            <div class="row mt-2">
                <div class="col-md-6 px-5">

                    <div class="crop-area-cover">
                        
                        <span v-show="imgSrc != '' && (imgCoverHeight < props.height || imgCoverWidth < props.width)">
                            Image too small
                        </span>
                        
                        <span v-show="imgCoverHeight >= props.height && imgCoverWidth >= props.width">
                            <vue-cropper
                                ref="cropper"
                                :aspect-ratio="props.aspectRatio"
                                :src="imgSrc"
                                :cropBoxResizable=false
                                preview=".cover-preview"
                                :dragMode="'none'"
                                :img-style="{ width: '350px', height: '350px' }"
                            />
                        </span>
                    </div>

                    <div class="image-settings-div">
                        <i class="bi bi-zoom-in image-settings" @click.prevent="zoom(0.2)"
                        ></i>
                        <i class="bi bi-zoom-out image-settings" @click.prevent="zoom(-0.2)"></i>
                        <i class="bi bi-chevron-left image-settings" @click.prevent="move(-10, 0)"></i>
                        <i class="bi bi-chevron-right image-settings" @click.prevent="move(10, 0)"></i>
                        <i class="bi bi-chevron-up image-settings" @click.prevent="move(0, -10)"></i>
                        <i class="bi bi-chevron-down image-settings" @click.prevent="move(0, 10)"></i>
                    </div>

                    <div class="mt-3">
                        <button 
                            class="btn btn-primary" 
                            style="width: 170px; margin-right: 5px;"
                            @click.prevent="reset"
                        >Reset
                        </button>
                        <button 
                            class="btn btn-primary" 
                            style="width: 170px; margin-left: 5px;"
                            @click.prevent="cropCover"
                        >Crop & Update
                        </button>
                        <!-- <a href="#" role="button" @click.prevent="reset">Reset</a>
                        <a href="#" role="button" @click.prevent="cropImage">Crop</a> -->
                    </div>
                    
                </div>

                <div class="col-md-6">
                
                    <div class="cover-preview-area">
                        <p>Preview</p>
                        <div v-if="imgCoverHeight >= props.height && imgCoverWidth >= props.width" class="cover-preview" />
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="mt-4 container-upload">
        <table class="table table-striped table-hover table-sm">
            <thead>
                <tr>
                    <th style="width: 72%">Cover</th>
                    <th class="pe-5" style="width: 20%; text-align: right;">Size</th>
                    <th style="width: 8%; text-align: right;">Actions</th>
                </tr>
            </thead>
            <tbody style="font-size: 13px;">
                <tr v-for="cover in props.model[props.baseRef]" :key="cover.id">
                    <td><a class="table-image-link" :href="cover.image" target="_blank">{{ getFileName(cover.image) }}</a></td>
                    <td class="pe-5" style="text-align: right;">
                        {{ getFileSize(cover.size) }}
                    </td>
                    <td>
                        <abbr style="cursor: pointer;" title="Delete">
                            <i 
                                @click="deleteCover(cover)" 
                                class="bi bi-trash text-danger float-end">
                            </i>
                        </abbr>
                        <abbr style="cursor: pointer;" title="Set as cover">
                            <i 
                                @click="setCover(cover)" 
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

import VueCropper from 'vue-cropperjs';
import 'cropperjs/dist/cropper.css';

import { getFileName, getFileSize } from '@/composables/handleFiles'

const paramStore = useParamStore()

const props = defineProps([
    'model',
    'callback',
    'endpoint',
    'baseRef',
    'width',
    'height',
    'aspectRatio'
])

const cropper = ref(null)
const inputCover = ref(null)

const errors = []

const imgSrc = ref('')
const cropImg = ref('')
const data = ref(null)

const coverFile = ref('')
const imgCoverWidth = ref(0)
const imgCoverHeight = ref(0)
const mime_type = ref('')

const setImage = (e) => {
    coverFile.value = e.target.files[0];
    const file = coverFile.value

    if (file == undefined) {
        imgSrc.value = ''
        imgCoverWidth.value = 0
        imgCoverHeight.value = 0
        mime_type.value = ''
    }

    if (file != undefined) {

        mime_type.value = file.type

        if (file.type.indexOf('image/') === -1) {
            createToast(
                'Invalid file type selected. Select an image', 
                paramStore.toastDanger
            )
            return;
        }
        if (typeof FileReader === 'function') {
            const reader = new FileReader();
            reader.onload = (event) => {

                imgSrc.value = event.target.result;

                nextTick(() => {
                    cropper.value.replace(event.target.result)
                })

                var img = new Image

                img.onload = () => {
                    imgCoverWidth.value = img.width
                    imgCoverHeight.value = img.height
                }

                img.src = reader.result;
                
            }

            reader.readAsDataURL(file);

        } else {
            this.createToast(
                'Sorry, FileReader API not supported', 
                paramStore.toastDanger
            )
        }
    }
}

const move = (offsetX, offsetY) => {
    cropper.value.move(offsetX, offsetY);
}

const reset = () => {
    cropper.value.reset();
}

const zoom = (percent) => {
    cropper.value.relativeZoom(percent);
}

const cropCover = async () => {
    cropper.value.getCroppedCanvas({ width: props.width, height: props.height}).toBlob((blob) => {
        const formData = new FormData()

        formData.append('reffield', props.model.id)
        formData.append('image', blob, coverFile.value.name)

        if (props.model[props.baseRef].length == 0) {
            formData.append('isCover', true)
        }

        axios 
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
    }, mime_type.value)

    inputCover.value.value = ''
    imgSrc.value = ''
    imgCoverWidth.value = 0
    imgCoverHeight.value = 0
    mime_type.value = ''

}

const setCover = async (cover) => {

    const formFalse = new FormData()
    formFalse.append('isCover', false)

    for (let i = 0; i < props.model[props.baseRef].length; i ++) {

        const imageID = props.model[props.baseRef][i].id

        await axios
            .patch(`/api/v1/${props.endpoint}/${imageID}/`, formFalse, { 
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
    formTrue.append('isCover', true)

    await axios
        .patch(`/api/v1/${props.endpoint}/${cover.id}/`, formTrue, { 
            headers: {
                "Content-Type": "multipart/form-data",
            }
        })
        .then(response => {
            console.log(response)
            createToast(
                'Cover changed successfully', 
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

const deleteCover = async (image) => {
    await axios 
        .delete(`/api/v1/${props.endpoint}/${image.id}`)
        .then(response => {
            // console.log(response)
            props.callback()
            createToast(
                `${getFileName(image.image)} deleted successfully`, 
                paramStore.toastSuccess
            )
        })
}
</script>

<style lang="scss" scoped>
.crop-area-cover {
    width: 350px !important;
    height: 350px !important;
    display:flex;
    justify-content: center;
    align-items: center;
    background-color: grey;
    margin-top: 20px;
}

.cover-preview-area {
    width: 300px;
    margin-top: 15px;
    font-size: 20px;
}

.cover-preview {
    width: 150%;
    height: 300px;
    overflow: hidden;
}
</style>