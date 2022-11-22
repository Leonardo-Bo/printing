<template>

    <div class="warning-dim">
        <template v-if="isUser">
            Your device is not large enough to view this content
        </template>
        <template v-else>
            <span style="font-size: 20px;">
                403: You are not authorized to be here
            </span>
        </template>
    </div>

    <div class="container-profile">
        <template v-if="isUser">
            <h2 class="mb-5">Hello {{ profile.username }}</h2>

            <div class="row">

                <div class="col col-md-4 offset-md-2">

                    <div class="card h-100">
                        <div class="card-header">
                            <strong>Personal informations</strong>
                        </div>

                        <div class="card-body">   

                            <form @submit.prevent="editProfile">
                                <div class="row g-3">
                                    
                                    <div class="col-md-12">
                                        <label>Username*</label>
                                        <input
                                            type="text"
                                            class="form-control form-control-sm"
                                            id="username"
                                            v-model="profile.username">
                                    </div>

                                    <div class="col-md-12">
                                        <label>Email*</label>
                                        <input
                                            type="email"
                                            class="form-control form-control-sm"
                                            id="email"
                                            v-model="profile.email">
                                    </div>

                                    <div class="col-md-12">
                                        <label>Full name</label>
                                        <input
                                            type="text"
                                            class="form-control form-control-sm"
                                            id="first_name"
                                            v-model="profile.full_name">
                                    </div>

                                </div>
                                <div class="mt-3 float-end">
                                    <button type="submit" class="btn btn-sm btn-outline-secondary">Edit profile</button>
                                </div>
                            </form>
                        </div>
                    </div>

                </div>

                <div class="col col-md-4">

                    <div class="card">
                        <div class="card-header">
                            <strong>Settings</strong>
                        </div>

                        <div class="card-body">

                            <div class="d-grid gap-2">
                                <button 
                                    class="btn btn-outline-secondary btn-sm mx-3" 
                                    @click="editPasswordModal()"
                                >
                                Change password
                                </button>
                                <button 
                                    class="btn btn-outline-secondary mt-4 btn-sm mx-3" 
                                    @click="deleteUserModal()"
                                >
                                Delete account
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

            </div>

        </template>
        <template v-else>
            <span style="font-size: 20px;">
                403: You are not authorized to be here
            </span>
        </template>
        
    </div>

    <div class="modal fade" id="edit_passwordModal" tabindex="-1" aria-hidden="true" data-bs-backdrop="static">
        <div class="modal-dialog modal-lg">
            <div class="modal-content bg-light">
                <div class="modal-header">
                    <h6 class="modal-title">Edit password</h6>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>

                <form @submit.prevent="editPassword">
                    <div class="modal-body">
                        <div class="row g-3">
                            
                            <div class="col-md-12">
                                <label>Current password*</label>
                                <input
                                    type="password"
                                    class="form-control form-control-sm"
                                    v-model="current_password">
                            </div>

                            <div class="col-md-12">
                                <label>New password*</label>
                                <input
                                    type="password"
                                    class="form-control form-control-sm"
                                    v-model="new_password">
                            </div>

                            <div class="col-md-12">
                                <label>Repeat new password*</label>
                                <input
                                    type="password"
                                    class="form-control form-control-sm"
                                    v-model="re_new_password">
                            </div>

                        </div>
                    </div>
                    <div class="modal-footer">
                        <div class="mt-3 float-end">
                            <button type="submit" class="btn btn-sm btn-outline-primary">Edit password</button>
                        </div>
                    </div>
                </form>
                
            </div>
        </div>
    </div>

    <div class="modal fade" id="delete_profileModal" tabindex="-1" aria-hidden="true" data-bs-backdrop="static">
        <div class="modal-dialog modal-lg">
            <div class="modal-content bg-light">
                <div class="modal-header">
                    <h6 class="modal-title">Delete user account</h6>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form @submit.prevent="deleteUser">

                    <div class="modal-body">
                        Warning! You are deleting your account.

                        <div class="col-md-6 mt-4">
                            <label>Enter your password*</label>
                            <input
                                type="password"
                                class="form-control form-control-sm"
                                v-model="del_password">
                        </div>

                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-sm btn-outline-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="submit" class="btn btn-sm btn-outline-danger">Delete Account</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
    
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { Modal } from 'bootstrap'

import { useParamStore } from '@/stores/ParamStore'
import { useUserStore } from '@/stores/UserStore'
import { useRouter } from 'vue-router';

