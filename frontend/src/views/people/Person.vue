<template>
    <div class="person-container">
        <template v-if="isPerson">
            <div class="header" :style="{ backgroundImage: 'url(' + person.cover + ')' }">    
            </div>
            <div>
                <div class="row">

                    <div class="left col-lg-4">
                        <div class="photo-left">
                            <img class="photo" :src="person.pic"/>
                        </div>
                    </div>

                    <div class="center col-lg-3">
                        <div class="profile-name">{{ person.name }}</div>
                        <div class="profile-role" v-html="person.roleMD"></div>
                    </div>

                    <div class="col-lg-5 ccol">
                        <div class="row d-flex justify-content-end">
                            
                            <div class="right-email col-lg-auto">
                                <div class="float-end text-secondary" style="margin-top: 5px; font-size: 20px;">
                                    <span class="profile-email">{{ person.email }}</span>
                                </div>
                            </div>

                            <div class="right-links col-lg-auto">
                                <div class="float-end text-secondary" style="margin-top: 5px; font-size: 20px;">
                                <span v-show="person.link_scholar">
                                    <abbr style="cursor: pointer;" title="Scholar">
                                        <a :href="person.link_scholar" target="_blank">
                                            <img src="@/assets/icons/scholar.svg/" style="width: 30px; margin-right: 15px;">
                                        </a>
                                    </abbr>
                                </span>
                                
                                <span v-show="person.pdf">
                                    <abbr style="cursor: pointer;" title="Curriculum">
                                        <a :href="person.pdf" target="_blank">
                                            <img src="@/assets/icons/cv.svg/" style="width: 24px; margin-right: 15px;">
                                        </a>
                                    </abbr>
                                </span>

                                <span v-show="person.github">
                                    <abbr style="cursor: pointer;" title="Github">
                                        <a :href="person.github" target="_blank">
                                            <img src="@/assets/icons/github.svg/" style="width: 30px; margin-right: 15px;">
                                        </a>
                                    </abbr>
                                </span>
                                
                                <span v-show="person.linkedin">
                                    <abbr style="cursor: pointer;" title="Linkedin">
                                        <a :href="person.linkedin" target="_blank">
                                            <img src="@/assets/icons/linkedin.svg/" style="width: 30px;">
                                        </a>
                                    </abbr>
                                </span>
                                </div>
                            </div>

                        </div>
                    </div>

                </div>
            </div>

            <div class="md-content" v-html="person.contentMD"></div>
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

const person = ref({})
const isPerson = ref(false)

const getPerson = async () => {
    paramStore.isLoading = true

    const personSlug = route.params.slug
            
    await axios
        .get(`/api/v1/people/${personSlug}`)
        .then(response => {
            person.value = response.data
            // console.log(person.value)
            isPerson.value = true
 
            if (person.value.content != null) {
                person.value.contentMD = marked(person.value.content)
            } else {
                person.value.contentMD = ''
            }

            if (person.value.role != null) {
                person.value.roleMD = marked(person.value.role)
            } else {
                person.value.roleMD = ''
            }

            if (person.value.pic_person.length > 0) {
                person.value.pic = person.value.pic_person.filter(
                    pic => pic.isPic == true)[0].image
            } else {
                person.value.pic = '/media/website/people/pic_default.png'
            }

            if (person.value.cover_person.length > 0) {
                person.value.cover = person.value.cover_person.filter(
                    cover => cover.isCover == true)[0].image
            } else {
                person.value.cover = '/media/website/people/cover_person.jpg'
            }

            if (person.value.pdf_personCV.length > 0) {
                person.value.pdf = person.value.pdf_personCV.filter(
                    pdf => pdf.isPDF == true)[0].file
            } else {
                person.value.pdf = ''
            }
        })
        .catch(error =>{
            console.log(error)
        })
    paramStore.isLoading = false
}

onMounted(() => {
    getPerson()
})
</script>

<style scoped lang="scss">

.person-container {
//   max-width: 1250px;
    max-width: 1000px;
    margin: 30px auto 100px;
    padding: 0 !important;
    width: 85%;
    background-color: #fff;
}

.header {
    background: #eee;
    background-repeat: no-repeat;
    background-position: center;
    background-size: cover;
    background-color: black;
    height: 250px;
    border-radius: 25px;
}

.row {
    --bs-gutter-x: 0;
}

.profile-name{
    font-size: 30px;
    font-weight: bold;
    margin-top: 5px;
}

.profile-email {
    font-size: 15px; 
    margin-right: 20px;
}

.profile-role{
    font-size: 18px;
}

@media (max-width:800px) {
    .header {
        height: 150px;
    } 
}

.ccol {
    margin: 0;
    padding: 0;
}

.left {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    padding: 0;
    margin: 0 -55px 0 0;
}

.center {
    //   display: flex;
    //   align-items: right;
    justify-content: left;
    margin: 0;
    padding: 0;
    margin-right: 55px;
    //   flex-direction: column;
    //   float: left;
}

.right-email {
    margin: 0;
    padding: 0;
}

.right-links {
    margin: 0px;
    padding: 0px;
}

.photo {
    width: 180px;
    height: 180px;
    margin-top: -90px;
    border-radius: 100px;
    border: 1px solid #fff;
    padding: 7px;
    background: #fff;
}

@media (max-width:991px) {
    .active {
        right: calc(50% - 60px);
        top: 50px;
    }

    .center {
        align-items: center;
        justify-content: center;
        flex-direction: column;
        text-align: center;
        margin: 0px;
    }

    .right-email {
        display: flex;
        text-align: center;
        flex-direction: column;
        padding: 0 0 0 20px;
        margin: 0px;
    }

    .right-links {
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        padding: 0px;
        margin: 0px;
    }
}

.md-content {
	text-align: justify;
	&:deep(p) {
		hyphens: auto;
        -ms-hyphens: auto;
        -webkit-hyphens: auto;
	}
}
</style>