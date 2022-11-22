<template>
    <template v-if="!userStore.isAuthenticated">
        <div class="container">
            <div class="row d-flex flex-column justify-content-center align-items-center mt-5 mb-5">
                <div class="card col-md-4 pt-3 pb-3 card-login-signup">
                    <div class="md-12">
                        <h5 class="text-center">LOGIN</h5>
                        <hr>
                        <form @submit.prevent="loginForm">

                            <div class="form-group mb-2">
                                <label class="fl-sign">
                                    <i class="bi bi-person"></i> Username:
                                </label>
                                <input
                                    type="text" 
                                    name="username" 
                                    id="id_username" 
                                    class="form-control shadow-none fc-sign"
                                    v-model="username"
                                >
                            </div>

                            <div class="form-group mb-2">
                                <label class="fl-sign">
                                    <i class="bi bi-key"></i> Password:
                                </label>
                                <div class="input-group">
                                    <input 
                                        type="password" 
                                        name="password1" 
                                        id="id_password1" 
                                        class="form-control shadow-none fc-sign"
                                        v-model="password"
                                    >
                                </div>
                            </div>
                            <small>
                                <router-link to="/reset-password" class="py-0 forgot-pwd">Forgot password?</router-link> 
                            </small>

                            <div class="d-grid gap-2 col-12 mx-auto pb-2 mt-4">
                                <button class="btn btn-success" type="submit">Login</button>
                            </div>
                        </form>

                    <small>
                        <span style="color: #dcdee0;">Don't have an account yet? </span> 
                        <router-link class="ml-2" to="/signup">Request registration</router-link>
                    </small>
                </div>
            </div>
        </div>
    </div>
    </template>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router';

import { useParamStore } from '@/stores/ParamStore'
import { useUserStore } from '@/stores/UserStore'

import { createToast } from "mosha-vue-toastify"

const paramStore = useParamStore()
const userStore = useUserStore()
const router = useRouter()

const errors = ref([])

const username = ref('')
const password = ref('')

const loginForm = async () => {
    paramStore.isLoading = true

    errors.value = []

    if (username.value === '') {
        createToast(
            'missing username',
            paramStore.toastDanger
        )
        errors.value.push(1)
    }

    if (password.value === '') {
        createToast(
            'missing password',
            paramStore.toastDanger
        )
        errors.value.push(1)
    }

    if (!errors.value.length) {

        axios.defaults.headers.common["Authorization"] = ""
        localStorage.removeItem("token")

        const formData = {
            username: username.value,
            password: password.value
        }

        await axios
            .post("/api/v1/token/login/", formData)
            .then(response => {
                const token = response.data.auth_token

                userStore.token = token
                axios.defaults.headers.common["Authorization"] = "Token " + token
                localStorage.setItem("token", token)

                router.push('/')
            })
            .catch(error => {
                if (error.response) {
                    for (const property in error.response.data) {
                        errors.value.push(`${property}: ${error.response.data[property]}`)
                        createToast(`${property}: ${error.response.data[property]}`, paramStore.toastDanger)
                    }
                    console.log(JSON.stringify(error.response.data))
                } else if (error.message) {
                    console.log(JSON.stringify(error.message))
                } else {
                    console.log(JSON.stringify(error))
                }
            })

        await axios
            .get('/api/v1/users/me')
            .then(response => {
                userStore.isAuthenticated = true
                userStore.user.id = response.data.id 
                userStore.user.username = response.data.username 
                userStore.user.email = response.data.email
                userStore.user.fullname = response.data.full_name
            
                localStorage.setItem('user_username', response.data.username)
                localStorage.setItem('user_id', response.data.id)
                localStorage.setItem('user_email', response.data.email)
                localStorage.setItem('user_fullname', response.data.full_name)
            })
            .catch(error => {
                console.log(error)
            })
    }

    paramStore.isLoading = false
}
</script>

<style lang="scss" scoped>
.card-login-signup {
    border-radius: 20px;
    background-color: #38444a;
    color: #dcdee0;
}
.fl-sign {
    font-size: 14px;
}
.fc-sign {
    background-color: #415970;
    border: 0px;
    color: #dcdee0;
    height: 30px;
    font-size: 14px;

    &:focus {
        background-color: #415970;
        color: #dcdee0;
        outline: none;
    }
}
.fc-login-signup:focus {
    background-color: #415970;
    color: #dcdee0;
}
.forgot-pwd {
    color: #dcdee0;
    text-decoration: none;
}
.forgot-pwd:hover {
    color: #dcdee0;
    text-decoration: underline;
}
</style>