import { createToast } from "mosha-vue-toastify"

const paramStore = useParamStore()
const userStore = useUserStore()
const router = useRouter()

const profile_errors = ref([])
const pass_errors = ref([])
const del_errors = ref([])

const profile = ref({})
const isUser = ref(false)

const modal_edit_password = ref(null)
const modal_delete_profile = ref(null)

const current_password = ref('')
const new_password = ref('') 
const re_new_password = ref('') 
const del_password = ref('') 

onMounted(() => {
    getProfile()
})
        
const editPasswordModal = () => {
    modal_edit_password.value = new Modal(document.getElementById('edit_passwordModal'), {})
    modal_edit_password.value.show()
} 

const deleteUserModal = () => {
    modal_delete_profile.value = new Modal(document.getElementById('delete_profileModal'), {})
    modal_delete_profile.value.show()
}

const getProfile = async () => {
    paramStore.isLoading = true

    await axios
        .get(`/api/v1/users/me`)
        .then(response => {
            profile.value = response.data              
            // console.log(profile.value)
            isUser.value = true
        })
        .catch(error =>{
            console.log(error)
        })

    paramStore.isLoading = false
}

const editProfile = async () => {
    paramStore.isLoading = true

    var regex = /^[A-Za-z0-9]+$/

    if (regex.test(profile.value.username)) {

    //    console.log(regex.test(profile.value.username))
        userStore.user.username = profile.value.username
        userStore.user.fullname = profile.value.full_name

        profile_errors.value = []

        await axios
            .patch(`/api/v1/users/me/`, profile.value)
            .then(response => {
                createToast(
                    'profile edited successfully', 
                    paramStore.toastSuccess
                )
            })
            .catch(error => {
                if (error.response) {
                    for (const property in error.response.data) {
                        profile_errors.value.push(`${property}: ${error.response.data[property]}`)
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
    
    } else {
        createToast(
            'username must contain only alphanumeric characters', 
            paramStore.toastDanger
        )
    }
}

const editPassword = async () => {
    paramStore.isLoading = true

    pass_errors.value = []

    const password = {
        current_password: current_password.value,
        new_password: new_password.value,
        re_new_password: re_new_password.value
    }

    // userStore.user.password = new_password.value

    await axios
        .post(`/api/v1/users/set_password/`, password)
        .then(response => {
            // console.log(response)
            modal_edit_password.value.hide();
            createToast(
                'password edited successfully', 
                paramStore.toastSuccess
            )
        })
        .catch(error => {
            if (error.response) {
                for (const property in error.response.data) {
                    pass_errors.value.push(`${property}: ${error.response.data[property]}`)
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

    current_password.value = ''
    new_password.value = ''
    re_new_password.value = ''
    
    paramStore.isLoading = false
}

const deleteUser = async () => {
    paramStore.isLoading = true

    del_errors.value = []

    await axios
        .delete('api/v1/users/me/', { data: { current_password: del_password.value } }) //{username: this.profile.username, email: this.profile.email})
        .then(response => {
            // console.log(response)
            modal_delete_profile.value.hide();
            createToast(
                'profile deleted successfully', 
                paramStore.toastSuccess
            )                    
        })
        .catch(error => {
            if (error.response) {
                for (const property in error.response.data) {
                    del_errors.value.push(`${property}: ${error.response.data[property]}`)
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

        if (!del_errors.value.length) {

            axios.defaults.headers.common['Authorization'] = ''
            localStorage.removeItem('token')
            localStorage.removeItem('user_username')
            localStorage.removeItem('user_id')
            localStorage.removeItem('user_fullname')
            
            userStore.token = ''
            userStore.isAuthenticated = false
            userStore.user.id = null
            userStore.user.username = ''
            userStore.user.email = ''
            userStore.user.fullname = ''
            
            router.push('/')

        }
    paramStore.isLoading = false
}
</script>

<style scoped>
* {
	box-sizing: border-box;
}

@media screen and (max-width: 1219px) {

    .warning-dim {
        font-size: 30px;
        text-align: center;
        margin-top: 30px;

    }

    .container-profile {
        display: none;
    }
}

@media screen and (min-width: 1220px) {
    
    .warning-dim {
        display: none;
    }

    .container-profile {
        margin-top: 60px;
        margin-bottom: 100px;
        margin-left: 180px;
        margin-right: 180px;
        padding-bottom: 5px;
    }

}
</style>