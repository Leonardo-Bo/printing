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
                </select> <span class="ms-2">research fields per page</span>
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
                <th style="width: 15%;"><i class="bi bi-arrow-down-up float-end" @click="sort('id')"></i>ID</th>
                <th style="width: 24%;"><i class="bi bi-arrow-down-up float-end" @click="sort('show_in_home')"></i>In home</th>
                <th style="width: 15%;"><i class="bi bi-arrow-down-up float-end" @click="sort('author.username')"></i>Created by</th>
                <th style="width: 13%;"><i class="bi bi-arrow-down-up float-end" @click="sort('created_at')"></i>Created at</th>
                <th style="width: 15%;"><i class="bi bi-arrow-down-up float-end" @click="sort('author_update.username')"></i>Updated by</th>
                <th style="width: 13%;"><i class="bi bi-arrow-down-up float-end" @click="sort('updated_at')"></i>Updated at</th>
                <th style="width: 5%; text-align: right;">Actions</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="(item, index) in sortedCarousel" v-bind:key="item.id">
                <td>{{ index + 1 }}</td>
                <td>{{ item.show_in_home }}</td>
                <td>{{ item.author[0].username }}</td>
                <td>{{ formatDate(item.created_at) }}</td>
                <td>{{ item.author_update[0].username }}</td>
                <td>{{ formatDate(item.updated_at) }}</td>
                <td>
                    <abbr style="cursor: pointer;" title="Delete">
                        <i 
                            @click="$emit('carouselIdDelete', item)" 
                            class="bi bi-trash text-danger float-end">
                        </i>
                    </abbr>
                    <abbr style="cursor: pointer;" title="Edit">
                        <i 
                            @click="$emit('carouselIdEdit', item.id)" 
                            class="bi bi-pencil-square text-warning me-3 float-end">
                        </i>
                    </abbr>
                </td>
                <!-- <td><a :href="'/research-fields/' + project.slug" class="td-link">{{ project.title }}</a></td> -->                
            </tr>
        </tbody>
    </table>

    <div class="row py-3">
        <div class="col-7">
            <template v-if="filterCount != 1">
                {{ filterCount }} carosuel items found
            </template>
            <template v-else>
                {{ filterCount }} carousel item found
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
    carousel: Object,
    showSearch: Boolean
})

const dayjs = require('dayjs')

defineEmits(['carouselIdEdit', 'carouselIdDelete'])

let copyCarousel = props.carousel.map(row => { return row })
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

const hasFilter = (_carousel_, fil) => {
    if(fil.value !== '') {
        _carousel_ = _carousel_.filter(
            item =>  
            item.show_in_home.toString().indexOf(fil.value.toLowerCase()) >= 0 ||
            item.content.toLowerCase().indexOf(fil.value.toLowerCase()) >= 0 ||
            item.author[0].username.toLowerCase().indexOf(fil.value.toLowerCase()) >= 0 ||
            item.author_update[0].username.toLowerCase().indexOf(fil.value.toLowerCase()) >= 0
        )
    }
    return _carousel_
}

const sortedCarousel = computed(() => {
    let _carousel = copyCarousel;

    _carousel = hasFilter(_carousel, filter)

    return _carousel.sort((a,b) => {
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
    let _carousel = copyCarousel;

    _carousel = hasFilter(_carousel, filter)
    return Math.ceil(_carousel.length / pageSize.value)
})

const filterCount = computed(() => {
    let _carousel = copyCarousel;

    _carousel = hasFilter(_carousel, filter)
    return _carousel.length
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
