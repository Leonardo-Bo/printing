<template>
    <div class="container">
        <div class="row d-flex flex-column min-vh-100 justify-content-center align-items-center">
            <div class="card col-md-4 pt-3 pb-3 card-login-signup">
                <div class="md-12">
                    <h5 class="text-center">RESET PASSWORD</h5>
                    <hr>
                    <form @submit.prevent="resetPasswordConfirm">
                        <div class="form-group mb-3">
                            <label class="form-label mb-0">
                                <i class="bi bi-key"></i> New password:
                            </label>
                            <input
                                type="password" 
                                class="form-control fc-login-signup"
                                v-model="password1"
                            >
                        </div>

                        <div class="form-group mb-3">
                            <label class="form-label mb-0">
                                <i class="bi bi-key"></i> Repeat new password:
                            </label>
                            <input
                                type="password" 
                                class="form-control fc-login-signup"
                                v-model="password2"
                            >
                        </div>

                        <div class="d-grid gap-2 col-12 mx-auto pb-2 mt-5">
                            <button class="btn btn-primary" type="submit">Confirm</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { createToast } from 'mosha-vue-toastify';
import { useRoute, useRouter } from 'vue-router';

import { useParamStore } from '@/stores/ParamStore';
const paramStore = useParamStore()
const route = useRoute()
const router = useRouter()

const password1 = ref('')
const password2 = ref('')
const errors = ref([])

const resetPasswordConfirm = async () => {
    paramStore.isLoading = true
    errors.value = []

    if (!errors.value.length) {

        const formData = {
            uid: route.params.uid,
            token: route.params.token,
            new_password: password1.value,
            re_new_password: password2.value                     
        }

        await axios
            .post("/api/v1/users/reset_password_confirm/", formData)
            .then(response => {
                // console.log(response)
                createToast(
                    'Password reset successfully', 
                    paramStore.toastSuccess
                )
                router.push('/login')
            })
            .catch(error => {
                if (error.response) {
                    for (const property in error.response.data) {
                        this.errors.push(`${property}: ${error.response.data[property]}`)
                        createToast(
                            `${property}: ${error.response.data[property]}`, 
                            paramStore.toastDanger
                        )
                    }
                    console.log(JSON.stringify(error.response.data))
                } else if (error.message) {
                    console.log(JSON.stringify(error.message))
                } else {
                    console.log(JSON.stringify(error))
                }
            })

        password1.value = ''
        password2.value = ''
    }
    paramStore.isLoading = false
}
</script>
