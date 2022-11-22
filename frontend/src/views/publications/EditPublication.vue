<template>
<div>
    <h4 class="inline-h mb-4">Edit Publication</h4>

    <div v-if="isReady && isReady2" class="container-upload">
        <form @submit.prevent="editPublication">

            <div class="form-group mb-3">
                <label class="mb-1">Title*</label>
                <input
                    type="text"
                    class="form-control input-size"
                    style="font-size: 14px"
                    id="title"
                    v-model="publication_copy.title">
            </div>

            <div class="form-group mb-3">
                <label class="mb-1">Authors*</label>
                <input
                    type="text"
                    class="form-control"
                    style="font-size: 14px"
                    id="authors"
                    v-model="publication_copy.authors">
            </div>

            <div class="row">
                <div class="col-md-5">
                    <div class="form-group mb-3">
                        <label class="mb-1">Magazine*</label>
                        <input
                            type="text"
                            class="form-control"
                            style="font-size: 14px"
                            id="magazine"
                            v-model="publication_copy.magazine">
                    </div>               
                </div>

                <div class="col-md-5">
                    <div class="form-group mb-3">
                        <label class="mb-1">DOI*</label>
                        <input
                            type="text"
                            class="form-control"
                            style="font-size: 14px"
                            id="doi"
                            v-model="publication_copy.doi">
                    </div>
                </div>

                <div class="col-md-2">
                    <div class="form-group mb-3">
                        <label class="mb-1">Year*</label>
                        <input
                            type="text"
                            class="form-control"
                            style="font-size: 14px"
                            id="doi"
                            v-model="publication_copy.year">
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col md-6">

                    <div class="form-group mb-3">
                        <label class="mb-1">Corresponding Author</label>
                        <input
                            type="text"
                            class="form-control"
                            style="font-size: 14px"
                            id="link"
                            v-model="publication_copy.corresponding">
                    </div>

                    <div class="form-group mb-3">
                        <label class="mb-1">Link</label>
                        <input
                            type="text"
                            class="form-control"
                            style="font-size: 14px"
                            id="link"
                            v-model="publication_copy.link">
                    </div>

                    <div class="form-group mb-3">
                        <label class="mb-1">Related Research Fields</label>

                        <Multiselect
                            v-model="relatedFieldsSelector.value"
                            v-bind="relatedFieldsSelector"
                            placeholder=""
                            class="multiselect-blue"
                        >
                            <template v-slot:multiplelabel="{ values }">
                                <div class="multiselect-multiple-label">
                                    <template v-if="values.length==1">
                                        {{ values.length }} field selected    
                                    </template>
                                    <template v-else>
                                        {{ values.length }} fields selected
                                    </template>
                                </div>
                            </template>
                        </Multiselect>

                    </div>

                </div>
                <div class="col-md-6">
                    
                    <div class="form-group mb-3">
                        <label class="mb-1">Bibtex</label>
                        <textarea style="height: 197px; font-size: 14px" class="form-control" v-model="publication_copy.bibtex"></textarea>
                    </div>
                    
                </div>
            </div>

            <div class="mt-4" align="right">
                <router-link 
                    type="button" 
                    class="btn btn-sm btn-outline-secondary ms-1" 
                    to="/settings/publications"
                >Cancel
                </router-link>
                <button 
                    type="submit" 
                    class="btn btn-sm btn-outline-primary ms-1">Edit Publication
                </button>
            </div>
        </form>
    </div>

    <hr style="margin-top: 40px;">

    <pdf-publication
        :publication="publication"
        :callback="getPublication"
    />
    
</div>

</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import axios from 'axios'

import Multiselect from '@vueform/multiselect'

import PdfPublication from '@/components/files/PublicationPdf.vue'

import { createToast } from "mosha-vue-toastify"
import { useParamStore } from '@/stores/ParamStore'
import { useUserStore } from '@/stores/UserStore'
import { useRoute, useRouter } from 'vue-router';

const paramStore = useParamStore()
const userStore = useUserStore()
const router = useRouter()
const route = useRoute()

const publication = ref({})
const publication_copy = ref([])
// const publicationPDF = ref(undefined)
 
// const files = ref([])
const research_fields = ref([])
const errors = ref([])

const relatedFieldsSelector = ref({
    mode: 'multiple',
    hideSelected: false, 
    closeOnSelect: false,
    value: [],
    options: {}
})

const isReady = ref(false)
const isReady2 = ref(false)

const getPublication = async () => {
    paramStore.isLoading = true
    errors.value = []
    
    const publicationID = route.params.id
    
    await axios
        .get(`/api/v1/publications/${publicationID}`)
        .then(response => {
            publication.value = response.data
            // console.log(this.publication)
        })
        .catch(error =>{
            console.log(error)
        })

        if (publication.value.authors == '#') {
            publication.value.authors = ''
        }

        if (publication.value.magazine == '#') {
            publication.value.magazine = ''
        }

        if (publication.value.doi == '#') {
            publication.value.doi = ''
        }

        if (publication.value.year == '#') {
            publication.value.year = ''
        }

        relatedFieldsSelector.value.value = publication.value.field.map(field => field.id)

        if (publication_copy.value.length == 0) {
            publication_copy.value = publication.value
        }

        if (publication_copy.value.pdf_publication != publication.value.pdf_publication) {
            publication_copy.value.pdf_publication = publication.value.pdf_publication
        }

    isReady.value = true
    paramStore.isLoading = false
}

const getResearchFields = async () => {
    paramStore.isLoading = true

    await axios
        .get('/api/v1/research/')
        .then(response => {
            // this.loading = false
            research_fields.value = response.data
        })
        .catch(error =>{
            console.log(error)
        })

    let fields_title = research_fields.value.map(field => field.title)
    let keys = research_fields.value.map(key => key.id)

    for (var i = 0; i < keys.length; i++) {
        relatedFieldsSelector.value.options[keys[i]] = fields_title[i]
    }

    isReady2.value = true;
    paramStore.isLoading = false
}

onMounted(() => {
    getPublication()
    getResearchFields()
})

const editPublication = async () => {
    paramStore.isLoading = true    
    
    const publicationID = route.params.id

    publication_copy.value.author = publication_copy.value.author[0].id
    publication_copy.value.author_update = userStore.user.id

    if (publication_copy.value.field == "no-field") {
        publication_copy.value.field = null
    } 

    publication_copy.value.field = relatedFieldsSelector.value.value
                
    errors.value = []

    await axios
        .patch(`/api/v1/publications/${publicationID}/`, publication_copy.value)
        .then(response => {
            router.push('/settings/publications')

            createToast(
                'publication edited successfully', 
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

<style src="@vueform/multiselect/themes/default.css"></style>

<style lang="scss" scoped>
@import '~simplemde/dist/simplemde.min.css';

.input-size {
    font-size: 14px;
}

.multiselect-blue {
    --ms-tag-bg: #DBEAFE;
    --ms-tag-color: #2563EB;
    --ms-option-bg-selected: #2563EB;
    --ms-option-bg-selected-pointed: #2563EB;
    --ms-font-size: 14px;
    --ms-line-height: 1.50;
    --ms-option-line-height: 0.8;
    --ms-option-font-size: 14px;
}
</style>