import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import { createPinia } from 'pinia'

import axios from 'axios'
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import '@/assets/styles/main.scss'
import 'bootstrap-icons/font/bootstrap-icons.css'
// import 'boxicons'
// import 'boxicons/css/boxicons.min.css'
import 'mosha-vue-toastify/dist/style.css'

const pinia = createPinia()
axios.defaults.baseURL = process.env.NODE_ENV === 'production' ? 'https://printing.bio-groups.com' : 'http://127.0.0.1:8000'

createApp(App).use(pinia).use(router, axios).mount('#app')
