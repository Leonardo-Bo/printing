<template>
<div class="warning-dim">
    Your device is not large enough to view this content
</div>

<div class="container-settings">
    <div id="settingsSidebar" class="sidebar">

        <template v-if="!isOpen">
            <div class="row d-flex align-items-center" @click="openNav">
                <div class="col col-md-10">
                    <i class="bi bi-chevron-double-right ps-1"></i>
                </div>
                <div class="col col-md-2" style="margin: 0; padding: 0;">
                    <div class="sidebar-item">.</div>
                    <hr style="margin: 2px; width: 0px;">
                    <div class="sidebar-item">.</div>
                    <div class="sidebar-item">.</div>
                    <div class="sidebar-item">.</div>
                    <div class="sidebar-item">.</div>
                    <div class="sidebar-item">.</div>
                    <div class="sidebar-item">.</div>
                </div>
            </div>    
        </template>
        <template v-else>
            <div class="row d-flex align-items-center">
                <div class="col col-md-10">
                    <router-link to="/settings" class="sidebar-item">SETTINGS</router-link>
                    <hr style="margin: 2px;">
                    <router-link to="/settings/carousel" class="sidebar-item">Carousel</router-link>
                    <router-link to="/settings/research-fields" class="sidebar-item">Research</router-link>
                    <router-link to="/settings/people" class="sidebar-item">People</router-link>
                    <router-link to="/settings/tools" class="sidebar-item">Tools</router-link>
                    <router-link to="/settings/news" class="sidebar-item">News</router-link>
                    <router-link to="/settings/publications" class="sidebar-item">Publications</router-link>
                </div>
                <div class="col col-md-2">
                    <div v-show="showIcon" @click="closeNav">
                        <i class="bi bi-chevron-double-left"></i>
                    </div>
                </div>
            </div>
        </template>

    </div>

    <div id="settingsMain" class="content-settings mt-4">
        <router-view/>
    </div>
</div>
</template>

<script setup>
import { ref } from 'vue'

const isOpen = ref(true) 
const showIcon = ref(true)

const openNav = () => {
    document.getElementById("settingsSidebar").style.width = "250px";
    document.getElementById("settingsMain").style.marginLeft = "250px";
    isOpen.value = true
    setTimeout(() => { showIcon.value = true }, 1000);
}

const closeNav = () => {
    document.getElementById("settingsSidebar").style.width = "25px";
    document.getElementById("settingsMain").style.marginLeft= "25px";
    isOpen.value = false
    showIcon.value = false
}
</script>

<style lang="scss" scoped>
@media screen  and (max-width: 1219px) {
    .container-settings {
        display: none;
    }

    .warning-dim {
        font-size: 30px;
        text-align: center;
        margin-top: 30px;

    }
}

@media screen  and (min-width: 1220px) {
    .warning-dim {
        display: none;
    }

    .sidebar {
        position: fixed;
        left: 0;
        width: 250px;
        background-color: #f1f1f1;
        overflow-x: hidden;
        transition: 1.0s;
        border-top-right-radius: 10px;
        border-bottom-right-radius: 10px;
        z-index: 1;
        -webkit-box-shadow: 0 0 10px #888;
        box-shadow: 0 0 10px #888;
        padding-top: 10px;
        padding-bottom: 10px;
    }

    .sidebar-item {
        margin-left: 20px;
        padding: 8px 0px 8px 15px;
        display: block;
        font-size: 16px;
        font-weight: bold;
        text-decoration: none;
        color: #38444a;
        cursor: pointer;
        border-left: solid 4px transparent;
        z-index: 1;
    }

    .sidebar-item:hover {
        padding: 8px 0px 8px 15px;
        font-size: 16px;
        font-weight: bold;
        text-decoration: none;
        color: #38444a;
        cursor: pointer;
        border-left-color: #38444a;
        z-index: 1;
    }

    .router-link-exact-active {
        padding: 8px 0px 8px 15px;
        font-size: 16px;
        font-weight: bold;
        text-decoration: none;
        color: #38444a;
        cursor: pointer;
        border-left-color: #38444a;
        z-index: 1;
    }

    // .openbtn {
    //     font-size: 20px;
    //     cursor: pointer;
    //     background-color: #111;
    //     color: white;
    //     padding: 10px 15px;
    //     border: none;
    // }

    // .openbtn:hover {
    //     background-color: #444;
    // }

    #settingsMain {
      transition: margin-left 1s;
    }

    .content-settings {
        display: grid;
        margin-left: 250px;
        padding-top: 20px;
        padding-left: 40px;
        margin-right: 40px;
        margin-bottom: 50px;
    }

    .show-sidebar-btn {
        position: absolute; 
        top: 50%; 
        font-size: 15px; 
        color: #38444a;
    }

    .hide-sidebar-btn {
        position: absolute; 
        top: 50%; 
        font-size: 15px; 
        color: #38444a;
        padding-left: 230px;
    }
}
</style>
