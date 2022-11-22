<template>
    <div 
        class="check-char"
        :class="{'check-warning': charactersRemaining <= this.inputWarn }"
    >
        {{ charactersRemaining }} characters remaining
    </div>
</template>

<script>
export default {
    name: 'CharCount',

    props: [
        'input',
        'inputLen',
        'inputWarn'
    ],

    computed: {
        charactersRemaining: function() {
            return this.inputLen - this.input.length;

        }
    }

}
</script>

<style lang="scss" scoped>
.check-char {
    font-size: 12px;
    margin-top:5px;
}

.check-warning {
    color: #ee2c2c;
}
</style>