<template>
    <div class="field-container">
        <template v-if="isField">
            <h2 class="mb-3">{{ field.title }}</h2>
            <div class="md-content" v-html="field.contentMD"></div>
        </template>
        <template v-else>
            <span style="font-size: 20px;">
                404: Page does not exist
            </span>
        </template>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { marked } from 'marked';
import { useParamStore } from '@/stores/ParamStore'
import { useRoute } from 'vue-router'

const paramStore = useParamStore()
const route = useRoute()

const field = ref({})
const isField = ref(false)

const getResearchField = async () => {
    paramStore.isLoading = true

    const fieldSlug = route.params.slug
    
    await axios
        .get(`/api/v1/research/${fieldSlug}`)
        .then(response => {
            field.value = response.data
            // console.log(field.value)
            field.value.contentMD = marked(field.value.content)
            isField.value = true
        })
        .catch(error =>{
            console.log(error)
        })
    paramStore.isLoading = false
}

onMounted(() => {
    getResearchField()
})
</script>

<style lang="scss" scoped>
.field-container {
    margin-top: 60px;
    margin-bottom: 100px;
}

.md-content {
	text-align: justify;
	&:deep(p) {
		hyphens: auto;
        -ms-hyphens: auto;
        -webkit-hyphens: auto;
	}
}

@media screen and (min-width: 279px) and (max-width: 769px) {
    .field-container {
        margin-left: 20px;
        margin-right: 20px;
    }
}

@media screen and (min-width: 770px) and (max-width: 1179px) {
    .field-container {
        margin-left: 90px;
        margin-right: 90px;
    }
}

@media screen and (min-width: 1180px) {
    .field-container {
        margin-left: 180px;
        margin-right: 180px;
    }
}
</style>