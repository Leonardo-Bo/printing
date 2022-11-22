<template>

    <div class="mt-4">
        <h5 class="inline-h mb-4">Pic profile</h5>

        <div class="container-upload">
            <input
                class="form-control"
                ref="inputPic"
                type="file"
                name="image"
                @change="setImage"
            />

            <div class="row mt-2">
                <div class="col-md-8 px-5">

                    <div class="crop-area-pic">
                        
                        <span v-show="imgSrc != '' && (imgPicHeight < 300 || imgPicWidth < 300)">
                            Image too small
                        </span>
                        
                        <span v-show="imgPicHeight > 300 && imgPicWidth > 300">
                            <vue-cropper
                                ref="cropper"
                                :aspect-ratio="1/1"
                                :src="imgSrc"
                                :cropBoxResizable=false
                                preview=".pic-preview"
                                :dragMode="'none'"
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
                            @click.prevent="cropPicPerson"
                        >Crop & Update
                        </button>
                    </div>
                    
                </div>

                <div class="col-md-4">
                
                    <div class="pic-preview-area">
                        <p>Preview</p>
                        <div v-if="imgPicHeight >= 300 && imgPicWidth >= 300" class="pic-preview" />
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="mt-4 container-upload">
        <table class="table table-striped table-hover table-sm">
            <thead>
                <tr>
                    <th style="width: 72%">Pic</th>
                    <th class="pe-5" style="width: 20%; text-align: right;">Size</th>
                    <th style="width: 8%; text-align: right;">Actions</th>
                </tr>
            </thead>
            <tbody style="font-size: 13px;">
                <tr v-for="pic in person.pic_person" :key="pic.id">
                    <td><a class="table-image-link" :href="pic.image" target="_blank">{{ getFileName(pic.image) }}</a></td>
                    <td class="pe-5" style="text-align: right;">
                        {{ getFileSize(pic.size) }}
                    </td>
                    <td>
                        <abbr style="cursor: pointer;" title="Delete">
                            <i 
                                @click="deletePicPerson(pic)" 
                                class="bi bi-trash text-danger float-end">
                            </i>
                        </abbr>
                        <abbr style="cursor: pointer;" title="Set as pic">
                            <i 
                                @click="setPicPerson(pic)" 
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
    'person',
    'callback'
])

const cropper = ref(null)
const inputPic = ref(null)

const errors = []

const imgSrc = ref('')
const cropImg = ref('')
const data = ref(null)

const picFile = ref('')
const imgPicWidth = ref(0)
const imgPicHeight = ref(0)
const mime_type = ref('')


const setImage = (e) => {
    picFile.value = e.target.files[0];
    const file = picFile.value

    if (file == undefined) {
        imgSrc.value = ''
        imgPicWidth.value = 0
        imgPicHeight.value = 0
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
                    imgPicWidth.value = img.width
                    imgPicHeight.value = img.height
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

const cropPicPerson = async () => {
    cropper.value.getCroppedCanvas({ width: 300, height: 300}).toBlob((blob) => {
        const formData = new FormData()

        formData.append('reffield', props.person.id)
        formData.append('image', blob, picFile.value.name)

        if (props.person.pic_person.length == 0) {
            formData.append('isPic', true)
        }

        axios 
            .post('/api/v1/person-pic/', formData, { 
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

    inputPic.value.value = ''
    imgSrc.value = ''
    imgPicWidth.value = 0
    imgPicHeight.value = 0
    mime_type.value = ''

}

const setPicPerson = async (pic) => {

    const formFalse = new FormData()
    formFalse.append('isPic', false)

    for (let i = 0; i < props.person.pic_person.length; i ++) {

        const imageID = props.person.pic_person[i].id

        await axios
            .patch(`/api/v1/person-pic/${imageID}/`, formFalse, { 
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
    formTrue.append('isPic', true)

    await axios
        .patch(`/api/v1/person-pic/${pic.id}/`, formTrue, { 
            headers: {
                "Content-Type": "multipart/form-data",
            }
        })
        .then(response => {
            console.log(response)
            createToast(
                'Pic changed successfully', 
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

const deletePicPerson = async (image) => {
    await axios 
        .delete(`/api/v1/person-pic/${image.id}`)
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

<style scoped>
.crop-area-pic {
    width: 350px !important;
    height: 350px !important;
    display:flex;
    justify-content:center;
    align-items:center;
    background-color: grey;
    margin-top: 20px;
}

.pic-preview-area {
    width: 300px;
    margin-top: 15px;
    font-size: 20px;
}

.pic-preview {
    width: 200px;
    height: 200px;
  /* width: 100%; */
  /* height: 100%; */
  /* height: calc(372px * (9 / 16)); */
    overflow: hidden;
    border-radius: 50%;
}

/* .crop-area-pic-inside {
    width: 350px !important;
    height: 350px !important;
    display:flex;
    justify-content:center;
    align-items:center;
    background-color: grey;
} */
</style>
