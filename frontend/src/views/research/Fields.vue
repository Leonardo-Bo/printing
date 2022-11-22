<template>
    <div class="fields-container">
        <span v-for="field in research_fields" :key="field.id">
            <div class="card" v-show="field.content">
                <figure class="card__thumb">
                    <img :src="field.cover" class="card__image">
                    <figcaption class="card__caption">
                        <h2 class="card__title">{{ field.title }}</h2>
                        <div class="card__snippet" v-html="get15words(field.contentMD)"></div>
                        <router-link :to="{ name: 'ResearchFieldDetail', params: { slug: field.slug }}" class="card__button">Read more</router-link>
                    </figcaption>
                </figure>
            </div>
        </span>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { marked } from 'marked'

import { useParamStore } from '@/stores/ParamStore'

const paramStore = useParamStore()

const loading = ref(false)
const research_fields = ref([])

const getResearchFields = async () => {
    paramStore.isLoading = true
    loading.value = true

    await axios
        .get('/api/v1/research/')
        .then(response => {

            loading.value = false
            research_fields.value = response.data 
            
            for (let i = 0; i < research_fields.value.length; i++) {
                research_fields.value[i].contentMD = marked(research_fields.value[i].content)
                
                if (research_fields.value[i].cover_research.length > 0) {
                    research_fields.value[i].cover = research_fields.value[i].cover_research.filter(
                        ci => ci.isCover == true)[0].image
                } else {
                    research_fields.value[i].cover = '/media/website/research/cover_field.png'
                }        
            }
            research_fields.value = research_fields.value.filter(a => a.show_in_page === true).sort((a, b) => { return a.position - b.position })
        })
        .catch(error =>{
            console.log(error)
        })

    paramStore.isLoading = true
}

onMounted(() => {
    getResearchFields()
})

const get15words = (value) => {
            return value.split(' ').slice(0, 14).join(' ').concat(' &#8230;')
        }
</script>

<style lang="scss" scoped>

$desktop: 300px;

@mixin breakpoint($point) {
  @if $point == desktop {
    @media (min-width: $desktop) {
      @content;
		}
	}
}

.fields-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    width: 100%;
    margin-top: 30px;
    margin-bottom: 80px;
}
.card {
	width: 240px;
    height: 360px;
    margin: 20px;
    border-radius: 15px;
    box-shadow: 0 5px 10px 0 rgba(0, 0, 0, 0.5);

    @include breakpoint(desktop) {
        width: 300px;
        height: 450px;
    }
	&:hover {
		.card__caption {
			top: 50%;
			transform: translateY(-50%);
		}
		.card__thumb {
			&::after {
				top: 0;
			}
		}
		.card__snippet {
			margin: 20px 0;
		}
	}
	&__thumb {
		position: absolute;
        max-height: 360px;
        overflow: hidden;
        /* margin: 0; */
        /* padding: 0; */
        border-radius: 15px;

		@include breakpoint(desktop) {
			max-height: 450px;
		}
		&::after {
			position: absolute;
			// top: 0;
            top: calc(100% - 140px);
			display: block;
			content: '';
			width: 100%;
			height: 100%;
            background: linear-gradient(0deg, rgba(0, 0, 0, 0.75) 100%, rgba(255, 255, 255, 0) 100%);
			transition: 1.5s;
            margin: 0;
            padding: 0;
		}
	}
	&__image {
		transition: .5s ease-in-out;
        width: 240px;
        height: 360px;
        border-radius: 15px;

        @include breakpoint(desktop) {
			width: 300px;
            height: 450px;
		}
	}
	&__caption {
		position: absolute;
        top: calc(100% - 110px);
        z-index: 1;
        padding: 0 20px;
        color: white;
        transform: unset;
        text-align: center;
        transition: 1.5s;
    }
	&__title {
		display: -webkit-box;
        max-height: 85px;
        overflow: hidden;
        text-align: center;
        font-size: 23px;
        line-height: 28px;
        text-shadow: 0px 1px 5px black;
        text-overflow: ellipsis;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        padding-bottom: 40px;
	}
	&__snippet {
		display: -webkit-box;
        max-height: 150px;
        margin: 60px 0;
        overflow: hidden;
        font-size: 16px;
        line-height: 20px;
        text-overflow: ellipsis;
        transition: 0.5s ease-in-out;
        -webkit-line-clamp: 5;
        -webkit-box-orient: vertical;
	}
	&__button {
		display: inline-block;
        padding: 10px 20px;
        color: white;
        border: 1px solid white;
        font-size: 12px;
        text-transform: uppercase;
        text-decoration: none;
        transition: 0.5s;
		&:hover {
			color: black;
			background-color: white;
		}
	}
}
</style>