<template>
    <div class="mb-4">
        <label>
            <select v-model="perPage" v-on:change="showPerPage" class="table-select px-1">
                <option value="5">5</option>
                <option value="10">10</option>
                <option value="15">15</option>
                <option value="20">20</option>
                <option value="25">25</option>
            </select> tools per page
        </label>
        <input class="float-end px-1" type="search" v-model="filter" placeholder="Search...">
    </div>

    <table class="table table-bordered">
        <thead>
            <tr>
                <th style="width: 39%;"><i class="bi bi-arrow-down-up float-end" @click="sort('name')"></i>Name</th>
                <th style="width: 15%;"><i class="bi bi-arrow-down-up float-end" @click="sort('author.username')"></i>Created by</th>
                <th style="width: 13%;"><i class="bi bi-arrow-down-up float-end" @click="sort('created_at')"></i>Created at</th>
                <th style="width: 15%;"><i class="bi bi-arrow-down-up float-end" @click="sort('author_update.username')"></i>Updated by</th>
                <th style="width: 13%;"><i class="bi bi-arrow-down-up float-end" @click="sort('updated_at')"></i>Updated at</th>
                <th style="width: 5%; text-align: right;">Actions</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="tool in sortedTools" v-bind:key="tool.slug">
                <td>{{ tool.name }}</td>
                <td>{{ tool.author[0].username }}</td>
                <td>{{ formatDate(tool.created_at) }}</td>
                <td>{{ tool.author_update[0].username }}</td>
                <td>{{ formatDate(tool.updated_at) }}</td>
                <td>
                    <abbr style="cursor: pointer;" title="Delete">
                        <i 
                            @click="$emit('toolSlugDelete', tool)" 
                            class="bi bi-trash text-danger float-end">
                        </i>
                    </abbr>
                    <abbr style="cursor: pointer;" title="Edit">
                        <i 
                            @click="$emit('toolSlugEdit', tool.slug)" 
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
                {{ filterCount }} tool found
            </template>
            <template v-else>
                {{ filterCount }} tools found
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
    tools: Object,
})

const dayjs = require('dayjs')

defineEmits(['toolSlugEdit', 'toolSlugDelete'])

let copyTools = props.tools.map(row => { return row })
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

const hasFilter = (_tools_, fil) => {
    if(fil.value !== '') {
        _tools_ = _tools_.filter(
            tool => tool.name.toLowerCase().indexOf(fil.value.toLowerCase()) >= 0 ||
            tool.content.toLowerCase().indexOf(fil.value.toLowerCase()) >= 0 ||
            tool.author_update[0].username.toLowerCase().indexOf(fil.value.toLowerCase()) >= 0 ||
            tool.author[0].username.toLowerCase().indexOf(fil.value.toLowerCase()) >= 0
        );
    }
    return _tools_
}

const sortedTools = computed(() => {
    let _tools = copyTools;

    _tools = hasFilter(_tools, filter)

    return _tools.sort((a,b) => {
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
    let _tools = copyTools;

    _tools = hasFilter(_tools, filter)
    return Math.ceil(_tools.length / pageSize.value)
})

const filterCount = computed(() => {
    let _tools = copyTools;

    _tools = hasFilter(_tools, filter)
    return _tools.length
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
