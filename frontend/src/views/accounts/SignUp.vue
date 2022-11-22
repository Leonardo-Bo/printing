<template>
    <template v-if="!userStore.isAuthenticated">
        <div class="container">
            <div class="row d-flex flex-column justify-content-center align-items-center mt-5 mb-5">
                <div class="card col-md-4 pt-3 pb-3 card-login-signup">
                    <div class="md-12">
                        <h5 class="text-center">SIGN UP</h5>
                        <hr>
                        <form @submit.prevent="signupForm">

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
                                    <i class="bi bi-envelope"></i> Email:
                                </label>
                                <input 
                                    type="email" 
                                    name="email" 
                                    id="id_email" 
                                    class="form-control shadow-none fc-sign"
                                    v-model="email"
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
                                        v-model="password1"
                                    >
                                </div>
                            </div>

                            <div class="form-group mb-2">
                                <label class="fl-sign">
                                    <i class="bi bi-key"></i> Repeat Password:
                                </label>
                                <div class="input-group">
                                    <input 
                                        type="password" 
                                        name="password2" 
                                        id="id_password2" 
                                        class="form-control shadow-none fc-sign"
                                        v-model="password2"
                                    >
                                </div>
                            </div>

                            <div class="d-grid gap-2 col-12 mx-auto pb-2 mt-5">
                                <button class="btn btn-success" type="submit">Send Request</button>
                            </div>
                        </form>

                        <small>
                            <span style="color: #dcdee0;">Do you already have an account? </span> 
                            <router-link class="ml-2" to="/login">Login</router-link>
                        </small>
                    </div>
                </div>
            </div>
        </div>
    </template>
    <template v-else>
        <div class="container">
            <div class="row d-flex flex-column justify-content-center align-items-center">
                <h1 style="text-align: center; margin-top: 150px;">You are already logged in</h1>
            </div>
        </div>
    </template>

    <div class="modal" id="signUpConfirm_modal" tabindex="-1">
        <div class="modal-dialog modal-lg modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Your registration request was successful</h5>
                </div>
                <div class="modal-body">
                    <p class="mb-1">An email will arrive when the administrator activates your account.</p>
                    <p style="font-size: 12px">This page can be closed.</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { Modal } from 'bootstrap'

import { useParamStore } from '@/stores/ParamStore'
import { useUserStore } from '@/stores/UserStore'

import { createToast } from "mosha-vue-toastify"

const paramStore = useParamStore()
const userStore = useUserStore()

const errors = ref([])


const signupConfirm_modal = ref(null)

const signupConfirmModal = () => {
    signupConfirm_modal.value = new Modal(document.getElementById('signUpConfirm_modal'), {})
    signupConfirm_modal.value.show()
}


const username = ref('')
const email = ref('')
const password1 = ref('')
const password2 = ref('')

const signupForm = () => {
    paramStore.isLoading = true
    errors.value = []

    if (username.value == '') {
        createToast(
            'missing username',
            paramStore.toastDanger
        )
        errors.value.push(1)
    }

    if (email.value == '') {
        createToast(
            'missing email',
            paramStore.toastDanger
        )
        errors.value.push(1)
    }

    if (password1.value == '') {
        createToast(
            'missing password',
            paramStore.toastDanger
        )
        errors.value.push(1)
    }

    if (password1.value != password2.value) {
        createToast(
            'the two password fields didn\'t match',
            paramStore.toastDanger
        )
        errors.value.push(1)
    }
    
    if (!errors.value.length) {

        var regex = /^[A-Za-z0-9]+$/

        if (regex.test(username.value)) {

            const formData = {
                username: username.value,
                email: email.value, 
                password: password1.value,
                re_password: password2.value
            }

            axios
                .post("/api/v1/users/", formData)
                .then(response => {
                    console.log(response)
                    username.value = ''
                    email.value = ''
                    password1.value = ''
                    password2.value = ''
                    signupConfirmModal()
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
        } else {
            createToast(
                'username must contain only alphanumeric characters',
                paramStore.toastDanger
            )
        }
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
</style>
