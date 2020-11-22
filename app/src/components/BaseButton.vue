<template>
    <button
		class="baseButton"
		:disabled="isDisabled"
		:class="baseButtonClass"
	>
		<div class="baseButton__icon"><slot name="icon"></slot></div>
		<div class="baseButton__text" :class="textClass"><slot name="text"></slot></div>
	</button>
</template>
<script>
export default {
    props: {
        isDisabled: {
            type: Boolean,
            required: false,
            default: false
        },
        type: {
            type: String,
            required: false,
            default: "default",
            validator(value) {
                return ["default", "cancel", "purple"].indexOf(value) !== -1;
            }
        }
    },
    computed: {
        /**
         * @returns {String}
         */
        baseButtonClass() {
            return `baseButton--${this.type}`;
        },
        /**
         * @returns {String}
         */
        textClass() {
            return `baseButton__text--${this.type}`;
        }
    }
}
</script>
<style scoped>
.baseButton {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    height: 45px;
    width: fit-content;
    border-radius: 1px 6px 1px 6px;
    padding: 5px 10px;
    border: none;
    cursor: pointer;
}
.baseButton--default {
    background-color: peachpuff;
}
.baseButton--default:hover {
    background-color: #ffbf86;
}
.baseButton--cancel {
    border: solid 2px #e3e3e3;
    background-color: #fff;
}
.baseButton--cancel:hover {
    background-color: #e3e3e3;
}
.baseButton--purple {
    border: solid 5px#a594b7;
    background-color:#cfbae5;
}
.baseButton--purple:hover {
    background-color: #baa7ce;
}
.baseButton__text {
    font-size: 14px;
    font-weight: bold;
}
.baseButton__text--default {
    color: #432000;
}
.baseButton__text--cancel {
    color: #6e6e6e;
}
.baseButton__text--purple {
    color: #524a5b;
}

</style>
