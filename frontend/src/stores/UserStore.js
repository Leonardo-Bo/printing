import { defineStore } from 'pinia'

export const useUserStore = defineStore('UserStore', {
    state: () => {
        return {
            isAuthenticated: false,
            token: '',
            user: {
                id: null,
                username: '',
                email: '',
                fullname: ''
            }
        }
    },

    actions: {
        initializeStore() {
            if (localStorage.getItem('token')) {
                this.token = localStorage.getItem('token')
                this.isAuthenticated = true
                this.user.id = localStorage.getItem('user_id')
                this.user.username = localStorage.getItem('user_username')
                this.user.email = localStorage.getItem('user_email')
                this.user.fullname = localStorage.getItem('user_fullname')
            } else {
                this.token = ''
                this.isAuthenticated = false
                this.user.id = null
                this.user.username = ''
                this.user.email = ''
                this.user.fullname = ''
            }
        }
    }
})