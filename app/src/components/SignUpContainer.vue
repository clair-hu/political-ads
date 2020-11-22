<template>
    <div class="signUp">
        <div class="signUp__title">
            sign up form
        </div>
        <div class="signUp__info">
            Fill out this sign up form to register on the platform. You can use a fake email address and a phony password which is stored using google firebase.
        </div>
        <div class="signUp__info">
            password must be at least 8 characters
        </div>
        <base-input-field class="baseInput--margin" v-model="email" placeholder-text="email" />
        <base-input-field class="baseInput--margin" v-model="username" placeholder-text="username" />
        <base-password-field class="baseInput--margin" v-model="password" placeholder-text="password" />
        <base-password-field class="baseInput--margin" v-model="confirmPassword" placeholder-text="confirm password" />
        <v-select class="select--margin" v-model="chosenCandidate" label="user_name" :options="candidateList" placeholder="Select a candidate to mimic"></v-select>
        <base-button class="baseButton--margin" type="purple" @click.native="handleSignUp()">
            <template slot="text">
                sign up
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
            username: "",
            password: "",
            confirmPassword: "",
            signUpKey: "",
            candidateList: [],
            chosenCandidate: null
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
        async handleSignUp() {
            //make sure both passwords are equal
            if(this.confirmPassword.length < 8){
                alert("Password is too short, please make it at least 8 characters");
                return;
            }
            if(this.confirmPassword !== this.password){
                alert("Passwords don't match");
                return;
            }

            if(this.chosenCandidate == null){
                alert("Please choose an official candidate to mimic");
                return;
            }

            let data = {
                email: this.email,
                username: this.username,
                password: this.password,
                confirmPassword: this.confirmPassword,
                signUpKey: this.signUpKey,
                mimic_candidate: this.chosenCandidate
            };
            try {
                await this.$store.dispatch("postNewUser", data);
            } catch (error) {
                alert("Whoops! There was an error signing up up :(");
                alert(error);
            }
        },
        async getOfficialCandidates() {
            let response = await this.axios.get("http://localhost:5000/official-candidates")
            return response.data["candidates"]
        }
    },
    async mounted(){
        this.candidateList = await this.getOfficialCandidates();
    }
}
</script>
<style scoped>
.signUp {
    display: flex;
    flex-direction: column;
    justify-content: center;
    width: 400px;
    margin: 40px auto;
    padding: 40px;
    background-color: #72808C;
    border-radius: 5px;
}
.signUp__title {
    align-self: center;
    margin: 10px;
    padding: 5px;
    border: solid 4px #cfbae5;
    font-size: 30px;
    font-weight: 900;
    font-style: italic;
}
.signUp__info {
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
.select--margin{
    background-color: white;
    color: white;
    border-radius: 2px;
    font-size: 14px;
}
</style>
