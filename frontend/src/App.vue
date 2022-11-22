<template>
    <Navbar />    
    <div class="main">
        <div class="is-loading-bar center-ring" v-bind:class="{'is-loading': paramStore.isLoading }">
            <div class="lds-dual-ring"></div>
        </div>
        <router-view/>
    </div>
    <Footer />    
</template>

<script setup>
import axios from 'axios'

import { useParamStore } from '@/stores/ParamStore';
import { useUserStore } from '@/stores/UserStore';

import Navbar from '@/components/layout/Navbar';
import Footer from '@/components/layout/Footer';

const paramStore = useParamStore()
const userStore = useUserStore()

userStore.initializeStore()

if (userStore.token) {
    axios.defaults.headers.common['Authorization'] = "Token " + userStore.token
} else {
    axios.defaults.headers.common['Authorization'] = ""
}
</script>


<style lang="scss">
#app {
    font-family: "Lato", sans-serif; /* Poppins, Avenir, Helvetica, Arial, sans-serif; */
//   -webkit-font-smoothing: antialiased;
//   -moz-osx-font-smoothing: grayscale;
//   text-align: center;
    color: #38444a;
}

/* Works on Firefox */
* {
  scrollbar-width: thin;
  scrollbar-color: grey lightgrey;
}

/* Works on Chrome, Edge, and Safari */
*::-webkit-scrollbar {
  width: 6px;
}

*::-webkit-scrollbar-track {
  background: lightgrey;
}

*::-webkit-scrollbar-thumb {
  background-color: grey;
  border-radius: 20px;
  border: 1px solid lightgrey;
}

html, body {
    height: 100%;
    width: 100%;
    margin: 0; 
}

.main {
    padding-top: 90px;
    min-height: calc(100vh - 150px);
    position: relative;
}
</style>
