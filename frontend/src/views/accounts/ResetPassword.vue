<template>
    <div class="container">
        <div class="row d-flex flex-column min-vh-100 justify-content-center align-items-center">
            <div class="card col-md-4 pt-3 pb-3 card-login-signup">
                <div class="md-12">
                    <h5 class="text-center">RESET PASSWORD</h5>
                    <hr>
                    <form @submit.prevent="resetPassword">
                        <div class="form-group mb-3">
                            <label class="form-label mb-0">
                                <i class="bi bi-person"></i> Email:
                            </label>
                            <input
                                type="text" 
                                class="form-control fc-login-signup"
                                v-model="email"
                            >
                        </div>

                        <div class="d-grid gap-2 col-12 mx-auto pb-2 mt-5">
                            <button class="btn btn-primary" type="submit">Send request</button>
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

import { useParamStore } from '@/stores/ParamStore';
const paramStore = useParamStore()

const email = ref('')
const errors = ref([])

const resetPassword = async () => {
    paramStore.isLoading = true
    errors.value = []

    if (!errors.value.length) {
        await axios
            .post("/api/v1/users/reset_password/", { email: email.value})
            .then(response => {
                alert("Your request has been sent.\nYou will receive an email with your password reset form.");
                // console.log(response)
            })
            .catch(error => {
                if (error.response) {
                    for (const property in error.response.data) {
                        errors.value.push(`${property}: ${error.response.data[property]}`)
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

        email.value = ''
    }
    paramStore.isLoading = false
}
</script>
