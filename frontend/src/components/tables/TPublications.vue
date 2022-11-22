<template>
    <div class="mb-4">
        <div class="row justify-content-between">
            <div class="col-4">
                <select v-model="perPage" v-on:change="showPerPage" class="table-select px-1">
                    <option value="5">5</option>
                    <option value="10">10</option>
                    <option value="15">15</option>
                    <option value="20">20</option>
                    <option value="25">25</option>
                </select> <span class="ms-2">publications fields per page</span>
            </div>
            <div class="col-4">
                <!-- <div v-show="showSearch"> -->
                    <input class="float-end px-1" type="search" v-model="filter" placeholder="Search...">
                <!-- </div> -->
            </div>
        </div>
    </div>

    <table class="table table-bordered">
        <thead>
            <tr>
                <th style="width: 39%;"><i class="bi bi-arrow-down-up float-end" @click="sort('title')"></i>Title</th>
                <th style="width: 15%;"><i class="bi bi-arrow-down-up float-end" @click="sort('author.username')"></i>Created by</th>
                <th style="width: 13%;"><i class="bi bi-arrow-down-up float-end" @click="sort('created_at')"></i>Created at</th>
                <th style="width: 15%;"><i class="bi bi-arrow-down-up float-end" @click="sort('author_update.username')"></i>Updated by</th>
                <th style="width: 13%;"><i class="bi bi-arrow-down-up float-end" @click="sort('updated_at')"></i>Updated at</th>
                <th style="width: 5%; text-align: right;">Actions</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="pub in sortedPublications" v-bind:key="pub.id">
                <td>{{ pub.title }}</td>
                <td>{{ pub.author[0].username }}</td>
                <td>{{ formatDate(pub.created_at) }}</td>
                <td>{{ pub.author_update[0].username }}</td>
                <td>{{ formatDate(pub.updated_at) }}</td>
                <td>
                    <abbr style="cursor: pointer;" title="Delete">
                        <i 
                            @click="$emit('publicationIdDelete', pub)" 
                            class="bi bi-trash text-danger float-end">
                        </i>
                    </abbr>
                    <abbr style="cursor: pointer;" title="Edit">
                        <i 
                            @click="$emit('publicationIdEdit', pub.id)" 
                            class="bi bi-pencil-square text-warning me-3 float-end">
                        </i>
                    </abbr>
                </td>
            </tr>
        </tbody>
    </table>

    <div class="row py-3">
        <div class="col-7">
            <template v-if="filterCount != 1">
                {{ filterCount }} publications found
            </template>
            <template v-else>
                {{ filterCount }} publication found
            </template>
        </div>

        <div class="col-5">
            <v-pagination
                v-model="currentPage"
                :pages="pageCount"
                :range-size="1"
                active-color="#B1C3D7"
                @update:modelValue="loadPage"
                class = "float-end"
            />
        </div>
    </div>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import VPagination from "@hennge/vue3-pagination";
import "@hennge/vue3-pagination/dist/vue3-pagination.css";

const props = defineProps({
    publications: Object,
})

const dayjs = require('dayjs')

defineEmits(['publicationIdEdit', 'publicationIdDelete'])

let copyPublications = props.publications.map(row => { return row })
const currentSortDir = ref('asc')
const currentSort = ref('title')
const currentPage = ref(1)
const pageSize = ref(15)
const perPage = ref(15)
const filter = ref('')

const sort = (s) => {
    if(s === currentSort.value) {
        currentSortDir.value = currentSortDir.value==='asc'?'desc':'asc';
    }
    currentSort.value = s;
}

const loadPage = (page) => {
    currentPage.value = page
}

const showPerPage = () => {
    pageSize.value = perPage.value;
    currentPage.value = 1
}

const hasFilter = (_publications_, fil) => {
    if(fil.value !== '') {
        _publications_ = _publications_.filter(
            pub => pub.title.toLowerCase().indexOf(fil.value.toLowerCase()) >= 0 ||
            pub.authors.toLowerCase().indexOf(fil.value.toLowerCase()) >= 0 || 
            pub.magazine.toLowerCase().indexOf(fil.value.toLowerCase()) >= 0 ||
            pub.author_update[0].username.toLowerCase().indexOf(fil.value.toLowerCase()) >= 0 ||
            pub.author[0].username.toLowerCase().indexOf(fil.value.toLowerCase()) >= 0
        );
    }
    return _publications_
}

const sortedPublications = computed(() => {
    let _publications = copyPublications;

    _publications = hasFilter(_publications, filter)

    return _publications.sort((a,b) => {
        let modifier = 1;
        if(currentSortDir.value === 'desc') modifier = -1;
        if(a[currentSort.value] < b[currentSort.value]) return -1 * modifier;
        if(a[currentSort.value] > b[currentSort.value]) return 1 * modifier;
        return 0;
    }).filter((row, index) => {
        let start = (currentPage.value-1)*pageSize.value;
        let end = currentPage.value*pageSize.value;
        if(index >= start && index < end) return true;
    });

})

const pageCount = computed(() => {
    let _publications = copyPublications;

    _publications = hasFilter(_publications, filter)
    return Math.ceil(_publications.length / pageSize.value)
})

const filterCount = computed(() => {
    let _publications = copyPublications;

    _publications = hasFilter(_publications, filter)
    return _publications.length
})

watch(() => filter.value, () => {
    currentPage.value = 1;
})

const formatDate = (value) => {
    if (value) {
        return dayjs(String(value)).format('DD/MM/YY')
    }
}
</script>
