<template>
    <div class="modal fade" id="delete_modal" tabindex="-1" aria-hidden="true" data-bs-backdrop="static">
        <div class="modal-dialog modal-lg">
            <div class="modal-content bg-light">
                <div class="modal-header">
                    <h6 class="modal-title">Delete {{ props.title }}</h6>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="$emit('closeModal')"></button>
                </div>
                <form @submit.prevent="deleteObject">
    
                    <div class="modal-body">
                        {{ warning }}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-sm btn-outline-secondary" data-bs-dismiss="modal" @click="$emit('closeModal')">Cancel</button>
                        <button type="submit" class="btn btn-sm btn-outline-danger">Delete</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>
    
    
<script setup>
import { ref, watch } from 'vue'
import axios from 'axios'
import { Modal } from 'bootstrap'

import { createToast } from "mosha-vue-toastify"

import { useParamStore } from '@/stores/ParamStore'

const paramStore = useParamStore()


const props = defineProps({
    model: String,
    title: String,
    warning: String,
    identifier: [String, Number],
    callback: Function,
    openDeleteModal: Boolean,
    endpoint: String
})

const emit = defineEmits(['closeModal'])


const modal_delete = ref(null)

watch(() => props.openDeleteModal, () => {
    if (props.openDeleteModal) {
        modal_delete.value = new Modal(document.getElementById('delete_modal'), {})
        modal_delete.value.show()
    }
})

const deleteObject = async () => {
    paramStore.isLoading = true

    await axios 
        .delete(`/api/v1/${props.endpoint}/${props.identifier}`)
        .then(response => {
            modal_delete.value.hide();
            createToast(
                `${props.model} deleted successfully`,
                paramStore.toastSuccess 
            )
            props.callback()
        })
        .catch(error => {
            console.log(error)
        })

    emit('closeModal')
    paramStore.isLoading = false
}
</script>