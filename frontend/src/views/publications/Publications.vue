<template>
    <div class="publication-container">
        <div class="row justify-content-between">
            <div class="col col-md-4">
                <h4 class="head-title">Publications</h4>
            </div>
            <div class="col col-md-4">
                <div class="multiselect-container">
                    <Multiselect
                        v-model="relatedFieldsSelector.value"
                        v-bind="relatedFieldsSelector"
                        placeholder="Show publications by research field"
                        class="multiselect-blue"
                    >
                        <template v-slot:multiplelabel="{ values }">
                            <div class="multiselect-multiple-label">
                                <template v-if="values.length==1">
                                    {{ values[0].label }}    
                                </template>
                                <template v-else>
                                    {{ values.length }} research fields selected
                                </template>
                            </div>
                        </template>
                    </Multiselect>
                </div>
            </div>
        </div>
        
        <p class="equal-authors">* <em>Contributed equally to this work</em></p>
        
        <template v-if="relatedFieldsSelector.value.length == 0">

            <div v-for="pub in publicationsYear" :key="pub.id" class="mt-4">
                <div class="pub-year">{{ pub.year }}</div>
                <div class="pub-block" v-for="p in pub.pub" :key="p.id">
                    <div>
                        <em>{{ p.authors }}</em>
                    </div>
                    <div class="pub-title text-primary">
                        {{ p.title }}
                    </div> 
                    <div>
                        <em>{{ p.magazine }}</em> &mdash; {{ p.year }} &mdash; {{ p.doi }} 
                    </div>
                    
                    
                    <span v-show="p.pdf">
                        <a :href="p.pdf" target="_blank">
                            <i class="bi bi-file-pdf text-danger me-1"></i>
                            <strong class="text-dark">PDF</strong>
                        </a>
                    </span> 
                    
                    <span class="ms-1 me-1" v-show="p.pdf && p.link">&mdash;</span>
                    <span class="ms-1 me-1" v-show="p.pdf && p.bibtex">&mdash;</span>
                    <span class="ms-1 me-1" v-show="p.pdf && p.corresponding">&mdash;</span>
                    
                    <span v-show="p.link"> 
                        <a :href="p.link" target="_blank">
                            <i class="bi bi-link-45deg text-danger me-1"></i>
                            <strong class="text-dark">Link</strong>
                        </a> 
                    </span>

                    <span class="ms-1 me-1" v-show="p.link && p.bibtex">&mdash;</span>
                    <span class="ms-1 me-1" v-show="p.link && p.corresponding">&mdash;</span>

                    <span v-show="p.bibtex">
                        <abbr title="Copy BibTeX" @click="copyBibtex(p.bibtex)">
                            <i  
                                class="bi bi-file-code text-danger me-1">
                            </i>
                            <strong class="text-dark">BibTeX</strong>
                        </abbr>
                    </span>

                    <span class="ms-1 me-1" v-show="p.bibtex && p.corresponding">&mdash;</span>

                    <span v-show="p.corresponding">
                        <abbr title="Copy Corresponding Author Email" @click="copyEmail(p.corresponding)">
                            <i 
                                class="bi bi-envelope text-danger me-1">
                            </i> 
                            <strong class="text-dark">{{ p.corresponding }}</strong>
                        </abbr>
                    </span>

                </div>
            </div>

        </template>

        <template v-else>
            <template v-if="publicationsField.length">
                <div v-for="field in publicationsField" :key="field.slug">
                    <template v-if="relatedFieldsSelector.value.includes(field.field)">
                        <div class="field-title">{{ field.field }}</div>

                        <div v-for="pub in field.pubs" :key="pub.id">
                            <div class="pub-year">{{ pub.year }}</div>
                            
                            <div class="pub-block" v-for="p in pub.pub" :key="p.id">
                                <div>
                                    <em>{{ p.authors }}</em>
                                </div>
                                <div class="pub-title text-primary">
                                    {{ p.title }}
                                </div>
                                <div>
                                    <em>{{ p.magazine }}</em> &mdash; {{ p.year }} &mdash; {{ p.doi }} 
                                </div>
                                
                                <span v-show="p.pdf">
                                    <a :href="p.pdf" target="_blank">
                                        <i class="bi bi-file-pdf text-danger me-1"></i>
                                        <strong class="text-dark">PDF</strong>
                                    </a>
                                </span> 
                                
                                <span class="ms-1 me-1" v-show="p.pdf && p.link">&mdash;</span>
                                <span class="ms-1 me-1" v-show="p.pdf && p.bibtex">&mdash;</span>
                                <span class="ms-1 me-1" v-show="p.pdf && p.corresponding">&mdash;</span>
                                
                                <span v-show="p.link"> 
                                    <a :href="p.link" target="_blank">
                                        <i class="bi bi-link-45deg text-danger me-1"></i>
                                        <strong class="text-dark">Link</strong>
                                    </a> 
                                </span>

                                <span class="ms-1 me-1" v-show="p.link && p.bibtex">&mdash;</span>
                                <span class="ms-1 me-1" v-show="p.link && p.corresponding">&mdash;</span>

                                <span v-show="p.bibtex">
                                    <abbr title="Copy BibTeX" @click="copyBibtex(p.bibtex)">
                                        <i  
                                            class="bi bi-file-code text-danger me-1">
                                        </i>
                                        <strong class="text-dark">BibTeX</strong>
                                    </abbr>
                                </span>

                                <span class="ms-1 me-1" v-show="p.bibtex && p.corresponding">&mdash;</span>

                                <span v-show="p.corresponding">
                                    <abbr title="Copy Corresponding Author Email" @click="copyEmail(p.corresponding)">
                                        <i 
                                            class="bi bi-envelope text-danger me-1">
                                        </i> 
                                        <strong class="text-dark">{{ p.corresponding }}</strong>
                                    </abbr>
                                </span>

                            </div>
                        </div>
                    </template>    
                </div>
            </template>
            <template v-else>
                No publication associated to this research field
            </template>
        </template>

        <div class="equal-authors pb-4">* <em>Contributed equally to this work</em></div>

    </div>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { marked } from 'marked'
