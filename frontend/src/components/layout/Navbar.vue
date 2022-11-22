<template>
    <div class="navbar" id="navbar" ref="navbar">

        <div class="nav-left">
            <router-link class="logo ms-3" to="/">
                <img class="img" src="~@/assets/Logo.png">
            </router-link>
        </div>

        <div class="nav-center">
            <div class="toggle-button" @click="showMenu">
                <span class="bar"></span>
                <span class="bar"></span>
                <span class="bar"></span>
            </div>

            <div class="items">
                <ul>
                    <li>
                        <router-link class="nav-link" to="/research-fields">
                            RESEARCH
                        </router-link>
                    </li>
                    <li>
                        <router-link class="nav-link" to="/people">
                            PEOPLE
                        </router-link>
                    </li>
                    <li>
                        <router-link class="nav-link" to="/tools">
                            TOOLS 
                            <!-- <i class="ms-2 bi bi-caret-down-fill" style="font-size: 10px;"></i> -->
                        </router-link>
                    </li>
                    <li>
                        <router-link class="nav-link" to="/news">
                            NEWS
                        </router-link>
                    </li>
                    <li>
                        <router-link class="nav-link" to="/publications">
                            PUBLICATIONS
                        </router-link>
                    </li>
                    <li>
                        <router-link class="nav-link" to="/contacts">
                            CONTACTS
                        </router-link>
                    </li>
                </ul>
            </div>
        </div>

        <div class="nav-right">
            <template v-if="userStore.isAuthenticated">
                <span class="sign" @click="dropNav">
                    <i class="bi bi-person-fill ndd"></i>
                    <i class="bi bi-three-dots-vertical ndd"></i>
                </span>
            </template>
        </div>

    </div>

    <div v-show="showDropdown" class="nav-dropdown ndd">
        <router-link style="text-decoration: none;" to="/account" class="nav-drop-active">
            <p class="mb-2 mt-2 nav-dropdown-item">
                Account <i class="bi bi-person float-end"></i>
            </p>
        </router-link>
        <router-link style="text-decoration: none;" to="/settings" class="nav-drop-active">
            <p class="mb-2 mt-2 nav-dropdown-item">
                Settings <i class="bi bi-gear float-end"></i>
            </p>
        </router-link>
        <p class="mb-1 nav-dropdown-item" @click="logout()">Logout <i class="bi bi-door-open float-end"></i></p>
    </div>

    <template v-if="showItems">
        <div class="half-size">
            <ul>
                <li>
                    <router-link class="nav-link" to="/research-fields" @click="showMenu">
                        RESEARCH
                    </router-link>
                </li>
                <li>
                    <router-link class="nav-link" to="/people" @click="showMenu">
                        PEOPLE
                    </router-link>
                </li>
                <li>
                    <router-link class="nav-link" to="/tools" @click="showMenu">
                        TOOLS 
                        <!-- <i class="ms-2 bi bi-caret-down-fill" style="font-size: 10px;"></i> -->
                    </router-link>
                </li>
                <li>
                    <router-link class="nav-link" to="/news" @click="showMenu">
                        NEWS
                    </router-link>
                </li>
                <li>
                    <router-link class="nav-link" to="/publications" @click="showMenu">
                        PUBLICATIONS
                    </router-link>
                </li>
                <li>
                    <router-link class="nav-link" to="/contacts" @click="showMenu">
                        CONTACTS
                    </router-link>
                </li>
            </ul>
        </div>
    </template>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useParamStore } from '@/stores/ParamStore'
import { useUserStore } from '@/stores/UserStore'
import { useRouter } from 'vue-router';

import axios from 'axios'

const paramStore = useParamStore()
const userStore = useUserStore()
const router = useRouter()

const showDropdown = ref(false)
const showItems = ref(false)

const showMenu = () => {
    showItems.value = !showItems.value
}

onMounted(() => {
    document.addEventListener('click', closeDropdown)
})

onBeforeUnmount(() => {
    document.removeEventListener('click', closeDropdown)
})

const closeDropdown = (e) => {
    const classname = e.target.className;
    if (showDropdown.value && !classname.includes("ndd")) {
            showDropdown.value = false;
    }
}

const dropNav = () => {
    showDropdown.value = !showDropdown.value
}

const logout = () => {
    console.log("logout")

    axios.defaults.headers.common['Authorization'] = ""

    localStorage.removeItem('token')
    localStorage.removeItem('user_id')
    localStorage.removeItem('user_username')
    localStorage.removeItem('user_email')
    localStorage.removeItem('user_fullname')
    
    userStore.token = ''
    userStore.isAuthenticated = false
    userStore.user.id = null
    userStore.user.username = ''
    userStore.user.email = ''
    userStore.user.fullname = ''
    
    showDropdown.value = false
    router.push('/')
}
</script>

<style lang="scss" scoped>
.navbar {
    overflow: hidden;
    background-color: #eee; /* #f5f5f5; */
    position: fixed;
    top: 0;
    width: 100%;
    height: 90px;
    z-index: 8;
    box-shadow: 0 4px 4px 0 rgba(0,0,0,.2);
}
.toggle-button {
    position: absolute;
    top: 1.75rem;
    right: 1rem;
    display: none;
    flex-direction: column;
    justify-content: space-between;
    width: 30px;
    height: 21px;
}
.toggle-button .bar {
    height: 3px;
    width: 100%;
    background-color: #38444a;
    border-radius: 10px;
}
.sign, .sign:hover, .sign:focus {
    color: #38444a;
    cursor: pointer;
    position: absolute;
    bottom: 0;
    right: 0;
    margin-bottom: 15px;   
}
.nav-left { 
    text-align: left;
    // background-color: yellow;
    height: 75px;
    margin-bottom: 5px;
    float: left;
}
.nav-center {
    height: 75px;
    margin-bottom: 5px;
    // background-color: orange;
    float: left;
}
.img {
    width: auto;
    height: 75px;
}
.nav-link {
    color: #38444a;
}
.logo {
    text-decoration: none;
    color: #38444a;
    padding: 0;
    background-color: #eee;
}

