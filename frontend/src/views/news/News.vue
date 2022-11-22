<template>
    <div class="news-container">
        <div>
            <h4 class="head-title">News</h4>
            <input class="head-search" type="search" v-model="filter" placeholder="Search...">
        </div>

        <div v-for="news, index in sortedNews" :key="news.slug">
            <div 
                class="postcard" 
                :class="setClasses(index)"
            >
                <span class="postcard__img_content" href="#">
                    <img class="postcard__img" :src="news.cover" alt="Image Title" />
                </span>
                <div class="postcard__text t-dark">
                    <h1 :class="{'postcard__title blue': index % 3 == 0, 'postcard__title red': index % 3 == 1, 'postcard__title orange': index % 3 == 2}">
                        <router-link :to="{ name: 'NewsDetail', params: { slug: news.slug }}">{{ news.title }}</router-link>
                    </h1>
                    <div class="postcard__subtitle small">
                        <span>
                            {{ formatDate(news.publicated_at) }} | 
                            <span v-show="news.show_author && news.author.full_name" class="author">{{ news.author.full_name }}</span>
                            <span v-show="!news.show_author" class="author">Team</span>
                        </span>
                    </div>
                    <div class="postcard__bar"></div>
                    <div class="postcard__preview-txt long" v-html="get60words(news.contentMD)"></div>
                    <div class="postcard__preview-txt medium" v-html="get30words(news.contentMD)"></div>
                    <div class="postcard__preview-txt short" v-html="get15words(news.contentMD)"></div>
                </div>
            </div>
        </div>

        <div style="display: flex; justify-content: center; margin-top: 80px;">
            <v-pagination
                v-model="currentPage"
                :pages="pageCount"
                :range-size="1"
                active-color="#f1f1f1"
                @update:modelValue="loadPage"
                class="float-end"
                @click="backOnTop"
            />
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import axios from 'axios'
import { marked } from 'marked'

import VPagination from "@hennge/vue3-pagination";
import "@hennge/vue3-pagination/dist/vue3-pagination.css";

import { useParamStore } from '@/stores/ParamStore'

const paramStore = useParamStore()

const dayjs = require('dayjs')

const all_news = ref([])
const pageSize = ref(9)
const currentPage = ref(1) 
const perPage = ref(9)
const filter = ref('')

const currentSortDir = ref('asc')
const currentSort = ref('title')

const getNews = async () => {
    paramStore.isLoading = true

    await axios
        .get('/api/v1/news/')
        .then(response => {
            all_news.value = response.data 
            // console.log(all_news.value)

            for (let i = 0; i < all_news.value.length; i++) {
                all_news.value[i].contentMD = marked(all_news.value[i].content)
                
                if (all_news.value[i].cover_news.length > 0) {
                    all_news.value[i].cover = all_news.value[i].cover_news.filter(
                        ci => ci.isCover == true)[0].image
                } else {
                    all_news.value[i].cover = '/media/website/news/cover_news.png'
                }
            }

            var today = new Date();
            var dd = String(today.getDate()).padStart(2, '0');
            var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
            var yyyy = today.getFullYear();

            today = yyyy + '-' + mm + '-' + dd;

            all_news.value = all_news.value.filter(news => 
                news.publicated_at <=  today & 
                news.content != ""
            )

        })
        .catch(error =>{
            console.log(error)
        })

    paramStore.isLoading = false
}

onMounted(() => {
    getNews()
})

const setClasses = (index) => {
    if (index % 3 == 0 & index % 2 == 0 ) {
        return 'blue even blue-even'
    }

    if (index % 3 == 0 & index % 2 == 1 ) {
        return 'blue odd blue-odd'
    }

    if (index % 3 == 1 & index % 2 == 0 ) {
        return 'red even red-even'
    }

    if (index % 3 == 1 & index % 2 == 1 ) {
        return 'red odd red-odd'
    }

    if (index % 3 == 2 & index % 2 == 0 ) {
        return 'orange even orange-even'
    }

    if (index % 3 == 2 & index % 2 == 1 ) {
        return 'orange odd orange-odd'
    }
}

const loadPage = (page) => {
    currentPage.value = page;
}

