<template>
    <div class="tools-container">
        <span v-for="tool in tools" :key="tool.id">
            <div class="card-container">
                <div class='card' :style="{ backgroundImage: 'url(' + tool.cover + ')' }">
                    <div class='info'>
                        <h1 class='title'>{{ tool.name }}</h1>
                        <div class="description" v-html="tool.contentMD"></div>
                        <div style="text-align: center;">
                            <a :href="tool.link" target="_blank" class="card__button">Open tool</a>
                        </div>
                    </div>
                </div>
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
const tools = ref([])

const getTools = async () => {
    paramStore.isLoading = true
    loading.value = true

    await axios
        .get('/api/v1/tools/')
        .then(response => {
            loading.value = false
            tools.value = response.data 
            // console.log(tools.value)

            tools.value = tools.value.filter(tool => tool.show_tool == true)
            
            for (let i = 0; i < tools.value.length; i++) {
                tools.value[i].contentMD = marked(tools.value[i].content)
                
                if (tools.value[i].cover_tool.length > 0) {
                    tools.value[i].cover = tools.value[i].cover_tool.filter(
                        ci => ci.isCover == true)[0].image
                } else {
                    tools.value[i].cover = '/media/website/tools/cover_tool.png'
                }
            }            
        })
        .catch(error =>{
            console.log(error)
        })

    paramStore.isLoading = false
}

onMounted(() => {
    getTools()
})
</script>

<style lang="scss" scoped>

$desktop: 1076px;
$desktop2: 1550px;

@mixin breakpoint($point) {
    @if $point == desktop {
        @media (min-width: $desktop) {
            @content;
		}
	}
}

@mixin breakpoint2($point) {
    @if $point == desktop {
        @media (min-width: $desktop2) {
            @content;
		}
	}
}

.tools-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    margin-left: auto;
    margin-right: auto;
    margin-top: 30px;
    margin-bottom: 80px;

    @include breakpoint(desktop) {
        width: 850px;
    }

    @include breakpoint2(desktop) {
        width: 1000px;
        margin-top: 100px;
    }
}

.card-container {
    padding: 10px;
}

.card {
    border-radius: 5px;
    margin: 0 auto;
    width: 250px;
    height: 250px;
    border: solid 2px #eee;
    overflow: hidden;
    background-size: cover;

    @include breakpoint2(desktop) {
        width: 300px;
        height: 300px;
    }

    &__button {
		display: inline-block;
        padding: 10px 20px;
        color: #2c3e50;
        border: 1px solid #2c3e50;
        font-size: 12px;
        text-transform: uppercase;
        text-decoration: none;
        transition: 0.5s;

		&:hover {
			color: white;
			background-color: #2c3e50;
		}
	}
    
}

.info {
    position: relative;
    width: 100%;
    height: 250px;
    background-color: #eee;
    opacity: 0.85;
    transform: translateY(100%)
        translateY(-60px)
        translateZ(0);
    transition: transform 0.5s ease-out;

    @include breakpoint2(desktop) {
        width: 300px;
        height: 300px;
    }
}

.info:before {
    z-index: -1;
    display: block;
    position: absolute;
    content: ' ';
    width: 100%;
    height: 100%;
    overflow: hidden;
    background-size: cover;
    transform: translateY(-100%)
        translateY(88px)
        translateZ(0);
    transition: transform 0.5s ease-out;
}

.card:hover .info,
.card:hover .info:before {
    transform: translateY(0) translateZ(0);
}

.title {
    margin: 0;
    padding: 20px;
    font-size: 20px;
    line-height: 1;
    font-weight: 500;
}

.description {
    margin: 0;
    padding: 0 20px 10px 20px;
    font-size: 14px;
}
</style>