import Multiselect from '@vueform/multiselect'
import { createToast } from "mosha-vue-toastify"

import { useParamStore } from '@/stores/ParamStore'

const paramStore = useParamStore()

const loading = ref(false)
const publications = ref([])

const publicationsField = ref([])
const publicationsYear = ref([])

const research_fields = ref([])

const relatedFieldsSelector = ref({
    mode: 'multiple',
    hideSelected: false, 
    closeOnSelect: false,
    value: [],
    options: {}
})

const getPublications = async () => {
    paramStore.isLoading = true
    loading.value = true

    await axios
        .get('/api/v1/publications/')
        .then(response => {

            loading.value = false
            publications.value = response.data 
            // console.log(publications.value)                    
        })
        .catch(error =>{
            console.log(error)
        })

    for (let i = 0; i < publications.value.length; i++) {
        
        if (publications.value[i].pdf_publication.length > 0) {
            publications.value[i].pdf = publications.value[i].pdf_publication.filter(
                pdf => pdf.isPDF == true)[0].file
        } else {
            publications.value[i].pdf = ''
        }

        let fullDate = "10 " + publications.value[i].year
        let year = new Date(fullDate)
        publications.value[i].fullYear = year.getFullYear()
    }

    let pubList = publications.value.reduce((b, a) => {
        let index = b.findIndex(f => f.year === a.fullYear);
        if (index < 0) b.push({
            year: a.fullYear,
            pub: [a]
        });
        else b[index].pub.push(a);
        return b;
        }, []).sort((a, b) => b.year - a.year);


    for (let i = 0; i < pubList.length; i++) {
        pubList[i].pub = pubList[i].pub.sort((a, b) => {
            return new Date("10 " + b.year).getTime() - new Date("10 " + a.year).getTime(); 
        })
    }
    
    publicationsYear.value = pubList
    // console.log(publicationsYear.value)


    let pubListField = publications.value.reduce((b, a) => {
        for (let i = 0; i < a.field.length; i++) {
            let index = b.findIndex(f => f.field === a.field[i].title);
            if (index < 0) b.push({
                field: a.field[i].title,
                pubs: [a]
            });
            else b[index].pubs.push(a);
        }
        return b
    }, []).sort((a, b) => a.field.localeCompare(b.field));

    for (let i = 0; i < pubListField.length; i++) {
        let pubListFieldYear = pubListField[i].pubs.reduce((b, a) => {
            let index = b.findIndex(f => f.year === a.fullYear);
            if (index < 0) b.push({
                year: a.fullYear,
                pub: [a]
            });
            else b[index].pub.push(a);
            return b;
            }, []).sort((a, b) => b.year - a.year);

            pubListField[i].pubs = pubListFieldYear
    }

    for (let i = 0; i < pubListField.length; i++) {
        for (let j = 0; j < pubListField[i].pubs.length; j++) {
            pubListField[i].pubs[j].pub = pubListField[i].pubs[j].pub.sort((a, b) => {
            return new Date("10 " + b.year).getTime() - new Date("10 " + a.year).getTime(); 
            })
        }
    }

    publicationsField.value = pubListField
    paramStore.isLoading = false
}

