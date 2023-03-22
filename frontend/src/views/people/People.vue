<template>
    <div class="container">

        <span v-for="person in people" :key="person.id">
            <div class="card-profile">
                <div class="our-team">
                    <div class="picture">
                        <img class="img-fluid" :src="person.pic">
                    </div>
                    <div class="team-content">
                        <h4 class="name">{{ person.name }}</h4>
                        <h5 class="title" v-html="person.roleMD"></h5>
                    </div>
                    <router-link :to="{ name: 'PersonDetail', params: { slug: person.slug }}" class="profile-link">
                        <strong>VIEW FULL PROFILE</strong>
                    </router-link>
                </div>
            </div>
        </span>

    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { marked } from 'marked';

import { useParamStore } from '@/stores/ParamStore'

const paramStore = useParamStore()

const loading = ref(false)
const people = ref([])


const getPeople = async () => {
    paramStore.isLoading = true
    loading.value = true

    await axios
        .get('/api/v1/people/')
        .then(response => {
            loading.value = false
            people.value = response.data
            // console.log(people.value)
            for (let i = 0; i < people.value.length; i++) {
                if (people.value[i].pic_person.length > 0) {
                    people.value[i].pic = people.value[i].pic_person.filter(
                        pic => pic.isPic == true)[0].image
                } else {
                    people.value[i].pic = '/media/website/people/pic_default.png'
                }

                if (people.value[i].role != null) {
                    people.value[i].roleMD = marked(people.value[i].role)
                } else {
                    people.value[i].roleMD = ''
                }
            }
            people.value = people.value.filter(a => a.show_in_page === true).sort((a, b) => { return a.position - b.position })
            // console.log(people.value)
        })
        .catch(error =>{
            console.log(error)
        })

    paramStore.isLoading = false
}

onMounted(() => {
    getPeople()
})
</script>

<style lang="scss" scoped>
.container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  width: 100%;
  margin-top: 30px;
  margin-bottom: 80px;
}

.card-profile {
    width: 220px;
    margin-top: 10px;
    margin-left: 10px;
    margin-right: 10px;
    margin-bottom: 10px;
    height: 300px;
}

.our-team {
    padding-top: 20px;
    padding-bottom: 40px;
    background-color: #fff;
    text-align: center;
    overflow: hidden;
    position: relative;
    height: 300px;
}

.our-team .picture {
    display: inline-block;
    height: 110px;
    width: 110px;
    margin-bottom: 15px;
    z-index: 1;
    position: relative;
}

.our-team .picture::before {
    content: "";
    width: 100%;
    height: 0;
    border-radius: 50%;
    background-color: #38444a;
    position: absolute;
    bottom: 135%;
    right: 0;
    left: 0;
    opacity: 0.9;
    transform: scale(3);
    transition: all 0.3s linear 0s;
}

.our-team:hover .picture::before {
    height: 100%;
}

.our-team .picture::after {
    content: "";
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background-color: #fff;
    position: absolute;
    top: 0;
    left: 0;
    z-index: -1;
}

.our-team .picture img {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    transform: scale(1);
    transition: all 0.9s ease 0s;
}

.our-team:hover .picture img {
    transform: scale(0.8);
}

.our-team .title {
    display: block;
    font-size: 15px;
    color: #4e5052;
    text-transform: capitalize;
}

.our-team .profile-link {
    width: 100%;
    padding: 0;
    margin: 0;
    background-color: #1369ce;
    position: absolute;
    bottom: -100px;
    left: 0;
    transition: all 0.5s ease 0s;
}

.our-team:hover .profile-link {
    bottom: 0;
}

.our-team .profile-link {
    display: inline-block;
}

.our-team .profile-link {
    display: block;
    padding: 10px;
    font-size: 12px;
    color: white;
    transition: all 0.3s ease 0s;
    text-decoration: none;
}

// .our-team .profile-link :hover {

// }
</style>