@media screen and (max-width: 349px) {
    .toggle-button {
        display: flex;
    }
    .nav-left { 
        width: 90%;
    }
    .nav-center {
        width: 10%;
    }
    .nav-right {
        width: 0%;
        display: none;
        // background-color: green;
    }
    .items {
        display: none;
    }
    ul {
        padding: 0;
        margin: 0;
    }
    ul > li {
        zoom:1;
        font-weight: bold;
        font-size: 14px;
        list-style-type: none;
    }
}

@media screen and (min-width: 350px) and (max-width: 539px) {
    .toggle-button {
        display: flex;
    }
    .nav-left { 
        width: 90%;
    }
    .nav-center {
        width: 10%;
    }
    .nav-right {
        width: 0%;
        display: none;
        // background-color: green;
    }
    .items {
        display: none;
    }
    ul {
        padding: 0;
        margin: 0;
    }
    ul > li {
        zoom:1;
        font-weight: bold;
        font-size: 14px;
        list-style-type: none;
    }
}

@media screen and (min-width: 540px) and (max-width: 914px) {
    .toggle-button {
        display: flex;
    }
    .nav-left {
        width: 90%;
    }
    .nav-center {
        width: 10%;
    }
    .nav-right {
        width: 0%;
        display: none;
        // background-color: green;
    }
    .items {
        display: none;
    }
    ul {
        padding: 0;
        margin: 0;
    }
    ul > li {
        zoom:1;
        font-weight: bold;
        font-size: 14px;
        list-style-type: none;
    }
}

@media screen and (max-width: 914px) {
    .half-size {
        margin-top: 89px;
        padding: 10px;
        background-color: #eee;
        width: 100%;
        position: fixed;
        right: 0;
        top: 0;
        text-align: center;
        z-index: 8;
        border-top: 2px solid lightgray;
        // float: right;
        // margin-bottom: 190px;
    }
    .router-link-exact-active {
        font-size: 14px;
        margin: 0;
        background-color: lightgray;
    }
}

@media screen and (min-width: 915px) and (max-width: 1219px) {
    .nav-left {
        width: 30%;
    }
    .nav-center {
        width: 65%;
    }
    .nav-right {
        display: none;
    }
    .items {
        position: absolute;
        bottom: 0;
        right: 0;
        margin-right: 2%;
    }
    .active-right::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background-color: #38444a;
    }
    .nav-drop-active {
        padding: 0;
    }
    ul > li {
        display: inline-block;
        zoom:1;
        // *display:inline;
        margin-left: 40px;
        font-weight: bold;
        font-size: 12px;
    }
    .item-end {
        font-weight: bold;
        font-size: 14px;
        text-decoration: none;
        // bottom: 0;
        // right: 0;
        // margin: 0;
        padding: 45px 0 0 0;
        color: #38444a;
        border-top: none;
        position: relative;
        float: right;
    }
}

@media screen and (min-width: 1219px) {
    .nav-left {
        width: 30%;
    }
    .nav-center {
        width: 65%;
    }
    .nav-right {
        width: 5%;
        height: 75px;
        margin-bottom: 5px;
        // background-color: green;
        float: left;
    }
    .items {
        position: absolute;
        bottom: 0;
        right: 0;
        margin-right: 5%;
    }
    .active-right::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background-color: #38444a;
    }
    .nav-drop-active {
        padding: 0;
    }
    ul > li {
        display: inline-block;
        zoom:1;
        // *display:inline;
        margin-left: 75px;
        font-weight: bold;
        font-size: 14px;
    }
    .item-end {
        font-weight: bold;
        font-size: 14px;
        text-decoration: none;
        padding: 45px 0 0 0;
        color: #38444a;
        border-top: none;
        position: relative;
        float: right;
    }
}

@media screen and (min-width: 915px) {
    .nav-link {
        text-decoration: none;
        bottom: 0;
        right: 0;
        margin: 0;
        padding: 40px 0 0 0;
        border-top: none;
        position: relative;
        &::before {
            content: "";
            position: absolute;
            top: 0;
            left: 50%;
            width: 0%;
            height: 4px;
            background: #38444a;
            transition: all 250ms ease-in-out;
        }
        &:hover, &:focus {
            color: #38444a;
        }
        &:hover::before, &:hover::after {
            width: 100%;
            left: 0;
            color: #38444a;
        }
    }
    .nav-dropdown {
        position: fixed;
        right: 0;
        top: 0;
        width: 150px;
        background-color: #eee;
        border-radius: 5px;
        margin-top: 92px;
        margin-right: 2px;
        box-shadow: 0 4px 4px 0 rgba(0,0,0,.2);
        border: 1px solid #eee;
        padding-left: 8px;
        padding-right: 8px;
        z-index: 1;
    }
    .nav-dropdown-item {
        font-size: 14px;
        font-weight: bold;
        text-decoration: none;
        color: #38444a;
        cursor: pointer;
        border-left: solid 4px transparent;
        padding-left: 8px;
        &:hover {
            font-size: 14px;
            font-weight: bold;
            text-decoration: none;
            color: #38444a;
            cursor: pointer;
            border-left-color: #38444a;    
        }
    }
    .router-link-exact-active {
        font-size: 14px;
        margin: 0;
        &::before {
            content: "";
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background-color: #38444a;
            margin: 0;
            padding: 0;
        }
    }
}
</style>