const getResearchFields = async () => {
    paramStore.isLoading = true

    await axios
        .get('/api/v1/research/')
        .then(response => {
            research_fields.value = response.data
        })
        .catch(error =>{
            console.log(error)
        })

    let fields_title = research_fields.value.map(field => field.title).sort((a, b) => a.localeCompare(b))
    let keys = research_fields.value.map(key => key.title).sort((a, b) => a.localeCompare(b))

    for (var i = 0; i < keys.length; i++) {
        relatedFieldsSelector.value.options[keys[i]] = fields_title[i]
    }
    paramStore.isLoading = false
}

onMounted(() =>{
    getPublications()
    getResearchFields()
})

const copyBibtex = (str) => {
    // Create new element
    var el = document.createElement('textarea');
    // Set value (string to be copied)
    el.value = str;
    // Set non-editable to avoid focus and move outside of view
    el.setAttribute('readonly', '');
    el.style = {position: 'absolute', left: '-9999px'};
    document.body.appendChild(el);
    // Select text inside element
    el.select();
    // Copy text to clipboard
    document.execCommand('copy');
    // Remove temporary element
    document.body.removeChild(el);

    createToast(
        'BibTeX copied successfully', 
        paramStore.toastSuccess
    )
}

const copyEmail = (str) => {
    // Create new element
    var el = document.createElement('textarea');
    // Set value (string to be copied)
    el.value = str;
    // Set non-editable to avoid focus and move outside of view
    el.setAttribute('readonly', '');
    el.style = {position: 'absolute', left: '-9999px'};
    document.body.appendChild(el);
    // Select text inside element
    el.select();
    // Copy text to clipboard
    document.execCommand('copy');
    // Remove temporary element
    document.body.removeChild(el);

    createToast(
        'Corresponding email copied successfully', 
        paramStore.toastSuccess
    )
}
</script>

<style src="@vueform/multiselect/themes/default.css"></style>

<style scoped lang="scss">
.publication-container {
    max-width: 1000px;
    margin: 40px auto 60px;
    padding: 0 !important;
    width: 80%;
    background-color: #fff;
}

.multiselect-container {
    max-width: 300px;
}

.multiselect-blue {
    --ms-tag-bg: #DBEAFE;
    --ms-tag-color: #2563EB;
    --ms-option-bg-selected: #2563EB;
    --ms-option-bg-selected-pointed: #2563EB;
    --ms-font-size: 14px;
    --ms-line-height: 0.75;
    --ms-option-line-height: 0.75;
    --ms-option-font-size: 14px;
    z-index: 2;
}

.head-title {
    display: flex; 
    font-size: 30px;
    // margin-top: 20px;
}

.field-title {
    display: flex; 
    font-size: 24px;
    margin: 40px 0 20px 0;
    font-weight: 500;
}

.equal-authors {
    font-size: 13px; 
    margin: 20px 0;
}

a, abbr {
    text-decoration: none !important;
    cursor: pointer !important;
}

.pub-year {
    font-size: 26px; 
    margin-bottom: 10px;
    font-weight: bold;
}

.pub-block {
    margin-left: 40px;
    margin-bottom: 30px;
    font-size: 14px;
}

.pub-title {
    font-weight: 600; 
    font-size: 18px;
}

@media screen and (max-width: 399px) {
    .field-title {
        display: flex; 
        font-size: 20px;
        margin: 40px 0 20px 0;
        font-weight: 500;
    }
    
    .multiselect-blue {
        --ms-tag-bg: #DBEAFE;
        --ms-tag-color: #2563EB;
        --ms-option-bg-selected: #2563EB;
        --ms-option-bg-selected-pointed: #2563EB;
        --ms-font-size: 12px;
        --ms-line-height: 1;
        --ms-option-line-height: 0.75;
        --ms-option-font-size: 12px;
        padding: 10px 1px 10px 1px;
        z-index: 2;
    }
}
</style>