// const showPerPage = () => {
//     pageSize.value = perPage.value
//     currentPage.value = 1
// }

const get15words = (value) => {
    return value.split(' ').slice(0, 14).join(' ').concat(' &#8230;')
}

const get30words = (value) => {
    return value.split(' ').slice(0, 29).join(' ').concat(' &#8230;')
}

const get60words = (value) => {
    return value.split(' ').slice(0, 59).join(' ').concat(' &#8230;')
}

const backOnTop = () => {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}


const hasFilter = (_news_, fil) => {
    if(fil.value !== '') {
        _news_ = _news_.filter(
            news => news.title.toLowerCase().indexOf(fil.value.toLowerCase()) >= 0 || 
            news.content.toLowerCase().indexOf(fil.value.toLowerCase()) >= 0
        );
    }
    return _news_
}

const sortedNews = computed(() => {
    let _news = all_news.value;

    _news = hasFilter(_news, filter)

    return _news.sort((a,b) => {
        let modifier = 1;
        if(currentSortDir.value === 'desc') modifier = -1;
        if(a[currentSort.value] < b[currentSort.value]) return -1 * modifier;
        if(a[currentSort.value] > b[currentSort.value]) return 1 * modifier;
        return 0;
    }).filter((row, index) => {
        let start = (currentPage.value-1)*pageSize.value;
        let end = currentPage.value*pageSize.value;
        if(index >= start && index < end) return true;
    });

})

const pageCount = computed(() => {
    let _news = all_news.value

    _news = hasFilter(_news, filter)
    return Math.ceil(_news.length / pageSize.value)
})

// const filterCount = computed(() => {
//     let _news = all_news.value

//     _news = hasFilter(_news, filter)
//     return _news.length
// })

watch(() => filter.value, () => {
    currentPage.value = 1;
})

const formatDate = (value) => {
    if (value) {
        return dayjs(String(value)).format('DD MMM YY')
    }
}
</script>

<style lang="scss" scoped>
// @import url("https://fonts.googleapis.com/css2?family=Baloo+2&display=swap");
$main-green: #00ff00 !default;
// $main-green-rgb-015: rgba(121, 221, 9, 0.1) !default;
$main-green-rgb-015: rgba(0, 255, 0, 0.15) !default;
$main-orange: #ffa500 !default;
// $main-orange-rgb-015: rgba(189, 187, 73, 0.1) !default;
$main-orange-rgb-015: rgba(255, 165, 0, 0.15) !default;
$main-red: #ee2c2c !default;
// $main-red-rgb-015: rgba(189, 21, 11, 0.1) !default;
$main-red-rgb-015: rgba(238, 44, 44, 0.15) !default;
$main-blue: #36648b !default;
$main-blue-rgb-015: rgba(54, 100, 139, 0.15) !default;
// $main-blue-rgb-015: rgba(0, 118, 189, 0.1) !default;

a, a:hover {
	text-decoration: none;
	transition: color 0.3s ease-in-out;
}

.news-container {
//   max-width: 1250px;
    max-width: 1000px;
    margin: 60px auto 100px;
    padding: 0 !important;
    width: 80%;
    background-color: #fff;
}

.head-title {
    display: flex; 
    // justify-content: center;
    font-size: 30px;
    // margin-bottom: 50px;
}

.head-search {
    margin: 10px 1px 20px 1px;
    border-radius: 5px;
    padding: 4px 4px 4px 10px;
    width: 100%;
    border: 1px solid lightgray;

    &:focus {
        outline: none;
        box-shadow: none;
    }
}

