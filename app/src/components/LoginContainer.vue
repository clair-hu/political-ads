<template>
    <div class="login">
        <div class="login__title">
            login
        </div>
        <div class="login__info">
            hey! enter your username and password to see your stuff.
        </div>
        <base-input-field class="baseInput--margin" v-model="email" placeholder-text="email" />
        <base-password-field class="baseInput--margin" v-model="password" placeholder-text="password" />
        <base-button class="baseButton--margin" type="default" @click.native="handleLogin()">
            <template slot="text">
                login
            </template>
        </base-button>
    </div>
</template>
<script>
import BaseButton from "./BaseButton.vue";
import BaseInputField from "./BaseInputField.vue";
import BasePasswordField from "./BasePasswordField.vue";

export default {
    components: {
        BaseButton,
        BaseInputField,
        BasePasswordField
    },
    data() {
        return {
            email: "",
            password: "",
        };
    },
    computed: {
        user() {
            return this.$store.getters.user
        }
    },
    watch: {
        user(value) {
            if(value !== null && value !== undefined){
                //sign up complete, redirect
                this.$router.push('/dashboard');
            }
        }
    },
    methods: {
        async handleLogin() {
            let data = {
                email: this.email,
                password: this.password,
            };
            try {
                await this.$store.dispatch("postLogin", data);
            } catch (error) {
                alert("Whoops! There was an error logging in :(");
                alert(error);
            }
        }
    }
}
</script>
<style scoped>
.login {
    display: flex;
    flex-direction: column;
    justify-content: center;
    width: 400px;
    margin: 40px auto;
    padding: 40px;
    background-color: #72808C;
    border-radius: 5px;
}
.login__title {
    align-self: center;
    margin: 10px;
    padding: 5px;
    border: solid 4px peachpuff;
    font-size: 30px;
    font-weight: 900;
    font-style: italic;
}
.login__info {
    align-self: center;
    margin: 10px;
    text-align: center;
    font-size: 16px;
    font-weight: 300;
    font-style: italic;
}
.baseInput--margin {
    margin: 10px auto;
}
.baseButton--margin {
    margin: 10px auto;
    justify-self:flex-end;
}
</style>
