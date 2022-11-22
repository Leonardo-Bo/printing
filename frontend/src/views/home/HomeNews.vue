<template>
    <template v-if="isReady">
        <div class="home-news-container">
            <div v-for="news, index in all_news" :key="news.id">
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
                                {{ (news.publicated_at) }} | 
                                <span v-show="news.show_author && news.author.full_name" class="author">{{ news.author.full_name }}</span>
                                <span v-show="!news.show_author" class="author">Team</span>
                            </span>
                        </div>
                        <div class="postcard__bar"></div>
                        <div class="postcard__preview-txt medium" v-html="get120char(news.contentMD)"></div>
                    </div>
                </div>    
            </div>
        </div>
    </template>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { marked } from 'marked'

import { useParamStore } from '@/stores/ParamStore'

const paramStore = useParamStore()

const all_news = ref([])
const isReady = ref(false)

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

            all_news.value = all_news.value.sort((a, b) => {
                return new Date(b.publicated_at).getTime() - new Date(a.publicated_at).getTime()
            }).slice(0, 3)

            isReady.value = true

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

const get120char = (value) => {
    return value.slice(0, 119).concat('&#8230;')
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

.news-header {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    // width: 80%;
    font-size: 30px;
    font-weight: 600;
    border: solid 1px lightgray;
    padding: 5px;
    margin: 0px 250px;
    border-radius: 10px;
    background-color: #eee;
}


.home-news-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    width: 100%;
}

img {
    max-width: 100%;
    display: block;
    object-fit: cover;
}

// Cards
.postcard {
    // flex-wrap: wrap;
    display: flex;
    flex-direction: column;
    width: 300px;
    height: 450px;
    
    box-shadow: 0 4px 21px -12px rgba(0, 0, 0, 0.66);
    border-radius: 10px;
    border: solid 1px lightgray;
    margin: 20px 20px 60px 20px;
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
        font-size: 18px;
    }

    .postcard__img {
        max-height: 220px;
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
        height: 5px;
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
        font-size: 14px;
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
</style>