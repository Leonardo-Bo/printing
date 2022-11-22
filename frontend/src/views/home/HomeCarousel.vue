<template>
    <div id="homeCarousel" class="carousel slide mt-1 mb-5" data-bs-ride="carousel">
        
        <div class="carousel-indicators">
            <button 
                v-for="(item, idx) in carousel"
                :key="item.id"
                type="button"  
                data-bs-target="#carouselCaptions"
                :data-bs-slide-to="idx" :class="{ active: !idx }" aria-current="true">
            </button>
        </div>

        <div class="carousel-inner">
            <div 
                v-for="(item, idx) in carousel"
                :key="item.id"
                class="carousel-item" 
                :class="{ active: idx==0 }" 
            >
            <div class="header" :style="{ backgroundImage: 'url(' + item.cover + ')' }">    
            </div>
            <div id="caption-panel" class="carousel-caption">
                <h5>{{ item.title }}</h5>
                <p>{{ item.content }}</p>
                <template v-if="item.type == 'field'">
                    <router-link :to="{ name: 'ResearchFieldDetail', params: { slug: item.slug }}" class="btn btn-sm btn-dark float-end">READ MORE</router-link>
                </template>
                <template v-if="item.type == 'news'">
                    <router-link :to="{ name: 'NewsDetail', params: { slug: item.slug }}" class="btn btn-sm btn-dark float-end">READ MORE</router-link>
                </template>
            </div>
            </div>
        </div>

        <button class="carousel-control-prev" type="button" data-bs-target="#carouselCaptions" @click="prev()">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Previous</span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#carouselCaptions" @click="next()">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Next</span>
        </button>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { Carousel } from 'bootstrap'
import { useParamStore } from '@/stores/ParamStore'

const paramStore = useParamStore()

const carousel = ref([])
const carouselObj = ref(null)
const loading = ref(false)
const isReady = ref(false)
// const showPanel = ref('')
// const hidePanel = ref('')
// const ndx = ref('0')

const getCarousel = async () => {
    paramStore.isLoading = true
    loading.value = true

    await axios
        .get('/api/v1/carousel/')
        .then(response => {
            loading.value = false
            carousel.value = response.data 
            // console.log(carousel.value)
        })
        .catch(error =>{
            console.log(error)
        })

    for (let i=0; i < carousel.value.length; i++) {
        if (carousel.value[i].field != null) {
            carousel.value[i].title = carousel.value[i].field.title
            carousel.value[i].slug = carousel.value[i].field.slug
            carousel.value[i].type = "field"
        }

        if (carousel.value[i].news != null) {
            carousel.value[i].title = carousel.value[i].news.title
            carousel.value[i].slug = carousel.value[i].news.slug
            carousel.value[i].type = "news"
        }

        carousel.value[i].cover = carousel.value[i].cover_carousel.filter(
            ci => ci.isCover == true)[0].image
    }

    isReady.value = true
    paramStore.isLoading = false
}

const next = () => {
    carouselObj.value.next()
}

const prev = () => {
    carouselObj.value.prev()
}

onMounted(() => {
    let homeCarousel = document.querySelector('#homeCarousel')
    carouselObj.value = new Carousel(homeCarousel, { interval: 12000})
    getCarousel()
})
</script>

<style lang="scss" scoped>
.carousel {
    z-index: 0;
    background-color: black;
}
.header {
    background: #eee;
    background-repeat: no-repeat;
    background-position: center;
    background-size: cover;
    background-color: black;
    height: 400px;
}
#caption-panel {
    animation: cssAnimation 9.5s;
    animation-delay: 2.5s;
    opacity: 0;
}

@keyframes cssAnimation {
    from { opacity: 0; }
    25% { opacity: 1; }
    75% { opacity: 1; }
    to   { opacity: 0; }
}

.carousel-caption {
    padding: 1.25rem;
    color: #38444a;
    text-align: left;
    border-radius: 5px;
    left: 60%;
    bottom: 10%;
    background-color: rgba(238, 238, 238, 0.5);
}
.carousel-item {
  transition: transform 1.5s ease-in-out;
}

@media screen and (max-width: 768px) {
    .carousel-caption {
        padding: 1.25rem;
        color: #38444a;
        text-align: left;
        border-radius: 5px;
        left: 20%;
        right: 20%;
        bottom: 10%;
        background-color: rgba(238, 238, 238, 0.5);
    }
}
</style>