// Cards
.postcard {
    flex-wrap: wrap;
    display: flex;
    
    box-shadow: 0 4px 21px -12px rgba(0, 0, 0, 0.66);
    border-radius: 10px;
    border: solid 1px lightgray;
    margin: 0 0 2rem 0;
    overflow: hidden;
    position: relative;
    // background: #eee;
    background: #fff;

	.t-dark {
		color: #18151f;
	}
	
    a {
        color: inherit;
    }
	
	.small {
		font-size: 80%;
	}

    .postcard__title {
        font-size: 26px;
    }

    .postcard__img {
        max-height: 180px;
        // max-height: 100px;
        width: 100%;
        object-fit: cover;
        position: relative;
    }

    .postcard__img_content {
        display: contents;
    }

    .postcard__bar {
        width: 50px;
        height: 8px;
        margin: 10px 0 10px 0;
        // padding: 10px 0 20px 0;
        border-radius: 5px;
        background-color: #424242;
        transition: width 0.2s ease;
    }

    .postcard__text {
        // padding: 1.5rem;
        position: relative;
        display: flex;
        flex-direction: column;
        padding: 1.5rem 1rem 0.5rem 1rem;
    }

    &:before {
        content: "";
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        // background-image: linear-gradient(-70deg, #424242, transparent 50%);
        opacity: 1;
        border-radius: 10px;
    }

    &:hover .postcard__bar {
        width: 100px;
    }
}


@media screen and (min-width: 589px) {

    // .short {
    //     display: none;
    // }

    .even {
        flex-direction: row;
        .postcard__text::before {
            left: -12px !important;
        }
    }

    .odd {
        flex-direction: row-reverse;
        .postcard__text::before {
            right: -12px !important;
        }
    }

    .postcard {
        flex-wrap: inherit;

        .postcard__img {
            max-width: 300px;
            max-height: 100%;
            transition: transform 0.3s ease;
        }

        .postcard__text {
            padding: 1.5rem 2.5rem 1rem 2.5rem;
            // padding: 1.5rem 1rem 1.5rem 1rem;
            width: 100%;
        }

        .media.postcard__text:before {
            content: "";
            position: absolute;
            display: block;
            background: #18151f;
            top: -20%;
            height: 130%;
            width: 55px;
        }

        &:hover .postcard__img {
            transform: scale(1.1);
        }

        .postcard__preview-txt {
            overflow: hidden;
            text-overflow: ellipsis;
            text-align: justify;
            height: 200%;
            // margin-bottom: 10px;
        }
    }
}


// Color
.postcard .postcard__tagbox .blue.play:hover {
	background: $main-blue;
}
.blue .postcard__title:hover {
	color: $main-blue;
}
.blue .postcard__bar {
	background-color: $main-blue;
}

.blue .author {
    color: $main-blue;
}

// .blue::before {
// 	background-image: linear-gradient(0deg, $main-blue-rgb-015, transparent 50%);
// }

.postcard .postcard__tagbox .red.play:hover {
	background: $main-red;
}
.red .postcard__title:hover {
	color: $main-red;
}
.red .postcard__bar {
	background-color: $main-red;
}

.red .author {
    color: $main-red;
}

// .red::before {
// 	background-image: linear-gradient(-30deg, $main-red-rgb-015, transparent 50%);
// }
// .red:nth-child(2n)::before {
// 	background-image: linear-gradient(30deg, $main-red-rgb-015, transparent 50%);
// }

.postcard .postcard__tagbox .orange.play:hover {
	background: $main-orange;
	color: black;
}
.orange .postcard__title:hover {
	color: $main-orange;
}
.orange .postcard__bar {
	background-color: $main-orange;
}

.orange .author {
    color: $main-orange;
}

// .orange::before {
// 	background-image: linear-gradient(
// 		-30deg,
// 		$main-orange-rgb-015,
// 		transparent 50%
// 	);
// }
// .orange:nth-child(2n)::before {
// 	background-image: linear-gradient(
// 		30deg,
// 		$main-orange-rgb-015,
// 		transparent 50%
// 	);
// }


@media screen and (max-width: 859px) {
    .medium {
        display: none;
    }

    .long {
        display: none;
    }

    .postcard {
        .postcard__title {
            font-size: 24px;
        }

        .postcard__text {
        // padding: 1.5rem;
            position: relative;
            display: flex;
            flex-direction: column;
            padding: 1.5rem 1rem 1.5rem 1rem;
        }
    }
}

@media screen and (min-width: 860px) and (max-width: 1099px) {
    .short {
        display: none;
    }

    .long {
        display: none;        
    }
}

@media screen and (min-width: 1100px) {
    .short {
        display: none;
    }
    
    .medium {
        display: none;
    }
}
</style>