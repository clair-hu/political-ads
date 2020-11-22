<template>
    <input class="basePassword" type="password" v-bind:value="value" v-on:input="$emit('input', $event.target.value)" :placeholder="placeholderText"/>
</template>
<script>
export default {
    props: {
        placeholderText: {
            type: String,
            required: false,
            default: ""
        },
        value: {
            type:String,
            required: false,
            default: ""
        }
    }
}
</script>
<style scoped>
.basePassword{
    border: solid 2px #e6e6e6;
    border-radius: 2px;
    font-size: 14px;
    padding: 10px;
}
</style>