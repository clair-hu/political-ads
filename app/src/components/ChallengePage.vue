<template>
    <div id="challengePage">
        <base-navbar :links="navLinks" />
        <div class="challenge">
            <base-input-field class="baseInput--margin" v-model="challengeeUsername" placeholder-text="The user you want to challenge to" />
            <base-button class="baseButton--margin" type="purple" @click.native="startChallenge()">
                <template slot="text">
                    start challenge
                </template>
            </base-button>
        </div>
        <div class="challenge-results">
            <ul id="component-link">
                <li v-for="item in items" v-on:click="seen = item.challenge_id" :key="item.challenge_id" :challenge="item">
                <h1>Show more details for the {{item.challenge_id}} challenge</h1>
                <ChallengeResultContainer v-if="seen===item.challenge_id" :key="item.challenge_id" :challenge="item"/>
                </li>
            </ul>
        </div>
    </div>
</template>
<script>
import BaseNavbar from "./BaseNavbar.vue";
import BaseButton from "./BaseButton.vue";
import BaseInputField from "./BaseInputField.vue";
import ChallengeResultContainer from "./ChallengeResultContainer.vue";
export default {
    components: {
        BaseNavbar,
        BaseButton,
        BaseInputField,
        ChallengeResultContainer,
    },
    data(){
        return {
            seen: true,
            navLinks: [
                {
                    title: "Dashboard",
                    isActive: false,
                    url: "/dashboard"
                },
                {
                    title: "Spend Money",
                    isActive: false,
                    url: "/spend"
                },
                {
                    title: "Challenge",
                    isActive: true,
                    url: "/challenge"
                }
            ],
            challengeeUsername: "",
            items: []
        };
    },
    computed: {
        user() {
            return this.$store.getters.user;
        }
    },
    methods: {
        
        startChallenge() {
            console.log("challengee user name is " + this.challengeeUsername);
            const body = {
                "challenger_id":this.user["user_id"],
                "challengee_name":this.challengeeUsername
            }
            this.$http.post('http://localhost:5000/create-challenge', body).then( res => {
                console.log('response:', res)
                location.reload();
            },
            err => {
                console.log(err);
            })
            //TODO get challenge ID and show the challenge records
        },
    },
    async created () {
        //get history of challenges
        var response =  await this.$http.get('http://localhost:5000/user-challenges?user_id='+this.user["user_id"]);
        this.items = response.data.data
    }
}
</script>
<style scoped>
.baseInput--margin {
    margin: 10px auto;
}
.baseButton--margin {
    margin: 10px auto;
    justify-self:flex-end;
}
.btable--margin {
    margin: 10px auto;
    justify-self:flex-end;
}
</style>
